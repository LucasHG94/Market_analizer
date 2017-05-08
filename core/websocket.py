import traceback

from core import __core_app__ as core
from core.facade import Facade
from flask import jsonify
import json


class Websocket:

    @staticmethod
    def valid_response(data: any = None):
        return jsonify({'success': True, 'data': data})
        # return '__ng_jsonp__.__req0.finished(' + str(json.dumps({'success': True, 'data': data})) + ');'

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
    def hello_world2():
        return 'It works!'

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
    @core.app.route('/getCompanyData/<company_id>')
    def get_company_data(company_id: int):
        print('Params: ', company_id)
        try:
            data = Facade.get_company_data(core.session, company_id).serialize(daily_data=True)
            print(data)
            return Websocket.valid_response(data)
        except KeyError as ex:
            return Websocket.invalid_api_parameter('getCompanies', ex)
        except Exception as ex:
            # DEBUG
            return Websocket.invalid_response(ex)

