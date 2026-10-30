# DeepFamily 研发需求书 / R&D Requirements Document

> 版本 / Version：v0.1 草稿 / Draft — 2026-10-30
> 原始需求来源 / Original source：
> https://dcdeeptech.com/DeepFamily/preview/community-family-workspace.html?lang=en
> 状态 / Status：需求书，非已部署产品。原始页面是纯前端演示，
> 目前没有服务器、账户、上传或 AI 服务，所有示例均为虚构。
>
> Status: Requirements document, NOT a deployed product. The source
> page is a front-end-only demo with no server, account, upload, or
> AI service, and all examples on it are fictional.
>
> 阅读方式 / How to read this document：每节先中文、后英文，
> 两语内容对应，不是一份译一份的附录。需求编号（FR / NFR / DR）
> 在两语中通用，便于评审、测试和供应商对接时引用。
> Each section is given in Chinese first, then English. Requirement
> IDs (FR / NFR / DR) are shared across both languages so reviewers,
> testers, and suppliers can cite the same ID.

---

## 0. 文档控制 / Document Control

### 中文

- 目的：把原始演示页表达的“拟议架构”翻译成研发可实现、可测试、
  可验收的需求。演示页说什么、没说什么，研发都必须原样区分，
  不能把演示效果当成已实现功能。
- 适用范围：社区公益场景下，一家赞助家族向五户受支持家庭提供
  算力服务的系统。社区机构只作介绍，不进入算力与资料链路。
- 不适用：本需求书不承诺任何报价包含硬件、GPU 配额、AI 能力或
  云储存；不承诺任何效果数据；不包含真实家庭资料。
- 术语与机型确认（2026-10-30 已确认）：赞助主机是 Mac mini，
  不是 Mac Pro 塔式机、不是 Mac Studio、不是其他台式机。
  具体芯片、内存、SSD 仍待确认，规划基线为 M4 Pro 48 GB
  （见 docs/mac-mini-m4-pro.md）。

### English

- Purpose: translate the "proposed architecture" shown on the demo
  page into requirements that engineering can implement, test, and
  accept. What the demo shows and what it does not show must stay
  distinct; a demo effect is never treated as an implemented feature.
- Scope: a community-charity system in which one sponsor family
  provides compute services to five supported households. The
  community organisation only introduces the sponsor and is not in
  the compute or data chain.
- Exclusions: this document does not promise that any price includes
  hardware, GPU quota, AI capability, or cloud storage; it promises
  no effect data; it contains no real household data.
- Terminology and host confirmation (confirmed 2026-10-30): the
  sponsor host is a Mac mini — not a Mac Pro tower, not a Mac Studio,
  and not any other desktop. Exact chip, memory, and SSD are still
  to be confirmed; the planning baseline is M4 Pro, 48 GB (see
  docs/mac-mini-m4-pro.md).

---

## 1. 原始需求理解 / Understanding of the Original Requirement

### 中文

开发者对原始页面的理解如下，研发必须以这份理解为准，而不是以
页面视觉效果为准：

1. **拓扑是拟议的，不是已部署的。** 一家赞助家族拟提供五项
   彼此区分的算力服务，每项连接一户家庭；社区仅介绍赞助商。
   图中服务与安全措施均未上线。
2. **权责边界是核心需求，不是文案。** 社区不提供算力、不审核
   家庭资料、不参与运营；家庭分别决定自身资料许可与成果；
   赞助商提供资源也不自动获准查看家庭文件；运营、隔离、密钥、
   日志及删除责任须另行书面约定。
3. **演示是纯前端的。** 步骤、状态与示例文字预写在浏览器页面中；
   不验证邀请、不传输资料、不运行 AI；文件选择只做本地后缀与
   大小检查，不打开内容；关闭页面即清除检查结果。
4. **未来交互是方向说明，不是现有功能。** 语音转文字、文字提问
   与来源、语音提问与朗读，均标注为“未来”，当前没有模型、
   语音服务或资料索引。
5. **成本边界必须保留。** 该拓扑不表示硬件、GPU 配额、AI 能力
   或云储存已包含在当前每户支持或 S$98,000 私人项目报价内；
   启用前须另行约定成本、许可、隐私与安全。

### English

The developer's reading of the source page, which engineering must
follow rather than following the page's visuals, is:

