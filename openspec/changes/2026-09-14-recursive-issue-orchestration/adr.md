# ADR review: recursive issue orchestration

No new repository ADR is required.

ADR-0001 already establishes the durable ownership split between OpenSpec, qstack, pstack, ChronForge and qorch. H2 applies that decision recursively to issue execution and adds a derived orchestration-record schema.

If a future change makes a specific external orchestration engine or persistent pstack/orchestrate state mandatory to build ChronForge, that would be a new durable dependency decision and would require an ADR. H2 explicitly does not do that.
