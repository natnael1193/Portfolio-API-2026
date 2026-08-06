from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import DbDep, AdminDep
from app.models.cv import CV
from app.schemas.cv import CVCreate, CVUpdate, CVOut


router = APIRouter(prefix="/cv", tags=["cv"])

@router.get("", response_model=list[CVOut])
def list_cvs(db: Session = DbDep):
    return db.query(CV).all()


@router.post("", response_model=CVOut, status_code=201, dependencies=[AdminDep])
def create_cv(payload: CVCreate, db: Session = DbDep):
    cv = CV(**payload.model_dump())
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv


@router.patch("/{cv_id}", response_model=CVOut, dependencies=[AdminDep])
def update_cv(cv_id: int, payload: CVUpdate, db: Session = DbDep):
    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cv, field, value)
    db.commit()
    db.refresh(cv)
    return cv

@router.delete("/{cv_id}", status_code=204, dependencies=[AdminDep])
def delete_cv(cv_id: int, db: Session = DbDep):
    cv = db.query(CV).filter(CV.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    db.delete(cv)
    db.commit()