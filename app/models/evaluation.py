from sqlalchemy import Column, BigInteger, Text, ForeignKey, DateTime, func, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database import Base


class Evaluation(Base):
    __tablename__ = "evaluation"

    id = Column(BigInteger, primary_key=True, index=True)
    answer_id = Column(BigInteger, ForeignKey("answer.id"), nullable=False)

    evaluator = Column(Text, nullable=False)
    score = Column(Numeric(5, 2), nullable=False)
    details = Column(JSONB)
    evaluated_at = Column(DateTime(timezone=True), server_default=func.now())

    answer = relationship("Answer", back_populates="evaluations")