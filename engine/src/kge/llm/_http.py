"""Minimal JSON-over-HTTP helper (stdlib only) for the LLM adapters.

Avoids adding an HTTP dependency for providers that may never be enabled.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class LLMHTTPError(RuntimeError):
    pass


def post_json(url: str, payload: dict, *, headers: dict[str, str] | None = None, timeout: float = 60.0) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:  # pragma: no cover - network path
        detail = exc.read().decode("utf-8", "replace")
        raise LLMHTTPError(f"{exc.code} {exc.reason}: {detail}") from exc
    except urllib.error.URLError as exc:  # pragma: no cover - network path
        raise LLMHTTPError(f"could not reach {url}: {exc.reason}") from exc
