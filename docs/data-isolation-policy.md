# 家庭与赞助家庭的数据隔离策略 / Household vs Sponsor Data Isolation Policy

> 核心原则 / Core principle：赞助算力 ≠ 赞助方访问权。赞助家庭提供主机，不因此获得任何受支持家庭的资料访问权。
> Sponsor compute ≠ sponsor access. A sponsor family provides the host and gains no access to any supported household's data by doing so.
>
> 适用范围 / Scope：本策略覆盖 demo 代码（`demo/demo/isolation.py`）和真实部署必须遵守的同一规则。demo 用虚构资料验证规则；真实部署替换加密实现时，规则不变。
> This policy covers both the demo code (`demo/demo/isolation.py`) and the rules a real deployment must follow. The demo verifies the rules with fictional data; replacing the encryption implementation for production does not change the rules.
>
> 诚实边界 / Honest boundary：软件隔离不能独自对抗拥有主机 root 权限或物理接触的攻击者。第 8 节写明这一边界和缓解措施，不得把 demo 的隔离说成“赞助方在任何情况下都绝对看不到资料”。
> Software isolation alone cannot defeat an attacker with root access or physical access to the host. Section 8 states this boundary and its mitigations. Never describe demo isolation as "the sponsor can never see the data under any circumstances".

## 1. 角色 / Roles

### 中文

| 角色 | 身份 | 数据面权限 | 基础设施面权限 |
| --- | --- | --- | --- |
| 家庭成员 `household_member` | 某一户的成员，绑定一个 `tenant_id` | 只能读 / 写 / 复核自己那一户 | 无 |
| 赞助运营方 `sponsor_operator` | 提供主机的赞助家庭，以运营身份登录 | **无任何一户的数据面权限**，包括自己家庭以外的所有户 | 启动 / 停止服务、查看聚合健康状态、管理配额、做加密备份、轮换基础设施密钥 |
| 社区介绍方 `community_introducer` | 只负责介绍赞助方 | 无 | 无；只能看到介绍记录本身 |

关键规则：**同一个人、两个身份必须分开**。如果赞助家庭自己也想用家庭工作空间，它必须另外注册为一个普通租户（有自己的租户 ID 和自己的密钥），运营身份不会给它对该租户资料的任何额外权限。登录时用哪个身份，就只能做那个身份的事。

### English

| Role | Identity | Data-plane permission | Infrastructure-plane permission |
| --- | --- | --- | --- |
| Household member `household_member` | Member of one household, bound to one `tenant_id` | Read / write / review only that household | None |
| Sponsor operator `sponsor_operator` | The sponsor family, logged in as operator | **No data-plane permission for any household**, including households other than its own | Start / stop services, view aggregate health, manage quotas, make encrypted backups, rotate infrastructure keys |
| Community introducer `community_introducer` | Introduces the sponsor only | None | None; sees only the introduction record itself |

Key rule: **one person, two identities, kept separate**. If the sponsor family also wants a family workspace, it must register as an ordinary tenant (its own tenant ID and its own key). The operator identity grants no extra permission over that tenant's data. Whichever identity is used to log in determines what that session can do — nothing more.

## 2. 资料分级 / Data classification

### 中文

- **家庭内容**：文件、转录、问答、引用、向量。只属于该户，赞助方和社区方一律不可见。
- **家庭元数据**：文件名、文件标题、转录状态以外的业务信息。同样属于该户，赞助方不可见——文件名本身可能泄露信息，所以赞助方的运维视图里只出现匿名租户编号（如 `tenant_3`），不出现文件名。
- **运维元数据**：租户是否存在、服务是否运行、上次同步是否成功、存储总量、配额使用率。这是赞助方唯一可以看到的东西，且只能是聚合或按匿名租户编号呈现，不能反推内容。
- **审计日志**：谁、在何时、以什么身份、尝试访问哪一户、成功还是被拒绝。日志本身不记录任何家庭内容（不写问题原文、不写回答、不写文件内容）。

### English

