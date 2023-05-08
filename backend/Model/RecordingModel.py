from backend.Model.pathFinder import WavFinder
import os
from backend.Model.jsonCreator import JsonFileCreator
from backend.Model.pathFinder import JSONFinder


class RecordingModel:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    @staticmethod
    def get_recording(phone_number, date):
        if len(phone_number) > 10:
            path = r"Y:\Apache24\htdocs\rec\grabaciones"
            date = date.split(" ")
            day = date[0]
            hour = date[1]
            for da in day.split("-"):
                path += rf"\{da}"
            wav_name = f"out-{phone_number}"
            wav_finder = WavFinder(path)

            record = wav_finder.find_wav(wav_name)
            if record != -1:
                return record

    def set_score(self, total, ticket_score):
        if not os.path.exists("../analysed_records/scores"):
            os.makedirs("../analysed_records/scores")
        score = {
            "total": total,
            "ticket_score": ticket_score
        }
        JsonFileCreator.write(score, "../analysed_records/scores/"+self.name+".json")

    def get_score(self):
        jsonfinder = JSONFinder("../")
        return jsonfinder.find(self.name)
