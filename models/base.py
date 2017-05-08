
import traceback
from sqlalchemy import Column,Integer,Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.sql.schema import UniqueConstraint

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


class StateBonus(BaseAPI, Base):
    __tablename__ = 'state_bonus'

    date = Column('date', Date, nullable=False, primary_key=True)
    type = Column('type', Float)
    variation = Column('variation', Float)

    def serialize(self) -> dict:
        return {
            'date': self.date,
            'state_bonus': self.state_bonus,
            'variation': self.variation
        }


class Company(BaseAPI, Base):
    __tablename__ = 'company'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(255), nullable=False, unique=True)
    daily_data = relationship('DailyData', lazy='subquery')

    def serialize(self, daily_data: bool = False) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'dailyData': [daily_data.serialize() for daily_data in self.daily_data] if daily_data else None
        }


class DailyData(BaseAPI, Base):
    __tablename__ = 'daily_data'
    __table_args__ = (
        UniqueConstraint('company_id', 'date'),
    )

    # TODO: poner company_id y observed_at como calves únicas
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    company_id = Column('company_id', ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
    company = relationship('Company', lazy='subquery', foreign_keys=[company_id])
    date = Column('date', Date, nullable=False)

    price = Column('price', Float)
    difference = Column('difference', Float)
    percentage_difference = Column('percentage_difference', Float)
    capitalization = Column('capitalization', Float)
    BPA = Column('BPA', Float)
    PER = Column('PER', Float)
    PVC = Column('PVC', Float)
    PCF = Column('PCF', Float)
    dividend_yield = Column('dividend_yield', Float)
    interest_per_share = Column('interest_per_share', Float)
    last_value = Column('last_value', Float)

    def serialize(self, company: bool = False) -> dict:
        return {
            'date': self.date.isoformat(),
            'companyId': self.company_id,
            'company': self.company.serialize() if company else None,
            'price': self.price,
            'difference': self.difference,
            'percentageDifference': self.percentage_difference,
            'capitalization': self.capitalization,
            'BPA': self.BPA,
            'PER': self.PER,
            'PVC': self.PVC,
            'PCF': self.PCF,
            'dividendYield': self.dividend_yield,
            'interestPerShare': self.interest_per_share,
            'lastValue': self.last_value
        }

