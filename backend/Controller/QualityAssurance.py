from backend.Model.RecordingModel import RecordingModel
from backend.Model.AudioGPTRequestModel import AudioGPTRequestModel
from backend.Model.DataBase import SQLSERVERDBModel
from backend.Controller.GPTCreator import OpenAIRequestCreator
from backend.Controller.PhrasesController import EncouragedPhrasesController
from backend.Controller.PhrasesController import ProhibitedPhrasesController
from backend.Model.PhrasesModel import EncouragedPhrasesModel, ProhibitedPhrasesModel
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.pathFinder import JSONFinder
import subprocess



class QualityAssurance:

    @staticmethod
    def execute():
        controller = SQLSERVERDBModel()
        subprocess.call([r'C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat'])

        prompt = "Cliente- Alo ? Agente- Buenos Dias."

        for line in controller.test():
            print(line)
            final_wavs = RecordingModel.get_recordings(str(line[3]), str(line[4]))
            print(final_wavs)
            if final_wavs is not None:
                for final_wav in final_wavs:
                    """ Speech to Text """
                    audio = AudioGPTRequestModel(prompt, final_wav.path, final_wav.name)
                    audio_response = OpenAIRequestCreator.audio_request(audio)
                    audio.set_response(audio_response)

                    """ Refining Speech so That only the agent speech is collected """
                    refined_speech = SpeechRefinement.get_only_agent(audio.get_response())

                    """ Score Calculation """
                    positive_phrases_model = EncouragedPhrasesModel(final_wav.name, refined_speech)
                    positive, ticket_positive = EncouragedPhrasesController.calculate_score(positive_phrases_model)
                    negative_phrases_model = ProhibitedPhrasesModel(refined_speech)
                    negative = ProhibitedPhrasesController.calculate_score(negative_phrases_model)

                    total = negative + positive

                    positive_phrases_model.set_phrase_score(total, ticket_positive)

        """ Sending Info to The Database once all audios treated """


jsonfinder = JSONFinder("../analysed_records/audio_text/")
text_json = jsonfinder.find("out-0980427196")
refined_speech = SpeechRefinement.get_only_agent(text_json["text"])
print(refined_speech)
