
from core import __core_app__ as core


class CoreAPI:

    @staticmethod
    @core.app.route('/hello')
    def hello_world():
        return 'Hello, World!'

    @staticmethod
    @core.app.route('/')
    def hello_world2():
        return 'Hello!'
