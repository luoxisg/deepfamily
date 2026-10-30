# DeepFamily — Community Family Workspace: Requirements

> Status: requirements draft only. Not deployed.
> Source demo (front-end only, no server, no account, no upload, no AI):
> https://dcdeeptech.com/DeepFamily/preview/community-family-workspace.html?lang=en
>
> This README records what must be confirmed before any real service is built.
> It does not claim that any service, hardware, GPU quota, AI capability,
> or cloud storage is already included in any per-household support or
> in the S$98,000 private-project figure mentioned on the demo page.
> Those items must be agreed separately, in writing, before go-live.

## 1. Proposed topology (1 to 5)

- One sponsor family provides compute.
- Five compute services, each connected to one supported household.
  (The demo presents this as a proposed topology, not a measured capacity.)
- The community organisation only introduces the sponsor. It does not
  provide compute, review family data, or operate the service.
- Each household decides its own data permission and outputs.
  Sponsorship does not automatically grant the sponsor access to
  family files.
- Service operation, isolation, keys, logs, and deletion must be
  agreed in writing before any real data is handled.

## 2. Users and data source

- End users are on **free Google Drive** (typically 15 GB per Google
  account, shared across Gmail, Drive, and Photos — verify per account).
- The current gifted / free version **can limit upload quantity**.
  The limit is a product parameter, not a fixed fact:
  - `N` = max uploads per household (to be set, e.g. in the demo the
    check counter shows 0 / 20 — that is a demo counter, not a
    confirmed product limit).
  - `s` = average file size by type (photo / document / audio / video).
  - Per-household storage bound: `N × s ≤ free quota − account's existing use`.
- Supported sources (to be confirmed): photos, documents, audio
  recordings, video, and text notes. No real family data in demos.

## 3. Sponsor host — Mac mini (to be confirmed with the supplier's R&D)

The host model, memory, and SSD are **not yet fixed**. The supplier's
R&D must confirm, in technical terms:

- Exact model and configuration: M4 or M4 Pro, unified memory,
  SSD size, external-storage expandability.
- Multi-tenant architecture on a single host: process-level and
  data-level isolation, independent data directories, independent
  vector collections, independent keys, and a proof that retrieval
  cannot cross households.
- Scheduling under unified-memory bandwidth limits: how transcription,
  embedding, LLM generation, and TTS share bandwidth, and how
  pre-emption works.
- Measured capacity, not marketing claims, for both scenarios:
  five households time-shared, and five households online at once:
  aggregate token rate, time-to-first-token, and degradation threshold.
- Failure and scaling path: what happens on power loss, disk failure,
  or model-load failure, and whether scaling is by adding a host,
  upgrading the model, or compressing context.
- 24×7 sustained-load behaviour: thermal throttling, backup/restore,
  remote management.

Reference capacity model (estimates only, to be replaced by supplier
benchmarks on the exact machine):

- M4 Pro, 48 GB, 273 GB/s: text + voice Q&A comfortable at
  2–3 concurrent generating sessions, degraded at 4–5.
- M4 base, 16 GB, 120 GB/s: roughly half the above.
- Real-time digital-human video is **out of scope** for the
  1-to-5 comfort numbers above; it needs a separate capacity case
  (about 1 concurrent high-quality stream on a Mac mini class host).
- Registered households ≠ concurrent sessions. Registered capacity
  must be derived from peak-hour active fraction:
  `H_registered = C_max / (peak active fraction × generation duty cycle)`.

## 4. Planned services (future, not in the demo)

1. Speech-to-text: authorised oral recordings become editable text.
   Names, dates, and dialects must be reviewed by family members;
   automatic transcription is never treated as historical fact.
2. Text Q&A with sources: ask about authorised family material;
   answers must cite specific sources and mark insufficient or
   conflicting evidence.
3. Voice Q&A and read-aloud: microphone only with active household
   permission, with an equivalent text path.

Out of scope for v1 unless separately agreed: real-time digital-human
video, public sharing, and any claim of verified effects.

## 5. Google Drive integration (Drive API v3)

