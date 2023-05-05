from Model.RecordingModel import RecordingModel
from Model.AudioGPTRequestModel import AudioGPTRequestModel
from Model.DataBase import SQLSERVERDBModel
from Controller.GPTCreator import OpenAIRequestCreator
from Controller.PhrasesController import EncouragedPhrasesController
from Controller.PhrasesController import ProhibitedPhrasesController

controller = SQLSERVERDBModel()

prompt = "Cliente- Alo ? Agente- Buenos Dias. (Español)"

for line in controller.get_all_recordings_given_date('2023', '04', '26'):
    print(line)
    final_wav = RecordingModel.get_recording(str(line[3]), str(line[4]))
    print(final_wav)
    if final_wav is not None:
        audio = AudioGPTRequestModel(prompt, final_wav[1], final_wav[0])
        response = OpenAIRequestCreator.audio_request(audio)
        audio.set_response(response)

        positive, ticket_positive = EncouragedPhrasesController.calculate_score(audio.get_response())
        negative = ProhibitedPhrasesController.calculate_score(audio.get_response())

        total = negative + positive

        audio.set_score(total, ticket_positive)
