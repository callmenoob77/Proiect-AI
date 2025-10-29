from sqlalchemy import Column, BigInteger, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base
from .enums import AnswerSourceSQL


class Answer(Base):
    __tablename__ = "answer"

    id = Column(BigInteger, primary_key=True, index=True)
    question_id = Column(BigInteger, ForeignKey("question.id"), nullable=False)

    submitted_by = Column(Text)
    source = Column(AnswerSourceSQL, default='USER_UI')
    answer_text = Column(Text)
    answer_file_path = Column(Text)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship("Question", back_populates="answers")

    evaluations = relationship("Evaluation", back_populates="answer")