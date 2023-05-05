from decouple import config


class Conf:
    def __init__(self):
        pass

    @staticmethod
    def get_driver():
        return '{SQL Server}'

    @staticmethod
    def get_server():
        return config('server')

    @staticmethod
    def getuser():
        return config('user')

    @staticmethod
    def get_pwd():
        return config('pwd')

