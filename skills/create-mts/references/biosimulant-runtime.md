# Biosimulant Runtime Contract Snapshot

This reference records implementation facts relevant to specification work. It was
verified against the unreleased Biosimulant source on 2026-09-10. When the code is
available, inspect the current revision and treat it as authoritative over this
snapshot.

## Runtime model

- `BioModule` is the single runnable component contract. New finite and temporal
  modules override `execute(inputs, *, context)` and explicitly select
  `ExecutionPolicy.ONCE_BEFORE_RUN`, `ExecutionPolicy.EACH_WINDOW`, or
  `ExecutionPolicy.ONCE_AFTER_RUN`. Never quote uppercase member names; accepted
  literal values are lowercase. Existing temporal modules
  may retain `advance_window(start, end)`. A module cannot implement both hooks.
- `ExecutionContext` carries the public run bounds and, for `ExecutionPolicy.EACH_WINDOW`, the
  positive window bounds. BioWorld owns canonical output validation, signal
  construction, and boundary timestamps; direct execute calls do not update the
  committed-output cache.
- `SignalEmitterBioModule` centralizes typed output publication. `StatefulBioModule` supplies fixed internal stepping, state/history hooks, optional initial and zero-window publication, and bounded history. Components with unusual solver or timing semantics can implement `BioModule` directly.
- `BioWorld` drains ready before-run modules, advances each-window modules with
  atomic commits, then drains after-run modules. Once graphs use deterministic
  dependency layers. Within one temporal boundary, a newly emitted value moves
  only one acyclic edge because all `EACH_WINDOW` inputs are read before the
  atomic commit; temporal cycles retain the same next-window semantics.
- `BioWorld.settle(steps)` remains opt-in zero-time propagation for legacy temporal
  modules. Canonical modules do not run during settle in 0.0.26.
- On `biosimulant>=0.0.27`, Lab JSON results preserve terminal typed signals at
  `outputs.<module-alias>.<port>`. A managed design must retain that result file
  as a checksummed artifact and declare which terminal ports satisfy acceptance.
- Runs support progress events, pause/resume, cooperative stop, and world snapshot/restore. Snapshot reliability still depends on every stateful module implementing compatible serializable state.

## Signals and ports

- Port declarations use `SignalSpec`; runtime values use `ScalarSignal`, `ArraySignal`, `RecordSignal`, or `EventSignal`.
- Scalar, array, and record signals are state signals. Event signals have event kind and no interpolation. Values and specs must be JSON-serializable for transport; arrays also declare shape and normally dtype, while records with a schema require exactly its declared keys.
- Outputs declare the emitted signal type, dtype/shape or schema, optional emitted unit, interpolation, and description. Inputs may declare one or more `AcceptedSignalProfile` values, accepted units, freshness (`max_age`), and stale handling (`ignore`, `warn`, or `error`). Inputs cannot declare `emitted_unit`; outputs cannot declare accepted profiles.
- A record envelope does not erase the physical unit of the scientific quantity it carries. Preserve that unit at signal level for single-quantity records. Use unit `1` only for genuinely dimensionless records or mixed terminal reports whose schema documents field-level units and which are not wired as a single physical quantity.
- A connection is accepted only when state/event kind matches and an input profile accepts the source signal type, dtype, shape/schema, and emitted unit. The runtime validates compatibility; it does not perform unit conversion.
- Initial inputs are coerced against declared profiles. Ambiguous multi-profile inputs require a typed envelope including enough type, shape/schema, dtype, and unit information to select one profile.
- Event delivery is edge-like: a connection does not redeliver the same event timestamp. State signals retain their most recently committed value subject to freshness policy.

## Models, Labs, and packages

