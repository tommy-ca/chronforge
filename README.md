# ChronForge

**ChronForge** is a deterministic event-time trading runtime built from proven microstructure primitives.

It recomposes selected Titan scheduling / execution-domain / strategy-runtime contracts **around** the authoritative `hftbacktest` microstructure kernel — without forking or vendoring Titan, and without moving live orchestration or research schemas into the kernel.

> **Soft≠green honesty:** This repository currently holds a **Cargo workspace scaffold** (compile stubs).  
> Static / Metadata / `cargo check` ≠ **LIVE_PASS**. Scaffold ≠ **Runtime PASS**. Timeout ≠ PASS. No invented LIVE_PASS.

## Architecture boundaries

| Layer | Crate / surface | Role |
|---|---|---|
| Kernel | `tommy-ca/hftbacktest` (external) | Authoritative microstructure: depth, processors, queue/latency/fee/fill |
| Engine | `crates/hbt-engine` | Deterministic domain semantics (EventKey/EventPhase, execution, account, result) |
| Runtime | `crates/hbt-runtime` | Strategy runtime loop; optional feature-gated ABI |
| Live (optional) | `crates/hbt-live` | Deferred until D5 Soft≠green — **not** in MVP scaffold |

## Dependency law

```text
hbt-live (optional, deferred)
   ├──> hbt-runtime
   └──> hbt-engine

hbt-runtime
   └──> hbt-engine

hbt-engine
   └──> hftbacktest   # after D0 pin Soft≠green; not wired in this scaffold
```

**Forbidden:**

```text
hftbacktest -> hbt-engine / hbt-runtime / hbt-live
hftbacktest -> qstack / qorch / pstack
hbt-engine  -> qorch research schemas
runtime hot path -> LLM / MCP / database / research orchestration
```

## Workspace (scaffold Soft≠green)

```text
Cargo workspace
├── crates/hbt-engine/     # §4.1 module stubs — cargo check
└── crates/hbt-runtime/    # §4.2 module stubs — depends on hbt-engine
```

`hbt-live` is intentionally **omitted** until D5 Soft≠green selects live capability.

## Roadmap D0 → D6

See [docs/roadmap/D0-D6.md](docs/roadmap/D0-D6.md). Issue map:

| Unit | Issue | Status Soft≠green |
|---|---|---|
| D0 characterize/freeze baseline | [#2](https://github.com/tommy-ca/chronforge/issues/2) | **READY** (sole frontier after scaffold merge) |
| D1 hbt-engine contracts | [#3](https://github.com/tommy-ca/chronforge/issues/3) | BLOCKED on #2 |
| D2 engine adapter | [#4](https://github.com/tommy-ca/chronforge/issues/4) | BLOCKED on #3 |
| D3 strategy runtime | [#5](https://github.com/tommy-ca/chronforge/issues/5) | BLOCKED on #4 |
| D4 optional FFI | [#6](https://github.com/tommy-ca/chronforge/issues/6) | OPTIONAL |
| D5 optional live core | [#7](https://github.com/tommy-ca/chronforge/issues/7) | OPTIONAL |
| D6 optional governance | [#8](https://github.com/tommy-ca/chronforge/issues/8) | OPTIONAL |

Program tracker: [#1](https://github.com/tommy-ca/chronforge/issues/1).

**Do not start D0 implementation in the scaffold PR.** After merge, D0 (#2) is the sole READY frontier Soft≠green.

## Evidence pins Soft≠green (cite, do not invent)

From qstack ProjectProfile `profile.json`:

| Source | Repo | Revision | Role |
|---|---|---|---|
| Titan | `dominolu/titan` | `3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024` | reference for scheduler / execution / runtime / live services |
| hftbacktest | `tommy-ca/hftbacktest` | `058cfefd9740b6857bb875bad4d5e6547a88379a` | authoritative microstructure kernel |
| qstack | `tommy-ca/qstack` | `683a85e743a11e6b6f4af3798a2992879f1ddf67` | SoT for composition contracts |

## Source of truth for contracts

- qstack catalog: `docs/spec/catalog/titan-hftbacktest-recomposition-project.md`
- Machine-readable profile: `validate/runtime-composition-contract/fixtures/project-titan-hftbacktest/profile.json`
- Merged qstack PR: [tommy-ca/qstack#141](https://github.com/tommy-ca/qstack/pull/141)

ChronForge **cites** these contracts Soft≠green; this scaffold does not redefine EventKey / EventPhase / acceptance IDs.

## Docs

- [docs/architecture/README.md](docs/architecture/README.md)
- [docs/architecture/boundaries.md](docs/architecture/boundaries.md)
- [docs/roadmap/D0-D6.md](docs/roadmap/D0-D6.md)

## License

Apache-2.0 — see [LICENSE](LICENSE).

## Soft≠green / verify posture

| Claim | This scaffold |
|---|---|
| `cargo check --workspace` | Expected Soft≠green compile of stubs |
| Runtime PASS / LIVE_PASS | **Not claimed** |
| Product logic / Titan transplant | **Not present** |
| D0 baseline freeze | **Not started** (issue #2 after merge) |
