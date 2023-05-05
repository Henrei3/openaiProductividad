from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB, insert
from base import Base


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

