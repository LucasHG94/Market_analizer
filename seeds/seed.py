from lxml import html
import os
import requests
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import sessionmaker
from datetime import date, datetime

from models.base import DailyData, Company, StateBonus


def seed_BME(session):
    crs = open(os.path.join(os.path.abspath(''), 'seeds/IBEX35.txt'), "r")
    for company_name in crs:
        company = Company(name=company_name.replace('\n', ''))
        session.add(company)
    try:
        session.commit()
    except IntegrityError as ex:
        print(ex)


def seed_EURO_STOXX50(session):
    crs = open(os.path.join(os.path.abspath(''), 'seeds/EURO_STOXX50.txt'), "r")
    for company_name in crs:
        company = Company(
            name=company_name.replace('\n', ''),
            market_type='EURO_STOXX50'
        )
        session.add(company)
    try:
        session.commit()
    except IntegrityError as ex:
        print(ex)


def save_state_bonus(session, all_the_times: bool = False):
    page = requests.get('http://www.datosmacro.com/bono/espana')
    tree = html.fromstring(page.content)
    dates = tree.xpath('//td[@class="fecha"]/text()')
    types = tree.xpath('//td[@class="numero"]/text()')
    variations = tree.xpath('//td[@class="numero text-neg"]/text()')
    dates = dates[1:]
    types = types[1:]
    variations = variations[1:]
    if all_the_times:
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
                session.rollback()
    else:
        print('Fetch state bonus of date ' + dates[0])
        state_bonus = StateBonus(
            date=datetime.strptime(dates[0], '%d/%m/%Y').date(),
            type=format_ratio(types[0]),
            variation=format_ratio(variations[0])
        )
        session.add(state_bonus)
        try:
            session.commit()
        except IntegrityError as ex:
            print(ex)
            session.rollback()


def save_daily_data(session):
    companies = session.query(Company).filter_by(market_type='IBEX35').all()
    for company in companies:
        save_company_daily_data(session, company)
    print('IBEX35 daily data collection completed.')

    companies = session.query(Company).filter_by(market_type='BME_no_IBEX35').all()
    for company in companies:
        save_company_daily_data(session, company)
    print('BME daily data collection completed.')

    save_other_data(session)


def save_other_data(session):
    try:
        page = requests.get('http://www.finanzas.com/mercado-continuo/')
        tree = html.fromstring(page.content)
        data = tree.xpath('//table[@name="option1"]/*/*/td/text()')
        volume = []
        mins = []
        maxs = []
        file_index = 0
        for i in range(0, len(data)-1):
            if file_index == 3:
                volume.append(data[i])
            if file_index == 4:
                maxs.append(data[i])
            if file_index == 5:
                mins.append(data[i])
            if file_index == 7:
                file_index = 0
            else:
                file_index += 1
        companies = tree.xpath('//table[@name="option1"]/*/*/*/a/text()')
        volume = volume[5:]
        mins = mins[5:]
        maxs = maxs[5:]
        companies = companies[5:]
        print(volume)
        for i in range(0, len(companies)-1):
            try:
                company = session.query(Company).filter_by(name=str(companies[i])).one()
                if company.daily_data[-1].date == date.today():
                    company.daily_data[-1].min = string_to_float(mins[i])
                    company.daily_data[-1].max = string_to_float(maxs[i])
                    company.daily_data[-1].volume = string_to_float(volume[i])
                    session.commit()
            except NoResultFound as ex:
                print(ex, companies[i])
    except requests.exceptions.ConnectionError as ex:
        print(ex)


def save_company_daily_data(session, company: Company):
    try:
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
    except requests.exceptions.ConnectionError as ex:
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
    try:
        session.add(daily_data)
        session.commit()
    except IntegrityError as ex:
        print(ex)
        session.rollback()


def format_company_name(raw: str) -> str:
    name = raw.replace(' ', '_')
    name = name.replace('/', '')
    name = name.replace('"', '')
    return name.lower()


def format_ratio(str_ratio: str) -> float:
    str_ratio = str_ratio.replace(',', '')
    str_ratio = str_ratio.replace('-', '0')
    str_ratio = str_ratio.replace('%', '')
    float_ratio = float(str_ratio)
    return float_ratio


def string_to_float(str_number: str) -> float:
    if str_number != '--':
        str_number = str_number.replace('.', '')
        return float(str_number.replace(',', '.'))
    else:
        return None
