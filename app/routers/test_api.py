from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import random

from ..database import get_db
from ..models import Question
from ..schemas import GenerationRequest, AnswerSubmission, EvaluationResult

# Import corect pentru generator din app/core/
from ..core.generator import genereaza_intrebare_strategie
from ..core.evaluator import evaluate_answer

router = APIRouter()


@router.post("/test/generate")
def generate_test(num_questions: int = 5, db: Session = Depends(get_db)):
    """
    Generează un test cu N întrebări de tip multiple choice
    """
    if num_questions < 1 or num_questions > 20:
        raise HTTPException(
            status_code=400,
            detail="Numărul de întrebări trebuie să fie între 1 și 20"
        )

    test_questions = []

    for i in range(num_questions):
        try:
            # Generăm doar întrebări multiple choice
            question_data = genereaza_intrebare_strategie(answer_type="multiple")

            # Salvăm în baza de date
            # Punem options în problem_instance pentru a le păstra
            problem_instance_data = question_data.get("problem_instance", {})
            problem_instance_data["options"] = question_data.get("options", [])

            db_question = Question(
                title=question_data["title"],
                prompt=question_data["prompt"],
                question_type=question_data["question_type"],
                difficulty=question_data.get("difficulty", 3),
                problem_instance=problem_instance_data,
                correct_answer=question_data["correct_answer"],
                reference_solution=question_data["reference_solution"]
            )
            db.add(db_question)
            db.commit()
            db.refresh(db_question)

            # Construim răspunsul pentru frontend (fără răspunsul corect)
            # Extragem options din problem_instance
            options = db_question.problem_instance.get("options", []) if db_question.problem_instance else []

            test_questions.append({
                "id": db_question.id,
                "title": db_question.title,
                "prompt": db_question.prompt,
                "question_type": db_question.question_type,
                "difficulty": db_question.difficulty,
                "problem_instance": db_question.problem_instance,
                "options": options,
                "answer_type": "multiple"
            })
        except Exception as e:
            # Dacă o întrebare eșuează, continuăm cu următoarea
            print(f"Eroare la generarea întrebării {i + 1}: {e}")
            continue

    if len(test_questions) == 0:
        raise HTTPException(
            status_code=500,
            detail="Nu s-a putut genera nicio întrebare pentru test"
        )

    return {
        "test_id": random.randint(1000, 9999),
        "num_questions": len(test_questions),
        "questions": test_questions
    }


@router.post("/test/submit")
def submit_test(
        answers: Dict[int, str],  # {question_id: selected_answer}
        db: Session = Depends(get_db)
):
    """
    Trimite răspunsurile la un test complet
    Returns: {question_id: {is_correct, score, reference_solution, correct_answer}}
    """
    results = {}
    total_score = 0
    correct_count = 0

    for question_id, user_answer in answers.items():
        # Găsim întrebarea în DB
        db_question = db.query(Question).filter(Question.id == question_id).first()
        if not db_question:
            results[question_id] = {
                "error": "Question not found"
            }
            continue

        # Evaluăm răspunsul
        evaluation = evaluate_answer(
            db_question.correct_answer,
            user_answer,
            db_question.question_type
        )

        results[question_id] = {
            "is_correct": evaluation["is_correct"],
            "score": evaluation["score"],
            "reference_solution": db_question.reference_solution,
            "correct_answer": db_question.correct_answer.get("answer", "N/A"),
            "user_answer": user_answer
        }

        total_score += evaluation["score"]
        if evaluation["is_correct"]:
            correct_count += 1

    num_questions = len(answers)
    average_score = total_score / num_questions if num_questions > 0 else 0

    return {
        "results": results,
        "summary": {
            "total_questions": num_questions,
            "correct_answers": correct_count,
            "average_score": round(average_score, 2),
            "percentage": round(average_score, 2)
        }
    }