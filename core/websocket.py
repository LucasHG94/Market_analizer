"""
    Methods available in the API
"""

import traceback

from core import __core_app__ as core
from core.facade import Facade
from flask import jsonify
from datetime import datetime


class Websocket:

    @staticmethod
    def valid_response(data: any = None):
        return jsonify({'success': True, 'data': data})

    @staticmethod
    def invalid_response(data, err_code: int = 1) -> str:
        if isinstance(data, Exception):
            print(traceback.format_exc())
            data = str(data)

        return str({'success': False, 'errCode': err_code, 'data': data})

    @staticmethod
    def invalid_api_parameter(method, parameter) -> str:
        return str({
            'success': False,
            'errCode': 2,
            'data': '{!s} method needs the parameter {!s}'.format(method, parameter)
        })

    @staticmethod
    def no_result_found(method: str, id_) -> str:
        return str({
            'success': False,
            'errCode': 4,
            'data': {
                'method': method,
                'id': id_
            }
        })

    @staticmethod
    @core.app.route('/')
    def test():
        return 'It works!'

    @staticmethod
    @core.app.route('/getStateBonus/<from_date>/<to_date>')
    def get_state_bonus(from_date: str, to_date: str):
        try:
            data = [state_bonus.serialize() for state_bonus in
                    Facade.get_state_bonus(core.session,
                                           datetime.fromtimestamp(int(from_date)/1000),
                                           datetime.fromtimestamp(int(to_date)/1000))]
            return Websocket.valid_response(data)
        except KeyError as ex:
            return Websocket.invalid_api_parameter('getCompanies', ex)
        except Exception as ex:
            # DEBUG
            return Websocket.invalid_response(ex)

    @staticmethod
    @core.app.route('/getCompanies')
    def get_companies():
        try:
            data = [company.serialize() for company in Facade.get_companies(core.session)]
            return Websocket.valid_response(data)
        except KeyError as ex:
            return Websocket.invalid_api_parameter('getCompanies', ex)
        except Exception as ex:
            # DEBUG
            return Websocket.invalid_response(ex)

    @staticmethod
    @core.app.route('/getIBEX35Companies')
    def get_IBEX35_companies():
        try:
            data = [company.serialize() for company in Facade.get_IBEX35_companies(core.session)]
            return Websocket.valid_response(data)
        except KeyError as ex:
            return Websocket.invalid_api_parameter('getCompanies', ex)
        except Exception as ex:
            # DEBUG
            return Websocket.invalid_response(ex)

    @staticmethod
    @core.app.route('/getBMENoIBEX35Companies')
    def get_BME_no_IBEX35_companies():
        try:
            data = [company.serialize() for company in Facade.get_BME_no_IBEX35_companies(core.session)]
            return Websocket.valid_response(data)
        except KeyError as ex:
            return Websocket.invalid_api_parameter('getCompanies', ex)
        except Exception as ex:
            # DEBUG
            return Websocket.invalid_response(ex)

    @staticmethod
    @core.app.route('/getCompanyData/<company_id>/<from_date>/<to_date>')
    def get_company_data(company_id: int, from_date: str, to_date: str):
        try:
            data = Facade.get_company_by_id(core.session, company_id).serialize()
            data['dailyData'] = [daily_data.serialize() for daily_data in
                                 Facade.get_company_data(core.session,
                                                         company_id,
                                                         datetime.fromtimestamp(int(from_date)/1000),
                                                         datetime.fromtimestamp(int(to_date)/1000)
                                                         )]
            return Websocket.valid_response(data)
        except KeyError as ex:
            return Websocket.invalid_api_parameter('getCompanies', ex)
        except Exception as ex:
            # DEBUG
            return Websocket.invalid_response(ex)

    @staticmethod
    @core.app.route('/getLastData')
    def get_last_data():
        try:
            return Websocket.valid_response(Facade.get_last_data(core.session))
        except KeyError as ex:
            return Websocket.invalid_api_parameter('getCompanies', ex)
        except Exception as ex:
            # DEBUG
            return Websocket.invalid_response(ex)

