from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.dependencies import DbDep, AdminDep
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostOut
from app.schemas.common import PaginatedResponse
from app.services.revalidate import trigger_revalidate
import math

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PaginatedResponse[PostOut])
def list_posts(
    db: Session = DbDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    tag: str | None = None,
):
    q = db.query(Post).filter(Post.published == True)
    if tag:
        q = q.filter(Post.tags.contains([tag]))
    total = q.count()
    items = q.order_by(Post.published_at.desc(), Post.created_at.desc()) \
             .offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size,
                             total_pages=math.ceil(total / page_size))


@router.get("/{slug}", response_model=PostOut)
def get_post(slug: str, db: Session = DbDep):
    post = db.query(Post).filter(Post.slug == slug, Post.published == True).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("", response_model=PostOut, status_code=201, dependencies=[AdminDep])
def create_post(payload: PostCreate, db: Session = DbDep):
    if db.query(Post).filter(Post.slug == payload.slug).first():
        raise HTTPException(status_code=409, detail="Slug already exists")
    post = Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    if post.published:
        trigger_revalidate(f"/blog/{post.slug}")
    return post


@router.patch("/{post_id}", response_model=PostOut, dependencies=[AdminDep])
def update_post(post_id: int, payload: PostUpdate, db: Session = DbDep):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    trigger_revalidate(f"/blog/{post.slug}")
    return post


@router.delete("/{post_id}", status_code=204, dependencies=[AdminDep])
def delete_post(post_id: int, db: Session = DbDep):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    trigger_revalidate(f"/blog/{post.slug}")
    db.delete(post)
    db.commit()


@router.get("/admin/all", response_model=list[PostOut], dependencies=[AdminDep])
def admin_list_all(db: Session = DbDep):
    return db.query(Post).order_by(Post.created_at.desc()).all()
