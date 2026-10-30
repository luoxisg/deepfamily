# Google Drive API — Development Notes for DeepFamily

These are DeepFamily-specific development notes, not a copy of Google's
documentation. Always check the official docs first; the links below are
the authoritative source.

Official reference:

- [Drive API v3 reference](https://developers.google.com/drive/v3/reference)
- [Drive API scopes / authorisation](https://developers.google.cn/workspace/drive/api/guides/api-specific-auth?hl=en&authuser=00)
- [Create and manage files](https://developers.google.cn/workspace/drive/api/guides/create-file?hl=en&authuser=6)
- [Shared-drive support](https://developers.google.cn/workspace/drive/api/guides/enable-shareddrives?hl=en)
- [Python client library, drive_v3](https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.about.html)

## 1. What DeepFamily uses Drive for

- A household's authorised source material lives in that household's
  own Google Drive (free account).
- The sponsor host only reads what the household authorises. It never
  gets automatic access because it provides compute, and the community
  organisation never gets access because it made the introduction.
- Drive is a source store, not the vector store, not the chat log, and
  not the permission system. Permissions, tenant isolation, and
  deletion live on the sponsor host and must be implemented there.

## 2. API version and base

- Use Drive API **v3** only. Base: `https://www.googleapis.com/drive/v3`.
- Discovery document: `https://www.googleapis.com/discovery/v1/apis/drive/v3/rest`.
- Python: `build('drive', 'v3', credentials=creds)`.

## 3. Authorisation — narrowest scope first

| Job | Scope |
| --- | --- |
| Read-only sync (DeepFamily default) | `https://www.googleapis.com/auth/drive.readonly` or `drive.metadata.readonly` |
| User picks a file with Picker | `https://www.googleapis.com/auth/drive.file` |
| Full Drive access | Do NOT request by default. Only if a separately approved feature needs it. |

Rules:

- OAuth 2.0, per household, per account. Tokens stay on the sponsor
  host only, never in git, never in logs, never in chat.
- A token refresh failure is a sync failure, not a reason to fall
  back to a broader scope or a shared account.
- Service accounts are NOT a shortcut for a household's personal
  Drive: a service account can only see what was explicitly shared
  with it.

## 4. Methods DeepFamily needs

### List and search — `files.list` (`GET /drive/v3/files`)

- Always pass a minimal `fields` selector, e.g.
  `files(id,name,mimeType,modifiedTime,size,md5Checksum,parents)`.
- Always paginate with `nextPageToken`.
- Useful `q` filters:
  - `trashed=false`
  - `'<folderId>' in parents`
  - `name contains '...'` (for a user-typed search only, never as a
    substitute for an explicit folder authorisation)
  - `mimeType = 'application/vnd.google-apps.document'` etc.
- For shared drives, add `supportsAllDrives=true` and
  `includeItemsFromAllDrives=true` where the API requires it;
  otherwise shared-drive files will silently be missing.

### Download binary files — `files.get` with `alt=media`

- `GET /drive/v3/files/{fileId}?alt=media`.
- Stream large files; do not load a whole video into memory.
- Record `md5Checksum` + `modifiedTime` with every downloaded copy,
  so a later answer can be tied to an exact version.

### Export Google Workspace files — `files.export`

- `GET /drive/v3/files/{fileId}/export?mimeType=...`.
- Google Docs / Sheets / Slides cannot be downloaded with
  `alt=media`; they must be exported.
- Examples: Docs → `text/plain` or `application/pdf` for parsing,
  Sheets → `text/csv`. Keep the export MIME type in the chunk
  metadata, because a PDF export and a plain-text export of the same
  Doc are not identical sources.

### Create / upload (only where a feature needs it) — `files.create`

- `POST /drive/v3/files` for metadata, `POST /upload/drive/v3/files`
  for content.
- Small files: multipart upload. Large files: resumable upload
  (`uploadType=resumable`), with chunk retry and exponential backoff.
- Folders are files with
  `mimeType = 'application/vnd.google-apps.folder'`.

### Incremental sync — `changes`

- Never rescan the whole Drive on every run.
- `changes.getStartPageToken` → store the token per household →
  `changes.list` with that token → apply added / modified / removed.
- A removed file must remove its transcript, its vectors, and its
  caches within a bounded time (see main README §7, Exit).
- If the stored page token is expired/invalid, do a full re-list
  once, then store the new token — and log that a full re-list
  happened.

### Metadata and quota — `about.get`

- `about.get` → `storageQuota` shows used / total.
- Free accounts are typically 15 GB shared across Gmail, Drive, and
  Photos — verify per account, do not hard-code it as a guarantee.
- Before sync, check: `N × s ≤ quota remaining`, where `N` is the
  agreed upload limit and `s` is average file size. If it does not
  fit, sync must stop with a clear message, not silently skip files.

### Permissions — `permissions`

- Never make a family folder public by default.
- Sharing (`permissions.create`, role reader/writer/commenter) is a
  separate, explicitly approved household action, with its own audit
  entry.

## 5. Parsing after download (DeepFamily pipeline)

Drive gives bytes, not answers:

1. Download / export → verify hash + modifiedTime.
2. Parse by MIME type (text, PDF, DOCX, audio transcript, image OCR
   where authorised) → chunk with source metadata
   (file ID, modifiedTime, page/section, chunk ID).
3. Embed → store in the household's own vector collection only.
4. Retrieve → answer with citations → if the source changed, the
   old answer must not keep citing the old version.

## 6. Error handling checklist

- 401 / 403: token expired, revoked, or scope too narrow — re-auth
  that household, do not retry with a broader scope automatically.
- 404: file moved / deleted / never shared — treat as removed, not
  as a bug to work around.
- 429 / 5xx: exponential backoff, then stop and report; never
  hammer the API in a tight loop.
- Partial download: discard and re-download; never index a truncated
  file.
- Export size limits: Google Workspace exports have size limits
  (notably 10 MB for some export paths) — check the official docs
  for the current limit before promising a large Doc export.

## 7. What is NOT in this document

- No credentials, no tokens, no real file IDs, no real household data.
- No claim that Drive storage, AI, or hardware is included in any
  per-household support figure — see main README.
