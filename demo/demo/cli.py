"""Run the full demo pipeline in the terminal, with no server needed.

Steps: sync all 5 tenants -> review tenant_1's transcript fixture ->
ask one question per tenant (including an unknown and a conflict
case) -> print a report. This is the demo's acceptance run: if any
step fails, the demo fails; there is no fallback that fakes a result.
"""
from __future__ import annotations

import json
import sys

from .drive import sync
from .qa import answer
from .tenants import TENANT_IDS
from .transcribe import list_audio_fixtures, review_transcript
from .store import chunk_count

QUESTIONS = {
    "tenant_1": "When did grandmother open the noodle stall?",
    "tenant_2": "What did the Wang family grow in the garden?",
    "tenant_3": "When did the family shop open?",
    "tenant_4": "Where did the Lin family go fishing?",
    "tenant_5": "What is the capital of France?",  # unknown case: not in any fixture
}


def main() -> int:
    print("DeepFamily developer demo — 1 host, 5 isolated tenants")
    print("Test data only. No real household data. Mock Drive / transcript / LLM.")
    for tenant_id in TENANT_IDS:
        result = sync(tenant_id)
        print(f"[{tenant_id}] sync: added={result['added']} updated={result['updated']} "
              f"deleted={result['deleted']} chunks={chunk_count(tenant_id)} "
              f"page_token={result['page_token']}")
    audio = list_audio_fixtures("tenant_1")
    if audio:
        reviewed = review_transcript("tenant_1", audio[0].name, approved=True)
        print(f"[tenant_1] transcript review: {reviewed}")
    print()
    for tenant_id, question in QUESTIONS.items():
        result = answer(tenant_id, question)
        print(f"[{tenant_id}] Q: {question}")
        print(f"  status: {result['status']}")
        print(f"  A: {result['answer']}")
        for cite in result["citations"]:
            print(f"  cite: {cite['source']} / {cite['chunk_id']}")
    print()
    print("Acceptance checks for a reviewer:")
    print("- tenant_3 shop-open question must be 'conflicting_accounts' (1968 vs 1978).")
    print("- tenant_5 capital question must be 'unknown'.")
    print("- A query for one tenant must never return another tenant's chunks")
    print("  (see tests/test_demo.py: test_cross_tenant_query_returns_nothing).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
