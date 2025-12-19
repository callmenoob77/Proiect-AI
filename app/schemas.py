from pydantic import BaseModel, Field
from typing import Optional, List, Any, Literal, Dict


class GenerationRequest(BaseModel):
    """
    Corpul cererii pentru a genera o întrebare.
    Trimis de frontend.
    """
    answer_type: str = Field(default="multiple", description="Tipul răspunsului: 'multiple' sau 'text'")

class AnswerSubmission(BaseModel):
    """
    Corpul cererii pentru a trimite un răspuns.
    Trimis de frontend.
    """
    question_id: int
    user_answer: str  # Textul răspunsului (fie opțiunea selectată, fie textul scris)

class EvaluationResult(BaseModel):
    """
    Răspunsul trimis înapoi la frontend după evaluare.
    """
    is_correct: bool
    score: float
    reference_solution: str
    details: Optional[dict] = None
    correct_answer: Optional[str] = None  # Răspunsul corect (pentru debugging)

class CustomUserQuestion(BaseModel):
    """
    Corpul cererii pentru o întrebare scrisă manual de utilizator.
    """
    question_text: str = Field(
        ...,
        description="Textul întrebării scrise de utilizator"
    )

    question_category: Literal[
        "CSP",
        "MINIMAX",
        "STRATEGY",
        "THEORY"
    ] = Field(
        ...,
        description="Categoria selectată de utilizator"
    )

    answer_type: str = Field(
        default="multiple",
        description="Tipul răspunsului: 'multiple' sau 'text'"
    )
class PatternQuestionRequest(BaseModel):
    pattern_type: str        # CSP / MINIMAX / THEORY / STRATEGY
    pattern_id: str | None   # FC / MRV / AC3 / BASIC / etc
    inputs: Dict[str, Any]
    answer_type: str = "multiple"