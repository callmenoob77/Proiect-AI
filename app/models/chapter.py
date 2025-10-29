from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from ..database import Base
from .question import question_chapter_association

class Chapter(Base):
    __tablename__ = "chapter"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, unique=True)

    questions = relationship(
        "Question",
        secondary=question_chapter_association,
        back_populates="chapters"
    )