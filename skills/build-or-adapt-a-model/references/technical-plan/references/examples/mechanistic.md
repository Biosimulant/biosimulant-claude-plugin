DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Mechanistic MTS Example - MAPK ERK Signaling
Modeling Technical Specification: MAPK/ERK Cascade with Negative Feedback
This is an implementation-ready illustrative technical design. It is not an implemented or validated biological model.
1. Document Control
Field
Value
MTS identifier
EX-MTS-MECH-ERK-001
Version
1.0 example
Status
Illustrative, not approved for execution
MRS
EX-MRS-MECH-ERK-001
Model owner
Systems biology lead
Technical owner
Scientific software lead
Validation owner
Independent quantitative biology lead
Biosimulant fit
Adapter fit around authoritative SBML

2. Technical Decision Summary
Represent the reduced Raf-MEK-ERK cascade and inhibitory ERK feedback in SBML Level 3. Keep the SBML document and parameter-set manifest as the authoritative scientific artifacts. Execute it in a validated SBML simulator for calibration and parity checks, then expose the locked model through a Biosimulant BioModule adapter for composition, scenario runs, recording, and visualization.

The adapter does not reinterpret reaction semantics. If the Biosimulant result differs materially from the locked native execution, the native SBML result controls and the package fails verification.
3. Architecture
flowchart LR
    A["EGF stimulus module"] -->|"effective stimulus"| B["SBML MAPK adapter"]
    B -->|"Raf, ppMEK, ppERK"| C["Trajectory recorder"]
    B -->|"ppERK"| D["Scientific visualization"]
    E["Locked SBML and parameters"] --> B
Components
Alias
Responsibility
State
Implementation
stimulus
Convert an EGF condition into the approved upstream activation boundary
Current stimulus
Small deterministic BioModule
mapk
Load SBML, apply parameters and initial state, integrate one communication window, and emit observables
Full SBML species vector and solver time
SBML adapter backed by a validated stiff solver
recorder
Accumulate time, active Raf, ppMEK, and ppERK
Trajectory table
Stateful BioModule
visual
Produce transport-safe time-course and phase views
Latest trajectory
Visualization BioModule

4. Authoritative Model and Numerical Method
Representation: SBML Level 3 XML with stable species, reaction, parameter, compartment, and observable identifiers.
State tiers: Raf and active Raf; MEK, pMEK, and ppMEK; ERK, pERK, and ppERK.
Feedback: a monotone inhibitory term from ppERK to upstream Raf activation.
Units: minutes, nanomolar concentrations, and dimensionally defined rate constants.
Observation model: ppERK divided by conserved total ERK, with a separate assay scaling and background mapping.
Calibration: external profile-likelihood workflow using biological culture day as the resampling unit.
Native simulator: a locked SBML-capable solver with documented version.
Adapter solver: the same native solver library where packaging permits; otherwise SciPy solve_ivp with BDF and mandatory parity tests.
Default tolerances: relative 1e-8 and absolute 1e-10 nM, tightened during numerical verification.
Internal integration: adaptive, independent of the 0.1-minute world communication boundary.
Parameter Artifacts
parameters.csv records parameter identifier, value, unit, source class, source citation or fitted run, bound, transformation, and identifiability status. A fitted release stores an ensemble or profile-supported range rather than only one optimum.

initial-conditions.csv records each state, amount or concentration, unit, source, and condition-specific override.
5. Inputs, Outputs, and State
Port
Direction
Type
Unit
Meaning
effective_stimulus
Input
scalar float64
dimensionless
Approved EGF-to-cascade boundary value from 0 to 1
inhibitor_fraction
Input
scalar float64
fraction
Fractional MEK activity inhibition from 0 to 1
feedback_scale
Input
scalar float64
dimensionless
Multiplier on the locked feedback term
active_raf
Output
scalar float64
fraction
Active Raf divided by total Raf
pp_mek
Output
scalar float64
fraction
Doubly phosphorylated MEK fraction
pp_erk
Output
scalar float64
fraction
Doubly phosphorylated ERK fraction
state_summary
Output
record
mixed
Time, conservation residual, solver status, and observable summary


Invalid fractions are rejected. Solver failure returns EXECUTION_FAILED with the last valid time and solver diagnostics, but no partial successful trajectory.

The snapshot contains SBML state identifiers and values, current time, active parameter overrides, solver configuration, and model checksum. Restore requires the same SBML and parameter-set checksums.
6. Biosimulant Realization
Fit Decision
Question
Decision
Outcome
Adapter fit
Value
Time-aware composition, explicit perturbation inputs, state snapshots, trajectory inspection, and portable scenario runs
Authoritative artifact
SBML plus parameter and initial-condition manifests
Main limitation
Biosimulant does not validate reaction semantics or make the mechanism unique

model.yaml Excerpt
schema_version: "2.0"
title: "MAPK ERK Negative Feedback Model"
description: "SBML-backed reduced Raf-MEK-ERK signaling model."
standard: sbml
package: biosimulant/mapk-erk-feedback
version: 1.0.0

