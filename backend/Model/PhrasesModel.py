from backend.Model.DataBase import SQLSERVERDBModel
from backend.Controller.pathFinder import JSONFinder
from backend.Model.jsonCreator import JsonFileCreator
import os


class PhrasesModel:

    def __init__(self, name, phrase):
        self.name = name
        self.phrase = phrase

    def set_phrase_score(self, total, ticket_score):
        if not os.path.exists("../analysed_records/scores"):
            os.makedirs("../analysed_records/scores")
        score = {
            "total": total,
            "ticket_score": ticket_score
        }
        JsonFileCreator.write(score, "../analysed_records/scores/" + self.name + ".json")

    def get_phrase_score(self):
        jsonfinder = JSONFinder("../analysed_records/scores/")

        json = jsonfinder.find(self.name)
        if json != -1:
            return json["total"], json["ticket_score"]
        return 0, list()


class EncouragedPhrasesModel(PhrasesModel):

    encouraged = list()

    def __init__(self, name, phrase):
        PhrasesModel.__init__(self, name, phrase)
        cnxn = SQLSERVERDBModel()
        phrases = cnxn.get_positive_phrases()
        for data in phrases:
            self.encouraged.append(
                {data[2]: [data[3], data[4], data[5]], "PUNTAJE": data[6]}
            )

    def get_encouraged_list(self):
        return self.encouraged


class ProhibitedPhrasesModel:

    prohibited = list()

    def __init__(self, text):
        self.phrase = text
        self.cnxn = SQLSERVERDBModel()
        phrases = self.cnxn.get_negative_phrases()

        for data in phrases:
            self.prohibited.append([data[1], data[3]])

    def get_prohibited_phrases(self):
        return self.prohibited


