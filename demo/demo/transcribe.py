"""Transcription adapter.

Demo implementation: a fixture transcript file stands in for a local
Whisper-class model output. The review contract is real: a transcript
is NEVER indexed until a family review marks it reviewed. Names,
years, and places in a transcript are always "to be verified" until
that review happens. A real adapter replaces load_transcript() with
a local model call; review_transcript() does not change.
"""
from __future__ import annotations

from pathlib import Path

from .tenants import get_tenant, tenant_data_path, save_json, load_json
from .store import apply_sync


def list_audio_fixtures(tenant_id: str) -> list[Path]:
    folder = get_tenant(tenant_id).audio_dir
    return sorted(folder.glob("*.txt")) if folder.exists() else []


def load_transcript(tenant_id: str, audio_name: str) -> dict:
    """MOCK transcription: read the fixture transcript. Real adapter:
    run a local speech model and return its text in the same shape."""
    path = get_tenant(tenant_id).audio_dir / audio_name
    if not path.exists():
        raise FileNotFoundError(f"no such audio fixture: {audio_name}")
    return {
        "tenant_id": tenant_id,
        "audio": audio_name,
        "text": path.read_text(encoding="utf-8"),
        "status": "needs_review",
        "note": "Names, years, and places are TO BE VERIFIED by family review. "
                "Automatic transcription is never treated as fact.",
    }


def review_transcript(tenant_id: str, audio_name: str, approved: bool) -> dict:
    """Family review gate. Only approved transcripts enter the index."""
    transcript = load_transcript(tenant_id, audio_name)
    queue_path = tenant_data_path(tenant_id, "review_queue.json")
    queue = load_json(queue_path, {})
    queue[audio_name] = "approved" if approved else "rejected"
    save_json(queue_path, queue)
    if approved:
        apply_sync(tenant_id, {f"transcript-{audio_name}": transcript["text"]}, [])
    return {"tenant_id": tenant_id, "audio": audio_name, "status": queue[audio_name]}