- A model source tree has `model.yaml` (or the accepted legacy `biosim.yaml`) with a `biosim.entrypoint` resolving to a `BioModule`. The implementation also consumes initialization/setup, communication-step, dependency, runtime, and package identity metadata when present.
- On `biosimulant>=0.0.33`, `model.yaml` may repeat the class policy as `biosim.execution_policy` (`once_before_run`, `each_window`, or `once_after_run`) so tools that cannot import model code can tell when it runs. The Python attribute stays authoritative: loading fails when the declaration disagrees with the constructed module, and `biosimulant labs validate` fails when the source provably disagrees and warns when it cannot verify the value. `advance_window()` modules and `execute()` modules that set no policy resolve to `each_window`; omit the field when `__init__` chooses the policy from a constructor parameter. A Lab cannot override a model's policy.
- A Lab has `lab.yaml` with stable model aliases, a `models` list of path-based model trees, a `wiring` list using `alias.port`, and a `runtime` mapping. A runnable Lab needs a positive `runtime.communication_step`; duration and non-negative `settle_steps` control execution.
- A Lab whose models all declare a run-once policy is `finite`; any `each_window` model makes it `temporal`, and otherwise any undeclared model makes it `unknown`. Studio, Desktop, and `biosimulant labs serve` hide duration, communication step, and settle steps for finite Labs, but `runtime.communication_step` stays required and duration must stay positive. Wiring may only move forward through phases (before-run to any phase, each-window to each-window or after-run, after-run to after-run), with no cycles among run-once modules; `labs validate` reports violations between declared models. A world with no each-window modules crosses the run in one step.
- Each custom model manifest independently needs `biosim.entrypoint` and a positive `biosim.communication_step`; the Lab-level communication step does not replace this model-level field. Every canonical wiring entry uses a non-empty `to` list of exact destination `alias.port` strings, even for one destination; fan-out adds further destinations to that list.
- Lab `io.inputs` and `io.outputs` may expose public names mapped to internal `alias.port` references. Run overrides map public or dotted input names to model-local inputs without mutating the saved Lab.
- Labs may contain child Labs by local path or by exact `package` plus `version`. Child public I/O is remapped while the tree flattens to scoped aliases. Circular references are rejected and nesting is limited to five levels.
- Package-backed children require `biosimulant.lock` with lock version 1, exact package/version entries, and artifact SHA-256 values. Dependencies are materialized into Lab-owned state and validated against registry and downloaded checksums.
- `.bsilab` and `.bsimpkg` lab archives include normalized manifests and integrity checks. Packaging validates paths, manifests, exact dependency constraints where required, checksums, runtime compatibility, and embedded models/Labs.
- Current canonical CLI surfaces include `biosimulant labs validate`, `biosimulant labs run`, `biosimulant labs serve`, `biosimulant labs package`, and `biosimulant labs release`. Older `biosimulant pack` and `biosimulant packages` commands are removed.

## Adapters and presentation

- `OnnxClassifierModule` runs frozen ONNX inference behind typed array/record ports. The ONNX artifact and native inference semantics remain authoritative; parity and provider/determinism constraints belong in the MTS.
- `TelluriumSBMLBioModule` wraps SBML with a Tellurium runner, exposed parameter/initial-condition inputs, state/summary/trajectory outputs, snapshots, and numerical behavior. SBML remains authoritative and adapter tests must cover units, observables, parameters, solvers, and tolerances.
- `LibCellMLBioModule` compiles and runs CellML through libCellML-generated Python. CellML remains authoritative; code-generation/runtime versions, cached artifacts, algebraic solver needs, and native parity require locking.
- `VisualSpec` is a renderer-neutral JSON object with `render`, `data`, and optional `description`. Supported consumers may render timeseries, bars, tables, images, graphs, structures, text, or a fallback; scientific meaning must not depend on presentation alone.

## Fit and evidence boundary

- **Native fit** is appropriate when typed temporal or finite composition, wiring,
  snapshots, scenarios, inspection, or common execution surfaces provide material
  value.
- **Adapter fit** keeps a domain-native artifact authoritative and adds a frozen typed wrapper with declared parity tolerances and limitations.
- **External boundary** keeps the core workflow in its proper runtime and versions only a useful exchange, scoring, import/export, or inspection boundary.
- **Not suitable** records the better stack and a reassessment trigger when Biosimulant adds no justified value.

Biosimulant validates technical contracts, packaging, and execution. It does not establish that a scientific mechanism is correct, an estimator is identifiable, a prediction generalizes, a generated candidate is useful, or an MRS acceptance criterion has been met.
