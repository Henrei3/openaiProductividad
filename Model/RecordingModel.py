from Model.pathFinder import WavFinder
import os
from Model.jsonCreator import JsonFileCreator
from Model.pathFinder import JSONFinder


class RecordingModel:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    @staticmethod
    def get_recording(phone_number, date):

        path = r"Y:\Apache24\htdocs\rec\grabaciones"
        date = date.split(" ")
        day = date[0]
        hour = date[1]
        for da in day.split("-"):
            path += rf"\{da}"
        print(path)
        wav_name = f"out-{phone_number}"
        wav_finder = WavFinder(path)

        record = wav_finder.find_wav(wav_name)
        if record != -1:
            record_hour = record[0].split("-")[4]
            date = hour.split(":")
            segment = record_hour[0]+record_hour[1]
            if segment == date[0] and record_hour[2] == date[1][0]:
                if os.stat(record[1]).st_size / (1024 * 1024) > 1:
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
