"""Local Ollama adapter (no secrets, runs offline against a local daemon).

Enable with ``KGE_LLM_PROVIDER=ollama`` and (optionally) ``KGE_LLM_MODEL`` /
``KGE_LLM_BASE_URL``. Uses the native ``/api/generate`` endpoint.
"""

from __future__ import annotations

from ..config import settings
from ._entail_prompt import ENTAIL_SYSTEM, entail_prompt, parse_score
from ._http import post_json


class OllamaClient:
    def __init__(self) -> None:
        self.base_url = (settings.llm_base_url or "http://localhost:11434").rstrip("/")
        self.model = settings.llm_model or "llama3.1"
        self.timeout = settings.llm_timeout_s
        self.name = f"ollama:{self.model}"

    def _generate(self, prompt: str, system: str | None) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system
        data = post_json(f"{self.base_url}/api/generate", payload, timeout=self.timeout)
        return (data.get("response") or "").strip()

    def generate(self, prompt: str, *, system: str | None = None, max_tokens: int = 512) -> str:
        return self._generate(prompt, system)

    def entail(self, premise: str, hypothesis: str) -> float:
        return parse_score(self._generate(entail_prompt(premise, hypothesis), ENTAIL_SYSTEM))
