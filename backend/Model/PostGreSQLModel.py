from backend.Model.recordingsDB import Gestion, PatronesExito, Contenido
from backend.Model.base import Session
from typing import Optional


class PostGre:

    def __init__(self):
        self.session = Session()

    def add_gestion(self, gestion_id: str, cellphone: str):
        gestion = Gestion(gestion_id, cellphone)
        self._add(gestion)
        return gestion

    def add_contenido(self, g_id: int, nombre: str, audio_text: dict, score: dict, gpt_answer:  Optional[dict]):
        contenido = Contenido(g_id, nombre, audio_text, score, gpt_answer)
        self._add(contenido)
        return contenido

    def _add(self, value):
        self.session.add(value)
        self.session.commit()

    def close(self):
        self.session.close()
