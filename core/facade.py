from datetime import date

from models.base import Company, DailyData


class Facade:

    @staticmethod
    def get_companies(session):
        return session.query(Company).all()

    @staticmethod
    def get_all_daily_data(session):
        return session.query(DailyData).filter_by(date=date.today()).one()

    @staticmethod
    def get_company_daily_data(session, id):
        return session.query(DailyData).filter_by(id=id).filter_by(date=date.today()).one()

    @staticmethod
    def get_company_data(session, id):
        return session.query(Company).filter_by(id=id).one()

    # @staticmethod
    # def get_range_company_data(session, id, start, end):
    #     return session.query(DailyData).filter_by(id=id).filter_by(date=date.today()).one()

