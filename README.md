# DeepFamily — 社区家庭工作空间：需求 / Community Family Workspace: Requirements

> 状态：仅为需求草稿，尚未部署。
> Status: requirements draft only. Not deployed.
>
> 来源演示（仅前端，无服务器、无账号、无上传、无 AI）：
> Source demo (front-end only, no server, no account, no upload, no AI):
> https://dcdeeptech.com/DeepFamily/preview/community-family-workspace.html?lang=en
>
> 本 README 记录在搭建任何真实服务之前必须确认的事项。
> This README records what must be confirmed before any real service is built.
>
> 它不声称任何服务、硬件、GPU 配额、AI 能力或云存储已经包含在任何按户支持费用或演示页提到的 S$98,000 私人项目费用中。
> It does not claim that any service, hardware, GPU quota, AI capability, or cloud storage is already included in any per-household support or in the S$98,000 private-project figure mentioned on the demo page.
>
> 这些事项在上线前必须另行书面约定。
> Those items must be agreed separately, in writing, before go-live.

## 1. 拟议拓扑（1 对 5） / Proposed topology (1 to 5)

### 中文

- 一个赞助家庭提供算力。
- 五个算力服务，每个服务对应一个受支持家庭（演示页呈现的是拟议拓扑，不是已实测的容量）。
- 社区组织只负责介绍赞助方，不提供算力、不审阅家庭资料、不运营服务。
- 每个家庭自行决定自己的资料权限和输出。赞助不自动赋予赞助方访问家庭文件的权利。
- 服务运营、隔离、密钥、日志和删除，必须在处理任何真实资料前书面约定。

### English

- One sponsor family provides compute.
- Five compute services, each connected to one supported household. (The demo presents this as a proposed topology, not a measured capacity.)
- The community organisation only introduces the sponsor. It does not provide compute, review family data, or operate the service.
- Each household decides its own data permission and outputs. Sponsorship does not automatically grant the sponsor access to family files.
- Service operation, isolation, keys, logs, and deletion must be agreed in writing before any real data is handled.

## 2. 用户与资料来源 / Users and data source

### 中文

- 最终用户使用**免费 Google Drive**（通常每个 Google 账号 15 GB，与 Gmail、Drive、Photos 共用——按账号核实）。
- 当前赠送版 / 免费版**可以限制上传数量**。该限制是一个产品参数，不是固定事实：
  - `N` = 每户最大上传数（待定；例如演示中的计数器显示 0 / 20——那只是演示计数器，不是已确认的产品限制）。
  - `s` = 按类型区分的平均文件大小（照片 / 文档 / 音频 / 视频）。
  - 每户存储上限：`N × s ≤ 免费配额 − 该账号已有使用量`。
- 待确认的支持来源：照片、文档、音频录音、视频和文字笔记。演示中不得使用真实家庭资料。

### English

- End users are on **free Google Drive** (typically 15 GB per Google account, shared across Gmail, Drive, and Photos — verify per account).
- The current gifted / free version **can limit upload quantity**. The limit is a product parameter, not a fixed fact:
  - `N` = max uploads per household (to be set, e.g. in the demo the check counter shows 0 / 20 — that is a demo counter, not a confirmed product limit).
  - `s` = average file size by type (photo / document / audio / video).
  - Per-household storage bound: `N × s ≤ free quota − account's existing use`.
- Supported sources (to be confirmed): photos, documents, audio recordings, video, and text notes. No real family data in demos.

## 3. 赞助主机——Mac mini（需与供应商研发确认） / Sponsor host — Mac mini (to be confirmed with the supplier's R&D)

### 中文

主机型号、内存和 SSD **尚未确定**。供应商研发必须用技术语言确认：

- 确切型号和配置：M4 还是 M4 Pro、统一内存、SSD 大小、外部存储扩展能力。
- 单台主机上的多租户架构：进程级和数据级隔离、独立数据目录、独立向量库、独立密钥，以及检索绝不会跨户的证明。
- 统一内存带宽限制下的调度：转录、向量化、LLM 生成和 TTS 如何共享带宽，以及抢占如何工作。
- 实测容量（不是宣传说法），覆盖两种场景：五户分时使用，以及五户同时在线：聚合 token 速率、首 token 延迟和性能下降阈值。
- 故障与扩展路径：断电、磁盘故障或模型加载失败时会怎样，扩展是增加主机、升级模型主机，还是压缩上下文。
- 24×7 持续负载表现：散热节流、备份 / 恢复、远程管理。

