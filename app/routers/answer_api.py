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

    question = db.query(models.Question).filter(models.Question.id == submission.question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Întrebarea nu a fost găsită.")

    new_answer = models.Answer(
        question_id=submission.question_id,
        answer_text=submission.user_answer,
        source='USER_UI' 
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    correct_answer_json = question.correct_answer

    if not correct_answer_json:
        raise HTTPException(status_code=500, detail="Întrebarea nu are un răspuns corect definit.")

    evaluation_result = evaluate_answer(correct_answer_json, submission.user_answer)

    new_evaluation = models.Evaluation(
        answer_id=new_answer.id,
        evaluator="algorithmic_evaluator_v1",
        score=evaluation_result["score"],
        details=evaluation_result["details"]
    )
    db.add(new_evaluation)
    db.commit()

    correct_answer_text=None
    if "answer" in correct_answer_json:
        correct_answer_text = correct_answer_json["answer"]

    return schemas.EvaluationResult(
        is_correct=evaluation_result["is_correct"],
        score=evaluation_result["score"],
        reference_solution=question.reference_solution,
        details=evaluation_result["details"],
        correct_answer=correct_answer_text
    )

