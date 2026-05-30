"""The LLM client contract and the config-driven factory.

Two capabilities cover Wave 2's needs:

* ``generate`` — free-form completion, used by the LLM **author** to extract
  grounded claims from retrieved source text.
* ``entail`` — a 0..1 score that the cited text *entails* an assertion, used by
  the **verifier** behind the existing ``Verifier(entailment=...)`` seam.

Concrete adapters live alongside this module and are imported lazily so that
installing/operating the engine never requires a provider SDK or network unless
that provider is actually selected.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMClient(Protocol):
    name: str

    def generate(self, prompt: str, *, system: str | None = None, max_tokens: int = 512) -> str: ...

    def entail(self, premise: str, hypothesis: str) -> float:
        """Probability in ``[0, 1]`` that ``premise`` supports ``hypothesis``."""
        ...


def get_llm_client(provider: str | None = None) -> LLMClient:
    """Return the configured LLM client. Defaults to the offline ``fake``.

    Adapters are imported lazily so a missing optional dependency for an unused
    provider never breaks import of the engine.
    """
    from ..config import settings

    provider = (provider or settings.llm_provider or "fake").lower()
    if provider == "fake":
        from .fake import FakeLLMClient

        return FakeLLMClient()
    if provider == "ollama":
        from .ollama import OllamaClient

        return OllamaClient()
    if provider == "openai":
        from .openai_compat import OpenAICompatClient

        return OpenAICompatClient()
    raise ValueError(f"unknown LLM provider {provider!r} (known: fake, ollama, openai)")