参考容量模型（仅为估算，需用供应商在确切机器上的基准替换）：

- M4 Pro，48 GB，273 GB/s：文字 + 语音问答在 2–3 个并发生成会话时舒适，4–5 个时下降。
- M4 基础款，16 GB，120 GB/s：约为上述一半。
- 实时数字人视频**不在**上述 1 对 5 舒适数字的范围内；它需要单独的容量案例（Mac mini 级主机上约 1 路高质量并发流）。
- 注册家庭数 ≠ 并发会话数。注册容量必须按高峰时段活跃比例推导：`H_registered = C_max / (高峰活跃比例 × 生成占用率)`。

### English

The host model, memory, and SSD are **not yet fixed**. The supplier's R&D must confirm, in technical terms:

- Exact model and configuration: M4 or M4 Pro, unified memory, SSD size, external-storage expandability.
- Multi-tenant architecture on a single host: process-level and data-level isolation, independent data directories, independent vector collections, independent keys, and a proof that retrieval cannot cross households.
- Scheduling under unified-memory bandwidth limits: how transcription, embedding, LLM generation, and TTS share bandwidth, and how pre-emption works.
- Measured capacity, not marketing claims, for both scenarios: five households time-shared, and five households online at once: aggregate token rate, time-to-first-token, and degradation threshold.
- Failure and scaling path: what happens on power loss, disk failure, or model-load failure, and whether scaling is by adding a host, upgrading the model, or compressing context.
- 24×7 sustained-load behaviour: thermal throttling, backup/restore, remote management.

Reference capacity model (estimates only, to be replaced by supplier benchmarks on the exact machine):

- M4 Pro, 48 GB, 273 GB/s: text + voice Q&A comfortable at 2–3 concurrent generating sessions, degraded at 4–5.
- M4 base, 16 GB, 120 GB/s: roughly half the above.
- Real-time digital-human video is **out of scope** for the 1-to-5 comfort numbers above; it needs a separate capacity case (about 1 concurrent high-quality stream on a Mac mini class host).
- Registered households ≠ concurrent sessions. Registered capacity must be derived from peak-hour active fraction: `H_registered = C_max / (peak active fraction × generation duty cycle)`.

## 4. 计划服务（未来功能，演示中没有） / Planned services (future, not in the demo)

### 中文

1. 语音转文字：经授权的口述录音变成可编辑文字。姓名、日期和方言必须由家庭成员复核；自动转录绝不被当作历史事实。
2. 带来源的文字问答：就经授权的家庭资料提问；回答必须引用具体来源，并标注证据不足或证据冲突。
3. 语音问答和朗读：仅在家庭主动授权时使用麦克风，并提供等效的文字路径。

除非另行约定，v1 范围之外：实时数字人视频、公开分享，以及任何已验证效果的声称。

### English

1. Speech-to-text: authorised oral recordings become editable text. Names, dates, and dialects must be reviewed by family members; automatic transcription is never treated as historical fact.
2. Text Q&A with sources: ask about authorised family material; answers must cite specific sources and mark insufficient or conflicting evidence.
3. Voice Q&A and read-aloud: microphone only with active household permission, with an equivalent text path.

Out of scope for v1 unless separately agreed: real-time digital-human video, public sharing, and any claim of verified effects.

## 5. Google Drive 集成（Drive API v3） / Google Drive integration (Drive API v3)

### 中文

官方文档：https://developers.google.com/drive/v3/reference

按顺序要求：

- OAuth 2.0，使用与任务匹配的最窄权限。只读同步：`drive.readonly` / `drive.metadata.readonly`。仅当用户通过 Picker 选择文件时才用 `drive.file`。默认绝不申请完整 `drive` 权限。
- `files.list`，带 `q` 过滤（`trashed=false`、`'<folderId>' in parents`），用 `nextPageToken` 分页，只取最小 `fields`。
- 二进制文件：`files.get`，带 `alt=media`。
- Google Docs / Sheets / Slides：用 `files.export` 导出为请求的 MIME 类型——它们不能作为二进制文件直接下载。
- 增量同步：`changes.getStartPageToken` + `changes.list`。每次运行时不要全量重扫 Drive。
- 配额：`about.get` → `storageQuota`。删除必须在有限时间内删除文件、其转录、其向量和其缓存。
- 权限：默认绝不把家庭文件夹设为公开。分享是另一项需明确批准的操作。

