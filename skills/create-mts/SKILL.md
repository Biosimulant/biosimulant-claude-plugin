---
name: create-mts
description: Create or revise a Modeling Technical Specification (MTS) that implements an approved Model Requirements Specification for a biological or computational model. Use when defining architecture, methods, interfaces, verification, reproducibility, delivery, Biosimulant fit, and operations; do not use to invent or weaken MRS acceptance requirements.
metadata:
  version: "2026.09.12.5"
---

# Create MTS

Translate an approved MRS into a traceable implementation contract. The MTS explains how the requirements will be satisfied; it does not replace, reinterpret, or weaken them.

## Gate and ground the work

1. Locate the MRS and verify its identifier, version, `Approved` status, approvals, and mandatory requirements. A full MTS requires an approved, versioned MRS. If the MRS is Draft, In review, missing, or materially inconsistent, produce only a gap analysis or clearly non-authoritative skeleton and stop before calling it a completed MTS.
2. Read [references/suite-lifecycle.md](references/suite-lifecycle.md) and [references/mts-suite-guidance.md](references/mts-suite-guidance.md).
3. Inspect relevant code, manifests, environments, model artifacts, data/partition manifests, tests, operational constraints, and native scientific runtimes before choosing the architecture.
4. Classify every component by model job. Read only the matching example reference(s):
   - predictive or ML: [references/examples/predictive-ml.md](references/examples/predictive-ml.md)
   - mechanistic: [references/examples/mechanistic.md](references/examples/mechanistic.md)
   - generative: [references/examples/generative.md](references/examples/generative.md)
   - optimization: [references/examples/optimization.md](references/examples/optimization.md)
   - simulation or digital twin: [references/examples/digital-twin.md](references/examples/digital-twin.md)
   - statistical estimation: [references/examples/statistical-estimation.md](references/examples/statistical-estimation.md)
   Read every applicable example for a hybrid model, without carrying over illustrative thresholds or claims.
5. Read [references/biosimulant-runtime.md](references/biosimulant-runtime.md) before making a Biosimulant fit decision or specifying a Biosimulant implementation. When the referenced repository is available, inspect it and treat the current code as authoritative over the snapshot.

Prefer evidence over questions. Ask only about design decisions, operational constraints, or ownership that cannot be derived from the approved MRS and project artifacts. Never invent scientific evidence, approvals, parity tolerances, resource budgets, or validation results.

## Create or revise

For a new MTS, read [assets/master-template.md](assets/master-template.md) and
draft a working copy in the conversation. Preserve the master template. This
Claude package does not run local helpers or code; store a requested document
through the declared Biosimulant connection after exact change approval.

For a revision, preserve the MTS identifier lineage, update version/date/revision history, record the decision and alternatives, assess MRS impact and revalidation impact, and keep prior evidence traceable. If the intended use or any MRS-controlled requirement changes, return the issue to the MRS owner instead of changing it in the MTS.

When working through the Biosimulant Agent Gateway, draft and validate the MTS with this skill, then submit its contents through `technical_spec_set` in `workspace_change_prepare`. The Gateway commit is an immutable storage revision, not approval of the MTS or satisfaction of the MRS. Show the prepared diff and digest before `workspace_change_apply`, and preserve the document's own review state and traceability.

## Build the traceable design

- Include every mandatory MRS identifier in the traceability matrix. Map it to a component or design decision, test or validation protocol, evidence artifact, accountable owner, and the original acceptance criterion.
- Use stable `MTS-*`, component, data, and test identifiers. Derived technical requirements must name their source MRS requirement.
- Preserve scientific meaning, units, ranges, time bases, coordinate systems, uncertainty, and failure semantics across every boundary.
- Separate authoritative scientific artifacts from adapters, packages, and presentation layers. Lock data, preprocessing, equations/architecture, parameters/weights, thresholds, environments, schemas, adapters, validation protocols, and analysis plans before locked validation.
- Define invalid input, out-of-domain, nonidentifiable, infeasible, abstention, and execution-failure behavior with machine-readable status and safe user interpretation.
- Include unit, interface, data/leakage, scientific-behavior, numerical, regression, integration, robustness, performance, reproducibility, and acceptance tests as applicable.
- Distinguish verification evidence from scientific validation evidence. A package that validates and runs may still fail the MRS.

## Decide Biosimulant fit

Choose exactly one outcome and justify it with evidence:

- **Native fit:** typed composition, whether temporal or finite, materially benefits
  the model. Retain the Biosimulant realization section.
