DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Simulation Digital Twin MTS Example - CHO Fed-Batch Culture
Modeling Technical Specification: CHO Fed-Batch Predictive Digital Twin
This is an implementation-ready illustrative technical design for research process development. It is not an implemented twin, manufacturing control system, or report of achieved forecasts.
1. Document Control
Field
Value
MTS identifier
EX-MTS-DT-CHO-FEDBATCH-001
Version
1.0 example
Status
Illustrative, not approved for execution
MRS
EX-MRS-DT-CHO-FEDBATCH-001
Scientific owner
Upstream process development lead
Model owner
Bioprocess modeling lead
Technical owner
Scientific software lead
Validation owner
Process analytics lead
Biosimulant fit
Native fit

2. Technical Decision Summary
Implement the twin as a stateful multi-module Biosimulant Lab. A process module advances viable and nonviable cells, culture volume, extracellular metabolites, and product. A state-estimation module assimilates accepted daily measurements into an ensemble state. A scenario coordinator snapshots synchronized state and restores it into isolated forecast branches. Recorders emit traceable state, forecast, uncertainty, and failure outputs.

The twin uses a hybrid process model with mechanistic balances and frozen data-driven rate corrections. It is accepted on synchronization, forecast, scenario, numerical, and failure-handling evidence, not on whether every internal state has a unique biological interpretation.
3. Architecture
flowchart LR
    A["Batch initializer"] --> B["State estimator"]
    C["Measurement and process events"] --> B
    B --> D["Hybrid CHO process model"]
    D --> B
    B --> E["Scenario coordinator"]
    E --> F["Isolated forecast branches"]
    F --> G["Forecast recorder"]
    B --> H["Current-state recorder"]
Modules
Alias
Responsibility
State
Communication step
initializer
Validate batch identity, static attributes, recipe, initial state, and planned events
Initialization record
1 hour
events
Emit ordered feed, sample-removal, set-point, and measurement events
Event cursor
1 hour
estimator
Maintain 200 ensemble state members and assimilate accepted observations
Ensemble states and covariance
1 hour
process
Advance the hybrid cell, metabolite, volume, and product dynamics
Process state for each member
1 hour, with 0.25-hour internal integration
scenarios
Snapshot synchronized state and run the five allowed scenario definitions
Branch registry
On request at a communication boundary
recorder
Persist current state, forecasts, intervals, event lineage, and statuses
Append-only run record
1 hour

4. State, Events, and Model Method
State Vector
State
Unit
Constraint
Viable-cell density
10^6 cells/mL
Nonnegative
Nonviable-cell density
10^6 cells/mL
Nonnegative
Culture volume
mL
Positive and event-reconciled
Glucose
mmol/L
Nonnegative
Lactate
mmol/L
Nonnegative
Glutamine-equivalent substrate
mmol/L
Nonnegative
Ammonia
mmol/L
Nonnegative
Product titer
g/L
Nonnegative and nondecreasing before sampling correction
Latent rate corrections
rate-specific
Bounded by training-supported ranges

Hybrid Process Model
Deterministic base: material-balance ODEs for cells, substrates, products, culture volume, feed additions, and sample removals.
Data-driven correction: frozen bounded regressors for effective growth, death, uptake, production, and byproduct rates.
Input variables: current state, process set points, media and feed identifiers, and declared batch attributes.
Training: external, grouped by complete bioreactor run with the six latest eligible runs locked for testing.
Integration: adaptive stiff solver inside each one-hour communication window.
Ensemble: 200 members for state assimilation and 500 deterministic-resampled trajectories for each released scenario forecast.
State Assimilation
Use an ensemble Kalman filter with observation-specific error variances from assay qualification. Before assimilation:

Validate batch, timestamp, units, assay status, and event completeness.
Reconcile culture volume using additions and removals.
Reject or flag impossible rate-of-change observations without silent clipping.
Assimilate only accepted observations.
Project ensemble members back into the nonnegative and approved state domain.
Record prior, observation, innovation, posterior, and rejection status.

