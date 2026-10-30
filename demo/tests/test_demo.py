"""Acceptance tests for the developer demo. Run from demo/:
python3 -m unittest discover -s tests -v

These tests use only the fictional fixtures in demo/fixtures/.
They must pass on this VM and, unchanged, on a Mac mini.
"""
import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from demo.drive import sync
from demo.qa import answer
from demo.store import chunk_count, retrieve
from demo.tenants import TENANT_IDS, tenant_data_path
from demo.transcribe import review_transcript


def setUpModule():
    for tid in TENANT_IDS:
        sync(tid)


def tearDownModule():
    data = Path(__file__).resolve().parent.parent / "demo_data"
    if data.exists():
        shutil.rmtree(data)


class TestIsolation(unittest.TestCase):
    def test_cross_tenant_query_returns_nothing(self):
        # "noodle stall" exists only in tenant_1. No other tenant may see it.
        for tid in TENANT_IDS:
            if tid == "tenant_1":
                continue
            self.assertEqual(retrieve(tid, "noodle stall"), [])

    def test_unknown_tenant_is_rejected(self):
        with self.assertRaises(ValueError):
            retrieve("tenant_99", "noodle stall")

    def test_path_escape_is_rejected(self):
        from demo.tenants import tenant_data_path as path_for
        with self.assertRaises(ValueError):
            path_for("tenant_1", "..", "tenant_2", "index.json")


class TestSync(unittest.TestCase):
    def test_sync_is_incremental(self):
        first = sync("tenant_1")
        second = sync("tenant_1")
        self.assertEqual(second["added"], [])
        self.assertEqual(second["updated"], [])
        self.assertEqual(second["page_token"], first["page_token"] + 1)

    def test_deletion_propagates_to_store(self):
        # Remove a fixture file temporarily, sync, check its chunks are gone.
        fixture = Path(__file__).resolve().parent.parent / "fixtures" / "drive" / "tenant_2" / "garden-notes.txt"
        text = fixture.read_text()
        try:
            fixture.unlink()
            result = sync("tenant_2")
            self.assertIn("garden-notes.txt", result["deleted"])
            self.assertEqual(retrieve("tenant_2", "rooftop garden"), [])
        finally:
            fixture.write_text(text)
            sync("tenant_2")


class TestQA(unittest.TestCase):
    def test_answered_with_citation(self):
        result = answer("tenant_1", "When did grandmother open the noodle stall?")
        self.assertEqual(result["status"], "answered")
        self.assertTrue(result["citations"])
        self.assertEqual(result["citations"][0]["source"], "family-history.txt")

    def test_unknown_is_not_fabricated(self):
        result = answer("tenant_5", "What is the capital of France?")
        self.assertEqual(result["status"], "unknown")
        self.assertEqual(result["citations"], [])

    def test_conflict_is_not_resolved(self):
        result = answer("tenant_3", "When did the family shop open?")
        self.assertEqual(result["status"], "conflicting_accounts")
        texts = " ".join(c["text"] for c in result["citations"])
        self.assertIn("1968", texts)
        self.assertIn("1978", texts)

    def test_unreviewed_transcript_is_not_indexed(self):
        # tenant_1 audio fixture is not indexed until review_transcript approves it.
        # (The CLI approves it; a fresh sync here does not index audio.)
        self.assertNotIn("transcript", " ".join(c["text"] for c in retrieve("tenant_2", "noodle stall")))


if __name__ == "__main__":
    unittest.main()
