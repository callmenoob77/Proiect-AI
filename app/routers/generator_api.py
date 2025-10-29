from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..core.generator import genereaza_intrebare_strategie
from .. import models  # Acest import este corect

router = APIRouter()
@router.post("/generate/strategy", response_model=None)
def handle_generate_strategy_question(db: Session = Depends(get_db)):
    question_data = genereaza_intrebare_strategie()

    chapter_name = question_data.pop("chapter_name")

    chapter_db = db.query(models.Chapter).filter(models.Chapter.name == chapter_name).first()

    if not chapter_db:

        raise HTTPException(status_code=404, detail=f"Capitolul '{chapter_name}' nu a fost gasit.")

    new_question = models.Question(**question_data)

    new_question.chapters.append(chapter_db)

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question