1. **The topology is proposed, not deployed.** One sponsor family
   proposes five distinct compute services, each connected to one
   household; the community only introduces the sponsor. The services
   and safeguards in the diagram are not live.
2. **The responsibility boundary is a core requirement, not copy.**
   The community provides no compute, reviews no household data, and
   does not operate the service; each household decides its own data
   permission and outputs; providing resources does not automatically
   entitle the sponsor to view household files; operations, isolation,
   keys, logging, and deletion must be agreed separately in writing.
3. **The demo is front-end only.** Steps, states, and example text
   are pre-written in the browser page; it validates no invitation,
   transmits no data, and runs no AI; file selection only checks
   suffix and size locally, does not open content; closing the page
   clears the check result.
4. **Future interactions are direction, not current features.**
   Speech-to-text, text Q&A with sources, and voice Q&A / read-aloud
   are all marked "future"; there is currently no model, voice
   service, or data index.
5. **The cost boundary must be preserved.** The topology does not
   mean hardware, GPU quota, AI capability, or cloud storage is
   included in current per-household support or in the S$98,000
   private-project price; cost, permission, privacy, and security
   must be agreed separately before activation.

---

## 2. 目标与非目标 / Goals and Non-Goals

### 中文

**目标：**

- G1：让五户家庭在各自授权范围内，用自己的资料保存记忆、
  转录口述、提问并获得带来源的回答。
- G2：让赞助算力可运行、可隔离、可审计、可退出，而不让赞助
  变成资料访问权。
- G3：让社区介绍角色可证明：介绍发生过，但介绍方不接触资料。

**非目标（v1 不做）：**

- 不做公开分享、社交、家族树公开出版。
- 不做实时数字人视频（需另立容量与成本案）。
- 不做跨户资料聚合、跨户搜索、跨户推荐。
- 不用家庭资料训练任何共享模型。
- 不宣称转录、回答或任何指标有已验证的效果。

### English

**Goals:**

- G1: Let five households, within their own authorisations, preserve
  memories from their own material, transcribe oral recordings, ask
  questions, and receive answers with sources.
- G2: Make sponsor compute runnable, isolated, auditable, and
  exitable — without turning sponsorship into a right to access data.
- G3: Make the community's introducer role provable: the introduction
  happened, but the introducer does not touch data.

**Non-goals (v1):**

- No public sharing, social features, or public family-tree publishing.
- No real-time digital-human video (needs a separate capacity and
  cost case).
- No cross-household data aggregation, search, or recommendation.
- No training of any shared model on household data.
- No claim of verified effects for transcription, answers, or any metric.

---

## 3. 角色与信任边界 / Roles and Trust Boundaries

### 中文

| 角色 | 能做什么 | 明确不能做什么 |
| --- | --- | --- |
| 赞助家族（算力提供方） | 提供并运维主机；按约定启停服务 | 未经家庭授权查看、复制、导出家庭文件、转录、向量或回答 |
| 受支持家庭（每户独立） | 授权自身资料来源；决定许可与成果；随时撤回与删除 | 访问其他家庭的任何资料、索引或回答 |
| 社区机构（介绍方） | 介绍赞助商；记录介绍关系（不含资料内容） | 提供算力、审核资料、参与运营、接触家庭资料 |
| 运维方（如与赞助方不同，须书面指定） | 按约定做健康检查、备份、恢复 | 以运维为名读取家庭资料内容 |
| 供应商（主机 / 模型供应商） | 按研发需求提供主机、模型与基准数据 | 以供应商身份访问家庭资料 |

信任原则：默认不信任链路上的任何一方能“顺便”看到资料；
隔离必须由架构保证（独立进程 / 独立资料目录 / 独立向量库 /
独立密钥），而不是靠操作规范保证。

### English

| Role | Can do | Must NOT do |
| --- | --- | --- |
| Sponsor family (compute provider) | Provide and operate the host; start/stop services as agreed | View, copy, or export household files, transcripts, vectors, or answers without household authorisation |
| Supported household (each independent) | Authorise its own data sources; decide permissions and outputs; withdraw and delete at any time | Access any other household's data, index, or answers |
| Community organisation (introducer) | Introduce the sponsor; record the introduction (without data content) | Provide compute, review data, operate the service, or touch household data |
| Operator (if different from sponsor, must be named in writing) | Health checks, backup, and restore as agreed | Read household data content in the name of operations |
| Supplier (host / model supplier) | Supply host, models, and benchmark data per the R&D requirements | Access household data as a supplier |

