"""Provider-agnostic LLM access (Wave 2, ADR-013).

The author and verifier never import a vendor SDK directly — they depend on the
``LLMClient`` protocol and obtain a concrete client from :func:`get_llm_client`,
which is selected by ``KGE_LLM_PROVIDER``. ``fake`` is a deterministic, offline
client so the whole publish-then-verify loop (and CI) runs without secrets or a
network. Swapping to a hosted API or local Ollama is a config change, not a code
change.
"""

from .client import LLMClient, get_llm_client
from .fake import FakeLLMClient

__all__ = ["LLMClient", "get_llm_client", "FakeLLMClient"]
