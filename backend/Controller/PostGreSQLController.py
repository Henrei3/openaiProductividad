from backend.Model.PostGreSQLModel import PostGre
from backend.Controller.pathFinder import JSONFinder


class PostgreController:
    @staticmethod
    def add_qa_processes(gestion_id: str, name: str, score: dict):
        postgre = PostGre()
        cellphone = name[4:-34]
        gestion = postgre.add_gestion(gestion_id, cellphone)

        jsonfinder = JSONFinder("../analysed_records/audio_text")

        audio = jsonfinder.find(name)

        postgre.add_contenido(gestion.id, name, audio, score, None)

        postgre.close()
