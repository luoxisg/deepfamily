# DeepFamily 开发者 Demo / Developer Demo — 1 台主机，5 个隔离租户 / 1 Host, 5 Isolated Tenants

> 这是什么 / What this is：最小端到端切片，验证 DeepFamily 最有风险的部分——租户隔离、Drive 同步、转录复核、带来源问答、并发度量——全部在一台主机上完成。
> The smallest end-to-end slice that proves the riskiest parts of DeepFamily — tenant isolation, Drive sync, transcription review, cited Q&A, and concurrency measurement — on one host.
>
> 这不是什么 / What this is NOT：不是家庭产品，不是真实 AI 服务，不是 Mac mini 基准。所有资料均为虚构测试资料。
> Not a household product, not a real AI service, not a Mac mini benchmark. All data is fictional test data.
>
> 本 Demo 在本机和 Mac mini 上都能原样运行。仅用 Python 3.10+ 标准库，无需 pip 安装、无需 API 密钥、无云端调用。
> This demo runs unchanged on this VM and on a Mac mini. Python 3.10+ standard library only. No pip installs, no API keys, no cloud calls.

## 快速开始 / Quick Start

### 中文

```bash
cd demo
python3 -m demo.cli
```

你应该看到：5 个租户同步完成、tenant_1 的转录已复核、5 个回答——其中包括一个 `conflicting_accounts` 案例（tenant_3：店铺开业 1968 vs 1978）和一个 `unknown` 案例（tenant_5：法国首都不在任何测试资料中）。

### English

```bash
cd demo
python3 -m demo.cli
```

You should see: 5 tenants synced, tenant_1's transcript reviewed, and 5 answers — including a `conflicting_accounts` case (tenant_3: shop opened 1968 vs 1978) and an `unknown` case (tenant_5: capital of France, not in any fixture).

## 运行测试 / Run the Tests

### 中文

```bash
cd demo
python3 -m unittest discover -s tests -v
```

测试覆盖：跨户查询返回空、未知租户被拒绝、路径越界被拒绝、同步是增量的、删除会传导到索引、回答带引用、未知绝不编造、冲突并列呈现。

### English

```bash
cd demo
python3 -m unittest discover -s tests -v
```

Tests cover: cross-tenant queries return nothing, unknown tenants are rejected, path escapes are rejected, sync is incremental, deletion propagates to the store, answers carry citations, unknown is never fabricated, and conflicts are shown side by side.

## 运行开发者面板 / Run the Developer Dashboard

### 中文

```bash
cd demo
python3 -m demo.server
# 打开 http://127.0.0.1:8001
```

面板是故意做得很简陋的：它是一个开发者工具，不是家庭产品界面。显示租户、块数量、音频测试文件、问答表单和基准按钮。

### English

```bash
cd demo
python3 -m demo.server
# open http://127.0.0.1:8001
```

The dashboard is intentionally plain. It is a developer tool, not a household product UI. It shows tenants, chunk counts, audio fixtures, a Q&A form, and a benchmark button.

## 运行基准 / Run the Benchmark

### 中文

```bash
cd demo
python3 -c "from demo.benchmark import run_all; import json; print(json.dumps(run_all(), indent=2))"
# 生成 benchmark_report.json（1 / 3 / 5 并发会话）
```

### English

```bash
cd demo
python3 -c "from demo.benchmark import run_all; import json; print(json.dumps(run_all(), indent=2))"
# writes benchmark_report.json (1 / 3 / 5 concurrent sessions)
```

## 目录结构 / Layout

```
demo/
  demo/
    tenants.py     租户注册与路径隔离（构建租户路径的唯一方式）
                   Tenant registry + path isolation (the only way to build a tenant path)
    drive.py       同步契约：page token、配额检查、新增/更新/删除
                   Sync contract: page token, quota check, added/updated/deleted
    store.py       每户独立块索引与关键词检索（无共享索引）
                   Per-tenant chunk store + keyword retrieval (no shared index)
    transcribe.py  转录复核门：未经家庭复核绝不进索引
                   Transcript review gate: nothing is indexed before family review
    qa.py          只依据检索到的块回答：已回答 / 未知 / 冲突
                   Answer only from retrieved chunks: answered / unknown / conflicting
    isolation.py   家庭与赞助方隔离：身份门禁、审计链、每户密封备份
                   Household vs sponsor isolation: identity gate, audit chain, per-household sealed backup
    benchmark.py   并发问答计时（1 / 3 / 5 会话）
                   Concurrent Q&A timing (1 / 3 / 5 sessions)
    server.py      标准库开发者面板（http://127.0.0.1:8001）
                   Stdlib developer dashboard (http://127.0.0.1:8001)
    cli.py         全流程验收运行（无需服务器）
                   Full pipeline acceptance run (no server needed)
  fixtures/
    drive/tenant_1..5/   虚构 Drive 文件夹（每户一个）
                         Fictional Drive folders (one per tenant)
    audio/tenant_1/      虚构转录测试文件（不是真实录音）
                         Fictional transcript fixture (not a real recording)
  tests/test_demo.py     验收测试
  tests/test_isolation.py  家庭与赞助方隔离测试
                         Acceptance tests, plus household vs sponsor isolation tests
  demo_data/             运行时数据，首次运行生成，不进 git
                         Runtime data, created on first run, NOT in git
```

