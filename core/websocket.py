import traceback

from core import __core_app__ as core
from core.facade import Facade


class Websocket:

    @staticmethod
    @core.app.route('/hello')
    def hello_world():
        return 'Hello, World!'

    @staticmethod
    @core.app.route('/')
    def hello_world2():
        return 'Hello!'

    @staticmethod
    @core.app.route('/companies')
    def get_companies():
        try:
            data = [company.serialize() for company in Facade.get_companies(core.session)]
            print(Websocket.valid_response(data))
            return Websocket.valid_response(data)
        except KeyError as ex:
            return Websocket.invalid_api_parameter('getCompanies', ex)
        except Exception as ex:
            # DEBUG
            return Websocket.invalid_response(ex)

    @staticmethod
    def valid_response(data: any = None) -> str:
        return str({'success': True, 'data': data})

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