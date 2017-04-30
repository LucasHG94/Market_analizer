from core.app import CoreApp

__core_app__ = CoreApp()


def init_app():
    from core.websocket import Websocket
    __core_app__.run()


def get_core_app():
    return __core_app__
