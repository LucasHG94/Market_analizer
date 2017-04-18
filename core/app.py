import os
from threading import Thread

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class CoreApp(Thread):

    @property
    def app(self) -> dict:
        return self._app

    @property
    def engine(self) -> dict:
        return self._engine

    @property
    def base(self) -> dict:
        return self._base

    def run(self):
        self.app.run(host='0.0.0.0', debug=True, port=int(os.environ.get("PORT", 5000)), threaded=True)

    def __init__(self):
        self._app = Flask(__name__)
        self._app.config.from_object(__name__)

        self._app.config.update(dict(
            DATABASE=os.path.join(self._app.root_path, 'database/market.db'),
            SECRET_KEY='123',
            USERNAME='admin',
            PASSWORD='123'
        ))
        self._app.config.from_envvar('MARKET_SETTINGS', silent=True)

        self._engine = create_engine('sqlite:///' + self._app.config['DATABASE'])
        self._base = declarative_base()
