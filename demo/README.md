# DeepFamily Developer Demo — 1 host, 5 isolated tenants

> What this is: the smallest end-to-end slice that proves the risky
> parts of DeepFamily — tenant isolation, Drive sync, transcription
> review, cited Q&A, and concurrency measurement — on one host.
> What this is NOT: a household product, a real AI service, or a
> Mac mini benchmark. All data is fictional test data.
>
> This demo runs on this VM and, unchanged, on a Mac mini.
> It uses Python 3.10+ standard library only. No pip installs,
> no API keys, no cloud calls.

## Quick start (2 minutes)

```bash
cd demo
python3 -m demo.cli
```

You should see: 5 tenants synced, tenant_1's transcript reviewed,
and 5 answers — including a `conflicting_accounts` case (tenant_3:
shop opened 1968 vs 1978) and an `unknown` case (tenant_5: capital
of France, not in any fixture).

## Run the tests

```bash
cd demo
python3 -m unittest discover -s tests -v
```

Tests cover: cross-tenant queries return nothing, unknown tenants
are rejected, path escapes are rejected, sync is incremental,
deletion propagates to the store, answers carry citations, unknown
is never fabricated, and conflicts are shown side by side.

## Run the developer dashboard

```bash
cd demo
python3 -m demo.server
# open http://127.0.0.1:8001
```

The dashboard is intentionally plain. It shows tenants, chunk counts,
audio fixtures, a Q&A form, and a benchmark button.

## Run the benchmark

```bash
cd demo
python3 -c "from demo.benchmark import run_all; import json; print(json.dumps(run_all(), indent=2))"
# writes benchmark_report.json (1 / 3 / 5 concurrent sessions)
```

## Layout

```
demo/
  demo/
    tenants.py     Tenant registry + path isolation (the only way to build a tenant path)
    drive.py       Sync contract: page token, quota check, added/updated/deleted
    store.py       Per-tenant chunk store + keyword retrieval (no shared index)
    transcribe.py  Transcript review gate: nothing is indexed before family review
    qa.py          Answer only from retrieved chunks: answered / unknown / conflicting
    benchmark.py   Concurrent Q&A timing (1 / 3 / 5 sessions)
    server.py      Stdlib developer dashboard (http://127.0.0.1:8001)
    cli.py         Full pipeline acceptance run (no server needed)
  fixtures/
    drive/tenant_1..5/   Fictional Drive folders (one per tenant)
    audio/tenant_1/      Fictional transcript fixture (not a real recording)
  tests/test_demo.py     Acceptance tests
  demo_data/             Runtime data, created on first run, NOT in git
```

## What is real, what is mocked — read before quoting any number

| Part | Status |
| --- | --- |
| Tenant isolation (separate dirs, no shared index, path-escape rejection) | Real code, tested |
| Incremental sync, quota check, deletion propagation | Real code, tested (fixture folder as Drive) |
| Retrieval, citations, unknown, conflict handling | Real code, tested |
| Drive source | MOCK: local fixture folder. Real adapter = Drive API v3 (`files.list`, `files.get` alt=media, `files.export`, `changes.list`) — see `demo/drive.py` and `docs/google-drive-api.md` |
| Transcription | MOCK: fixture transcript. Real adapter = a local Whisper-class model on the Mac mini. Review gate is real and unchanged. |
| Answer wording | MOCK: template from retrieved chunks. Real adapter = a local LLM (MLX / llama.cpp) constrained to the same chunks and the same three outcomes. |
| Benchmark numbers on this VM | Mock path only (retrieval + template). On a Mac mini with a real model, re-measure with that model; do not quote VM numbers as Mac mini capacity. |
| TTS / voice first-packet | Not implemented in this demo. Measure it separately when a real TTS model is chosen. |

## On a Mac mini (when a host is available)

1. Clone this repo onto the Mac mini. Confirm the machine first:
   Mac mini (confirmed 2026-10-30 — not a Mac Pro tower, not a Mac Studio).
   Record chip, memory, and SSD; the planning baseline is M4 Pro, 48 GB.
2. Run the tests and the CLI exactly as above. They must pass unchanged.
3. Replace the three adapters only (`drive.py` source, `transcribe.py`
   model, `qa.py` model), keeping tenant, store, and QA contracts.
4. Re-run the benchmark with the real model at 1 / 3 / 5 concurrent
   sessions and record: time-to-first-token, aggregate tokens/second,
   and first-voice-packet latency while transcription runs.
5. Do NOT use real household data for this demo. Use the fictional
   fixtures, or a separate fictional corpus, until a household gives
   written authorisation for a pilot.

## Acceptance criteria for this demo

- [ ] `python3 -m unittest discover -s tests -v` passes.
- [ ] `python3 -m demo.cli` shows 5 synced tenants, 1 reviewed transcript,
      1 conflict case, and 1 unknown case.
- [ ] Cross-tenant query test passes (no tenant sees another's chunks).
- [ ] Deletion test passes (removing a source file removes its chunks).
- [ ] Benchmark report is generated for 1 / 3 / 5 concurrent sessions.
- [ ] No real household data, no cloud call, and no claimed Mac mini
      capacity number appears anywhere in the demo output.
