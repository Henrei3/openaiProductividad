from backend.Model.pathFinder import WavFinder
import os
from backend.Model.jsonCreator import JsonFileCreator
from backend.Model.pathFinder import JSONFinder
import subprocess


class RecordingModel:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    @staticmethod
    def get_recordings(phone_number, date):
        if len(phone_number) > 10:
            subprocess.call("../openRepo.bat")
            path = r"Y:\Apache24\htdocs\rec\grabaciones"
            date = date.split(" ")
            day = date[0]
            for da in day.split("-"):
                path += rf"\{da}"
            wav_name = f"out-{phone_number}"
            wav_finder = WavFinder(path)

            record = wav_finder.find_wavs(wav_name)
            if len(record) != 0:
                return record
            return None

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