Trust principle: no party on the chain is assumed to be able to
"incidentally" see data. Isolation must be guaranteed by
architecture (separate processes / data directories / vector stores /
keys), not by operating procedures alone.

---

## 4. 系统架构 / System Architecture

### 中文

```
                社区机构（仅介绍，灰色虚线）
                        │
                        │ 介绍
                        ▼
              ┌─────────────────────┐
              │   赞助主机（1 台）    │
              │  Mac mini + M4 Pro   │
              │  ┌───────────────┐  │
              │  │ 同步服务       │  │── 家庭 A 的 Drive（只读）
              │  │ 转录 / 嵌入    │  │── 家庭 B 的 Drive（只读）
              │  │ 检索 / LLM     │  │── 家庭 C 的 Drive（只读）
              │  │ TTS / 语音     │  │── 家庭 D 的 Drive（只读）
              │  │ 每户独立租户   │  │── 家庭 E 的 Drive（只读）
              │  └───────────────┘  │
              └─────────────────────┘
        每户：独立资料目录 + 独立向量库 + 独立密钥
        禁止：跨户检索、跨户共享模型、跨户日志混写
```

架构要点：

- 主机内部按租户隔离，不是在界面上分开显示而已。
- Drive 是来源，不是权限系统；权限与隔离在主机侧实现。
- 所有推理原则上在主机本地完成；任何云端调用都须单项授权、
  单项记录，且不得成为默认路径。
- 模型、向量库与原始文件须版本对应；模型升级后须重新验证，
  不得静默改变旧资料的回答。

### English

```
                Community (introduction only, dashed line)
                        │
                        │ introduces
                        ▼
              ┌─────────────────────┐
              │   Sponsor host (1)  │
              │  Mac mini + M4 Pro  │
              │  ┌───────────────┐  │
              │  │ Sync service  │  │── Household A Drive (read-only)
              │  │ Transcribe /  │  │── Household B Drive (read-only)
              │  │  embed        │  │── Household C Drive (read-only)
              │  │ Retrieval /   │  │── Household D Drive (read-only)
              │  │  LLM / TTS    │  │── Household E Drive (read-only)
              │  │ Per-tenant    │  │
              │  └───────────────┘  │
              └─────────────────────┘
        Per household: own data dir + own vector store + own key
        Forbidden: cross-tenant retrieval, shared models,
        mixed tenant logs
```

Architecture points:

- Isolation is inside the host, per tenant — not merely separate
  views in the UI.
- Drive is a source, not the permission system; permission and
  isolation are implemented on the host.
- Inference is, in principle, local on the host; any cloud call
  needs per-item authorisation and per-item logging, and must never
  be the default path.
- Model, vector store, and originals must be version-matched; after
  a model upgrade, answers for old material must be re-validated,
  never silently changed.

---

## 5. 功能需求 / Functional Requirements

优先级：M = 必须 / Must，S = 应该 / Should，C = 可以 / Could。
Priority: M = Must, S = Should, C = Could.

### FR-01 家庭入驻与授权 / Household onboarding and authorisation — M

中文：每户独立入驻；入驻须记录：家庭标识（不含真实姓名也可
用代号）、授权资料来源（Drive 文件夹）、授权范围（只读）、
授权人、授权时间、撤回方式。未授权前，系统不得同步、解析、
嵌入该户任何资料。

English: Each household onboards independently. Onboarding must
record: household ID (a code may be used instead of a real name),
authorised data source (Drive folder), scope (read-only),
authoriser, time, and withdrawal method. Before authorisation, the
system must not sync, parse, or embed any of that household's data.

验收 / Acceptance：无授权记录的家庭在同步列表中不可见；
授权记录可导出为审计条目（不含文件内容）。

### FR-02 资料来源接入 / Data-source connection — M

中文：支持家庭自有 Google Drive（免费账户）只读接入；支持
文件夹级授权；支持断线重连与增量同步（见第 6 节）。演示页的
“云盘连接 · 未开放”在 v1 必须变为可用，但默认只读。

English: Support read-only access to a household's own Google Drive
(free account), at folder level, with reconnect and incremental sync
(see §6). The demo's "cloud drive connection — not open" must become
available in v1, read-only by default.

### FR-03 本地文件检查 / Local file check — M

