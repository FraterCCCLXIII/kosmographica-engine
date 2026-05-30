"""Hosted, OpenAI-compatible chat-completions adapter.

Works with any OpenAI-compatible endpoint (OpenAI, Azure, Together, local
vLLM/LM Studio, …). Enable with ``KGE_LLM_PROVIDER=openai`` and set
``KGE_LLM_API_KEY``, ``KGE_LLM_MODEL``, and optionally ``KGE_LLM_BASE_URL``.
"""

from __future__ import annotations

from ..config import settings
from ._entail_prompt import ENTAIL_SYSTEM, entail_prompt, parse_score
from ._http import LLMHTTPError, post_json


class OpenAICompatClient:
    def __init__(self) -> None:
        if not settings.llm_api_key:
            raise LLMHTTPError("KGE_LLM_API_KEY is required for the openai provider")
        self.base_url = (settings.llm_base_url or "https://api.openai.com/v1").rstrip("/")
        self.model = settings.llm_model or "gpt-4o-mini"
        self.timeout = settings.llm_timeout_s
        self.api_key = settings.llm_api_key
        self.name = f"openai:{self.model}"

    def _chat(self, prompt: str, system: str | None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        data = post_json(
            f"{self.base_url}/chat/completions",
            {"model": self.model, "messages": messages, "temperature": 0},
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=self.timeout,
        )
        return (data["choices"][0]["message"]["content"] or "").strip()

    def generate(self, prompt: str, *, system: str | None = None, max_tokens: int = 512) -> str:
        return self._chat(prompt, system)

    def entail(self, premise: str, hypothesis: str) -> float:
        return parse_score(self._chat(entail_prompt(premise, hypothesis), ENTAIL_SYSTEM))
