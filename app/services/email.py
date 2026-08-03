import resend
from app.config import get_settings
from app.models.message import Message

settings = get_settings()
resend.api_key = settings.resend_api_key


async def send_contact_email(msg: Message) -> None:
    if not settings.resend_api_key or not settings.contact_email:
        return  # skip in development if not configured

    resend.Emails.send({
        "from": "Portfolio Contact <onboarding@resend.dev>",
        "to": settings.contact_email,
        "reply_to": msg.email,
        "subject": f"[Portfolio] {msg.subject or 'New message'} — from {msg.name}",
        "html": f"""
            <h2>New contact message</h2>
            <p><strong>From:</strong> {msg.name} &lt;{msg.email}&gt;</p>
            <p><strong>Subject:</strong> {msg.subject or '—'}</p>
            <hr>
            <p>{msg.body.replace(chr(10), '<br>')}</p>
        """,
    })
