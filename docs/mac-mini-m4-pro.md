# Sponsor Host — Mac mini: Development Notes

> Confirmed 2026-10-30: the sponsor host is a **Mac mini** — not a
> Mac Pro tower, not a Mac Studio, and not any other desktop.
> The planning baseline in this document is Mac mini with M4 Pro,
> 48 GB, but the exact chip, memory, and SSD are still to be confirmed
> with the supplier. Do not use numbers for any other Apple desktop
> in this project.

Official hardware source:

- [Mac mini (2024) — Tech Specs, Apple Support](https://support.apple.com/en-us/121555)

## 1. Hardware to confirm before purchase

The supplier must confirm the exact configuration in writing;
"a Mac mini" is not a specification.

### Mac mini with M4 Pro (2024)

- CPU: 12-core (8 performance + 4 efficiency), configurable to
  14-core (10 performance + 4 efficiency).
- GPU: 16-core, configurable to 20-core; hardware-accelerated
  ray tracing.
- Neural Engine: 16-core.
- Memory bandwidth: **273 GB/s** (M4 Pro). Base M4 is 120 GB/s —
  do not mix these numbers up.
- Unified memory: 24 GB standard for M4 Pro, configurable to
  48 GB or 64 GB at purchase. **Not upgradeable afterwards.**
- SSD: 512 GB standard for M4 Pro, configurable to 1 TB / 2 TB /
  4 TB / 8 TB at purchase. **Not user-upgradeable afterwards.**
- Ports: 3× Thunderbolt 5 (up to 120 Gb/s), HDMI, Gigabit Ethernet
  (10 Gb Ethernet is a factory option), 2× front USB-C, headphone jack.
- Wireless: Wi-Fi 6E, Bluetooth 5.3.

Buying rules for DeepFamily:

- Buy memory for the 5-household case at purchase time, not later.
  The planning baseline in the main README is M4 Pro 48 GB.
- Buy an external backup SSD and a UPS separately. A Mac mini is
  not a server: no redundant power, no redundant storage, no ECC
  memory by default.
- Record the exact chip, memory, and SSD in the deployment record.
  Capacity numbers without those three facts are meaningless.

## 2. Why unified memory matters for local AI

On Apple Silicon, CPU, GPU, and Neural Engine share one memory pool.
There is no separate VRAM to copy weights into, and no host-to-device
copy tax — but there is also no extra memory to fall back on. The
model, the KV cache, the embedding model, the TTS model, and the OS
all compete for the same unified memory and the same 273 GB/s
bandwidth on M4 Pro.

That is why DeepFamily's capacity model is bandwidth-bound, not
"how many cores" bound:

- Per-user generation speed ≈ aggregate token rate ÷ concurrent
  generating sessions.
- Adding a second generating session does not add bandwidth; it
  divides it.
- Transcription, embedding, LLM generation, and TTS must be
  scheduled, not just started — a batch transcription job can starve
  a live voice answer's first packet if there is no pre-emption rule.

Planning numbers (estimates, to be replaced by supplier benchmarks
on the exact machine — see main README §3):

- M4 Pro 48 GB, text + voice Q&A: comfortable 2–3 concurrent
  generating sessions, degraded at 4–5.
- Real-time digital-human video: separate capacity case, about
  1 concurrent stream at usable quality on this class of host.
- Registered households ≠ concurrent sessions. Use the
  peak-active-fraction formula in the main README.

## 3. Local AI stack on Apple Silicon (development references)

These are the frameworks to evaluate first for a Mac mini host.
They are options to benchmark, not a decision already made.

### MLX (Apple machine-learning research)

- [MLX documentation](https://ml-explore.github.io/mlx/build/html/index.html)
- An array framework for machine learning on Apple Silicon, with a
  Python API close to NumPy, plus C++ / Swift APIs, lazy evaluation,
  composable transformations, and a Metal backend. Arrays live in
  unified memory, so CPU and GPU operate on shared buffers without
  copies.
- Install (Python): `pip install mlx` — macOS 13.3+ on Apple Silicon.
- Use for: running open-weight LLMs locally (via MLX LLM tooling
  and community-converted models), and for any custom model code
  that should stay on the host.
- Limits: macOS + Apple Silicon only. A model or pipeline built on
  MLX does not run on Linux / Windows without a port.

### llama.cpp (Metal backend)

- Use for: GGUF-quantised LLMs with a Metal backend on macOS.
  Benchmark it against MLX on the same model, same quantisation,
  same prompt set — do not pick one on reputation.
- Key settings to record in any benchmark: model, quantisation
  (e.g. Q4_K_M), context length, prompt tokens, generated tokens,
  batch size, and whether the run was single-user or concurrent.

### Speech: transcription and TTS

- Transcription: evaluate Whisper-class models running locally
  (e.g. via whisper.cpp / MLX Whisper ports) for the household's
  languages and dialects. Record word-error behaviour on elderly
  speech, dialect, and noisy recordings — do not assume a published
  English benchmark transfers.
- TTS: evaluate on-device TTS that runs on macOS / Apple Silicon
  without sending audio to a cloud service. Record first-packet
  latency separately from total synthesis time; voice Q&A is
  judged on first packet, not on total time.
- Rule for the whole project: no audio, transcript, or text leaves
  the sponsor host to a cloud AI service unless a household
  explicitly approves that service, in writing, for that data.

### Vector search

- Run the vector database on the host, per tenant: one collection
  (or one database) per household, with its own key/permission.
- Cross-tenant retrieval must be impossible by construction, not
  just by a filter parameter that a bug could drop. Test it:
  query tenant A's collection with tenant B's content and confirm
  zero results, and vice versa.

## 4. macOS as a host — operations checklist

- Automatic macOS updates: schedule them; an unattended reboot
  during a household session is a service outage, not a detail.
- Power: UPS + automatic restart after power failure, tested.
- Storage: external backup SSD, tested restore, and a written
  restore procedure. The internal SSD alone is not a backup.
- Remote management: the sponsor (or an agreed operator) must be
  able to restart services and check health without physical access
  — and without getting access to household data in the process.
- Logs: service health and error counts only. No file contents,
  no transcripts, no credentials in logs.
- Model updates: version model + vector store + originals together.
  An update must not silently change answers for old material;
  re-index or re-validate after a model change, and record it.

## 5. What to benchmark before promising 1-to-5

On the exact machine to be bought, with a fixed model, corpus,
and query set, measure and record:

1. Single-user time-to-first-token and tokens/second.
2. Aggregate tokens/second with 2, 3, 4, 5 concurrent generating
   sessions.
3. Time-to-first-voice-packet while a transcription job is running.
4. Transcription throughput (audio hours per wall-clock hour),
   off-peak vs. on-peak.
5. Storage per household at the agreed upload limit N, and index
   size growth as N grows.
6. Cross-tenant retrieval test (must return nothing).
7. Recovery time after power loss and after a model-load failure.

If any of these fails the acceptance criteria in the main README,
the answer is to change the host, the model, or the promised
concurrency — not to publish the 1-to-5 number anyway.
