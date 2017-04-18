from core.app import CoreApp

__core_app__ = CoreApp()


def init_app():
    from core.api import CoreAPI
    __core_app__.run()


def get_core_app():
    return __core_app__
