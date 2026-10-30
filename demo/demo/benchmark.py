"""Concurrency benchmark.

Runs the same Q&A question for N concurrent sessions and measures
wall-clock time, time to first completed answer, and aggregate
tokens/second (words/second in this mock, model tokens/second on a
real Mac mini model). This measures the demo's retrieval + template
path, NOT a real LLM — on a Mac mini, swap qa.answer() for the real
model call and keep the same measurement code, so numbers stay
comparable. Results are written to benchmark_report.json.
"""
from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .qa import answer, token_count
from .tenants import save_json

QUESTIONS = {
    "tenant_1": "When did grandmother open the noodle stall?",
    "tenant_2": "What did the Wang family grow in the garden?",
    "tenant_3": "When did the family shop open?",
    "tenant_4": "Where did the Lin family go fishing?",
    "tenant_5": "How long did the Huang children walk to school?",
}


def _one(args) -> dict:
    tenant_id, question = args
    started = time.perf_counter()
    result = answer(tenant_id, question)
    elapsed = time.perf_counter() - started
    return {"tenant_id": tenant_id, "status": result["status"],
            "elapsed_s": elapsed, "tokens": token_count(result["answer"])}


def run(concurrency: int) -> dict:
    tenants = list(QUESTIONS)[:concurrency] if concurrency <= 5 else list(QUESTIONS) * (concurrency // 5 + 1)
    jobs = [(tid, QUESTIONS[tid]) for tid in tenants[:concurrency]]
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        results = list(pool.map(_one, jobs))
    total = time.perf_counter() - started
    total_tokens = sum(r["tokens"] for r in results)
    return {
        "concurrency": concurrency,
        "sessions": len(results),
        "total_s": round(total, 4),
        "first_answer_s": round(min(r["elapsed_s"] for r in results), 4),
        "aggregate_tokens_per_s": round(total_tokens / total, 1) if total else 0,
        "statuses": [r["status"] for r in results],
        "note": "Mock path (retrieval + template). On a Mac mini with a real "
                "model, these numbers must be re-measured with that model.",
    }


def run_all() -> dict:
    report = {"runs": [run(n) for n in (1, 3, 5)]}
    out = Path(__file__).resolve().parent.parent / "benchmark_report.json"
    save_json(out, report)
    return report