Official docs: https://developers.google.com/drive/v3/reference

Required, in order:

- OAuth 2.0 with the narrowest scope that fits the job.
  Read-only sync: `drive.readonly` / `drive.metadata.readonly`.
  Use `drive.file` only when the user picks files via Picker.
  Never request full `drive` scope by default.
- `files.list` with `q` filters (`trashed=false`,
  `'<folderId>' in parents`), pagination via `nextPageToken`,
  and minimal `fields`.
- Binary files: `files.get` with `alt=media`.
- Google Docs / Sheets / Slides: `files.export` to a requested
  MIME type — they cannot be downloaded as binary files.
- Incremental sync: `changes.getStartPageToken` +
  `changes.list`. Do not rescan the whole Drive on every run.
- Quota: `about.get` → `storageQuota`. Deletion must remove the
  file, its transcript, its vectors, and its caches within a bounded
  time.
- Permissions: never make a family folder public by default.
  Sharing is a separate, explicitly approved action.

## 6. RAG and trust requirements

- Every answer must be traceable to a source file, page/section,
  and version. If the source was modified or deleted, the answer
  must not cite the old version.
- Unknown stays unknown. Do not fabricate prices, regulations,
  customer commitments, or test data. Do not present a project
  target as a verified result.
- Conflicting accounts must be shown as conflicting, not resolved
  silently by the model.
- Dialect, accent, and elderly speech: transcription error must be
  measured, and family review must break the error-propagation chain
  (transcript → chunk → vector → retrieval → answer).
- No verified-effect percentages may be claimed without a
  verifiable, household-approved case record.

## 7. Non-functional requirements

- Privacy: sponsor compute ≠ sponsor access. Community introduction
  ≠ community access. Each household's data is isolated by design.
- Security: tokens stored only on the host, never in code or git
  history; logs must not contain file contents or credentials.
- Reliability: the Mac mini is not a server by default — external
  backup, UPS, and a restore procedure are required for a community
  service.
- Operability: model, vector store, and original files must be
  versioned together; an update must not silently change answers
  for old material.
- Exit: when sponsorship ends, or a household withdraws, data
  export and deletion must work without the sponsor's cooperation
  beyond the agreed procedure.

## 8. Open questions for the supplier's R&D director (1 to 5)

These are vendor-architecture questions, not academic research
questions. They are the acceptance test for the 1-to-5 claim:

1. How is five-tenant isolation implemented and proven on one host?
2. What is the measured aggregate token rate and time-to-first-token
   for five households time-shared vs. five online at once?
3. How are transcription, embedding, LLM, and TTS scheduled under
   unified-memory bandwidth limits, and what is the degradation
   threshold?
4. What is the failure mode and recovery time for power, disk, and
   model-load failures, per household?
5. What changes in the architecture when going from 5 to 10
   households — another host, a larger model host, or a smaller model?

## 9. Open research questions (for the NUS topic, separate from §8)

1. How does an upload-quantity limit change what families choose
   to preserve, and how can that selection bias be measured?
2. How can small, heterogeneous, dialect-heavy family corpora be
   cited and conflict-labelled so transcription errors do not become
   “facts” after repeated retrieval?
3. How are data sovereignty, withdrawal, and exit rights designed
   when compute is sponsored, storage is on a free third-party
   platform, and introduction is by a community organisation?

## 10. Acceptance criteria (v1)

- [ ] Host model, memory, SSD, and supplier benchmarks confirmed
      in writing for the 1-to-5 case.
- [ ] Five isolated tenant workspaces demonstrated; a cross-tenant
      retrieval test returns nothing.
- [ ] Free-Drive sync works read-only, incrementally, with quota
      checks, for the agreed upload limit N.
- [ ] Transcription + text Q&A + voice Q&A work end-to-end on
      authorised test data only (no real family data in testing).
- [ ] Every answer shows its source; unknown and conflicting
      cases are labelled, not smoothed over.
- [ ] Deletion and exit procedures tested end-to-end.
- [ ] No claim in any demo, pitch, or README states that hardware,
      GPU, AI, or storage is included unless it is separately agreed.
