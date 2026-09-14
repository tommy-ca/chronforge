//! Feature-gated optional foreign ABI (stub Soft≠green).
//! Enabled only with `--features abi`. Empty until D4 Soft≠green selects FFI.
//! Native layout remains authority Soft≠green (qstack A-ABI-001/002 when selected).

/// Placeholder ABI marker Soft≠green.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct AbiStub;
