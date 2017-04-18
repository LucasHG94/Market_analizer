import os
from threading import Thread

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from models.base import Base, Company


class CoreApp(Thread):

    @property
    def app(self) -> dict:
        return self._app

    @property
    def engine(self) -> dict:
        return self._engine

    @property
    def base(self) -> dict:
        return Base

    def run(self):
        self.app.run(host='0.0.0.0', debug=True, port=int(os.environ.get("PORT", 5000)), threaded=True)

    def seed_IBEX35(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        crs = open("/home/sturm/Workspace/Market_analizer/seeds/IBEX35.txt", "r")
        for company_name in crs:
            company = Company(name=company_name)
            session.add(company)
        try:
            session.commit()
        except IntegrityError as ex:
            print(ex)

    def show_data(self):
        connection = self.engine.connect()
        result = connection.execute("select name from Company")
        for row in result:
            print("Nombre:", row['name'])
        connection.close()

    def __init__(self):
        self._app = Flask(__name__)
        self._app.config.from_object(__name__)
        self._app.config.update(dict(
            DATABASE=os.path.join('/home/sturm/Workspace/Market_analizer', 'database/market.db'),
            SECRET_KEY='123',
            USERNAME='admin',
            PASSWORD='123'
        ))
        self._app.config.from_envvar('MARKET_SETTINGS', silent=True)
        self._engine = create_engine('sqlite:///' + self._app.config['DATABASE'])
        Base.metadata.create_all(self.engine)
        # Base.metadata.drop_all(self.engine)
        # self.seed_IBEX35()
        self.show_data()
