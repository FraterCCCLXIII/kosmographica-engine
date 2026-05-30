"""Engine settings, driven by environment variables (12-factor)."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="KGE_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://kosmo:kosmo@localhost:5459/kosmographica"

    # Lowest trust tier that the public read API is allowed to surface.
    # `machine_validated` and above are public-but-badged; `machine_unverified` is hidden.
    public_min_tier: str = "machine_validated"

    # --- LLM (provider-agnostic, Wave 2) -------------------------------------
    # Author + verifier call a thin LLMClient. No provider is pinned: pick one at
    # deploy time. "fake" is a deterministic offline client used by tests/CI.
    llm_provider: str = "fake"  # fake | ollama | openai
    llm_model: str = ""  # provider default applied when blank
    llm_base_url: str = ""  # e.g. http://localhost:11434 (ollama) or an OpenAI-compatible base
    llm_api_key: str = ""
    llm_timeout_s: float = 60.0

    # Entailment acceptance threshold for the publish-then-verify gate.
    verify_accept_threshold: float = 0.6

    # --- Embeddings (DEFERRED to Wave 3) -------------------------------------
    # The Retriever seam supports a future VectorRetriever; for now retrieval is
    # keyword/graph-based and this stays "none".
    embedding_provider: str = "none"


settings = Settings()
