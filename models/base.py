
import traceback
from sqlalchemy import Column,Integer,Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey

Base = declarative_base()


class BaseAPI:
    @staticmethod
    def valid_response(data: any = None) -> dict:
        return {'success': True, 'data': data}

    @staticmethod
    def invalid_response(data, err_code: int = 1) -> dict:
        if isinstance(data, Exception):
            print(traceback.format_exc())
            data = str(data)

        return {'success': False, 'errCode': err_code, 'data': data}


class Company(BaseAPI, Base):
    __tablename__ = 'company'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(255), nullable=False, unique=True)
    daily_data = relationship('DailyData', lazy='subquery')

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'dailyDatas': [daily_data.serialize() for daily_data in self.daily_data]
        }


class DailyData(BaseAPI, Base):
    __tablename__ = 'daily_data'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    company_id = Column('company_id', ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
    company = relationship('Company', lazy='subquery', foreign_keys=[company_id])
    observed_at = Column('observed_at', Date, nullable=False)
    BPA = Column('BPA', Float)
    PER = Column('PER', Float)
    PVC = Column('PVC', Float)
    PCF = Column('PCF', Float)
    dividend_yield = Column('dividend_yield', Float)
    state_bonus = Column('state_bonus', Float)
    interest_per_share = Column('interest_per_share', Float)
    last_value = Column('last_value', Float)

