import pyodbc
from backend.Model.Conf import Conf

class Connexion:
    __cnxn = None

    def __new__(cls):
        if cls.__cnxn is None:
            conection_info = f'DRIVER={Conf.get_driver()};Server={Conf.get_server()};UID={Conf.getuser()};Pwd={Conf.get_pwd()}'
            cls.__cnxn = pyodbc.connect(conection_info)
        return cls.__cnxn
