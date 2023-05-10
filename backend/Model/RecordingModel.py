from backend.Controller.pathFinder import WavFinder
import os
from backend.Model.jsonCreator import JsonFileCreator


class RecordingModel:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    @staticmethod
    def get_recordings(phone_number, date):
        if len(phone_number) >= 10:
            path = r"Y:\Apache24\htdocs\rec\grabaciones"
            date = date.split(" ")
            day = date[0]
            for da in day.split("-"):
                path += rf"\{da}"
            wav_name = f"out-{phone_number}"
            print(wav_name)
            wav_finder = WavFinder(path)

            records = wav_finder.find_wavs(wav_name)
            if len(records) != 0:
                one_mega_records = list()
                for record in records:
                    file_size = os.stat(record.path)
                    if file_size.st_size / (1024*1024) >= 1:
                        one_mega_records.append(record)
                if len(one_mega_records) != 0:
                    return one_mega_records
            return None

    def set_score(self, total, ticket_score):
        if not os.path.exists("../analysed_records/scores"):
            os.makedirs("../analysed_records/scores")
        score = {
            "total": total,
            "ticket_score": ticket_score
        }
        JsonFileCreator.write(score, "../analysed_records/scores/"+self.name+".json")
