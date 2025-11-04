from pydantic import BaseModel, Field
from typing import Optional, List, Any

class GenerationRequest(BaseModel):
    answer_type: str = Field(default="multiple", description="Tipul răspunsului: 'multiple' sau 'text'")

class AnswerSubmission(BaseModel):
    question_id: int
    user_answer: str

class EvaluationResult(BaseModel):
    is_correct: bool
    score: float
    reference_solution: str
    details: Optional[dict] = None
    correct_answer: Optional[str] = None