中文：上传 / 选择文件前，先做本地格式与大小检查（演示页已有
此行为，v1 保留并明确化）：只检查后缀与大小，不打开内容、不
上传；检查结果在关闭页面 / 会话后清除；真实资料不得在演示
模式下被处理。检查计数（如 0 / 20）只是示例计数器，不是已
确认的产品上限；真实上限 N 须在配置中单独设定并在界面明示。

English: Before upload/selection, check format and size locally
(the demo already does this; v1 keeps and clarifies it): check suffix
and size only, do not open content or upload; clear the check result
when the page/session closes; real data must not be processed in demo
mode. A check counter (e.g. 0 / 20) is only an example counter, not a
confirmed product limit; the real limit N must be set in configuration
and shown in the UI.

### FR-04 语音转文字 / Speech-to-text — M

中文：将获准的口述录音转成可编辑文字；转录结果须可由家人
逐句复核修改；人名、年代、方言须标注为“待复核”，不得把自动
转录当作史实；转录错误率须在测试集上度量并记录（见第 8 节）。

English: Transcribe authorised oral recordings into editable text;
results must be reviewable and correctable sentence by sentence by
family members; names, years, and dialect must be marked "to be
verified" — automatic transcription is never treated as historical
fact; transcription error must be measured on a test set and recorded
(see §8).

### FR-05 文字提问与来源 / Text Q&A with sources — M

中文：用文字询问已授权的家族资料；每个回答须附具体来源
（文件、页 / 节、版本）；证据不足标“证据不足”，不同说法标
“说法不一致”并并列呈现，不得由模型自行裁决；无来源不得
编造回答，须回答“未知 / 未找到”。

English: Ask authorised family material in text; every answer must
cite a specific source (file, page/section, version); insufficient
evidence is marked "insufficient evidence", conflicting accounts are
marked "conflicting accounts" and shown side by side, never resolved
silently by the model; without a source, the system must answer
"unknown / not found", never fabricate.

### FR-06 语音提问与朗读 / Voice Q&A and read-aloud — M

中文：家庭主动授权后可用语音提问、听取回答；麦克风授权须
是显式、单次 / 会话级、可随时关闭；必须提供同等文字操作，
语音不是唯一路径；语音回答须与文字回答来源一致。

English: After a household's active authorisation, voice questions
and read-aloud are available; microphone authorisation must be
explicit, per-session, and closable at any time; an equivalent text
path must always exist — voice is never the only path; voice answers
must carry the same sources as text answers.

### FR-07 家庭工作台 / Household workspace — S

中文：每户独立工作台：授权来源、同步状态、转录待复核清单、
提问历史（仅本户）、删除与退出入口。不得出现其他家庭的任何
条目、计数或提示。

English: One workspace per household: authorised sources, sync
status, transcription review queue, question history (own household
only), and delete/exit entry. No entry, count, or hint from any other
household may appear.

### FR-08 社区介绍记录 / Community introduction record — S

中文：社区可记录“介绍了哪家赞助商给哪户”（代号即可），
记录不得包含家庭文件、转录、问题或回答内容；介绍记录的查看
权限与家庭资料权限完全分离。

English: The community may record "which sponsor was introduced to
which household" (codes suffice); the record must contain no household
files, transcripts, questions, or answers; viewing introduction
records is fully separated from household-data permissions.

### FR-09 删除与退出 / Deletion and exit — M

中文：家庭撤回授权或退出时，须在约定时间内删除：原始副本、
转录、向量、缓存、日志中的内容字段；删除须可验证（删除清单
+ 复查计数为零）；赞助结束不影响家庭取回自身原始资料的权利，
原始资料始终在家庭自己的 Drive 中。

English: On withdrawal or exit, within the agreed time, delete:
original copies, transcripts, vectors, caches, and content fields in
logs; deletion must be verifiable (deletion checklist + re-check count
zero); end of sponsorship does not affect a household's right to its
own originals, which always remain in the household's own Drive.

### FR-10 演示模式 / Demo mode — M

中文：保留一个与真实服务完全隔离的演示模式：只用虚构示例，
不连接服务器、不处理真实资料；进入演示模式与进入真实服务
在界面上必须明显区分，不得让用户误把演示当成已上线服务。

