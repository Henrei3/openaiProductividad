from backend.Model.PatternModel import PatternModel
from backend.Controller.pathFinder import JSONFinder

class SpeechRefinement:

    @staticmethod
    def refine_speech_textUser(speech, name):
        text = speech.replace("Agente 1-", "\n -").replace(".", ". \n").replace("?", "? \n")
        text = text.replace(name+"-", "\n -")
        return text

    @staticmethod
    def refine_speech_textOpenAI(speech):

        text = speech.replace("Agente 1-", "-").replace("Agente-", "-")
        return text


class PatternController:
    """ Frequency Reader is a class that reads a json input and counts the frequency of each word """

    """countWords is a method that takes a .json name as an input and
     outputs on a json file already created or creates one with the occurrences of all the words in the .json content
     section"""
    @staticmethod
    def countWords(json_name):
        pattern_model = PatternModel()
        count = pattern_model.get_pattern()
        jsonfinder = JSONFinder("../")
        json = jsonfinder.find(json_name+"GPT")
        string = ""
        for test in json["content"]:
            if test != " ":
                if test != "." and test != ":" and test != "," and not test.isnumeric() and test != "\n":
                    string += test
            else:
                if len(string) > 3:
                    if string.lower() in count:
                        count[string.lower()] = count[string.lower()] + 1
                    else:
                        count.update({string.lower(): 1})
                string = ""

        count2 = dict(sorted(count.items(), key=lambda item: item[1]))
        while len(count2) > 100:
            to_pop = list(count2)[0]
            count2.pop(to_pop)
        pattern_model.set_pattern(count2)
        return count2
