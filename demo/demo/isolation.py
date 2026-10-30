"""Household vs sponsor isolation.

Rule (see docs/data-isolation-policy.md): sponsor compute is NOT
sponsor access. A sponsor operator has an infrastructure plane only:
service health, aggregate quotas, encrypted backups. It has NO data
plane for ANY household -- including the sponsor family's own tenant,
which must be accessed under a separate household-member identity.

Every data function in this module takes a Principal FIRST and
refuses before touching any data. Denials are audited. The audit log
records identity, tenant code, operation and allowed/denied -- never
any household content.

Encryption here is DEMO-GRADE, not production crypto: a household
passphrase derives a key (PBKDF2-HMAC-SHA256); content is sealed with
an HMAC counter-mode stream plus an HMAC tag, so it proves "cannot
be opened without the household key". A real deployment replaces
seal/open with a standard AEAD (AES-GCM / XChaCha20-Poly1305) and
household-held keys. The access rules do not change when the cipher
changes.

Authenticity note: Principal objects in this demo are supplied by
the caller. A real deployment must build them from a verified login
session/token server-side, never from a client-claimed identity.
"""
from __future__ import annotations

import base64
import hashlib
import hmac as hmac_lib
import json
import secrets
from dataclasses import dataclass
from pathlib import Path

from .qa import answer as _raw_answer
from .tenants import TENANT_IDS, get_tenant, load_json, save_json, tenant_data_path
from .transcribe import review_transcript as _raw_review

# ---------------------------------------------------------------- roles

HOUSEHOLD_MEMBER = "household_member"
SPONSOR_OPERATOR = "sponsor_operator"
COMMUNITY_INTRODUCER = "community_introducer"


@dataclass(frozen=True)
class Principal:
    """One session, one identity. A sponsor operator has tenant_id=None
    precisely because it is bound to NO household."""

    kind: str
    tenant_id: str | None = None
    name: str = "anonymous"

    def __post_init__(self) -> None:
        if self.kind == HOUSEHOLD_MEMBER:
            if self.tenant_id not in TENANT_IDS:
                raise ValueError("household member must be bound to a known tenant")
        elif self.kind in (SPONSOR_OPERATOR, COMMUNITY_INTRODUCER):
            if self.tenant_id is not None:
                raise ValueError(f"{self.kind} must not be bound to a tenant")
        else:
            raise ValueError(f"unknown principal kind: {self.kind}")


def household_member(tenant_id: str, name: str = "household") -> Principal:
    return Principal(kind=HOUSEHOLD_MEMBER, tenant_id=tenant_id, name=name)


def sponsor_operator(name: str = "sponsor") -> Principal:
    return Principal(kind=SPONSOR_OPERATOR, name=name)


def community_introducer(name: str = "community") -> Principal:
    return Principal(kind=COMMUNITY_INTRODUCER, name=name)


# ---------------------------------------------------------------- audit

def _audit_path() -> Path:
    # Audit lives beside tenant data, not inside any tenant's folder:
    # it must not be readable as household content, and it must not
    # contain household content either (see _audit()).
    base = Path(__file__).resolve().parent.parent / "demo_data"
    base.mkdir(parents=True, exist_ok=True)
    return base / "audit.jsonl"