English: Keep a demo mode fully isolated from the real service:
fictional examples only, no server connection, no real data processed;
entering demo mode vs. entering the real service must be clearly
distinguished in the UI, so no user mistakes the demo for a live service.

---

## 6. 资料与 Google Drive 需求 / Data and Google Drive Requirements

### 中文

- DR-01：Drive API v3；只读同步默认 scope 为
  `drive.readonly` / `drive.metadata.readonly`，不得默认申请完整
  `drive` 权限。详见 docs/google-drive-api.md。
- DR-02：增量同步：`changes.getStartPageToken` +
  `changes.list`；不得每次全量扫描；token 失效时只做一次全量
  重列并记录。
- DR-03：普通文件用 `files.get` + `alt=media` 下载；
  Docs / Sheets / Slides 用 `files.export` 导出，并在元数据中
  记录导出格式（同文件不同导出格式不是同一来源）。
- DR-04：每次同步记录文件 ID、modifiedTime、哈希；回答引用
  必须绑定到该版本；来源变更或删除后，旧回答不得继续引用旧版本。
- DR-05：免费账户配额：同步前检查
  `N × s ≤ 剩余配额`（N = 约定上传上限，s = 平均文件大小）；
  不满足时停止并明示，不得静默跳过文件。15 GB 只是免费账户
  的典型值，须按账户实测，不得硬编码为保证。
- DR-06：共享云端硬盘如需支持，须加 `supportsAllDrives` 相关
  参数，否则共享盘文件会静默缺失。
- DR-07：权限：家庭文件夹默认不公开；任何分享须家庭显式批准
  并单独审计。

### English

- DR-01: Drive API v3; read-only sync defaults to
  `drive.readonly` / `drive.metadata.readonly`; never request full
  `drive` scope by default. See docs/google-drive-api.md.
- DR-02: Incremental sync via `changes.getStartPageToken` +
  `changes.list`; never rescan the whole Drive each run; on token
  expiry, do one full re-list and log it.
- DR-03: Binary files via `files.get` + `alt=media`; Docs / Sheets /
  Slides via `files.export`, recording the export format in metadata
  (different export formats of the same file are not the same source).
- DR-04: Record file ID, modifiedTime, and hash on every sync;
  answer citations must bind to that version; after a source changes
  or is deleted, old answers must not keep citing the old version.
- DR-05: Free-account quota: before sync, check
  `N × s ≤ remaining quota` (N = agreed upload limit, s = average file
  size); if it does not fit, stop with a clear message, never silently
  skip files. 15 GB is only a typical free-account value and must be
  verified per account, never hard-coded as a guarantee.
- DR-06: Shared drives, if supported, need `supportsAllDrives`
  parameters, otherwise shared-drive files will silently be missing.
- DR-07: Permissions: household folders are not public by default;
  any sharing needs explicit household approval and its own audit entry.

---

## 7. 检索与 AI 需求 / Retrieval and AI Requirements

### 中文

- AR-01：分块须保留来源元数据（文件 ID、modifiedTime、页 / 节、
  块 ID）；无元数据的块不得进入索引。
- AR-02：每户独立向量库；跨户检索在代码与权限层面必须不可达，
  并用跨户测试证明（以 B 户内容查 A 户库，结果须为零）。
- AR-03：检索须支持混合检索（向量 + 关键词）与重排序参数记录；
  小规模、异构、方言重的家庭语料须单独度量，不得套用通用基准。
- AR-04：回答规则：只依据检索到的授权内容回答；引用来源；
  未找到时说未知；冲突时并列；不得编造价格、法规、客户承诺
  或效果数据；不得把项目目标（如“降低 30%”类表述）说成已
  验证结果。
- AR-05：转录 → 分块 → 嵌入 → 检索 → 生成的误差传播链须可
  追踪：转录复核是断链点，未经复核的转录不得作为“事实”进入
  回答。
- AR-06：模型、提示词、向量库版本须记录；模型变更后须重新
  验证旧资料回答，不得静默改变。

### English

- AR-01: Chunks must carry source metadata (file ID, modifiedTime,
  page/section, chunk ID); chunks without metadata must not enter
  the index.
- AR-02: One vector store per household; cross-tenant retrieval must
  be unreachable at code and permission level, and proven by a
  cross-tenant test (querying A's store with B's content must return zero).
- AR-03: Retrieval must support hybrid retrieval (vector + keyword)
  with recorded reranker parameters; small, heterogeneous,
  dialect-heavy household corpora must be measured separately, never
  assumed from generic benchmarks.
