from fastapi import APIRouter, Query
from sqlalchemy.orm import Session
from app.core.dependencies import DbDep
from app.models.page_view import PageView
from pydantic import BaseModel

router = APIRouter(prefix="/views", tags=["views"])


class ViewsOut(BaseModel):
    path: str
    count: int


@router.get("", response_model=ViewsOut)
def get_views(path: str = Query(..., description="Page path e.g. /projects/my-project"),
              db: Session = DbDep):
    record = db.query(PageView).filter(PageView.path == path).first()
    return ViewsOut(path=path, count=record.count if record else 0)


@router.post("", response_model=ViewsOut)
def increment_views(path: str = Query(...), db: Session = DbDep):
    record = db.query(PageView).filter(PageView.path == path).first()
    if record:
        record.count += 1
    else:
        record = PageView(path=path, count=1)
        db.add(record)
    db.commit()
    db.refresh(record)
    return ViewsOut(path=record.path, count=record.count)
