from backend.Model.DB.recordingsDB import Gestion, Contenido
from backend.Model.DB.base import Session, Base, engine
from sqlalchemy import text
from typing import Optional


class PostGre:

    def __init__(self):
        self.session = Session()
        Base.metadata.create_all(engine)

    def add_gestion(self, gestion_id: str, cellphone: str):
        gestion = Gestion(gestion_id, cellphone)
        self._add(gestion)
        return gestion

    def add_contenido(self, g_id: int, nombre: str, audio_text: dict, score: dict, gpt_answer:  Optional[dict]):
        contenido = Contenido(g_id, nombre, audio_text, score, gpt_answer)
        self._add(contenido)
        return contenido

    def get_contenido(self, y, m, d):
        return self.custom_requete(f"SELECT * FROM contenido where name like '%{y}{m}{d}%'")

    def _add(self, value):
        self.session.add(value)
        self.session.commit()

    def close(self):
        self.session.close()

    def custom_requete(self, requete:str):
        return self.session.execute(text(requete))
