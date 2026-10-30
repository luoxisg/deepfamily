"""Per-tenant chunk store. Retrieval is keyword-overlap scoring over
chunks that live ONLY in the querying tenant's file. A query for one
tenant can never read another tenant's file: the path is built from
the tenant_id, and there is no shared index anywhere.
"""
from __future__ import annotations

import re
from .tenants import tenant_data_path, save_json, load_json

_TOKEN = re.compile(r"[a-z0-9]+")

# Stopwords are excluded so a question like "What is the capital of
# France?" (content tokens: capital, france) does not match a chunk
# just because both contain "the" or "is". Without this, "unknown"
# would almost never trigger, which is exactly the fabrication path
# this demo must not have.
_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "what", "when", "where", "who", "how", "why", "which",
    "did", "do", "does", "of", "to", "in", "on", "at", "from",
    "by", "for", "with", "and", "or", "not", "it", "its",
}


def _tokens(text: str) -> set[str]:
    return {t for t in _TOKEN.findall(text.lower()) if t not in _STOPWORDS}


def _chunks_for_file(name: str, text: str) -> list[dict]:
    chunks = []
    conflict_group = None
    for line in text.splitlines():
        if line.startswith("CONFLICT_GROUP:"):
            conflict_group = line.split(":", 1)[1].strip()
            continue
        if not line.strip() or line.startswith("Fictional test data"):
            continue
        chunks.append({
            "chunk_id": f"{name}#{len(chunks)}",
            "source": name,
            "text": line.strip(),
            "conflict_group": conflict_group,
        })
    return chunks


def apply_sync(tenant_id: str, changed: dict[str, str], deleted: list[str]) -> None:
    path = tenant_data_path(tenant_id, "index.json")
    index = load_json(path, {"chunks": []})
    # Drop chunks from deleted or replaced files, then add new chunks.
    kept = [c for c in index["chunks"] if c["source"] not in deleted and c["source"] not in changed]
    for name, text in changed.items():
        kept.extend(_chunks_for_file(name, text))
    save_json(path, {"chunks": kept})


def retrieve(tenant_id: str, query: str, top_k: int = 3) -> list[dict]:
    """Return top chunks for THIS tenant only, scored by token overlap."""
    path = tenant_data_path(tenant_id, "index.json")
    index = load_json(path, {"chunks": []})
    query_tokens = _tokens(query)
    scored = []
    for chunk in index["chunks"]:
        overlap = len(query_tokens & _tokens(chunk["text"]))
        if overlap:
            scored.append((overlap, chunk))
    scored.sort(key=lambda item: -item[0])
    return [chunk for _, chunk in scored[:top_k]]


def chunk_count(tenant_id: str) -> int:
    path = tenant_data_path(tenant_id, "index.json")
    return len(load_json(path, {"chunks": []})["chunks"])
