//! ChronForge `hbt-engine` — deterministic domain semantics (scaffold Soft≠green).
//!
//! Module skeleton matches qstack catalog §4.1.
//! No product logic yet; stubs must `cargo check`.
//!
//! Dependency law: this crate MAY depend on `hftbacktest` after D0 pin Soft≠green;
//! never reverse (`hftbacktest` must not depend on this crate).

#![forbid(unsafe_code)]

pub mod domain;
pub mod scheduler;
pub mod execution;
pub mod account;
pub mod funding;
pub mod risk;
pub mod result;
pub mod adapters;

/// Scaffold crate identity Soft≠green (not a Runtime receipt).
pub const CRATE_NAME: &str = "hbt-engine";
pub const SCAFFOLD_VERSION: &str = "0.0.0";
