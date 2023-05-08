from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from backend.Model.base import Base
from marshmallow import Schema, fields


class Recordings(Base):

    __tablename__ = 'recordings'

    id = Column(Integer, primary_key=True)

    audio_text = Column(JSONB)

    gpt_answer = Column(JSONB)

    patterns = Column(JSONB)

    score = Column(JSONB)

    def __init__(self, audio_text, gpt_answer, patterns, score):

        self.audio_text = audio_text
        self.gpt_answer = gpt_answer
        self.patterns = patterns
        self.score = score


class RecordingSchemaGet(Schema):
    id = fields.Number()

    audio_text = fields.Dict()
    gpt_answer = fields.Dict()
    patterns = fields.Dict()
    score = fields.Dict()


class RecordingSchemaPost(Schema):
    audio_text = fields.Dict()
    gpt_answer = fields.Dict()
    patterns = fields.Dict()
    score = fields.Dict()


class Simple(Base):
    __tablename__ = 'simple'

    id = Column(Integer, primary_key=True)
    num = Column(Integer)

    def __init__(self, num):
        self.num = num


class SimpleSchemaPost(Schema):
    num = fields.Number()


class SimpleSchemaGet(Schema):
    id = fields.Number()
    num = fields.Number()
