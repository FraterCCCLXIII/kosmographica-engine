"""Verifier evaluation harness + baseline gate (Wave 2, W2.1).

Scores a :class:`~kge.verify.Verifier` against a gold set of
``(source, assertion, quotes, label)`` rows and reports precision/recall/F1 of
the *accept* decision versus the gold ``entailed`` label. The gate compares the
configured LLM verifier against the deterministic lexical baseline: a model swap
should not regress F1. ``label`` is one of ``entailed`` / ``not_entailed``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .verify import Verifier

DEFAULT_GOLD = Path(__file__).resolve().parents[2] / "evals" / "verifier_gold.jsonl"


@dataclass
class GoldItem:
    id: str
    source_text: str
    assertion: str
    quotes: list[str]
    label: str  # entailed | not_entailed


@dataclass
class Metrics:
    n: int
    tp: int
    fp: int
    tn: int
    fn: int

    @property
    def precision(self) -> float:
        denom = self.tp + self.fp
        return self.tp / denom if denom else 0.0

    @property
    def recall(self) -> float:
        denom = self.tp + self.fn
        return self.tp / denom if denom else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) else 0.0

    @property
    def accuracy(self) -> float:
        return (self.tp + self.tn) / self.n if self.n else 0.0

    def as_dict(self) -> dict:
        return {
            "n": self.n,
            "precision": round(self.precision, 3),
            "recall": round(self.recall, 3),
            "f1": round(self.f1, 3),
            "accuracy": round(self.accuracy, 3),
        }


def load_gold(path: str | Path = DEFAULT_GOLD) -> list[GoldItem]:
    items: list[GoldItem] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        items.append(
            GoldItem(
                id=row["id"],
                source_text=row["source_text"],
                assertion=row["assertion"],
                quotes=list(row.get("quotes", [])),
                label=row["label"],
            )
        )
    return items


def evaluate(verifier: Verifier, gold: list[GoldItem]) -> Metrics:
    tp = fp = tn = fn = 0
    for item in gold:
        result = verifier.verify(
            assertion=item.assertion, quotes=item.quotes, source_text=item.source_text
        )
        predicted_positive = result.outcome == "accept"
        gold_positive = item.label == "entailed"
        if predicted_positive and gold_positive:
            tp += 1
        elif predicted_positive and not gold_positive:
            fp += 1
        elif not predicted_positive and gold_positive:
            fn += 1
        else:
            tn += 1
    return Metrics(n=len(gold), tp=tp, fp=fp, tn=tn, fn=fn)


@dataclass
class EvalReport:
    baseline: Metrics
    candidate: Metrics
    candidate_name: str

    @property
    def passed(self) -> bool:
        # The model swap may not regress F1 against the lexical baseline.
        return self.candidate.f1 >= self.baseline.f1

    def as_dict(self) -> dict:
        return {
            "passed": self.passed,
            "baseline": self.baseline.as_dict(),
            "candidate": {"name": self.candidate_name, **self.candidate.as_dict()},
        }


def run_eval(client=None, *, gold_path: str | Path = DEFAULT_GOLD) -> EvalReport:
    """Evaluate the configured LLM verifier against the lexical baseline."""
    from .verify import make_llm_verifier

    gold = load_gold(gold_path)
    baseline = evaluate(Verifier(), gold)
    candidate_verifier = make_llm_verifier(client)
    candidate = evaluate(candidate_verifier, gold)
    return EvalReport(baseline=baseline, candidate=candidate, candidate_name=candidate_verifier.name)