- **Household content**: files, transcripts, Q&A, citations, vectors. Belongs to that household only; invisible to sponsor and community.
- **Household metadata**: file names, file titles, and other business information beyond transcript status. Also belongs to that household and is invisible to the sponsor — a file name alone can leak information, so the sponsor's operations view shows only anonymous tenant codes (e.g. `tenant_3`), never file names.
- **Operations metadata**: whether a tenant exists, whether the service is running, whether the last sync succeeded, total storage used, quota usage. This is the only thing the sponsor may see, and only in aggregate or per anonymous tenant code, never in a form that reveals content.
- **Audit log**: who, when, under which identity, attempted to access which household, and whether it was allowed or denied. The log itself records no household content (no question text, no answer, no file content).

## 3. 强制层 / Enforcement layers

### 中文

隔离不能只靠“约定不看”，必须四层同时成立，缺一层即视为未隔离：

1. **API 门禁**：每个数据函数先校验身份（`Principal`），再做任何事。赞助方调用数据函数时直接拒绝，不返回“空结果”来掩盖——拒绝本身要记入审计。
2. **路径隔离**：沿用 demo 已有的规则——数据路径只能由 `tenant_id` 构建，`..` 越界一律拒绝；没有全局索引、没有跨户回退。
3. **每户加密**：每户内容用该户自己的密钥密封（见第 5 节）。赞助方拿到备份文件也只能看到密文，无法解密。
4. **进程与会话隔离**：数据服务以每户独立的进程 / 沙箱运行（真实部署）；demo 层面用身份校验 + 独立目录模拟这一层。一次会话只能携带一个身份，不能在一次请求里“顺带”换身份。

### English

Isolation must not rest on "we agree not to look". All four layers must hold; missing one means not isolated:

1. **API gate**: every data function validates the identity (`Principal`) before doing anything. A sponsor calling a data function is denied outright, not handed an empty result to mask it — and the denial is audited.
2. **Path isolation**: the demo's existing rule — a data path can only be built from a `tenant_id`, `..` escapes are rejected, there is no global index and no cross-tenant fallback.
3. **Per-household encryption**: each household's content is sealed with that household's own key (see §5). A sponsor holding a backup file sees only ciphertext and cannot decrypt it.
4. **Process and session isolation**: in a real deployment the data service runs per household in a separate process / sandbox; the demo simulates this layer with identity checks plus separate directories. One session carries exactly one identity and cannot switch identities mid-request.

## 4. 赞助方允许 / 禁止清单 / Sponsor allow / deny list

### 中文

允许（基础设施面）：查看服务运行状态；查看聚合存储与配额；启停服务；做**加密**备份；轮换基础设施密钥；查看审计日志的“被拒绝尝试”统计（不含内容）。

禁止（数据面，一律拒绝并审计）：读取、搜索、导出任何一户的文件、转录、问答或向量；以任何理由“代家庭”复核转录；查看文件名、问题或回答；删除、修改任何一户的资料；用自己的运营身份访问自己家庭租户的资料（必须用该租户的家庭成员身份另行登录）；把备份解密、或把备份交给第三方解密。

### English

Allowed (infrastructure plane): view service health; view aggregate storage and quotas; start / stop services; make **encrypted** backups; rotate infrastructure keys; view statistics of denied attempts in the audit log (no content).

Denied (data plane — always refused and audited): reading, searching, or exporting any household's files, transcripts, Q&A, or vectors; "reviewing" a transcript on a household's behalf for any reason; viewing file names, questions, or answers; deleting or modifying any household's data; accessing the sponsor family's own tenant data under the operator identity (it must log in separately as a household member of that tenant); decrypting a backup, or handing a backup to a third party to decrypt.

## 5. 密钥归属 / Key custody

### 中文

- 每户一个独立密钥，由该户的口令派生（demo：PBKDF2-HMAC-SHA256），不存放在主机上的明文文件里；每次调用时由该户提供，不持久化。
- 赞助方不持有任何一户的密钥，也不持有可以推导出户密钥的主密钥。主机上没有“一把万能钥匙”。
- demo 的密封算法（HMAC 计数器模式流 + HMAC 标签）只是演示级实现：它验证“没有户密钥就打不开”，但**不是生产加密**。真实部署必须换成标准 AEAD（如 AES-GCM / XChaCha20-Poly1305，配合 libsodium 或系统密钥库），并由该户设备持有的密钥或该户控制的 KMS 管理——不能只放在主机本机的钥匙串里，否则有 root 权限的运营方仍可能提取。
- 密钥轮换：换密钥时用新密钥重密封该户内容，旧密钥销毁；轮换不得由赞助方单方面发起，必须有该户确认记录。

