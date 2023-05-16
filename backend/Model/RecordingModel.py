from backend.Controller.pathFinder import WavFinder
import os
from backend.Model.jsonCreator import JsonFileCreator
from backend.Controller.pathFinder import JSONFinder


class RecordingModel:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_score(self, total, ticket_score, gestion_id):
        if not os.path.exists("../analysed_records/scores"):
            os.makedirs("../analysed_records/scores")
        score = {
            "total": total,
            "ticket_score": ticket_score,
            "gestion_id": gestion_id
        }
        JsonFileCreator.write(score, "../analysed_records/scores/" + self.name + ".json")
