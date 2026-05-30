"""Engine settings, driven by environment variables (12-factor)."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="KGE_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://kosmo:kosmo@localhost:5459/kosmographica"

    # Lowest trust tier that the public read API is allowed to surface.
    # `machine_validated` and above are public-but-badged; `machine_unverified` is hidden.
    public_min_tier: str = "machine_validated"


settings = Settings()
