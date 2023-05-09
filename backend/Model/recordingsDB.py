from sqlalchemy import Integer, ForeignKey, Column
from sqlalchemy.dialects.postgresql import JSONB
from backend.Model.base import Base
from marshmallow import Schema, fields
from sqlalchemy.orm import Mapped, mapped_column


class Gestion(Base):

    __tablename__ = 'gestion'

    g_id = Column(Integer, primary_key=True)
    score = Column(JSONB)

    def __init__(self, score):
        self.score = score


class GestionSchemaGet(Schema):
    g_id = fields.Number()
    score = fields.Dict()


class GestionSchemaPost(Schema):
    score = fields.Dict()


class PatronesExito(Base):
    __tablename__ = "patronesexito"

    pe_id = Column(Integer, primary_key=True)
    patterns = Column(JSONB)

    def __init__(self, patterns):
        self.patterns = patterns


class PatronesExitoPost(Schema):
    patterns = fields.Dict()


class PatronesExitoGet(Schema):
    pe_id = fields.Number()
    patterns = fields.Dict()


class Audios(Base):
    __tablename__ = 'audio'

    audio_id = Column(Integer, primary_key=True)
    audio_text = Column(JSONB)
    gpt_answer = Column(JSONB)
    gestion_id = Column(ForeignKey("gestion.g_id"))

    def __init__(self, audio_text, gpt_answer, gestion_id):
        self.audio_text = audio_text
        self.gpt_answer = gpt_answer
        self.gestion_id = gestion_id


class AudiosSchemaPost(Schema):
    audio_text = fields.Dict()
    gpt_answer = fields.Dict()
    gestion_id = fields.Number()


class AudiosSchemaGet(Schema):
    audio_id = fields.Number()
    audio_text = fields.Dict()
    gpt_answer = fields.Dict()
    gestion_id = fields.Number()


