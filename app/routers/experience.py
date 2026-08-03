from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import DbDep, AdminDep
from app.models.experience import Experience
from app.schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceOut

router = APIRouter(prefix="/experience", tags=["experience"])


@router.get("", response_model=list[ExperienceOut])
def list_experience(db: Session = DbDep):
    return db.query(Experience).order_by(Experience.sort_order, Experience.start_date.desc()).all()


@router.post("", response_model=ExperienceOut, status_code=201, dependencies=[AdminDep])
def create_experience(payload: ExperienceCreate, db: Session = DbDep):
    exp = Experience(**payload.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


@router.patch("/{exp_id}", response_model=ExperienceOut, dependencies=[AdminDep])
def update_experience(exp_id: int, payload: ExperienceUpdate, db: Session = DbDep):
    exp = db.query(Experience).filter(Experience.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(exp, field, value)
    db.commit()
    db.refresh(exp)
    return exp


@router.delete("/{exp_id}", status_code=204, dependencies=[AdminDep])
def delete_experience(exp_id: int, db: Session = DbDep):
    exp = db.query(Experience).filter(Experience.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    db.delete(exp)
    db.commit()
