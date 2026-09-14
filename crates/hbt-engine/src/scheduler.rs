//! EventPhase, EventKey, deterministic scheduler (stub Soft≠green).
//!
//! Cite qstack catalog §6 — do not invent new contracts Soft≠green.
//!
//! EventKey fields (lexicographic order authoritative):
//!   timestamp, phase, source_priority, venue_no, asset_no, sequence
//!
//! Versioned same-timestamp phase contract (phase_contract_version = 2):
//!   10 OldResponseDelivery
//!   20 ExchangeState
//!   30 MarketDelivery
//!   40 StrategyCallback
//!   50 CommandArrival
//!   60 Matching
//!   65 PostMatchingSettlement
//!   70 ZeroLatencyResponse
//!   80 Timer
//!   90 PostTradeRisk

/// Placeholder scheduler marker Soft≠green.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct SchedulerStub;
