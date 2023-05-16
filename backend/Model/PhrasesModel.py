from backend.Model.DataBase import SQLSERVERDBModel
from backend.Controller.pathFinder import JSONFinder
from backend.Model.jsonCreator import JsonFileCreator
import os


class PhrasesModel:

    def __init__(self, phrase):
        self.phrase = phrase

    def set_phrase_score(self, total, ticket_score):
        if not os.path.exists("../analysed_records/scores"):
            os.makedirs("../analysed_records/scores")
        score = {
            "total": total,
            "ticket_score": ticket_score
        }
        JsonFileCreator.write(score, "../analysed_records/scores/" + self.name + ".json")

    def get_phrase_score(self) -> (int, list):
        jsonfinder = JSONFinder("../analysed_records/scores/")

        json = jsonfinder.find(self.name)
        if json != -1:
            print(json["ticket_score"])
            return json["total"], json["ticket_score"]
        return 0, list()


class EncouragedPhrasesModel(PhrasesModel):

    encouraged = list()

    def __init__(self, phrase, cedente):
        PhrasesModel.__init__(self, phrase)
        self.cnxn = SQLSERVERDBModel()
        element = self.cnxn.get_serialced_fromname(cedente)
        phrases = self.cnxn.get_positive_phrases(element[0])
        for data in phrases:
            self.encouraged.append(
                {data[2]: [data[3], data[4], data[5]], "PUNTAJE": data[6]}
            )

    def get_encouraged_list(self):
        if len(self.encouraged) == 0:
            element = self.cnxn.get_serialced_fromname('CEDENTE_GENERAL')
            phrases = self.cnxn.get_positive_phrases(element[0])
            for data in phrases:
                self.encouraged.append(
                    {data[2]: [data[3], data[4], data[5]], "PUNTAJE": data[6]}
                )
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