- AR-04: Answering rules: answer only from retrieved authorised
  content; cite sources; say unknown when not found; show conflicts
  side by side; never fabricate prices, regulations, customer
  commitments, or effect data; never present a project target as a
  verified result.
- AR-05: The error-propagation chain
  transcribe → chunk → embed → retrieve → generate must be traceable;
  family review of transcripts is the break point — unreviewed
  transcripts must not enter answers as "facts".
- AR-06: Model, prompt, and vector-store versions must be recorded;
  after a model change, answers for old material must be re-validated,
  never silently changed.

---

## 8. 非功能需求 / Non-Functional Requirements

### 中文

**NFR-01 性能与并发（M）：**

- 以赞助主机实测为准，不以宣传页为准。基准机型：Mac mini +
  M4 Pro 48 GB（见 docs/mac-mini-m4-pro.md）。
- 必须度量：单户首 token 延迟、聚合 token 速率、2 / 3 / 4 / 5
  户同时生成时的速率衰减、转录进行时语音首包延迟、转录吞吐
  （音频小时 / 实际小时）。
- 规划参考（估计值，须实测替换）：文本 + 语音问答舒适并发
  2–3 户，4–5 户降级；实时数字人视频不在此口径内。
- 注册户数 ≠ 并发户数：`注册上限 = 舒适并发 ÷（高峰活跃比例
  × 生成占空比）`，对外承诺用舒适值，极限值只用于内部压测。

**NFR-02 安全与隐私（M）：**

- 租户隔离、密钥分离、日志不含内容与凭证、token 只存主机、
  永不进代码仓库。
- 传输与静态资料加密；备份加密；备份恢复须实测。
- 任何云端 AI 调用须单项授权并记录，不得成为默认路径。

**NFR-03 可靠性（M）：**

- Mac mini 不是服务器：须配 UPS、外部备份盘、断电自动重启
  （均须实测）；单点故障（断电、磁盘、模型加载失败）的恢复
  时间与影响户数须写进运维手册。
- 服务健康检查与告警：同步失败、配额不足、模型加载失败须
  可见、可定位，不得静默失败。

**NFR-04 可用性与无障碍（S）：**

- 老年用户与方言用户优先：大字、简单步骤、文字替代语音、
  麦克风可随时关闭、错误提示用日常语言而非错误码。
- 演示模式与真实服务在视觉与文案上明显区分。

**NFR-05 可运维与可退出（M）：**

- 模型 / 向量库 / 原始文件版本对应；更新、回滚、删除、退出
  流程均须有书面步骤与测试记录。
- 赞助结束时，家庭取回与删除流程不依赖赞助方单方配合之外的
  额外条件。

### English

**NFR-01 Performance and concurrency (M):**

- Measured on the sponsor host, not taken from marketing pages.
  Baseline: Mac mini + M4 Pro 48 GB (see docs/mac-mini-m4-pro.md).
- Must measure: single-household time-to-first-token, aggregate token
  rate, rate decay with 2 / 3 / 4 / 5 concurrent generating sessions,
  first-voice-packet latency while transcription runs, and
  transcription throughput (audio hours per wall-clock hour).
- Planning reference (estimates, to be replaced by measurement):
  text + voice Q&A comfortable at 2–3 concurrent households, degraded
  at 4–5; real-time digital-human video is outside this scope.
- Registered households ≠ concurrent households:
  `registered cap = comfortable concurrency ÷ (peak active fraction
  × generation duty cycle)`; promise the comfortable number externally,
  use the hard number only for internal stress testing.

**NFR-02 Security and privacy (M):**

- Tenant isolation, separated keys, logs without content or
  credentials, tokens only on the host, never in a code repository.
- Encryption in transit and at rest; encrypted backups; restore tested.
- Any cloud AI call needs per-item authorisation and logging, and
  must never be the default path.

**NFR-03 Reliability (M):**

- A Mac mini is not a server: UPS, external backup disk, and
  automatic restart after power loss are required (all tested);
  recovery time and affected households for single-point failures
  (power, disk, model-load failure) must be written in the operations
  manual.
- Health checks and alerts: sync failure, quota shortage, and
  model-load failure must be visible and locatable, never silent.

**NFR-04 Usability and accessibility (S):**

