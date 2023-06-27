from backend.Model.DB.recordingsDB import Recording, Scores, Embedding
from backend.Model.DB.base import Session, Base, engine
from sqlalchemy import text
from typing import Optional


class PostGre:

    def __init__(self):
        self.session = Session()
        Base.metadata.create_all(engine)

    def add_recording(self, gestion_id: str, audio_text: dict, cellphone: str, name: str):
        gestion = Recording(gestion_id, audio_text, cellphone, name)
        self._add(gestion)
        return gestion

    def get_recording_given_name(self, name: str):
        request = f"SELECT * FROM recording WHERE name like '%{name}%';"
        return self.custom_requete(request)

    def update_recording_audio_text(self, recording_id: str, audio_text: dict):
        request = f"UPDATE recording SET audio_text = '{audio_text}' WHERE id = {recording_id};"
        self.custom_requete(request)

    def get_audio_text(self, recording_id: str):
        request = f"SELECT audio_text FROM recording WHERE id = {recording_id}"
        return self.custom_requete(request)

    def add_embedding(self, recording_id, embedding: dict):
        embedding = Embedding(recording_id, embedding)
        self._add(embedding)
        return embedding

    def get_embedding(self, name: str):
        return self.custom_requete(
            f"SELECT e_id, embedding FROM embeddings e JOIN recording r ON e.e_id=r.id where name like '%{name}%'"
        )

    def add_scores(self, recording_id: str, score: dict):
        scores = Scores(recording_id, score)
        self._add(scores)
        return scores

    def get_scores(self, y: str, m: str, d: str):
        return self.custom_requete(
            f"SELECT g_id, score FROM scores s JOIN recording r ON s.s_id=r.id where name like '%{y}{m}{d}%'"
        )

    def _add(self, value):
        self.session.add(value)
        self.session.commit()

    def close(self):
        self.session.close()

    def custom_requete(self, requete: str):
        return self.session.execute(text(requete))