### English

Official docs: https://developers.google.com/drive/v3/reference

Required, in order:

- OAuth 2.0 with the narrowest scope that fits the job. Read-only sync: `drive.readonly` / `drive.metadata.readonly`. Use `drive.file` only when the user picks files via Picker. Never request full `drive` scope by default.
- `files.list` with `q` filters (`trashed=false`, `'<folderId>' in parents`), pagination via `nextPageToken`, and minimal `fields`.
- Binary files: `files.get` with `alt=media`.
- Google Docs / Sheets / Slides: `files.export` to a requested MIME type — they cannot be downloaded as binary files.
- Incremental sync: `changes.getStartPageToken` + `changes.list`. Do not rescan the whole Drive on every run.
- Quota: `about.get` → `storageQuota`. Deletion must remove the file, its transcript, its vectors, and its caches within a bounded time.
- Permissions: never make a family folder public by default. Sharing is a separate, explicitly approved action.

## 6. RAG 与信任要求 / RAG and trust requirements

### 中文

- 每个回答必须可追溯到来源文件、页 / 章节和版本。如果来源被修改或删除，回答不得再引用旧版本。
- 未知就是未知。不得编造价格、法规、客户承诺或测试数据。不得把项目目标说成已验证结果。
- 证据冲突必须呈现为冲突，不得由模型悄悄解决。
- 方言、口音和老年人语音：必须度量转录错误，家庭复核必须切断错误传导链（转录 → 分块 → 向量 → 检索 → 回答）。
- 没有可核实、经家庭批准的案例记录，不得声称任何已验证的效果百分比。

### English

- Every answer must be traceable to a source file, page/section, and version. If the source was modified or deleted, the answer must not cite the old version.
- Unknown stays unknown. Do not fabricate prices, regulations, customer commitments, or test data. Do not present a project target as a verified result.
- Conflicting accounts must be shown as conflicting, not resolved silently by the model.
- Dialect, accent, and elderly speech: transcription error must be measured, and family review must break the error-propagation chain (transcript → chunk → vector → retrieval → answer).
- No verified-effect percentages may be claimed without a verifiable, household-approved case record.

## 7. 非功能需求 / Non-functional requirements

### 中文

- 隐私：赞助算力 ≠ 赞助方访问权。社区介绍 ≠ 社区访问权。各户资料按设计隔离。
- 安全：令牌只存放在主机上，绝不写进代码或 git 历史；日志不得包含文件内容或凭证。
- 可靠性：Mac mini 默认不是服务器——社区服务需要外部备份、UPS 和恢复流程。
- 可运维性：模型、向量库和原始文件必须一起版本化；更新不得悄悄改变旧资料的回答。
- 退出：赞助结束或某户退出时，资料导出和删除必须在约定流程内完成，无需超出约定流程的赞助方配合。

### English

- Privacy: sponsor compute ≠ sponsor access. Community introduction ≠ community access. Each household's data is isolated by design.
- Security: tokens stored only on the host, never in code or git history; logs must not contain file contents or credentials.
- Reliability: the Mac mini is not a server by default — external backup, UPS, and a restore procedure are required for a community service.
- Operability: model, vector store, and original files must be versioned together; an update must not silently change answers for old material.
- Exit: when sponsorship ends, or a household withdraws, data export and deletion must work without the sponsor's cooperation beyond the agreed procedure.

## 8. 给供应商研发总监的开放问题（1 对 5） / Open questions for the supplier's R&D director (1 to 5)

### 中文

这些是供应商架构问题，不是学术研究问题。它们是 1 对 5 声称的验收测试：

1. 单台主机上五租户隔离如何实现、如何证明？
2. 五户分时 vs 五户同时在线时，实测聚合 token 速率和首 token 延迟是多少？
3. 统一内存带宽限制下，转录、向量化、LLM 和 TTS 如何调度，性能下降阈值是多少？
4. 断电、磁盘和模型加载故障时，每户的故障模式和恢复时间是多少？
5. 从 5 户扩展到 10 户时架构如何变化——增加主机、更大的模型主机，还是更小的模型？

### English

These are vendor-architecture questions, not academic research questions. They are the acceptance test for the 1-to-5 claim:

