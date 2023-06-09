from pathlib import WindowsPath
from backend.Model.wavmodel import WavModel
import typing
import json


class WavFinder:

    def __init__(self, origin):
        self.path = WindowsPath(origin)

    def find_all(self):
        """ find_all searches for all the .wav files inside
        the origin path it then returns a list containing the name of the file and his path"""
        wavs = []
        for wav in self.path.rglob("*.wav"):

            wavs.append(WavModel(wav.stem, str(wav)))
        return wavs

    def find_wav(self, name):
        for wav in self.find_all():
            if name in wav.name:
                return wav
        return -1

    def find_wavs(self, name) -> typing.List[WavModel]:
        wavs = list()
        for wav in self.find_all():
            if name in wav.name:
                wavs.append(wav)
        return wavs


class JSONFinder:
    """ Json Finder is a class that will only have the json file name as an Input. It will return a JSON Object"""

    def __init__(self, origin):
        self.path = WindowsPath(origin)

    def findAll(self):
        """findAll : searches all occurences of a .json in the current directory './'
            it returns all jsons in an JSONObject form"""
        jsons = []
        for json_path in self.path.rglob("*.json"):
            with open(str(json_path), "r") as json_file:
                json_object = json.loads(json_file.read())
                jsons.append(json_object)
        return jsons

    def find(self, name):
        """ Searches for a single occurrence of the .json file
         or -1 when not found
         name shouldn't have .json extension """

        for json_file in self.path.rglob("*.json"):
            if name in str(json_file):
                with open(str(json_file), "r") as json_f:
                    return json.loads(json_f.read())
        return -1

    def findAll_given_name(self, name):
        """ Deprecated """
        jsons = list()
        for json_file in self.path.rglob("*.json"):
            if name in str(json_file):
                with open(str(json_file)) as json_o:
                    jsons.append(json.loads(json_o.read()))
        return jsons

    def findAll_plus_name(self):
        """ Deprecated """
        jsons = []
        for json_path in self.path.rglob("*.json"):
            with open(str(json_path), "r") as json_file:
                json_object = json.loads(json_file.read())
                jsons.append([str(json_path)[-53:-5], json_object])
        return jsons