### English

- One independent key per household, derived from that household's passphrase (demo: PBKDF2-HMAC-SHA256), never stored as plaintext on the host; supplied per call by the household and never persisted.
- The sponsor holds no household key and no master key from which a household key could be derived. There is no "one master key" on the host.
- The demo sealing algorithm (HMAC counter-mode stream + HMAC tag) is demonstration-grade only: it proves "it cannot be opened without the household key", but it is **not production encryption**. A real deployment must use a standard AEAD (e.g. AES-GCM / XChaCha20-Poly1305 via libsodium or a system keystore), with keys held on the household's device or in a KMS the household controls — not only in the host's local keychain, where an operator with root access could still extract them.
- Key rotation: re-seal that household's content under the new key and destroy the old key; rotation must not be initiated unilaterally by the sponsor — it needs a confirmation record from the household.

## 6. 审计 / Audit

### 中文

- 每次数据访问和每次被拒绝，都写入审计日志：时间、身份种类、匿名租户编号、操作、允许 / 拒绝。**不写内容**。
- 日志用哈希链连接：每条记录包含上一条的哈希，本条哈希覆盖全部字段。修改或删除中间记录会使链校验失败（demo：`verify_audit()`）。
- 哈希链只能**发现**篡改，不能**阻止**拿到主机的运营方删掉整份日志。真实部署必须把审计副本同步到主机之外的只追加存储（或定期交给各户自己保存的副本），并在书面协议里写明审计责任。

### English

- Every data access and every denial is written to the audit log: time, identity kind, anonymous tenant code, operation, allowed / denied. **No content is written**.
- The log is hash-chained: each entry carries the previous entry's hash, and its own hash covers all its fields. Modifying or deleting a middle entry breaks chain verification (demo: `verify_audit()`).
- A hash chain can only **detect** tampering, not **prevent** an operator holding the host from deleting the whole log. A real deployment must also sync an audit copy to append-only storage outside the host (or to copies each household keeps), and the written agreement must state who owns audit responsibility.

## 7. 备份、删除与退出 / Backup, deletion, and exit

### 中文

- 备份只备份密文。赞助方可以执行备份、验证备份完整性，但不能解密、不能恢复到可读状态——恢复必须由该户用自己的密钥完成。
- 删除由该户发起：删除源文件后，其转录、向量和缓存必须在有限时间内一并删除（demo 已有删除传导）；赞助方不得单方面删除任何一户的资料。
- 退出时：赞助结束或某户退出，该户的资料导出和删除必须在约定流程内完成，不依赖赞助方超出约定流程的配合；加密备份副本在保留期结束后销毁，销毁记录写入审计。

### English

- Backups contain ciphertext only. The sponsor may run a backup and verify its integrity, but cannot decrypt it and cannot restore it to a readable state — restoration must be done by the household with its own key.
- Deletion is initiated by the household: deleting a source file must also delete its transcript, vectors, and caches within a bounded time (the demo already propagates deletion); the sponsor must not unilaterally delete any household's data.
- On exit: when sponsorship ends or a household withdraws, that household's data export and deletion must complete within the agreed procedure, without depending on sponsor cooperation beyond that procedure; encrypted backup copies are destroyed after the retention period, and the destruction is recorded in the audit log.

## 8. 威胁模型与诚实边界 / Threat model and honest boundary

### 中文

本策略防范的：误操作越权（运营方误点进家庭资料）、普通软件漏洞导致的跨户读取、备份文件外泄后被直接读取、日志或文件名泄露内容。

本策略**不能独自防范**的：拥有主机 root 权限或物理接触的运营方主动绕过软件控制（例如直接读内存、替换服务二进制、删日志）。缓解措施是组合，不是单点：户持有密钥（主机上无明文密钥）、密文备份、哈希链审计 + 主机外审计副本、书面协议与退出权、以及“赞助方家庭租户与运营身份分离”。

