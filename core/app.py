import json
import os
import threading
from threading import Thread

from flask import Flask
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from models.base import Base, Company
from seeds.seed import seed_BME, save_daily_data, save_state_bonus

import time
import schedule
# import thread


class CoreApp(Thread):

    @property
    def app(self) -> dict:
        return self._app

    @property
    def cors(self) -> dict:
        return self._cors

    @property
    def engine(self) -> dict:
        return self._engine

    @property
    def session(self) -> dict:
        return self._session

    @property
    def base(self) -> dict:
        return Base

    def run(self):
        with open('/home/sturm/Workspace/Market_analizer/config/config.json') as raw_data:
            data = json.load(raw_data)
            self.app.run(host=data['host'], debug=False, port=int(os.environ.get("PORT", data['port'])), threaded=True)

    def seed_companies(self):
        seed_BME(self.session)

    def save_state_bonus(self):
        save_state_bonus(self.session, all_the_times=True)

    def seed_day(self):
        print('Initiating daily data collection.')
        save_daily_data(self.session)
        save_state_bonus(self.session)

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
        self.save_state_bonus()
        self.seed_companies()
        print('Database restarted')

    @staticmethod
    def job():
        print("I'm working...")

    @staticmethod
    def period_seed():
        while True:
            schedule.run_pending()
            time.sleep(60)

    def __init__(self):
        self._app = Flask(__name__)
        self._cors = CORS(self.app, resources={r"/*": {"origins": "*"}})
        self._app.config.from_object(__name__)
        self._app.config.update(dict(
            DATABASE=os.path.join(os.path.abspath(''), 'database/market.db'),
            SECRET_KEY='123',
            USERNAME='admin',
            PASSWORD='123',
            CORS_HEADERS='Content-Type'
        ))
        self._app.config.from_envvar('MARKET_SETTINGS', silent=True)
        self._engine = create_engine('sqlite:///' + self._app.config['DATABASE'],
                                     connect_args={'check_same_thread': False})
        Session = sessionmaker(bind=self.engine)
        self._session = Session()
        # self.seed_day()
        # schedule.every().day.at("18:00").do(self.seed_day)
        # schedule.every(10).seconds.do(self.seed_day)

        # t = threading.Thread(target=CoreApp.period_seed)
        # t.start()
