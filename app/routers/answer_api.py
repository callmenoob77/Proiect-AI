from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..core.evaluator import evaluate_answer
import json

router = APIRouter()


@router.post("/answer/submit", response_model=schemas.EvaluationResult)
def submit_answer(
        submission: schemas.AnswerSubmission,
        db: Session = Depends(get_db)
):
    """
    Acest endpoint primește un răspuns de la utilizator,
    îl salvează în baza de date și apoi îl evaluează.
    """

    # 1. Găsește întrebarea în baza de date
    question = db.query(models.Question).filter(models.Question.id == submission.question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Întrebarea nu a fost găsită.")

    # 2. Salvează răspunsul utilizatorului în tabela 'answer'
    new_answer = models.Answer(
        question_id=submission.question_id,
        answer_text=submission.user_answer,
        source='USER_UI'  # Setează sursa conform modelului tău
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    # 3. Evaluează algoritmic răspunsul
    # Extrage răspunsul corect (stocat ca JSON) din întrebare
    correct_answer_json = question.correct_answer

    if not correct_answer_json:
        raise HTTPException(status_code=500, detail="Întrebarea nu are un răspuns corect definit.")

    question_type = (
        question.question_type.name
        if hasattr(question.question_type, "name")
        else question.question_type
    )
    # Apelează algoritmul de evaluare
    evaluation_result = evaluate_answer(correct_answer_json, submission.user_answer,question_type )

    # 4. Salvează rezultatul evaluării în tabela 'evaluation'
    new_evaluation = models.Evaluation(
        answer_id=new_answer.id,
        evaluator="algorithmic_evaluator_v1",  # Poți schimba asta
        score=evaluation_result["score"],
        details=evaluation_result["details"]  # Salvează detaliile (ex: cuvinte cheie găsite)
    )
    db.add(new_evaluation)
    db.commit()

    correct_answer_text=None
    if "answer" in correct_answer_json:
        correct_answer_text = correct_answer_json["answer"]

    # 5. Returnează rezultatul evaluării la frontend
    return schemas.EvaluationResult(
        is_correct=evaluation_result["is_correct"],
        score=evaluation_result["score"],
        reference_solution=question.reference_solution,  # Trimite soluția de referință
        details=evaluation_result["details"],
        correct_answer=correct_answer_text
    )