因此，对外说法必须是：“赞助方在正常运营中看不到家庭资料，且有审计和加密作为制约”，而不是“赞助方在任何情况下都绝对看不到”。任何把 demo 隔离说成绝对保证的说法都是过度声称。

### English

What this policy defends against: accidental overreach by the operator (clicking into household data), cross-tenant reads through ordinary software bugs, backup files leaking and being read directly, and content leaking through logs or file names.

What this policy **cannot defend against alone**: an operator with root access or physical access to the host who deliberately bypasses software controls (e.g. reading memory, replacing the service binary, deleting logs). Mitigations are a combination, not a single point: household-held keys (no plaintext key on the host), ciphertext backups, hash-chained audit plus an off-host audit copy, a written agreement with exit rights, and separation of the sponsor family's tenant identity from its operator identity.

So the outward claim must be: "in normal operation the sponsor cannot see household data, with audit and encryption as constraints" — not "the sponsor can never see it under any circumstances". Any claim that demo isolation is an absolute guarantee is an overclaim.

## 9. 验收测试 / Acceptance tests

### 中文

- [ ] 赞助方调用任何数据函数（问答、复核、读取、导出）都被拒绝，且拒绝记入审计。
- [ ] 赞助方以运营身份访问自己家庭租户的资料也被拒绝（必须换家庭成员身份）。
- [ ] 赞助方只能看到匿名租户编号和聚合运维状态，看不到文件名、问题、回答。
- [ ] 没有户口令，赞助方打不开任何一户的密封备份；口令错误时解密失败，不返回部分明文。
- [ ] 篡改审计日志中间一条记录，`verify_audit()` 校验失败。
- [ ] 家庭成员只能访问自己那一户；跨户访问被拒绝（demo 已有测试，隔离模块复用同一规则）。
- [ ] 删除一户源文件后，其转录、向量和缓存一并删除；赞助方不能单方面删除。

### English

- [ ] A sponsor calling any data function (Q&A, review, read, export) is denied, and the denial is audited.
- [ ] A sponsor accessing its own family's tenant data under the operator identity is also denied (it must switch to a household-member identity).
- [ ] A sponsor sees only anonymous tenant codes and aggregate operations status — no file names, questions, or answers.
- [ ] Without the household passphrase, a sponsor cannot open any household's sealed backup; a wrong passphrase fails decryption and returns no partial plaintext.
- [ ] Tampering with a middle audit entry makes `verify_audit()` fail.
- [ ] A household member can access only its own household; cross-household access is denied (the demo already tests this, and the isolation module reuses the same rule).
- [ ] Deleting a household source file also deletes its transcript, vectors, and caches; the sponsor cannot unilaterally delete.

## 10. 从 demo 到真实部署的替换清单 / Demo-to-production replacement list

### 中文

- 密封算法：demo 的 HMAC 流 → 标准 AEAD（AES-GCM / XChaCha20-Poly1305）。
- 密钥存放：demo 的“调用时提供、不持久化”→ 该户设备持有或该户控制的 KMS；主机钥匙串不能是唯一存放点。
- 审计：demo 的本地哈希链 → 本地链 + 主机外只追加副本。
- 进程隔离：demo 的身份校验 + 独立目录 → 每户独立进程 / 沙箱 / 容器，操作系统级用户隔离。
- 身份认证：demo 的 `Principal` 对象（调用方传入）→ 真实登录会话 + 令牌，服务端校验，不得信任客户端自报的身份。

### English

- Sealing algorithm: demo HMAC stream → standard AEAD (AES-GCM / XChaCha20-Poly1305).
- Key storage: demo "supplied per call, never persisted" → held on the household's device or in a KMS the household controls; the host keychain must not be the only copy.
- Audit: demo local hash chain → local chain + off-host append-only copy.
- Process isolation: demo identity checks + separate directories → per-household processes / sandboxes / containers with OS-level user separation.
- Authentication: demo `Principal` object (supplied by the caller) → real login sessions + tokens, verified server-side, never trusting a client-claimed identity.