An observation is evidence with uncertainty, not an error-free replacement for the state.
Scenario Branching
At a synchronized communication boundary, create a versioned snapshot and restore it into separate branches for the reference schedule, six-hour feed delay, minus 10 percent feed, plus 10 percent feed when permitted, and no-further-feed stress case. Branches cannot write to the live twin state.
5. Input, Output, and Failure Contracts
Measurement Event
{
  "batch_id": "CHO_EXAMPLE_001",
  "observed_at": "2026-08-19T08:00:00Z",
  "measurement_set_id": "day03-lab-v1",
  "values": {
    "viable_cell_density": {"value": 7.2, "unit": "1e6_cell_per_mL"},
    "viability": {"value": 94.0, "unit": "percent"},
    "glucose": {"value": 4.1, "unit": "mmol_per_L"}
  },
  "quality_status": "accepted"
}
Forecast Record
{
  "batch_id": "CHO_EXAMPLE_001",
  "issued_at": "2026-08-19T08:05:00Z",
  "state_time": "2026-08-19T08:00:00Z",
  "synchronization_status": "synchronized",
  "model_version": "1.0.0",
  "scenario": "reference",
  "horizon_hours": 48,
  "forecasts": {
    "viable_cell_density": {"median": 10.4, "interval_80": [9.2, 11.7]},
    "product_titer": {"median": 0.81, "interval_80": [0.68, 0.95]}
  }
}

More than 30 hours without an accepted measurement returns STALE and no unqualified scenario recommendation.
An incomplete feed or sample-removal log returns EVENT_RECONCILIATION_REQUIRED.
An unsupported clone, media family, vessel scale, or process range returns OUT_OF_DOMAIN.
Failed assimilation leaves the last accepted snapshot unchanged.
Failed scenario branches do not affect successful branches or the live state.
6. Biosimulant Realization
Fit Decision
Question
Decision
Outcome
Native fit
Why
The system is stateful, time-aware, composed of typed modules, updated by events, and benefits from snapshots and isolated scenarios
Authoritative artifact
Versioned Lab plus locked process-model, estimator, and data-driven correction artifacts
Deployment
Local execution required; managed execution optional after parity validation
Prohibited use
Autonomous control or manufacturing release

Representative State Module Manifest
schema_version: "2.0"
title: "CHO Twin State Estimator"
description: "Assimilates qualified observations into a batch-specific ensemble state."
standard: other
package: biosimulant/cho-twin-estimator
version: 1.0.0

biosim:
  entrypoint: "src.estimator:ChoTwinEstimator"
  communication_step: 1.0

io:
  inputs:
    - name: process_prediction
      signal_type: record
      schema:
        batch_id: string
        ensemble_state: array
    - name: measurement_event
      signal_type: event
      schema:
        batch_id: string
        observed_at: string
        values: record
        quality_status: string
  outputs:
    - name: synchronized_state
      signal_type: record
      schema:
        batch_id: string
        state_time: string
        ensemble_state: array
        synchronization_status: string

runtime:
  python_version: "3.12"
  dependencies:
    packages:
      - numpy==1.26.4
      - scipy==1.12.0
lab.yaml Excerpt
schema_version: "2.0"
title: "CHO Fed-Batch Predictive Twin"
description: "Synchronizes a batch state and runs bounded feed scenarios."
package: biosimulant/cho-fedbatch-twin
version: 1.0.0

io:
  inputs:
    - name: batch_initialization
      maps_to: initializer.batch_initialization
    - name: measurement_event
      maps_to: events.measurement_event
    - name: process_event
      maps_to: events.process_event
    - name: scenario_request
      maps_to: scenarios.scenario_request
  outputs:
    - name: current_state
      maps_to: recorder.current_state
    - name: forecasts
      maps_to: recorder.forecasts
    - name: twin_status
      maps_to: recorder.twin_status

models:
  - path: models/batch-initializer
    alias: initializer
    parameters: {}
  - path: models/process-events
    alias: events
    parameters: {}
  - path: models/cho-process
    alias: process
    parameters:
      integration_step: 0.25
  - path: models/cho-estimator
    alias: estimator
    parameters:
      ensemble_size: 200
  - path: models/scenario-coordinator
    alias: scenarios
    parameters: {}
  - path: models/twin-recorder
    alias: recorder
    parameters: {}

