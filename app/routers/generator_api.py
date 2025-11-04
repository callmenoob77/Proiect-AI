from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.generator import genereaza_intrebare_strategie
from .. import models, schemas

router = APIRouter()


@router.post("/generate/strategy")
def handle_generate_strategy_question(
        request: schemas.GenerationRequest,
        db: Session = Depends(get_db)
):
    """
    Generează o întrebare de tip strategie.
    Acceptă answer_type: "multiple" sau "text"
    """
    try:
        question_data = genereaza_intrebare_strategie(answer_type=request.answer_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    chapter_name = question_data.pop("chapter_name")
    answer_type = question_data.pop("answer_type", "multiple")
    options = question_data.pop("options", None)

    # Găsește sau creează capitolul
    chapter_db = db.query(models.Chapter).filter(models.Chapter.name == chapter_name).first()

    if not chapter_db:
        # Creează capitolul dacă nu există
        chapter_db = models.Chapter(name=chapter_name)
        db.add(chapter_db)
        db.commit()
        db.refresh(chapter_db)

    # Creează întrebarea
    new_question = models.Question(**question_data)
    new_question.chapters.append(chapter_db)

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    # Pregătește răspunsul pentru frontend
    question_dict = {
        "id": new_question.id,
        "title": new_question.title,
        "prompt": new_question.prompt,
        "question_type": new_question.question_type.value if hasattr(new_question.question_type,
                                                                     'value') else new_question.question_type,
        "difficulty": new_question.difficulty,
        "problem_instance": new_question.problem_instance,
        "reference_solution": new_question.reference_solution,
        "answer_type": answer_type,
        "protected": new_question.protected
    }

    # Adaugă opțiunile doar pentru întrebări multiple
    if options:
        question_dict["options"] = options

    return question_dict