biosim:
  entrypoint: "src.mapk_adapter:MapkSbmlModule"
  init_kwargs:
    sbml_path: "model/mapk-erk-feedback.xml"
    parameter_path: "model/parameters.csv"
  communication_step: 0.1

io:
  inputs:
    - name: effective_stimulus
      signal_type: scalar
      dtype: float64
      accepted_units: [dimensionless]
    - name: inhibitor_fraction
      signal_type: scalar
      dtype: float64
      accepted_units: [fraction]
    - name: feedback_scale
      signal_type: scalar
      dtype: float64
      accepted_units: [dimensionless]
  outputs:
    - name: pp_erk
      signal_type: scalar
      dtype: float64
      emitted_unit: fraction
    - name: state_summary
      signal_type: record
      schema:
        time_min: float
        conservation_residual: float
        solver_status: string

runtime:
  python_version: "3.12"
  dependencies:
    packages:
      - python-libsbml==5.20.2
      - scipy==1.12.0
      - numpy==1.26.4
lab.yaml Excerpt
schema_version: "2.0"
title: "MAPK ERK Perturbation Lab"
description: "Runs and inspects stimulus and feedback perturbations."
package: biosimulant/mapk-erk-perturbation
version: 1.0.0

models:
  - path: models/stimulus
    alias: stimulus
    parameters: {}
  - path: models/mapk-erk-feedback
    alias: mapk
    parameters: {}
  - path: models/trajectory-recorder
    alias: recorder
    parameters: {}
  - path: models/mapk-visual
    alias: visual
    parameters: {}

wiring:
  - from: stimulus.effective_stimulus
    to:
      - mapk.effective_stimulus
  - from: mapk.state_summary
    to:
      - recorder.state_summary
  - from: recorder.trajectory
    to:
      - visual.trajectory

runtime:
  duration: 120.0
  communication_step: 0.1
  settle_steps: 2
Execution Commands
biosimulant labs validate ./mapk-erk-perturbation --strict --json
biosimulant labs run ./mapk-erk-perturbation --results-file results.json --json --no-open
biosimulant labs package ./mapk-erk-perturbation --out dist
biosimulant labs validate dist/biosimulant__mapk-erk-perturbation-1.0.0.bsilab --json
7. MRS Traceability and Verification
MRS requirement
Technical implementation
Test or protocol
Verification evidence
MRS-IN-001 to MRS-IN-005
Condition manifest, bounded perturbation ports, SBML initial states, and parameter manifest
MECH-T01, MECH-T07
Input, unit, and parameter-provenance report
MRS-OUT-001 to MRS-OUT-006
Stable observable mapping, trajectory summaries, and parameter-ensemble uncertainty
MECH-T03, MECH-T08
Output conformance and uncertainty report
MRS-DQ-001 to MRS-DQ-005
External assay pipeline enforces plate and biological-replicate gates
MECH-V01
Data-readiness report
MRS-MECH-001
SBML conservation rules and runtime invariant checks
MECH-T02
Conservation test suite
MRS-MECH-002 to MRS-MECH-006
Locked condition and perturbation simulation
MECH-V02
Validation report
MRS-MECH-007
Profile likelihood and parameter provenance
MECH-V03
Identifiability report
MRS-MECH-008
Native and adapter solver comparison
MECH-T03, MECH-T04
Numerical robustness and parity report

Required Tests
MECH-T01: Validate SBML structure, units, identifiers, and absence of unresolved references.
MECH-T02: Check nonnegativity and Raf, MEK, and ERK conservation for every permitted condition.
MECH-T03: Compare native and adapter trajectories at every assay time with maximum absolute observable difference no greater than 1e-6.
MECH-T04: Tighten tolerances and compare two stiff solvers against MRS-MECH-008.
MECH-T05: Snapshot at 30 minutes, restore in a fresh process, and reproduce the 30-to-120-minute trajectory.
MECH-T06: Reject an SBML or parameter checksum mismatch during restore.
MECH-T07: Verify zero stimulus, full inhibitor, zero feedback, and upper-bound stimulus cases.
MECH-T08: Run the complete Lab, confirm two settling hops, and validate visual JSON transport safety.

MECH-V01 is the assay data-readiness protocol, MECH-V02 is the locked holdout and perturbation protocol, and MECH-V03 is the profile-likelihood and parameter-provenance review.
8. Lock, Release, and Monitoring
The lock contains SBML, parameters, initial conditions, observation mapping, native solver environment, adapter environment, fit ensemble, calibration and validation manifests, model and Lab packages, reference trajectories, and checksums.

Release requires structural and practical identifiability review, numerical verification, native-adapter parity, held-out validation, clean package execution, and scientific approval. Publication to Hub is optional and must not expose restricted assay data.

Monitor dependency compatibility, package parity, solver warnings, conservation residuals, unsupported parameter overrides, and changes to the experimental observation model. Any reaction, state, endpoint, or intended perturbation change requires MRS review.
9. References
Adjacent Model Requirements Specification
https://docs.biosimulant.com/runtime/create-biomodule
https://docs.biosimulant.com/runtime/test-biomodule
