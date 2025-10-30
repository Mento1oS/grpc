# app/crud.py
from sqlalchemy.orm import Session
from . import models
from typing import List, Optional

def get_terms(db: Session, skip: int = 0, limit: int = 100) -> List[models.Term]:
    return db.query(models.Term).offset(skip).limit(limit).all()

def get_term_by_keyword(db: Session, keyword: str) -> Optional[models.Term]:
    return db.query(models.Term).filter(models.Term.keyword == keyword).first()

def get_term(db: Session, term_id: int) -> Optional[models.Term]:
    return db.query(models.Term).filter(models.Term.id == term_id).first()

def create_term(db: Session, keyword: str, definition: str, source: str = None) -> models.Term:
    db_obj = models.Term(keyword=keyword, definition=definition, source=source)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_term(db: Session, db_obj: models.Term, keyword: str = None, definition: str = None, source: str = None) -> models.Term:
    if keyword is not None:
        db_obj.keyword = keyword
    if definition is not None:
        db_obj.definition = definition
    if source is not None:
        db_obj.source = source
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_term(db: Session, db_obj: models.Term) -> None:
    db.delete(db_obj)
    db.commit()
