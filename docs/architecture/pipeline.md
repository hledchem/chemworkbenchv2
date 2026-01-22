# Architecture: Pipeline (Linear, DAG-Ready)

The pipeline is currently linear, but designed to evolve into a DAG without breaking the architecture.

## Linear Pipeline (Current)

raw → step1 → step2 → step3 → processed

- Steps defined in config
- Each step calls a pure math function
- Processors may add technique-specific transforms
- Intermediates stored for future DAG expansion

## DAG-Ready Design

The pipeline stores:

intermediates = { "baseline": ..., "smooth": ..., "normalize": ... }

This enables:

- branching
- multi-output transforms
- caching
- parallel execution

Future DAG config example:

{ "graph": { "nodes": [...], "edges": [...] } }


## Why Linear First

- Simpler
- Faster to implement
- Matches most spectroscopy workflows
- DAG can be added later without rewriting processors or math

