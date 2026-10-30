"""Tenant registry. Isolation rule: every data access takes a tenant_id
and may only touch that tenant's directory. There is no global store,
no shared vector collection, and no cross-tenant fallback.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

TENANT_IDS = ["tenant_1", "tenant_2", "tenant_3", "tenant_4", "tenant_5"]


@dataclass(frozen=True)
class Tenant:
    tenant_id: str
    code: str  # fictional household code, never a real name

    @property
    def data_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent / "demo_data" / self.tenant_id

    @property
    def drive_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent / "fixtures" / "drive" / self.tenant_id

    @property
    def audio_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent / "fixtures" / "audio" / self.tenant_id


def get_tenant(tenant_id: str) -> Tenant:
    if tenant_id not in TENANT_IDS:
        raise ValueError(f"unknown tenant: {tenant_id}")
    return Tenant(tenant_id=tenant_id, code=tenant_id.upper())


def tenant_data_path(tenant_id: str, *parts: str) -> Path:
    """The ONLY way to build a tenant data path. Anything outside the
    tenant's own directory is rejected, including '..' escapes."""
    tenant = get_tenant(tenant_id)
    base = tenant.data_dir.resolve()
    path = (base / Path(*parts)).resolve()
    if path != base and base not in path.parents:
        raise ValueError("path escapes tenant directory")
    return path


def ensure_tenant_dirs(tenant_id: str) -> Path:
    path = get_tenant(tenant_id).data_dir
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
