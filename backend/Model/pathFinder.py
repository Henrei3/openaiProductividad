from pathlib import WindowsPath
import json


class WavFinder:

    def __init__(self, origin):
        self.path = WindowsPath(origin)
    """ find_all searches for all the .wav files inside
    the origin path it then returns a list containing the name of the file and his path"""
    def find_all(self):
        wavs = []
        for wav in self.path.rglob("*.wav"):
            wavs.append([wav.stem, str(wav)])
        return wavs

    def find_wav(self, name):
        for wav in self.find_all():
            if name in wav[0]:
                return wav
        print("Not Found")
        return -1

    def find_wavs(self, name):
        wavs = list()
        for wav in self.find_all():
            if name in wav[0]:
                wavs.append(wav)
        return wavs



class JSONFinder:
    """ Json Finder is a class that will only have the json file name as an Input """
    """ It will return a JSON Object"""

    def __init__(self, origin):
        self.path = WindowsPath(origin)

    """findAll : searches all occurences of a .json in the current directory './' 
    it returns all jsons in an JSONObject form"""
    def findAll(self):
        jsons = []
        for json_path in self.path.rglob("*.json"):
            with open(str(json_path), "r") as json_file:
                json_object = json.loads(json_file.read())
                jsons.append(json_object)
        return jsons

    """find: searches for a single occurence of the {String} name .json and return its object """
    def find(self, name):
        for json_file in self.path.rglob("*.json"):
            if name in str(json_file):
                with open(str(json_file), "r") as json_f:
                    return json.loads(json_f.read())
        return -1

# Vulnerabilidades :
# 0 esta en todos los archivos
# name in wav_name no es correcto. Tiene que ser un numero completo 10 digitos