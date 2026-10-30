"""Household vs sponsor isolation tests.

These tests use fictional fixture data only. They prove the rules in
docs/data-isolation-policy.md, not production cryptography: the seal
is demo-grade (see isolation.py), and the access rules are what is
really being tested.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from demo import isolation
from demo.drive import sync
from demo.isolation import (
    community_introducer,
    guarded_answer,
    guarded_review,
    household_member,
    open_sealed,
    seal,
    sponsor_backup,
    sponsor_operations_view,
    sponsor_operator,
    verify_audit,
)


def _reset_audit():
    path = Path(__file__).resolve().parent.parent / "demo_data" / "audit.jsonl"
    if path.exists():
        path.unlink()


class TestSponsorIsolation(unittest.TestCase):
    def setUp(self):
        _reset_audit()
        # Sync tenant_1 so there is real (fictional) content to protect.
        sync("tenant_1")

    def test_sponsor_cannot_ask_qa(self):
        with self.assertRaises(PermissionError):
            guarded_answer(sponsor_operator(), "tenant_1", "When did grandmother open the noodle stall?")
        self.assertTrue(any(
            e["principal_kind"] == "sponsor_operator" and e["operation"] == "qa" and e["allowed"] is False
            for e in isolation.audit_entries()
        ))

    def test_sponsor_cannot_review_transcript(self):
        with self.assertRaises(PermissionError):
            guarded_review(sponsor_operator(), "tenant_1", "recording.txt", True)

    def test_community_cannot_ask_qa(self):
        with self.assertRaises(PermissionError):
            guarded_answer(community_introducer(), "tenant_1", "When did grandmother open the noodle stall?")

    def test_household_cannot_access_other_household(self):
        with self.assertRaises(PermissionError):
            guarded_answer(household_member("tenant_2"), "tenant_1", "When did grandmother open the noodle stall?")

    def test_household_can_access_own_household(self):
        result = guarded_answer(household_member("tenant_1"), "tenant_1", "When did grandmother open the noodle stall?")
        self.assertIn(result["status"], ("answered", "conflicting_accounts", "unknown"))

    def test_sponsor_cannot_use_operator_identity_for_own_tenant(self):
        # Sponsor operator is bound to NO tenant. Even if the sponsor
        # family's own workspace were tenant_1, the operator identity
        # alone must not open it; it must log in as a household member.
        with self.assertRaises(PermissionError):
            guarded_answer(sponsor_operator(), "tenant_1", "anything")
        own = guarded_answer(household_member("tenant_1"), "tenant_1", "When did grandmother open the noodle stall?")
        self.assertIn("tenant_id", own)

    def test_sponsor_view_has_no_content(self):
        view = sponsor_operations_view(sponsor_operator())
        blob = json.dumps(view, ensure_ascii=False)
        self.assertNotIn("noodle", blob)
        self.assertNotIn("grandmother", blob)
        self.assertTrue(all("tenant_id" in t for t in view["tenants"]))
        # Household members may not use the sponsor view at all.
        with self.assertRaises(PermissionError):
            sponsor_operations_view(household_member("tenant_1"))

    def test_sealed_backup_unopenable_without_passphrase(self):
        sealed = seal("tenant_1", "grandmother opened the shop in 1968", "household-secret")
        self.assertEqual(open_sealed(sealed, "household-secret"), "grandmother opened the shop in 1968")
        with self.assertRaises(ValueError):
            open_sealed(sealed, "wrong-passphrase")
        # Sponsor backup returns a sealed blob, never plaintext.
        backup = sponsor_backup(sponsor_operator(), "tenant_1", "grandmother opened the shop in 1968", "household-secret")
        self.assertFalse(backup["plaintext_included"])
        self.assertNotIn("1968", json.dumps(backup["sealed"]))
        with self.assertRaises(ValueError):
            open_sealed(backup["sealed"], "sponsor-guess")

    def test_audit_chain_detects_tampering(self):
        guarded_answer(household_member("tenant_1"), "tenant_1", "When did grandmother open the noodle stall?")
        with self.assertRaises(PermissionError):
            guarded_answer(sponsor_operator(), "tenant_1", "When did grandmother open the noodle stall?")
        self.assertTrue(verify_audit())
        # Tamper with a middle entry: chain must break.
        path = Path(__file__).resolve().parent.parent / "demo_data" / "audit.jsonl"
        lines = path.read_text(encoding="utf-8").splitlines()
        entry = json.loads(lines[0])
        entry["allowed"] = not entry["allowed"]
        lines[0] = json.dumps(entry)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertFalse(verify_audit())


if __name__ == "__main__":
    unittest.main()
