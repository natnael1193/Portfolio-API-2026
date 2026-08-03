from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import DbDep, AdminDep
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate, SkillOut

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=list[SkillOut])
def list_skills(db: Session = DbDep):
    return db.query(Skill).order_by(Skill.category, Skill.sort_order).all()


@router.post("", response_model=SkillOut, status_code=201, dependencies=[AdminDep])
def create_skill(payload: SkillCreate, db: Session = DbDep):
    skill = Skill(**payload.model_dump())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.patch("/{skill_id}", response_model=SkillOut, dependencies=[AdminDep])
def update_skill(skill_id: int, payload: SkillUpdate, db: Session = DbDep):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(skill, field, value)
    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/{skill_id}", status_code=204, dependencies=[AdminDep])
def delete_skill(skill_id: int, db: Session = DbDep):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