1. How is five-tenant isolation implemented and proven on one host?
2. What is the measured aggregate token rate and time-to-first-token for five households time-shared vs. five online at once?
3. How are transcription, embedding, LLM, and TTS scheduled under unified-memory bandwidth limits, and what is the degradation threshold?
4. What is the failure mode and recovery time for power, disk, and model-load failures, per household?
5. What changes in the architecture when going from 5 to 10 households — another host, a larger model host, or a smaller model?

## 9. 开放研究问题（NUS 课题，与第 8 节分开） / Open research questions (for the NUS topic, separate from §8)

### 中文

1. 上传数量限制如何改变家庭选择保留什么内容，这种选择偏差如何度量？
2. 对于小型、异构、方言重的家庭语料，如何引用和标注冲突，使转录错误在反复检索后不会变成“事实”？
3. 当算力由赞助方提供、存储在免费第三方平台、介绍方是社区组织时，数据主权、退出和删除权如何设计？

### English

1. How does an upload-quantity limit change what families choose to preserve, and how can that selection bias be measured?
2. How can small, heterogeneous, dialect-heavy family corpora be cited and conflict-labelled so transcription errors do not become “facts” after repeated retrieval?
3. How are data sovereignty, withdrawal, and exit rights designed when compute is sponsored, storage is on a free third-party platform, and introduction is by a community organisation?

## 10. 开发文档 / Development documentation

### 中文

- [docs/README.md](docs/README.md) — 开发笔记索引。
- [docs/google-drive-api.md](docs/google-drive-api.md) — DeepFamily 的 Drive API v3 笔记（权限、列出 / 搜索、下载 / 导出、增量同步、配额、权限）。
- [docs/mac-mini-m4-pro.md](docs/mac-mini-m4-pro.md) — 赞助主机笔记（待确认的 M4 Pro 硬件、统一内存、Apple Silicon 本地 AI 栈、主机运维、1 对 5 前的基准）。

2026-10-30 已确认：赞助主机是 Mac mini——不是 Mac Pro 塔式机，不是 Mac Studio，也不是任何其他台式机。确切芯片、内存和 SSD 仍待确认（规划基线：M4 Pro，48 GB）——见 docs/README.md。

### English

- [docs/README.md](docs/README.md) — index of development notes.
- [docs/google-drive-api.md](docs/google-drive-api.md) — Drive API v3 notes for DeepFamily (scopes, list/search, download/export, incremental sync, quota, permissions).
- [docs/mac-mini-m4-pro.md](docs/mac-mini-m4-pro.md) — sponsor host notes (M4 Pro hardware to confirm, unified memory, local AI stack on Apple Silicon, host operations, benchmarks before 1-to-5).

Confirmed 2026-10-30: the sponsor host is a Mac mini — not a Mac Pro tower, not a Mac Studio, and not any other desktop. Exact chip, memory, and SSD are still to be confirmed (planning baseline: M4 Pro, 48 GB) — see docs/README.md.

## 11. 验收标准（v1） / Acceptance criteria (v1)

### 中文

- [ ] 1 对 5 案例的主机型号、内存、SSD 和供应商基准已书面确认。
- [ ] 五个隔离租户工作空间已演示；跨租户检索测试返回空。
- [ ] 免费 Drive 同步只读、增量、带配额检查，适用于约定的上传限制 N。
- [ ] 转录 + 文字问答 + 语音问答在仅经授权的测试资料上端到端跑通（测试中不使用真实家庭资料）。
- [ ] 每个回答都显示来源；未知和冲突案例被标注，而不是被抹平。
- [ ] 删除和退出流程已端到端测试。
- [ ] 任何演示、推介或 README 中都没有声称硬件、GPU、AI 或存储已包含，除非已另行约定。

### English

- [ ] Host model, memory, SSD, and supplier benchmarks confirmed in writing for the 1-to-5 case.
- [ ] Five isolated tenant workspaces demonstrated; a cross-tenant retrieval test returns nothing.
- [ ] Free-Drive sync works read-only, incrementally, with quota checks, for the agreed upload limit N.
- [ ] Transcription + text Q&A + voice Q&A work end-to-end on authorised test data only (no real family data in testing).
- [ ] Every answer shows its source; unknown and conflicting cases are labelled, not smoothed over.
- [ ] Deletion and exit procedures tested end-to-end.
- [ ] No claim in any demo, pitch, or README states that hardware, GPU, AI, or storage is included unless it is separately agreed.
