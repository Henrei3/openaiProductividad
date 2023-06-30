from backend.Model.DB.recordingsDB import Recording, Scores, Embedding
from backend.Model.DB.base import Session, Base, engine
from sqlalchemy import text, select
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
        request = self.session.query(Recording).filter(Recording.name.like(f"{name}"))
        return self.session.execute(request)

    def update_recording_audio_text(self, recording_id: str, audio_text: dict):
        self.session.query(Recording).filter(Recording.id == recording_id).update(
            {Recording.audio_text: audio_text}, synchronize_session='auto'
        )
        self.session.commit()

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

    def add_score(self, score: Scores):
        return self._add(score)

    def update_score(self, score: Scores):
        s_id = str(score.s_id)
        self.session.query(Scores).filter(Scores.s_id == s_id).update(
            {Scores.score: score.score}, synchronize_session='auto'
        )
        self.session.commit()
        return score

    def get_scores_given_date(self, y: str, m: str, d: str):
        return self.custom_requete(
            f"SELECT g_id, score FROM scores s JOIN recording r ON s.s_id=r.id where name like '%{y}{m}{d}%'"
        )

    def get_score(self, s_id):
        query = select(Scores).where(Scores.s_id == f'{s_id}')
        return self.session.execute(query)

    def get_recordings_given_date(self, y: str, m: str, d: str):
        result = self.session.query(Recording).filter(Recording.audio_text != 'null', Recording.name.like(
            f'%{y}{m}{d}%')
        )
        return self.session.execute(result)

    def check_if_exists(self, table: Base, identifier: str):
        requete = select(table).where(table.id == identifier)
        return self.session.execute(requete)

    def _add(self, value):
        self.session.add(value)
        self.session.commit()
        return value

    def close(self):
        self.session.close()

    def custom_requete(self, requete: str):
        return self.session.execute(text(requete))
