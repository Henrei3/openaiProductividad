import typing

from backend.Controller.pathFinder import WavFinder
from backend.Model.wavmodel import WavModel
import os


class PossibleWav:
    @staticmethod
    def get_recordings(phone_number, date) -> typing.List[WavModel]:
        if len(phone_number) >= 10:
            path = r"Z:\Apache24\htdocs\rec\grabaciones"
            date = date.split(" ")
            day = date[0]
            for da in day.split("-"):
                path += rf"\{da}"
            wav_name = f"out-{phone_number}"
            wav_finder = WavFinder(path)
            records = wav_finder.find_wavs(wav_name)
            return PossibleWav.get_one_mega_records(records)

    @staticmethod
    def get_one_mega_records(records):
        if len(records) != 0:
            one_mega_records = list()
            for record in records:
                file_size = os.stat(record.path)
                if file_size.st_size / (1024 * 1024) >= 1:
                    one_mega_records.append(record)
            if len(one_mega_records) != 0:
                for to_print in one_mega_records:
                    print(to_print.path)
                return one_mega_records
        return None
