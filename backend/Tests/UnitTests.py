import unittest
from backend.Model.PhrasesModel import EncouragedPhrasesModel, ProhibitedPhrasesModel
from backend.Model.DB.SQLServer import SQLSERVERDBModel


class PhrasesUnitTesting(unittest.TestCase):
    def test_get_encouraged_list_when_ced_unexistent(self):
        phrases_test = EncouragedPhrasesModel("Hola Que tal", "nonexistingced")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)

    def test_get_encouraged_list_when_ced_exists(self):
        phrases_test = EncouragedPhrasesModel("Hola Que tal", "diners")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)
    def test_CEDENTE_GENERAL_exists(self):
        phrases_test = EncouragedPhrasesModel("Hola Que tal", "CEDENTE_GENERAL")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)


class ConexionTesting(unittest.TestCase):
    def test_cnxn_getserialced_working(self):
        cnxn = SQLSERVERDBModel()
        element = cnxn.get_serialced_fromname("diners")
        self.assertNotEquals(element, None)


if __name__ == '__main__':
    unittest.main()