wiring:
  - from: initializer.initial_state
    to:
      - estimator.initial_state
      - process.initial_state
  - from: events.accepted_events
    to:
      - estimator.events
      - process.events
  - from: process.process_prediction
    to:
      - estimator.process_prediction
  - from: estimator.synchronized_state
    to:
      - process.synchronized_state
      - scenarios.synchronized_state
      - recorder.current_state
  - from: scenarios.forecasts
    to:
      - recorder.forecasts

runtime:
  duration: 336.0
  communication_step: 1.0
  settle_steps: 1

Model time is hours from inoculation. Wall-clock timestamps remain in event and provenance records.
Execution Commands
biosimulant labs validate ./cho-fedbatch-twin --strict --json
biosimulant labs run ./cho-fedbatch-twin --results-file twin-results.json --json --no-open
biosimulant labs package ./cho-fedbatch-twin --out dist
biosimulant labs validate dist/biosimulant__cho-fedbatch-twin-1.0.0.bsilab --json
7. MRS Traceability and Tests
MRS requirement
Technical implementation
Test or protocol
Verification evidence
MRS-IN-001 to MRS-IN-008
Typed measurement, process-event, and batch schemas with unit and identity checks
DT-T05
Input conformance report
MRS-OUT-001 to MRS-OUT-005
State, forecast, interval, status, scenario, and provenance records
DT-T06 to DT-T08
Output conformance report
MRS-DQ-001 to MRS-DQ-005
Event validator and state-update acceptance rules
DT-T05, DT-T07
Data and failure report
MRS-DT-001 to MRS-DT-004
Time-ordered forecast replay and calibration
DT-T02, DT-V01
Locked twin validation report
MRS-DT-005
Synchronized and open-loop execution paths
DT-V02
Comparative forecast report
MRS-DT-006
State projection, material balances, and event reconciliation
DT-T01, DT-T03
Numerical integrity report
MRS-DT-007
Frozen scenario endpoints and prospective branches
DT-T06, DT-V03
Prospective scenario report
MRS-DT-008
Explicit stale, rejected, missing-event, and domain statuses
DT-T07
Failure-injection report
MRS-OPS-001 to MRS-OPS-002
Bounded ensemble execution and locked seeds
DT-T08, DT-T09
Performance and reproducibility report

Required Tests
DT-T01: Unit-test every material balance, feed addition, sample removal, and nonnegative state projection.
DT-T02: Replay complete runs in time order without exposing future measurements.
DT-T03: Compare one-shot and windowed process integration within numerical tolerance.
DT-T04: Assimilate known synthetic observations and verify the innovation and posterior calculation.
DT-T05: Reject duplicate, out-of-order, wrong-batch, wrong-unit, and failed-QC events.
DT-T06: Snapshot, restore, and reproduce each permitted scenario without mutating the live state.
DT-T07: Inject stale data, missing events, solver failure, one failed scenario branch, and corrupt snapshot checksums.
DT-T08: Compare local and managed results within declared Monte Carlo error before enabling managed execution.
DT-T09: Benchmark state update plus five scenario branches against the two-minute MRS limit.

DT-V01 is the time-ordered locked forecast protocol, DT-V02 is the synchronized-versus-open-loop comparison, and DT-V03 is the frozen prospective scenario protocol.
8. Lock, Release, and Monitoring
The lock includes module packages, Lab manifest, ODE and rate-correction artifacts, estimator configuration, observation-error table, scenario definitions, process-domain manifest, partition manifest, seeds, validation protocol, test fixtures, environment, and checksums.

Release requires complete MRS validation, failure injection, snapshot compatibility, local package execution, user interpretation review, and confirmation that no process-control write path exists.

Monitor state innovations, forecast residuals by horizon, interval coverage, stale and rejected events, out-of-domain rate, material-balance residuals, scenario failures, runtime, and cost. A new clone, scale, media family, sensor or assay method, control use, or horizon requires MRS review.
9. References
Adjacent Model Requirements Specification
https://docs.biosimulant.com/runtime/use-bioworld
https://docs.biosimulant.com/runtime/test-biomodule
