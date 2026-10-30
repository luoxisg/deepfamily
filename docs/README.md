# DeepFamily — Development Documentation Index

This folder holds DeepFamily-specific development notes. They are
summaries and checklists written for this project, with links to the
official documentation. They are not copies of official docs, and
they contain no credentials, tokens, or real household data.

## Documents

- [Google Drive API — development notes](google-drive-api.md)
  Drive API v3 for DeepFamily: narrowest OAuth scopes, `files.list`
  search, `files.get` download, `files.export` for Docs/Sheets/Slides,
  incremental sync with `changes`, quota checks, permissions, and
  error handling. Official reference:
  https://developers.google.com/drive/v3/reference

- [Household vs sponsor data isolation policy](data-isolation-policy.md)
  Chinese first, then English per section. Sponsor compute is not
  sponsor access: roles, allow/deny list, per-household keys, audit
  hash chain, backup/deletion/exit, threat model and honest boundary,
  and the demo-to-production replacement list. Demo code:
  `demo/demo/isolation.py`, tests: `demo/tests/test_isolation.py`.

- [Sponsor host — Mac mini with M4 Pro](mac-mini-m4-pro.md)
  Hardware to confirm before purchase, unified-memory bandwidth
  (273 GB/s on M4 Pro), local AI stack on Apple Silicon (MLX,
  llama.cpp, local speech), macOS host operations, and the benchmark
  list that must pass before 1-to-5 is promised. Official hardware
  specs: https://support.apple.com/en-us/121555

  Confirmed 2026-10-30: the sponsor host is a Mac mini — not a Mac Pro
  tower, not a Mac Studio, and not any other desktop. Exact chip,
  memory, and SSD are still to be confirmed; the planning baseline
  is M4 Pro, 48 GB.

## How to use these docs

1. Start from the main [README](../README.md) for requirements and
   acceptance criteria. These docs do not override it.
2. For any number in these docs (bandwidth, memory, quota, latency),
   check the official source linked at the top of the document
   before quoting it to a supplier, a professor, or a household.
3. For any capacity claim (especially 1 sponsor : 5 households),
   replace the planning estimates here with benchmarks measured on
   the exact machine to be bought, using the benchmark list in
   `mac-mini-m4-pro.md` §5.
