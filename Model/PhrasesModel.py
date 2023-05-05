from Model.DataBase import SQLSERVERDBModel


class EncouragedPhrasesModel:

    encouraged = list()

    def __init__(self):
        self.cnxn = SQLSERVERDBModel()
        phrases = self.cnxn.get_positive_phrases()
        for data in phrases:
            self.encouraged.append(
                {data[2]: [data[3], data[4], data[5]], "PUNTAJE": data[6]}
            )

    def get_encouraged_list(self):
        return self.encouraged


class ProhibitedPhrasesModel:

    prohibited = list()

    def __init__(self):
        self.cnxn = SQLSERVERDBModel()
        phrases = self.cnxn.get_negative_phrases()

        for data in phrases:
            self.prohibited.append([data[1], data[3]])

    def get_prohibiited_phrases(self):
        return self.prohibited
