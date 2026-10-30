"""DeepFamily developer demo: 1 host, 5 isolated tenants.

Standard library only, so it runs on a Mac mini with no pip installs.
Real code: tenant isolation, incremental sync, per-tenant retrieval,
citations, unknown and conflict handling, deletion propagation.
Mocked, clearly labelled: the Drive source (local fixture folder
instead of the Google Drive API), transcription (fixture transcript
instead of a Whisper model), and answer wording (template from
retrieved chunks instead of an LLM). On a real Mac mini, replace
those three adapters only; the tenant, store, and QA contracts
do not change.
"""
