from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_name: str = "Portfolio API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # Database
    database_url: str

    # Security
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours

    # CORS — comma-separated origins
    frontend_url: str = "http://localhost:3000"
    admin_url: str = "http://localhost:3001"

    # Revalidation webhook secret (shared with portfolio-frontend)
    revalidate_secret: str = ""

    # Cloudinary
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    # Anthropic
    anthropic_api_key: str = ""

    # Email (Resend)
    resend_api_key: str = ""
    contact_email: str = ""

    # GitHub (optional — for fetching repo stats server-side)
    github_token: str = ""
    

    @property
    def allowed_origins(self) -> list[str]:
        return [self.frontend_url, self.admin_url]


@lru_cache
def get_settings() -> Settings:
    return Settings()