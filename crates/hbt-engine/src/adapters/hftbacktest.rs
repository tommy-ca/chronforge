//! Bridge existing local/exchange processors to canonical facts (stub Soft≠green).
//!
//! Hard Cargo dep on `hftbacktest` lands after D0 (#2) pin Soft≠green.
//! Do not vendor Titan. Do not clone hftbacktest into this tree.

/// Placeholder adapter marker Soft≠green.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct HftbacktestAdapterStub;
