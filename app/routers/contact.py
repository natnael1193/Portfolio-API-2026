from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import DbDep, AdminDep
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageOut
from app.services.email import send_contact_email

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("", response_model=MessageOut, status_code=201)
async def submit_contact(payload: MessageCreate, db: Session = DbDep):
    msg = Message(**payload.model_dump())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    await send_contact_email(msg)
    return msg


@router.get("", response_model=list[MessageOut], dependencies=[AdminDep])
def list_messages(db: Session = DbDep, unread_only: bool = False):
    q = db.query(Message)
    if unread_only:
        q = q.filter(Message.read == False)
    return q.order_by(Message.created_at.desc()).all()


@router.patch("/{message_id}/read", response_model=MessageOut, dependencies=[AdminDep])
def mark_read(message_id: int, db: Session = DbDep):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.read = True
    db.commit()
    db.refresh(msg)
    return msg


@router.delete("/{message_id}", status_code=204, dependencies=[AdminDep])
def delete_message(message_id: int, db: Session = DbDep):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
