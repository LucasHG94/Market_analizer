from lxml import html
import requests
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.session import sessionmaker
from datetime import date, datetime

from models.base import DailyData, Company, StateBonus


def seed_IBEX35(session):
    crs = open("/home/sturm/Workspace/Market_analizer/seeds/IBEX35.txt", "r")
    for company_name in crs:
        company = Company(name=company_name.replace('\n', ''))
        session.add(company)
    try:
        session.commit()
    except IntegrityError as ex:
        print(ex)


def seed_state_bonus(session):
    page = requests.get('http://www.datosmacro.com/bono/espana')
    tree = html.fromstring(page.content)
    dates = tree.xpath('//td[@class="fecha"]/text()')
    types = tree.xpath('//td[@class="numero"]/text()')
    variations = tree.xpath('//td[@class="numero text-neg"]/text()')
    dates = dates[1:]
    types = types[1:]
    variations = variations[1:]
    for i in range(len(dates)):
        state_bonus = StateBonus(
            date=datetime.strptime(dates[i], '%d/%m/%Y').date(),
            type=format_ratio(types[i]) if i < len(types) else None,
            variation=format_ratio(variations[i]) if i < len(variations) else None
        )
        session.add(state_bonus)
    try:
        session.commit()
    except IntegrityError as ex:
        print(ex)


def seed_daily_data(session):
    companies = session.query(Company).all()
    for company in companies:
        seed_company_daily_data(session, company)


def format_company_name(raw: str) -> str:
    name = raw.replace(' ', '_')
    name = name.replace('"', '')
    return name.lower()


def seed_company_daily_data(session, company: Company):
    page = requests.get('http://www.infobolsa.es/cotizacion/informacion-' + format_company_name(company.name))
    tree = html.fromstring(page.content)
    ratios = tree.xpath('//td[@class="data"]/text()')
    price = tree.xpath('//div[@class="subdata1"]/div/text()')
    difference = tree.xpath('//div[@class="difs"]/div[1]/text()')
    percentage_difference = tree.xpath('//div[@class="difs"]/div[3]/text()')
    try:
        save_daily_entry(session, ratios, company.id, price, difference, percentage_difference)
    except IndexError as ex:
        print(ex)


def save_daily_entry(session, ratios: list, company_id: int, price, difference, percentage_difference):
    daily_data = DailyData(
        company_id=company_id,
        date=date.today(),
        price=format_ratio(price[0]) if len(price) > 0 else None,
        difference=format_ratio(difference[0]) if len(difference) > 0 else None,
        percentage_difference=format_ratio(percentage_difference[0]) if len(percentage_difference) > 0 else None,
        capitalization=format_ratio(ratios[0]) if ratios[0] != '-' else None,
        BPA=format_ratio(ratios[1]) if ratios[1] != '-' else None,
        PER=format_ratio(ratios[2]) if ratios[2] != '-' else None,
        PVC=format_ratio(ratios[3]) if ratios[3] != '-' else None,
        PCF=format_ratio(ratios[4]) if ratios[4] != '-' else None,
        dividend_yield=format_ratio(ratios[5]) if ratios[5] != '-' else None,
        interest_per_share=format_ratio(ratios[6]) if ratios[6] != '-' else None,
    )
    session.add(daily_data)
    session.commit()


def format_ratio(str_ratio: str) -> float:
    str_ratio = str_ratio.replace(',', '')
    str_ratio = str_ratio.replace('-', '0')
    str_ratio = str_ratio.replace('%', '')
    float_ratio = float(str_ratio)
    return float_ratio