## 什么是真实的、什么是 Mock 的——引用数字前必读 / What Is Real, What Is Mocked — Read Before Quoting Any Number

### 中文

| 部分 | 状态 |
| --- | --- |
| 租户隔离（独立目录、无共享索引、路径越界拒绝） | 真实代码，已测试 |
| 增量同步、配额检查、删除传导 | 真实代码，已测试（以测试文件夹代替 Drive） |
| 检索、引用、未知、冲突处理 | 真实代码，已测试 |
| Drive 来源 | Mock：本地测试文件夹。真实适配器 = Drive API v3（`files.list`、`files.get` alt=media、`files.export`、`changes.list`）——见 `demo/drive.py` 与 `docs/google-drive-api.md` |
| 转录 | Mock：测试转录文件。真实适配器 = Mac mini 上的本地 Whisper 类模型。复核门是真实的，不变。 |
| 回答措辞 | Mock：按检索到的块拼模板。真实适配器 = 本地 LLM（MLX / llama.cpp），约束为同一批块和同三种结果。 |
| 本机基准数字 | 仅为 Mock 路径（检索 + 模板）。上 Mac mini 用真实模型后必须重测，不得把本机数字说成 Mac mini 容量。 |
| TTS / 语音首包 | 本 Demo 未实现。选定真实 TTS 模型后单独度量。 |

### English

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

## 在 Mac mini 上运行 / On a Mac mini

### 中文

1. 把本仓库克隆到 Mac mini 上。先确认机型：Mac mini（2026-10-30 已确认——不是 Mac Pro 塔式机，不是 Mac Studio）。记录芯片、内存、SSD；规划基线为 M4 Pro 48 GB。
2. 按上面方法原样运行测试和 CLI，必须不改代码通过。
3. 只替换三个适配器（`drive.py` 来源、`transcribe.py` 模型、`qa.py` 模型），租户、索引、问答契约保持不变。
4. 用真实模型在 1 / 3 / 5 并发会话下重跑基准，记录：首 token 延迟、聚合 token 速率、转录进行时的语音首包延迟。
5. 本 Demo 不得使用真实家庭资料。用虚构测试资料，或另建虚构语料，直到某户书面授权试点。

### English

1. Clone this repo onto the Mac mini. Confirm the machine first: Mac mini (confirmed 2026-10-30 — not a Mac Pro tower, not a Mac Studio). Record chip, memory, and SSD; the planning baseline is M4 Pro, 48 GB.
2. Run the tests and the CLI exactly as above. They must pass unchanged.
3. Replace the three adapters only (`drive.py` source, `transcribe.py` model, `qa.py` model), keeping tenant, store, and QA contracts.
4. Re-run the benchmark with the real model at 1 / 3 / 5 concurrent sessions and record: time-to-first-token, aggregate tokens/second, and first-voice-packet latency while transcription runs.
5. Do NOT use real household data for this demo. Use the fictional fixtures, or a separate fictional corpus, until a household gives written authorisation for a pilot.

## 验收标准 / Acceptance Criteria

### 中文

- [ ] `python3 -m unittest discover -s tests -v` 通过。
- [ ] `python3 -m demo.cli` 显示 5 个同步租户、1 份已复核转录、1 个冲突案例、1 个未知案例。
- [ ] 跨户查询测试通过（任何租户都看不到其他租户的块）。
- [ ] 删除测试通过（删除源文件后其块也被删除）。
- [ ] 1 / 3 / 5 并发会话的基准报告已生成。
- [ ] Demo 输出中没有任何真实家庭资料、没有任何云端调用、没有任何被说成 Mac mini 容量的数字。

### English

- [ ] `python3 -m unittest discover -s tests -v` passes.
- [ ] `python3 -m demo.cli` shows 5 synced tenants, 1 reviewed transcript, 1 conflict case, and 1 unknown case.
- [ ] Cross-tenant query test passes (no tenant sees another's chunks).
- [ ] Deletion test passes (removing a source file removes its chunks).
- [ ] Benchmark report is generated for 1 / 3 / 5 concurrent sessions.
- [ ] No real household data, no cloud call, and no claimed Mac mini capacity number appears anywhere in the demo output.
