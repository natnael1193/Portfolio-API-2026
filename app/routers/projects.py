from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.dependencies import DbDep, AdminDep
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.schemas.common import PaginatedResponse
from app.services.revalidate import trigger_revalidate
import math
from sqlalchemy import cast, String

router = APIRouter(prefix="/projects", tags=["projects"])


# ── Public ────────────────────────────────────────────────

@router.get("", response_model=PaginatedResponse[ProjectOut])
def list_projects(
    db: Session = DbDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    tag: str | None = None,
    featured: bool | None = None,
):
    q = db.query(Project).filter(Project.published == True)
    if tag:
        q = q.filter(cast(Project.tags, String).contains(tag))
    if featured is not None:
        q = q.filter(Project.featured == featured)
    total = q.count()
    items = q.order_by(Project.sort_order, Project.created_at.desc()) \
             .offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size),
    )


@router.get("/{slug}", response_model=ProjectOut)
def get_project(slug: str, db: Session = DbDep):
    project = db.query(Project).filter(
        Project.slug == slug, Project.published == True
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# ── Admin ────────────────────────────────────────────────

@router.post("", response_model=ProjectOut, status_code=201, dependencies=[AdminDep])
def create_project(payload: ProjectCreate, db: Session = DbDep):
    existing = db.query(Project).filter(Project.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=409, detail="Slug already exists")
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    if project.published:
        trigger_revalidate(f"/projects/{project.slug}")
    return project


@router.patch("/{project_id}", response_model=ProjectOut, dependencies=[AdminDep])
def update_project(project_id: int, payload: ProjectUpdate, db: Session = DbDep):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    trigger_revalidate(f"/projects/{project.slug}")
    return project


@router.delete("/{project_id}", status_code=204, dependencies=[AdminDep])
def delete_project(project_id: int, db: Session = DbDep):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    trigger_revalidate(f"/projects/{project.slug}")
    db.delete(project)
    db.commit()


@router.get("/admin/all", response_model=list[ProjectOut], dependencies=[AdminDep])
def admin_list_all(db: Session = DbDep):
    return db.query(Project).order_by(Project.sort_order, Project.created_at.desc()).all()