import httpx
from app.config import get_settings

settings = get_settings()


def trigger_revalidate(path: str) -> None:
    """
    Calls the Next.js revalidation webhook on portfolio-frontend
    so Vercel rebuilds the ISR page after a content change.
    Fire-and-forget — failures are logged but never raise.
    """
    if not settings.revalidate_secret or not settings.frontend_url:
        return
    try:
        url = f"{settings.frontend_url}/api/revalidate"
        httpx.post(
            url,
            json={"path": path, "secret": settings.revalidate_secret},
            timeout=5.0,
        )
    except Exception:
        pass  # non-critical — content will revalidate on next timed interval
