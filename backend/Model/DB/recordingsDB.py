from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.dialects.postgresql import JSONB
from backend.Model.DB.base import Base
from marshmallow import Schema, fields


class Recording(Base):

    __tablename__ = 'recording'

    id = Column(Integer, primary_key=True)
    g_id = Column(Integer)
    audio_text = Column(JSONB)
    cellphone = Column(Integer)
    name = Column(String)

    def __init__(self, g_id, audio_text, cellphone, name):
        self.g_id = g_id
        self.audio_text = audio_text
        self.cellphone = cellphone
        self.name = name


class GestionSchemaGet(Schema):
    g_id = fields.Number()


class GestionSchemaPost(Schema):
    audio_text = fields.Dict()


class Scores(Base):
    __tablename__ = "scores"

    s_id = Column(ForeignKey("recording.id"), primary_key=True)
    score = Column(JSONB)

    def __init__(self, s_id, score):
        self.s_id = s_id
        self.score = score


class ContenidoSchemaPost(Schema):
    nombre = fields.String()
    score = fields.Dict()
    gpt_answer = fields.Dict()


class ContenidoSchemaGet(Schema):
    score = fields.Dict()
    gpt_answer = fields.Dict()


class Embedding(Base):
    __tablename__ = "embeddings"

    e_id = Column(ForeignKey("recording.id"), primary_key=True)
    embedding = Column(JSONB)

    def __init__(self, e_id, patterns):
        self.e_id = e_id
        self.embedding = patterns


class PatronesExitoPost(Schema):
    patterns = fields.Dict()


class PatronesExitoGet(Schema):
    pe_id = fields.Number()
    patterns = fields.Dict()