def _audit(principal: Principal, tenant_id: str | None, operation: str, allowed: bool) -> None:
    """Append one hash-chained entry. Content is never logged: only
    identity kind, anonymous tenant code, operation, allowed/denied."""
    path = _audit_path()
    entries = []
    if path.exists():
        entries = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    prev_hash = entries[-1]["entry_hash"] if entries else "0" * 64
    entry = {
        "principal_kind": principal.kind,
        "principal_name": principal.name,
        "tenant_id": tenant_id,
        "operation": operation,
        "allowed": allowed,
        "prev_hash": prev_hash,
    }
    payload = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    entry["entry_hash"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def verify_audit() -> bool:
    """True only if every entry's hash covers its fields and the chain
    links. Tampering with or deleting a middle entry breaks this."""
    path = _audit_path()
    if not path.exists():
        return True
    prev_hash = "0" * 64
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if entry["prev_hash"] != prev_hash:
            return False
        claimed = entry.pop("entry_hash")
        payload = json.dumps(entry, sort_keys=True, ensure_ascii=False)
        if hashlib.sha256(payload.encode("utf-8")).hexdigest() != claimed:
            return False
        entry["entry_hash"] = claimed
        prev_hash = claimed
    return True


def audit_entries() -> list[dict]:
    path = _audit_path()
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# ------------------------------------------------------------- data gate

def _require_household_access(principal: Principal, tenant_id: str, operation: str) -> None:
    """The ONLY data-plane gate. Sponsor and community are denied here,
    before any path is built or any file is read."""
    allowed = principal.kind == HOUSEHOLD_MEMBER and principal.tenant_id == tenant_id
    _audit(principal, tenant_id, operation, allowed)
    if not allowed:
        raise PermissionError(
            f"denied: {principal.kind} may not {operation} for {tenant_id}; "
            "sponsor compute is not sponsor access"
        )


def guarded_answer(principal: Principal, tenant_id: str, question: str) -> dict:
    """Q&A through the isolation gate. Sponsor questions are refused,
    not answered with an empty result."""
    _require_household_access(principal, tenant_id, "qa")
    return _raw_answer(tenant_id, question)


def guarded_review(principal: Principal, tenant_id: str, audio_name: str, approved: bool) -> dict:
    """Transcript review through the isolation gate. A sponsor may
    never review on a household's behalf, for any reason."""
    _require_household_access(principal, tenant_id, "review_transcript")
    return _raw_review(tenant_id, audio_name, approved)


def sponsor_operations_view(principal: Principal) -> dict:
    """The sponsor's ONLY view: aggregate operations metadata, by
    anonymous tenant code. No file names, no questions, no answers,
    no chunk contents, no per-tenant content counts."""
    if principal.kind != SPONSOR_OPERATOR:
        _audit(principal, None, "sponsor_operations_view", False)
        raise PermissionError("denied: only a sponsor operator may view operations status")
    _audit(principal, None, "sponsor_operations_view", True)
    view = {"tenants": [], "service": "running"}
    for tid in TENANT_IDS:
        data_dir = get_tenant(tid).data_dir
        # Storage total only -- never file names or contents.
        total_bytes = sum(p.stat().st_size for p in data_dir.rglob("*") if p.is_file()) if data_dir.exists() else 0
        view["tenants"].append({
            "tenant_id": tid,
            "data_present": data_dir.exists(),
            "storage_bytes": total_bytes,
        })
    return view


# ------------------------------------------------------- demo-grade seal

_ITERATIONS = 100_000


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, _ITERATIONS, dklen=32)


def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    out = b""
    counter = 0
    while len(out) < length:
        out += hmac_lib.new(key, nonce + counter.to_bytes(8, "big"), hashlib.sha256).digest()
        counter += 1
    return out[:length]


def seal(tenant_id: str, plaintext: str, passphrase: str) -> dict:
    """Seal household content for backup. Anyone holding the sealed
    blob without the passphrase gets ciphertext only."""
    get_tenant(tenant_id)  # validate tenant code
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(16)
    key = _derive_key(passphrase, salt)
    raw = plaintext.encode("utf-8")
    cipher = bytes(b ^ k for b, k in zip(raw, _keystream(key, nonce, len(raw))))
    tag = hmac_lib.new(key, nonce + cipher, hashlib.sha256).digest()
    return {
        "tenant_id": tenant_id,
        "salt_b64": base64.b64encode(salt).decode(),
        "nonce_b64": base64.b64encode(nonce).decode(),
        "cipher_b64": base64.b64encode(cipher).decode(),
        "tag_b64": base64.b64encode(tag).decode(),
        "note": "DEMO-GRADE seal, not production AEAD. See docs/data-isolation-policy.md §5.",
    }


def open_sealed(sealed: dict, passphrase: str) -> str:
    """Open a sealed blob. Wrong passphrase fails with no partial
    plaintext: the tag is verified before any byte is returned."""
    salt = base64.b64decode(sealed["salt_b64"])
    nonce = base64.b64decode(sealed["nonce_b64"])
    cipher = base64.b64decode(sealed["cipher_b64"])
    tag = base64.b64decode(sealed["tag_b64"])
    key = _derive_key(passphrase, salt)
    expected = hmac_lib.new(key, nonce + cipher, hashlib.sha256).digest()
    if not hmac_lib.compare_digest(expected, tag):
        raise ValueError("decryption failed: wrong passphrase or tampered sealed blob")
    raw = bytes(b ^ k for b, k in zip(cipher, _keystream(key, nonce, len(cipher))))
    return raw.decode("utf-8")


def sponsor_backup(principal: Principal, tenant_id: str, plaintext: str, passphrase: str) -> dict:
    """A sponsor may RUN a backup, but only as a sealed blob. The
    sponsor never receives plaintext back from this function, and the
    sealed blob is useless without the household passphrase -- which
    the sponsor does not hold. (In this demo the caller supplies the
    plaintext to seal; a real backup seals on the household side.)"""
    if principal.kind != SPONSOR_OPERATOR:
        _audit(principal, tenant_id, "sponsor_backup", False)
        raise PermissionError("denied: only a sponsor operator runs backups")
    _audit(principal, tenant_id, "sponsor_backup", True)
    sealed = seal(tenant_id, plaintext, passphrase)
    return {"tenant_id": tenant_id, "sealed": sealed, "plaintext_included": False}
