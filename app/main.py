from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, projects, posts, skills, experience, contact, views, chat, upload

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup if they don't exist (Alembic handles production migrations)
    if settings.environment == "development":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers under /api prefix
PREFIX = "/api"
app.include_router(auth.router, prefix=PREFIX)
app.include_router(projects.router, prefix=PREFIX)
app.include_router(posts.router, prefix=PREFIX)
app.include_router(skills.router, prefix=PREFIX)
app.include_router(experience.router, prefix=PREFIX)
app.include_router(contact.router, prefix=PREFIX)
app.include_router(views.router, prefix=PREFIX)
app.include_router(chat.router, prefix=PREFIX)
app.include_router(upload.router, prefix=PREFIX)


@app.get("/health")
def health():
    return {"status": "ok", "version": settings.app_version}
