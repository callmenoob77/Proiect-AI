from sqlalchemy import (
    Column, BigInteger, Integer, Text, ForeignKey, Table,
    JSON, DateTime, Boolean, SmallInteger, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database import Base
from .enums import QuestionTypeSQL

question_chapter_association = Table(
    'question_chapter',
    Base.metadata,
    Column('question_id', ForeignKey('question.id'), primary_key=True),
    Column('chapter_id', ForeignKey('chapter.id'), primary_key=True)
)


class Question(Base):
    __tablename__ = "question"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    prompt = Column(Text, nullable=False)

    question_type = Column(QuestionTypeSQL, nullable=False)

    difficulty = Column(SmallInteger)

    problem_instance = Column(JSONB)
    correct_answer = Column(JSONB)
    reference_solution = Column(Text)

    generated_by = Column(Text)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    protected = Column(Boolean, default=False)
    metadata_ = Column("metadata", JSONB)
    version = Column(Integer, default=1)

    chapters = relationship(
        "Chapter",
        secondary=question_chapter_association,
        back_populates="questions"
    )

    answers = relationship("Answer", back_populates="question")