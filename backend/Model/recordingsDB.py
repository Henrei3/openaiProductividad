from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.dialects.postgresql import JSONB
from backend.Model.base import Base
from marshmallow import Schema, fields
from sqlalchemy.orm import Mapped, mapped_column


class Gestion(Base):

    __tablename__ = 'gestion'

    id = Column(Integer, primary_key=True)
    g_id = Column(Integer)
    cellphone = Column(Integer)

    def __init__(self, g_id, cellphone):
        self.g_id = g_id
        self.cellphone = cellphone


class GestionSchemaGet(Schema):
    g_id = fields.Number()


class GestionSchemaPost(Schema):
    audio_text = fields.Dict()


class Contenido(Base):
    __tablename__ = "contenido"

    g_id = Column(ForeignKey("gestion.id"), primary_key=True)
    name = Column(String)
    audio_text = Column(JSONB)
    score = Column(JSONB)
    gpt_answer = Column(JSONB)

    def __init__(self, g_id, name, audio_text, score, gpt_answer):
        self.g_id = g_id
        self.name = name
        self.audio_text = audio_text
        self.score = score
        self.gpt_answer = gpt_answer


class ContenidoSchemaPost(Schema):
    nombre = fields.String()
    audio_text = fields.Dict()
    score = fields.Dict()
    gpt_answer = fields.Dict()


class ContenidoSchemaGet(Schema):
    audio_text = fields.Dict()
    score = fields.Dict()
    gpt_answer = fields.Dict()


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




