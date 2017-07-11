"""
    Queries to the database
"""

from datetime import date
from sqlalchemy import between

from models.base import Company, DailyData, StateBonus


class Facade:

    @staticmethod
    def get_state_bonus(session, from_date, to_date):
        return session.query(StateBonus).filter(between(StateBonus.date, from_date, to_date)).all()

    @staticmethod
    def get_companies(session):
        return session.query(Company).all()

    @staticmethod
    def get_IBEX35_companies(session):
        return session.query(Company).filter_by(market_type='IBEX35').all()

    @staticmethod
    def get_BME_no_IBEX35_companies(session):
        return session.query(Company).filter_by(market_type='BME_no_IBEX35').all()

    @staticmethod
    def get_all_daily_data(session):
        return session.query(DailyData).filter_by(date=date.today()).one()

    @staticmethod
    def get_company_daily_data(session, id):
        return session.query(DailyData).filter_by(id=id).filter_by(date=date.today()).one()

    @staticmethod
    def get_company_by_id(session, id):
        return session.query(Company).filter_by(id=id).one()

    @staticmethod
    def get_company_data(session, id, from_date, to_date):
        return session.query(DailyData).filter_by(company_id=id)\
            .filter(between(DailyData.date, from_date, to_date)).all()

    # @staticmethod
    # def get_range_company_data(session, id, start, end):
    #     return session.query(DailyData).filter_by(id=id).filter_by(date=date.today()).one()

    @staticmethod
    def get_last_data(session):
        companies = session.query(Company).filter_by().all()
        data = []
        for company in companies:
            data.append({'company': company.serialize(), 'lastData': company.daily_data[len(company.daily_data)-1].serialize()})
        return data

