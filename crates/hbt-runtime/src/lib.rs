//! ChronForge `hbt-runtime` — strategy runtime (scaffold Soft≠green).
//!
//! Module skeleton matches qstack catalog §4.2.
//! Depends on `hbt-engine` (path). Optional `abi` feature is empty Soft≠green.

#![forbid(unsafe_code)]

pub mod event;
pub mod source;
pub mod strategy;
pub mod runtime;
pub mod command;

#[cfg(feature = "abi")]
pub mod abi;

pub use hbt_engine as engine;

/// Scaffold crate identity Soft≠green (not a Runtime receipt).
pub const CRATE_NAME: &str = "hbt-runtime";
pub const SCAFFOLD_VERSION: &str = "0.0.0";
