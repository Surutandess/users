from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from typing import Optional
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class JWTModel(BaseModel):
    secret_key: Path = BASE_DIR / "certificates" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certificates" / "jwt-public.pem"
    algorithm: str = "RS256"
    expire_access_token_minutes: int = 30
    expire_refresh_token_days: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")
    auth: JWTModel = JWTModel()
    ADMIN_USERNAME: Optional[str] = None
    ADMIN_PASSWORD: Optional[str] = None
    DB_URL: str


settings = Settings()
