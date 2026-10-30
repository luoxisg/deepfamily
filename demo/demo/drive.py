"""Drive sync adapter.

Demo implementation: a local fixture folder stands in for a household's
Google Drive folder. The sync contract is the real one from
docs/google-drive-api.md, so a real adapter only needs to implement
list_source_files() and read_source_file() using Drive API v3:
files.list (q, nextPageToken), files.get alt=media, files.export for
Workspace files, and changes.getStartPageToken + changes.list for the
page token. Nothing else in the demo changes.

Sync state per tenant: {page_token, files: {name: {md5, size, mtime}}}.
A run returns added / updated / deleted file names. Deletion here
must trigger deletion in the store (see store.apply_sync).
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from .tenants import get_tenant, tenant_data_path, save_json, load_json

# Demo quota: 20 files (the demo counter on the source page is an
# example, not a product limit) and a small byte quota so the check
# is exercised without real 15 GB accounts.
UPLOAD_LIMIT_FILES = 20
QUOTA_BYTES = 15_000_000


def _md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def list_source_files(tenant_id: str) -> list[dict]:
    """MOCK Drive source: local fixture folder. Real adapter: Drive API."""
    folder = get_tenant(tenant_id).drive_dir
    out = []
    if folder.exists():
        for path in sorted(folder.glob("*.txt")):
            out.append({
                "name": path.name,
                "size": path.stat().st_size,
                "mtime": int(path.stat().st_mtime),
                "md5": _md5(path),
                "path": str(path),
            })
    return out


def check_quota(files: list[dict]) -> dict:
    total = sum(f["size"] for f in files)
    return {
        "file_count": len(files),
        "file_limit": UPLOAD_LIMIT_FILES,
        "total_bytes": total,
        "quota_bytes": QUOTA_BYTES,
        "ok": len(files) <= UPLOAD_LIMIT_FILES and total <= QUOTA_BYTES,
    }


def sync(tenant_id: str) -> dict:
    """Incremental sync. Returns added/updated/deleted + new page token."""
    from .store import apply_sync  # local import to avoid a cycle

    files = list_source_files(tenant_id)
    quota = check_quota(files)
    if not quota["ok"]:
        return {"tenant_id": tenant_id, "quota": quota, "error": "quota_or_limit_exceeded"}

    state_path = tenant_data_path(tenant_id, "sync_state.json")
    state = load_json(state_path, {"page_token": 0, "files": {}})
    old = state["files"]
    new = {f["name"]: {"md5": f["md5"], "size": f["size"], "mtime": f["mtime"]} for f in files}

    added = [n for n in new if n not in old]
    updated = [n for n in new if n in old and new[n]["md5"] != old[n]["md5"]]
    deleted = [n for n in old if n not in new]

    state["page_token"] = int(state["page_token"]) + 1
    state["files"] = new
    save_json(state_path, state)

    # Apply to the per-tenant store: index added/updated, drop deleted.
    changed = {}
    for f in files:
        if f["name"] in added or f["name"] in updated:
            changed[f["name"]] = Path(f["path"]).read_text(encoding="utf-8")
    apply_sync(tenant_id, changed, deleted)

    return {
        "tenant_id": tenant_id,
        "page_token": state["page_token"],
        "added": added,
        "updated": updated,
        "deleted": deleted,
        "quota": quota,
    }