- Elderly and dialect users first: large text, simple steps, text
  alternative to voice, microphone closable at any time, error messages
  in plain language, not error codes.
- Demo mode and real service must be clearly distinguished visually
  and in copy.

**NFR-05 Operability and exit (M):**

- Model / vector store / originals version-matched; update, rollback,
  delete, and exit procedures all need written steps and test records.
- At end of sponsorship, a household's retrieval and deletion process
  must not depend on extra conditions beyond the sponsor's agreed
  cooperation.

---

## 9. 供应商研发验收门 / Supplier R&D Acceptance Gates

### 中文

以下问题不是“了解一下”，而是 1 对 5 能否承诺的验收门。
供应商研发总监须书面回答并附实测数据，否则 1 对 5 不得对外承诺：

1. 单台主机上五租户隔离如何实现、如何证明跨户不可达？
2. 五户分时与五户同时在线两种场景下，聚合 token 速率、首 token
   延迟、降级阈值分别是多少？
3. 统一内存带宽受限下，转录、嵌入、LLM、TTS 的调度与抢占机制
   是什么？
4. 断电、磁盘、模型加载失败时，单户恢复时间与影响范围是多少？
5. 从 5 户扩到 10 户时，架构是加主机、换机型，还是降模型 /
   压缩上下文？代价分别是多少？

### English

The following are acceptance gates for the 1-to-5 promise, not
general enquiries. The supplier's R&D director must answer them in
writing with measured data; otherwise 1-to-5 must not be promised
externally:

1. How is five-tenant isolation implemented on one host, and how is
   cross-tenant unreachability proven?
2. For five households time-shared vs. five online at once, what are
   the aggregate token rate, time-to-first-token, and degradation
   threshold in each case?
3. Under unified-memory bandwidth limits, what are the scheduling and
   pre-emption mechanisms for transcription, embedding, LLM, and TTS?
4. On power, disk, or model-load failure, what is the per-household
   recovery time and blast radius?
5. Scaling from 5 to 10 households: add a host, change model/host, or
   shrink the model / compress context — at what cost in each case?

---

## 10. 实施阶段 / Implementation Phases

### 中文

- P0 演示隔离：保留纯前端演示，明确标注虚构与未上线；
  演示与真实服务入口分离。
- P1 隔离与同步：五租户隔离 + Drive 只读增量同步 + 配额检查
  + 删除验证；跨户测试必须通过，方可进入下一阶段。
- P2 转录与文字问答：转录复核流程 + 带来源的文字问答 +
  证据不足 / 说法不一致标注。
- P3 语音问答与朗读：显式麦克风授权 + 文字等效路径 +
  语音首包延迟度量。
- P4 小范围试点：单户真实资料（家庭自愿、书面授权）端到端
  验证；试点结论只写实测结果，不写效果承诺。

### English

- P0 Demo isolation: keep the front-end-only demo, clearly marked
  fictional and not live; demo and real-service entries separated.
- P1 Isolation and sync: five-tenant isolation + Drive read-only
  incremental sync + quota checks + deletion verification; the
  cross-tenant test must pass before moving on.
- P2 Transcription and text Q&A: transcription review flow + text
  Q&A with sources + insufficient-evidence / conflicting-account labels.
- P3 Voice Q&A and read-aloud: explicit microphone authorisation +
  equivalent text path + first-voice-packet latency measurement.
- P4 Small pilot: end-to-end verification on one household's real
  material (voluntary, written authorisation); pilot conclusions state
  measured results only, no effect promises.

---

## 11. 验收标准 / Acceptance Criteria

### 中文

v1 全部通过方可称为“可用”，缺一不可：

- [ ] 五租户隔离演示：跨户检索测试返回零结果。
- [ ] Drive 只读增量同步在约定上传上限 N 下工作，配额不足时
  明示停止。
- [ ] 转录 + 文字问答 + 语音问答在授权测试资料上端到端工作，
  不用真实家庭资料做测试。
- [ ] 每个回答有来源；未知与冲突有标注，不被平滑处理。
- [ ] 删除与退出端到端测试通过。
- [ ] 供应商研发验收门（第 9 节）书面回答 + 实测数据齐全。
- [ ] 演示、宣传、需求书中没有任何一处声称硬件、GPU、AI 或
  储存已包含在内，除非已另行书面约定。
