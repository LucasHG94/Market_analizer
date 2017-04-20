import os
from threading import Thread

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from models.base import Base, Company
from seeds.seed import seed_IBEX35, seed_daily_data, seed_state_bonus

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

    def seed_companies(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        seed_IBEX35(session)

    def seed_state_bonus(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        seed_state_bonus(session)

    def seed_day(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        seed_daily_data(session)

    def show_data(self):
        connection = self.engine.connect()
        result = connection.execute("select name from Company")
        for row in result:
            print("Nombre:", row['name'])
        connection.close()

    def start_database(self):
        Base.metadata.create_all(self.engine)
        print('Database created')

    def clean_database(self):
        Base.metadata.drop_all(self.engine)
        print('Database cleaned')

    def restart_database(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.seed_state_bonus()
        self.seed_companies()
        print('Database restarted')

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
        # self.restart_database()
        self.seed_day()