- **Adapter fit:** the native scientific artifact remains authoritative while a frozen wrapper adds composition, inspection, packaging, or delivery value. Retain realization and specify native-runtime parity tests.
- **External boundary:** the core belongs in another runtime, with only a versioned exchange/import/export/scoring boundary if useful. Retain external delivery and do not wrap the core for uniformity.
- **Not suitable:** another stack is clearer and safer for the standalone work. Retain external delivery, reproducibility controls, and a reassessment trigger.

Only native and adapter fits require `BioModule`, `BioSignal`, `BioWorld`, model/Lab manifests, packaging, and Biosimulant execution details. Delete the conditional section that does not apply.

For a Biosimulant realization, map intended behavior explicitly:

- new settle-independent temporal state evolution -> canonical
  `execute(inputs, *, context)` with explicit `ExecutionPolicy.EACH_WINDOW` and context window
  boundaries;
- finite preprocessing/inference -> the same signature with `ExecutionPolicy.ONCE_BEFORE_RUN`;
- final analysis/export -> the same signature with `ExecutionPolicy.ONCE_AFTER_RUN`;
- finite AI computation against evolving state -> the same signature with
  `ExecutionPolicy.EACH_WINDOW`;
- imported or settle-dependent temporal behavior -> retain the supported
  `advance_window()` compatibility hook and justify why it is needed.

Do not implement both hooks, generate the unreleased one-argument execute method,
infer policy from internal solver iterations, or add manifest execution-mode
fields. Specify phase-edge validation, connected-input readiness, context and
output-boundary timestamps, settle participation, invocation-count tests, and
native-runtime parity as applicable.

Account for dependency timing explicitly. In an `EACH_WINDOW` graph, atomic
commits mean newly emitted data traverses one acyclic edge per communication
boundary. Use deterministic before/after-run dependency layers for finite batch
pipelines that must drain in one run when that matches the intended semantics;
otherwise specify and test the latency. Preserve the physical unit of the
primary scientific quantity across record ports instead of treating every JSON
record as dimensionless. Require acceptance against the primary public terminal
output's count, timestamps, units, and values.

Convergence and numerical-accuracy tests must execute the declared step sizes,
derive approximations and errors, and apply the stated tolerance. A test that
ignores `dt` or code that hardcodes expected errors, endpoints, references, or
pass flags is invalid evidence.

Specify the enum import with the implementation. Never quote uppercase enum
member names. If a string literal is required, use only the exact lowercase
runtime values `once_before_run`, `each_window`, or `once_after_run`.

Specify every model runtime package as an exact reproducibility pin using
`name==version`. Do not write compatible ranges or bare package names in
`runtime.dependencies.packages`; Biosimulant managed validation rejects them.

## Validate

Review the document against [assets/master-template.md](assets/master-template.md),
the authoring rules, and the source evidence. Check required sections, identifiers,
traceability, unresolved items, approval state, and unchanged acceptance criteria.
Use available server validation through the declared connection. Do not run local
validators or claim a validator passed without returned evidence. A semantic
review is separate from scientific validation.

After the last implementation or evidence correction, reread the entire MRS and
MTS rather than only the edited section. Reconcile all repeated runtime bounds,
time conversions, units, parameter/override exposure, source-mutation statements,
dependency availability, test status, and approval language with the executable
artifacts and the evidence actually produced. Reject stale narrative even when
both structural validators exit zero; compilation or import success must never
be described as executed scientific acceptance evidence.

Do not submit or describe a full MTS as approval-ready while the review
finds any error, missing required section, missing mandatory MRS mapping, or
unapproved MRS. Correct the document and repeat the review first. If the user has explicitly authorized approval of the MRS, record
that approval and its receipt in the MRS before completing and reviewing the
MTS; otherwise stop at the non-authoritative skeleton or gap analysis.


## Visualization deliverables

Before authoring, call `get_biosimulant_authoring_contract` with topic `visualization`.
The complete catalog contains timeseries, bar, scatter, heatmap, graph, table, image,
structure3d and text, including payload examples, limits and retained artifact rules.
Almost every scientific Lab needs a useful visual of actual computed outputs; choose
the type by the user's question rather than always emitting a table. Record expected
views, source outputs, units and caveats in the MRS; record render/schema, owning module,
typed wiring, lifecycle, artifact retention and executable checks in the MTS.
Implement reusable `BioModule.visualize()` and declare `lab.yaml` visualization requirements
(or a justified opt-out for infrastructure-only work). Inspect actual composed results,
check plotted values against typed outputs, and verify artifacts and reopening. Missing
or invalid required views block qualification/publication. Ad-hoc Studio chat charts
do not satisfy this contract. Historical Labs without a declaration remain compatible.