- [ ] 运维手册包含单点故障恢复时间、备份恢复测试记录、
  模型更新与回滚步骤。

### English

All must pass before v1 can be called "usable":

- [ ] Five-tenant isolation demo: cross-tenant retrieval test returns zero.
- [ ] Drive read-only incremental sync works at the agreed upload
  limit N, and stops with a clear message on quota shortage.
- [ ] Transcription + text Q&A + voice Q&A work end-to-end on
  authorised test data only (no real household data in testing).
- [ ] Every answer has a source; unknown and conflicting cases are
  labelled, not smoothed over.
- [ ] Deletion and exit tested end-to-end.
- [ ] Supplier R&D acceptance gates (§9) answered in writing with
  measured data.
- [ ] No demo, pitch, or requirements text claims hardware, GPU, AI,
  or storage is included, unless separately agreed in writing.
- [ ] Operations manual covers single-point-failure recovery time,
  backup-restore test records, and model update/rollback steps.

---

## 12. 待决策事项 / Open Decisions

### 中文

1. 赞助主机最终配置：M4 还是 M4 Pro？内存 24 / 48 / 64 GB？
   SSD 多大？外部备份与 UPS 由谁出资？
2. 每户上传上限 N、主导媒介类型（照片 / 文档 / 音频 / 视频）
   是多少？是否含实时数字人视频？
3. 转录、LLM、TTS 的具体模型与量化方案（须在基准机上实测后定）。
4. 社区介绍记录的保存方、保存期限与查看权限。
5. 试点家庭的选择标准、授权书模板、退出流程的书面约定。
6. 机型已确认是 Mac mini，不再保留塔式机等其他机型的备选容量案；
   仍待确认的是 Mac mini 的具体芯片、内存与 SSD 配置。

### English

1. Final sponsor-host configuration: M4 or M4 Pro? Memory 24 / 48 /
   64 GB? SSD size? Who funds external backup and UPS?
2. Per-household upload limit N and dominant media type
   (photo / document / audio / video)? Is real-time digital-human
   video in scope?
3. Specific transcription, LLM, and TTS models and quantisation
   (to be fixed after benchmarking on the baseline host).
4. Community introduction records: holder, retention period, and
   viewing permissions.
5. Pilot-household selection criteria, authorisation form template,
   and written exit procedure.
6. Host form factor is confirmed as Mac mini; no alternative capacity
   case for a tower or other desktop is kept. What remains open is
   the Mac mini's exact chip, memory, and SSD configuration.

---

## 附录：原始页面到需求的追溯 / Appendix: Traceability from Source Page

### 中文

| 原始页面章节 | 对应需求 |
| --- | --- |
| 01 拟议公益算力拓扑 | §1、§3、§4、§9 |
| 02 交互演示（纯前端） | FR-03、FR-10、P0 |
| 03 资料来源（本地检查、云盘未开放） | FR-02、FR-03、§6 |
| 04 未来交互（语音转文字、文字提问与来源、语音提问与朗读） | FR-04、FR-05、FR-06、§7 |
| 权责边界与成本边界声明 | §1、§3、§11、§12 |
| 演示计数 0 / 20 | FR-03（示例计数器，非确认上限） |
| S$98,000 私人项目报价提及 | §1、§11（不表示已包含硬件 / GPU / AI / 储存） |

### English

| Source page section | Corresponding requirements |
| --- | --- |
| 01 Proposed charity compute topology | §1, §3, §4, §9 |
| 02 Interaction demo (front-end only) | FR-03, FR-10, P0 |
| 03 Data sources (local check, cloud drive not open) | FR-02, FR-03, §6 |
| 04 Future interactions (speech-to-text, text Q&A with sources, voice Q&A / read-aloud) | FR-04, FR-05, FR-06, §7 |
| Responsibility and cost boundary statements | §1, §3, §11, §12 |
| Demo counter 0 / 20 | FR-03 (example counter, not a confirmed limit) |
| S$98,000 private-project price mention | §1, §11 (does not mean hardware / GPU / AI / storage is included) |

---

*本文档为需求草稿，不构成服务已上线、已验证或已包含任何硬件 /
AI / 储存的声明。任何对外承诺须以书面约定与实测数据为准。*
*This document is a requirements draft. It is not a statement that any
service is live, verified, or includes any hardware / AI / storage.
Any external commitment must rest on a written agreement and measured
data.*
