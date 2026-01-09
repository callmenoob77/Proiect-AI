from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random

from ..database import get_db
from .. import models, schemas
from ..question_patterns import QUESTION_PATTERNS

router = APIRouter()

CHAPTER_BY_PATTERN = {
    "CSP": "Satisfacerea Constrangerilor (CSP)",
    "MINIMAX": "Algoritmi de cautare",
    "STRATEGY": "Algoritmi de cautare",
    "THEORY": "Algoritmi de cautare",
}
QUESTION_TYPE_BY_PATTERN = {
    "CSP": "CSP_PROBLEM",
    "MINIMAX": "MINIMAX_TREE",
    "STRATEGY": "A_STAR_DESCRIPTION",
    "THEORY": "A_STAR_DESCRIPTION",
}


#a
@router.post("/custom-question/ask")
def handle_custom_question(
    request: schemas.PatternQuestionRequest,
    db: Session = Depends(get_db)
):
    pattern_type = request.pattern_type
    pattern_id = request.pattern_id
    inputs = request.inputs
    answer_type = request.answer_type

    if pattern_type not in QUESTION_PATTERNS:
        raise HTTPException(status_code=400, detail="Categorie invalida")

    patterns_for_type = QUESTION_PATTERNS[pattern_type]

    if not pattern_id:
        pattern_id = random.choice(list(patterns_for_type.keys()))

    if pattern_id not in patterns_for_type:
        raise HTTPException(status_code=400, detail="Pattern invalid")

    pattern = patterns_for_type[pattern_id]

    expected_inputs = pattern.get("inputs", [])
    missing = [field for field in expected_inputs if field not in inputs]

    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Lipsesc campurile: {', '.join(missing)}"
        )

    try:
        prompt = pattern["template"].format(**inputs)
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Input invalid: {e.args[0]}"
        )

    qdata = {
        "title": f"{pattern_type} – {pattern_id}",
        "prompt": prompt,
        "question_type": QUESTION_TYPE_BY_PATTERN[pattern_type],
        "difficulty": 3,
        "problem_instance": inputs,
        "correct_answer": {},
        "reference_solution": "Rezolvare pe baza raspunsului utilizatorului.",
        "chapter_name": CHAPTER_BY_PATTERN[pattern_type],
    }


    chapter_name = qdata.pop("chapter_name")

    chapter_db = (
        db.query(models.Chapter)
        .filter(models.Chapter.name == chapter_name)
        .first()
    )
    if not chapter_db:
        chapter_db = models.Chapter(name=chapter_name)
        db.add(chapter_db)
        db.commit()
        db.refresh(chapter_db)

    new_question = models.Question(**qdata)
    new_question.chapters.append(chapter_db)

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "id": new_question.id,
        "title": new_question.title,
        "prompt": new_question.prompt,
        "question_type": new_question.question_type,
        "difficulty": new_question.difficulty,
        "problem_instance": new_question.problem_instance,
        "answer_type": answer_type,   # DOAR pt UI
        "protected": new_question.protected,
    }
