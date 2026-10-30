"""Q&A: answer ONLY from retrieved chunks for the querying tenant.

Rules (from the R&D requirements book):
- No retrieved chunk -> "unknown", never fabricated.
- Two retrieved chunks in the same conflict group with different
  text -> "conflicting accounts", shown side by side, never resolved.
- Otherwise -> answer template built from the retrieved chunks,
  with a citation (source file + chunk id) per claim.
The wording is a template, NOT an LLM. A real adapter replaces
build_answer() with a local model call that is constrained to the
same retrieved chunks and the same three outcomes.
"""
from __future__ import annotations

import re

from .store import retrieve

_YEAR = re.compile(r"\b(19|20)\d{2}\b")


def answer(tenant_id: str, question: str) -> dict:
    chunks = retrieve(tenant_id, question, top_k=3)
    if not chunks:
        return {
            "tenant_id": tenant_id,
            "question": question,
            "status": "unknown",
            "answer": "Unknown / not found in the authorised material for this household.",
            "citations": [],
        }

    # Conflict: same conflict group, different texts, both retrieved.
    groups: dict[str, list[dict]] = {}
    for chunk in chunks:
        if chunk.get("conflict_group"):
            groups.setdefault(chunk["conflict_group"], []).append(chunk)
    for group, members in groups.items():
        texts = {m["text"] for m in members}
        if len(texts) > 1:
            return {
                "tenant_id": tenant_id,
                "question": question,
                "status": "conflicting_accounts",
                "answer": "Conflicting accounts found; the system does not choose between them:",
                "citations": [
                    {"source": m["source"], "chunk_id": m["chunk_id"], "text": m["text"]}
                    for m in members
                ],
            }

    citations = [
        {"source": c["source"], "chunk_id": c["chunk_id"], "text": c["text"]}
        for c in chunks
    ]
    answer_text = "Based on the authorised material: " + " ".join(c["text"] for c in chunks)
    return {
        "tenant_id": tenant_id,
        "question": question,
        "status": "answered",
        "answer": answer_text,
        "citations": citations,
    }


def token_count(text: str) -> int:
    """Word count, used as a mock token count for the benchmark.
    On a Mac mini with a real model, replace with the model's token count."""
    return len(text.split())
