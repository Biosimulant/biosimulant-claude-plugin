DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Model Technical Specification Template
Modeling Technical Specification: {{Model or Project Name}}
TEMPLATE INSTRUCTION: Complete the common core, keep every applicable model-type module, and delete unused modules and instructional text before approval. Replace every {{placeholder}} with project content or Not applicable plus a reason. This document explains how the approved MRS will be implemented. It does not change MRS acceptance criteria.
1. Document Control
Field
Value
MTS identifier
{{MTS identifier}}
Version
{{Version}}
Status
Draft / In review / Approved / Superseded
Owning program
{{Program}}
Model owner
{{Name and role}}
Technical owner
{{Name and role}}
Validation owner
{{Name and role}}
Operational owner
{{Name and role}}
Created
{{YYYY-MM-DD}}
Last revised
{{YYYY-MM-DD}}
Approved MRS
{{Relative link, identifier, and version}}
Assay / Data Specification
{{Link and version}}
Validation protocol
{{Link and version, if available}}
Source repository
{{Repository and intended path}}

Contributors and Reviewers
Role
Name
Review responsibility
Scientific owner
{{Name}}
Scientific meaning and MRS fidelity
Model developer
{{Name}}
Algorithm, implementation, and tests
Data owner
{{Name}}
Data provenance and partition enforcement
Assay owner
{{Name}}
Observation and ground-truth implementation
Validation owner
{{Name}}
Independent verification and locked evaluation
Platform or infrastructure owner
{{Name}}
Runtime, deployment, security, and operations
Intended user
{{Name}}
Output interpretation and workflow fit

Approval
Approver
Scope
Decision
Date
Evidence
{{Name}}
Scientific design
Pending / Approved / Rejected
{{Date}}
{{Link}}
{{Name}}
Technical design
Pending / Approved / Rejected
{{Date}}
{{Link}}
{{Name}}
Validation design
Pending / Approved / Rejected
{{Date}}
{{Link}}
{{Name}}
Operational fit
Pending / Approved / Rejected
{{Date}}
{{Link}}

Revision History
Version
Date
Author
Material change
MRS impact
Revalidation impact
{{0.1}}
{{Date}}
{{Name}}
{{Change}}
None / Review required
None / Partial / Full

2. Technical Decision Summary
MRS objective: {{One-sentence requirement summary}}
Selected technical approach: {{Algorithm, formalism, or system}}
Why this approach: {{Evidence and trade-off}}
Primary model artifact: {{Weights, equations, parameters, executable, package, or statistical procedure}}
Development environment: {{Stack}}
Delivery environment: {{Stack}}
Biosimulant fit: Native fit / Adapter fit / External boundary / Not suitable
Model lock unit: {{Exact set of artifacts frozen as one version}}
Most important technical risk: {{Risk}}
Most important scientific limitation: {{Limitation}}
3. Scope, Boundaries, and Assumptions
Technical Scope
In scope
Out of scope
{{Components, interfaces, and workflows implemented here}}
{{Excluded capabilities, tools, and workflows}}

System Boundary
Upstream producer: {{Assay, data pipeline, user, sensor, or system}}
Downstream consumer: {{User, experiment, API, report, process, or system}}
Authoritative source of raw data: {{System}}
Authoritative source of model artifact: {{System}}
Authoritative source of acceptance: Approved MRS and {{acceptance record}}
Technical Assumptions
ID
Assumption
Basis
Consequence if false
Verification or monitor
MTS-ASM-001
{{Assumption}}
{{Evidence}}
{{Impact}}
{{Check}}

Dependencies
ID
Dependency
Version or constraint
Owner
Failure behavior
MTS-DEP-001
{{Dataset, library, solver, model, service, or package}}
{{Version}}
{{Owner}}
{{Response}}

4. MRS Traceability
Every mandatory MRS requirement must appear in this table. One MRS requirement may map to several components or tests. An MTS decision must not weaken the MRS threshold.

MRS ID
Requirement summary
Technical component or decision
Verification method
Evidence artifact
Owner
{{MRS-ID}}
{{Requirement}}
{{Implementation}}
Unit / integration / analysis / prospective experiment
{{Artifact}}
{{Owner}}

Derived Technical Requirements
MTS ID
Derived requirement
Source MRS ID
Acceptance criterion
Test
MTS-REQ-001
{{Technical requirement needed to satisfy the MRS}}
{{MRS-ID}}
{{Criterion}}
{{Test ID}}

5. Architecture and Data Flow
Architecture Overview
{{Describe the system as implemented, including external components and ownership boundaries.}}

flowchart LR
    A["{{Input or data source}}"] --> B["{{Validation and preprocessing}}"]
    B --> C["{{Model or estimation component}}"]
    C --> D["{{Uncertainty and decision logic}}"]
    D --> E["{{Output consumer}}"]
Components
Component ID
Component
Responsibility
Inputs
Outputs
Technology
Owner
CMP-001
{{Component}}
{{Single responsibility}}
{{Contract}}
{{Contract}}
{{Stack}}
{{Owner}}

Execution Sequence
{{Input acquisition and identity validation}}
{{Preprocessing or state initialization}}
{{Model execution}}
{{Uncertainty, calibration, or diagnostics}}
{{Output validation and persistence}}
{{User or downstream delivery}}
State and Persistence
Persistent state: {{State and location}}
Ephemeral state: {{State}}
Checkpoint or snapshot: {{Format and cadence}}
Artifact storage: {{Location and retention}}
Transaction or atomicity boundary: {{Definition}}
Recovery behavior: {{Definition}}
6. Data Implementation
Dataset Manifest
Dataset ID
Purpose
Source
Version
Unit of observation
Size
Checksum / immutable reference
DATA-001
Development / calibration / validation / external
{{Source}}
{{Version}}
{{Unit}}
{{N}}
{{Reference}}

Data Schema
Field
Type
Unit
Allowed values or range
Missingness
Source
MRS mapping
{{Field}}
{{Type}}
{{Unit}}
{{Rule}}
{{Rule}}
{{Source}}
{{MRS-IN-ID}}

Preprocessing
Step
Operation
Fitted from
Parameters / artifact
Leakage control
Failure behavior
1
{{Operation}}
Development data only / fixed standard
{{Artifact}}
{{Control}}
{{Response}}

Partition Enforcement
Grouping key: {{Donor, gene, sequence family, batch, site, time block, or other key}}
Partition manifest: {{Versioned artifact}}
Near-duplicate rule: {{Method and threshold}}
Temporal cutoff: {{Date or not applicable}}
External-data independence: {{Evidence}}
Test-set access control: {{Owner and process}}
Automated leakage tests: {{Tests}}
Data Quality Handling
Quality-gate implementation: {{Rules and code path}}
Biological replicate handling: {{Method}}
Technical replicate handling: {{Method}}
Missing data: {{Method and justification}}
Censoring and detection limits: {{Method}}
Outliers: {{Predeclared handling}}
Failed assay or corrupt input: {{Status and exclusion behavior}}
7. Input, Output, and Error Contracts
Inputs
MRS ID
Technical name
Type / schema
Unit
Validation
Invalid-input response
{{MRS-IN-ID}}
{{Name}}
{{Schema}}
{{Unit}}
{{Rule}}
Reject / warn / restricted result

Outputs
MRS ID
Technical name
Type / schema
Unit
Precision
Uncertainty
Consumer
{{MRS-OUT-ID}}
{{Name}}
{{Schema}}
{{Unit}}
{{Precision}}
{{Interval or distribution}}
{{Consumer}}

Status and Error Contract
Code
Condition
User-facing meaning
Machine behavior
Retryable?
OK
Valid supported result
{{Meaning}}
Return result and provenance
No
INVALID_INPUT
Input fails contract
{{Meaning}}
No model result
After correction
OUT_OF_DOMAIN
Input outside supported domain
{{Meaning}}
Abstain or return restricted result
Not without review
NONIDENTIFIABLE
Required estimate cannot be identified
{{Meaning}}
No unsupported point claim
With more evidence
INFEASIBLE
No solution satisfies constraints
{{Meaning}}
Return violated constraints
After constraint review
EXECUTION_FAILED
Model or solver failed
{{Meaning}}
Preserve logs and no partial success claim
Depends on cause

Provenance Contract
Every result must record: {{model version, code revision, input identity, data version, preprocessing version, configuration, dependency environment, hardware when relevant, random seed, issue time, and execution location}}.
8. Model Method and Uncertainty
Selected Method
Method: {{Name and version}}
Scientific rationale: {{Why it represents or solves the MRS problem}}
Technical rationale: {{Why it is feasible and maintainable}}
Baselines considered: {{Methods}}
Alternatives rejected: {{Methods and reasons}}
Known failure region: {{Conditions}}
Training, Fitting, or Calibration
Objective or likelihood: {{Definition}}
Parameter or weight initialization: {{Method}}
Optimization or estimation algorithm: {{Method}}
Hyperparameter selection: {{Method and partition}}
Stopping and convergence: {{Rule}}
Randomness: {{Seeds and repeated runs}}
Model selection: {{Locked rule}}
Final refit: {{Whether and how development partitions are combined}}
Uncertainty
Sources represented: {{Data, parameter, model, state, process, or residual uncertainty}}
Method: {{Bootstrap, ensemble, posterior, conformal, profile, propagation, or other}}
Calibration data: {{Partition}}
Coverage or calibration check: {{Metric and threshold}}
Unsupported interpretation: {{What the interval does not mean}}
Abstention rule: {{Rule}}
9. Biosimulant Fit Assessment
This section is required. Biosimulant is an orchestration and packaging option, not a mandatory implementation target.
Context
Biosimulant can embed runnable model components in a Lab, exchange typed BioSignals through named ports, execute finite components before, during, or after communication windows, advance temporal components through BioWorld, and expose the same versioned Lab through local, CLI, Studio, Hub, or managed execution surfaces. It does not make different scientific standards semantically equivalent and does not prove model correctness.
Decision
Field
Decision
Outcome
Native fit / Adapter fit / External boundary / Not suitable
Decision owner
{{Owner}}
Main value expected
{{Composition, timing, inspection, packaging, reuse, delivery, or none}}
Main mismatch or limitation
{{Limitation}}
Authoritative model artifact remains
{{Biosimulant package or external artifact}}
Reassessment trigger
{{Condition}}

Fit Evidence
Question
Yes / No
Evidence
Are there reusable components with stable typed interfaces?
{{Answer}}
{{Evidence}}
Do components exchange signals or advance through model time?
{{Answer}}
{{Evidence}}
Is explicit wiring, inspection, snapshotting, or scenario branching useful?
{{Answer}}
{{Evidence}}
Is local, CI, workbench, registry, or managed execution valuable?
{{Answer}}
{{Evidence}}
Does Biosimulant preserve the native scientific artifact and semantics?
{{Answer}}
{{Evidence}}
Is Biosimulant simpler and safer than the selected alternative?
{{Answer}}
{{Evidence}}

10. Biosimulant Realization
KEEP THIS SECTION ONLY FOR NATIVE FIT OR ADAPTER FIT. For an adapter, identify the external scientific artifact as authoritative and test the adapter against its native runtime.
BioModule Design
Alias
Class / adapter
Responsibility
State
Communication step
Execution policy
Source artifact
{{alias}}
{{Entrypoint}}
{{Responsibility}}
Stateless / stateful
{{Time and unit}}
ExecutionPolicy.ONCE_BEFORE_RUN / ExecutionPolicy.EACH_WINDOW / ExecutionPolicy.ONCE_AFTER_RUN
{{Artifact and version}}


Each module must define or intentionally omit:

setup(config) for run initialization;
inputs() and outputs() with typed SignalSpec contracts;
canonical execute(inputs, *, context) for every new finite or settle-independent temporal module;
an explicit execution_policy with a scientific invocation rationale for canonical modules;
advance_window(start, end), set_inputs(signals), and get_outputs() only for the supported imported or settle-dependent temporal compatibility contract;
exactly one computation hook per module;
snapshot() and restore() when branching, recovery, or reproducibility needs state;
request_stop() when work can block; and
visualize() only for transport-safe scientific visuals.
Signal and Port Contract
From
To
Signal type
dtype / schema
Shape
Emitted unit
Accepted units
Timing policy
{{alias.port}}
{{alias.port}}
scalar / array / record / event
{{Definition}}
{{Shape}}
{{Unit}}
{{Units}}
{{State, event, interpolation, or stale rule}}

Representative model.yaml
schema_version: "2.0"
title: "{{Model title}}"
description: "{{Model responsibility}}"
standard: {{sbml / cellml / neuroml / onnx / other}}
package: {{namespace/model-name}}
version: {{x.y.z}}

biosim:
  entrypoint: "{{src.module:ClassName}}"
  init_kwargs: {}
  setup: {}
  communication_step: {{positive number}}
  execution_policy: {{once_before_run / each_window / once_after_run}}

io:
  inputs:
    - name: {{input_name}}
      signal_type: {{scalar / array / record / event}}
      dtype: {{float64}}
      accepted_units: [{{unit}}]
  outputs:
    - name: {{output_name}}
      signal_type: {{scalar / array / record / event}}
      dtype: {{float64}}
      emitted_unit: {{unit}}

runtime:
  python_version: "{{3.12}}"
  dependencies:
    packages:
      - {{dependency==exact_version}}

biosim.execution_policy repeats the module's ExecutionPolicy from the BioModule Design table in lowercase and requires biosimulant>=0.0.33. The Python attribute stays authoritative and the runtime refuses to load a model whose declaration disagrees. Omit the field only when the policy depends on constructor parameters.

Declare runtime.remote.requirements only when remote execution needs a specific resource class:

runtime:
  remote:
    requirements:
      accelerator: gpu
      gpu_count: 1
Representative lab.yaml
schema_version: "2.0"
title: "{{Lab title}}"
description: "{{Lab purpose}}"
package: {{namespace/lab-name}}
version: {{x.y.z}}

io:
  inputs:
    - name: {{public_input}}
      maps_to: {{model_alias.input_port}}
  outputs:
    - name: {{public_output}}
      maps_to: {{model_alias.output_port}}

models:
  - path: models/{{model-name}}
    alias: {{model_alias}}
    parameters: {}

wiring: []

runtime:
  duration: {{positive duration}}
  communication_step: {{positive step}}
  settle_steps: {{non-negative integer}}

runtime.communication_step is required and positive. Model entries require stable aliases. Wiring uses alias.port. Use settle_steps only for downstream chains that must consume outputs produced at the final simulation boundary.
Execution and Packaging
biosimulant labs validate ./{{lab-directory}}
biosimulant labs run ./{{lab-directory}} --results-file results.json --json
biosimulant labs package ./{{lab-directory}} --out dist
biosimulant labs validate dist/{{lab-package}}.bsilab --json
biosimulant labs run dist/{{lab-package}}.bsilab --no-install-deps --json

Package reference: {{namespace/name@x.y.z}}
Local execution: {{Required / optional}}
Studio inspection: {{Required / optional}}
Hub visibility: Public / private / not published
Managed execution: {{Required / optional / prohibited}}
Local and managed parity requirement: {{Definition}}
Credentials and secrets: Never embedded in manifests or package references
Adapter Verification
For adapter fits, compare the wrapped component with the authoritative native execution using a versioned input suite. Define tolerated differences, ordering, units, randomness, and failure equivalence: {{Definition}}.
11. External or Not-Suitable Delivery
KEEP THIS SECTION FOR EXTERNAL BOUNDARY OR NOT SUITABLE. Delete it for native or adapter fit unless an additional external component remains.

Selected stack: {{Framework, language, workflow system, solver, notebook, or package}}
Why it is a better fit: {{Reason}}
Authoritative artifact: {{Artifact and version}}
Execution entry point: {{Command or interface}}
Environment: {{Lockfile, image, or package specification}}
Input and output exchange format: {{Schema}}
Boundary with Biosimulant, if any: {{Import, export, scoring, visualization, or none}}
Boundary versioning: {{Rule}}
Operational owner: {{Owner}}
Reassessment trigger: {{When composition or packaging value would justify integration}}
12. Verification and Test Design
Test Inventory
Test ID
Level
Requirement
Fixture or data
Expected result
Evidence
TEST-001
Unit / integration / scientific / numerical / regression / performance / acceptance
{{MRS or MTS ID}}
{{Fixture}}
{{Criterion}}
{{Artifact}}

Required Test Classes
Unit tests: functions, equations, transforms, constraints, and boundary behavior.
Interface tests: schema, dtype, shape, units, status, and provenance.
Data tests: identity, partitions, duplicates, leakage, missingness, and quality gates.
Scientific behavior tests: invariants, monotonicity where justified, controls, and known qualitative regimes.
Numerical tests: convergence, tolerance sensitivity, conservation, nonnegativity, and solver failure.
Regression tests: normalized outputs from a declared reference version.
Integration tests: complete data-to-result path and every external boundary.
Robustness tests: shifts, perturbations, invalid inputs, and out-of-domain conditions.
Performance tests: runtime, memory, throughput, hardware, and cost.
Reproducibility tests: clean environment, repeated seeds, and artifact checksums.
Acceptance tests: every MRS threshold on the correct locked evidence.
Biosimulant Tests
Keep only when Biosimulant is used.

Module ports match model.yaml.
Emitted BioSignals match type, shape, schema, unit, and time contracts.
snapshot() and restore() round-trip when state is required.
BioWorld wiring resolves and runs for the declared duration.
Final-boundary outputs are delivered with the declared settling behavior.
Package validation, build, and compatibility smoke tests pass.
Native and adapter outputs remain within declared parity tolerance.
Local and managed execution produce equivalent scientific results when both are supported.
13. Reproducibility, Security, Performance, and Cost
Reproducibility
Artifact
Required identity
Source code
Repository and commit
Model
Weights, equations, parameters, or package checksum
Data
Manifest, immutable references, and checksums
Environment
Lockfile, container, or reproducible package specification
Configuration
Versioned run configuration
Randomness
Seeds and nondeterminism statement
Reference execution
Command, expected outputs, and tolerance

Security and Data Governance
Data classification: {{Classification}}
Access control: {{Rule}}
Secrets: {{Storage and injection method}}
Personal or confidential data: {{Handling}}
Package and dependency scanning: {{Method}}
Serialization and untrusted input controls: {{Method}}
Audit events: {{Events}}
Retention and deletion: {{Rule}}
Performance and Cost
Requirement
Target
Reference environment
Measurement
Runtime
{{Target}}
{{Hardware}}
{{Benchmark}}
Peak memory
{{Target}}
{{Hardware}}
{{Benchmark}}
Throughput
{{Target}}
{{Hardware}}
{{Benchmark}}
Storage
{{Target}}
{{Environment}}
{{Measurement}}
Cost per run or batch
{{Target}}
{{Pricing basis and date}}
{{Measurement}}

14. Model Lock, Release, and Operations
Model Lock Manifest
The locked version includes:

source commit;
model artifact and checksum;
preprocessing and feature artifact;
parameter, threshold, and calibration artifacts;
dependency environment;
data and partition manifests;
test suite and reference fixtures;
analysis and validation protocol;
output schema and user interpretation guide; and
Biosimulant or external package identity when applicable.
Release Gate
Gate
Owner
Evidence
Required result
MRS traceability complete
{{Owner}}
{{Artifact}}
No unaddressed mandatory requirement
Verification complete
{{Owner}}
{{Artifact}}
All mandatory technical tests pass
Validation complete
{{Owner}}
{{Artifact}}
MRS computational and biological gates pass
Reproducibility complete
{{Owner}}
{{Artifact}}
Clean rerun passes
Operational readiness
{{Owner}}
{{Artifact}}
Monitoring, support, rollback, and training ready

Monitoring
Signal
Baseline
Threshold
Cadence
Response
Owner
Input-domain drift
{{Baseline}}
{{Threshold}}
{{Cadence}}
{{Response}}
{{Owner}}
Outcome performance
{{Baseline}}
{{Threshold}}
{{Cadence}}
{{Response}}
{{Owner}}
Failure or abstention rate
{{Baseline}}
{{Threshold}}
{{Cadence}}
{{Response}}
{{Owner}}
Runtime and cost
{{Baseline}}
{{Threshold}}
{{Cadence}}
{{Response}}
{{Owner}}

Change, Rollback, and Retirement
Recalibration trigger: {{Trigger}}
Retraining or refitting trigger: {{Trigger}}
MRS reapproval trigger: {{Intended-use or requirement change}}
Revalidation scope rule: {{Rule}}
Rollback artifact and procedure: {{Procedure}}
Incident owner: {{Owner}}
Retirement trigger: {{Trigger}}
Archive contents and retention: {{Rule}}
15. Model-Specific Technical Modules
TEMPLATE INSTRUCTION: Keep every applicable module. Hybrid systems may retain several. Identify which component each field applies to.
15A. Predictive / ML Technical Module
KEEP THIS MODULE IF a component predicts a class, probability, rank, continuous target, event, or future outcome from observed features.

Target implementation: {{Target transform and horizon}}
Feature implementation: {{Feature sources and availability}}
Architecture: {{Model family and version}}
Loss: {{Objective and weighting}}
Sampling and imbalance: {{Method}}
Group-aware split enforcement: {{Method}}
Hyperparameter search: {{Space, budget, and selection metric}}
Calibration: {{Method and partition}}
Uncertainty or abstention: {{Method}}
Explanation: {{Global and case-level method}}
Export artifact: {{Native, ONNX, or other format}}
Inference batching: {{Rule}}
Retraining pipeline: {{External workflow and trigger}}
15B. Mechanistic Technical Module
KEEP THIS MODULE IF explicit biological entities, reactions, transport, interactions, or causal mechanisms are represented.

Formalism: ODE / PDE / stochastic / rule-based / constraint-based / agent-based / other
Authoritative representation: {{SBML, CellML, NeuroML, equations, or code}}
States and observables: {{Implementation}}
Reactions and rate laws: {{Implementation}}
Initial and boundary conditions: {{Implementation}}
Parameter table and provenance: {{Artifact}}
Solver and version: {{Solver}}
Absolute and relative tolerances: {{Values}}
Stiffness and event handling: {{Method}}
Conservation and physical constraints: {{Tests}}
Identifiability: {{Structural and practical method}}
Sensitivity analysis: {{Method and ranges}}
Native-runtime parity: {{Method and tolerance}}
15C. Generative Technical Module
KEEP THIS MODULE IF a component proposes new sequences, structures, molecules, constructs, protocols, or designs.

Generator and version: {{Artifact}}
Conditioning representation: {{Implementation}}
Sampling procedure: {{Seeds, temperatures, schedules, or search}}
Hard-constraint engine: {{Implementation and order}}
Soft scoring and ranking: {{Implementation}}
Invalid-output handling: {{Status and denominator}}
Novelty databases and versions: {{Manifest}}
Diversity and clustering: {{Method}}
Memorization checks: {{Method and limitation}}
Candidate registry: {{Schema and immutable identity}}
Computational funnel: {{Stage counts}}
Experimental selection lock: {{Artifact}}
GPU and scheduler: {{External or managed stack}}
15D. Optimization Technical Module
KEEP THIS MODULE IF a component recommends settings, formulations, schedules, or interventions under objectives and constraints.

Decision-variable encoding: {{Types, units, and bounds}}
Objective implementation: {{Functions and scaling}}
Hard constraints: {{Implementation}}
Soft penalties: {{Implementation}}
Solver and version: {{Solver}}
Initialization and seeds: {{Method}}
Stopping and optimality tolerance: {{Rule}}
Infeasibility diagnosis: {{Method}}
Multiple-objective selection: {{Pareto or lexicographic rule}}
Surrogate model: {{If used}}
Uncertainty and robust optimization: {{Method}}
Duplicate recommendation rule: {{Method}}
Confirmatory design export: {{Format}}
15E. Simulation / Digital Twin Technical Module
KEEP THIS MODULE IF a component represents an evolving system, updates from observations, or runs scenarios over time.

Twin or simulated asset identity: {{Schema}}
State vector and units: {{Definition}}
Event model: {{Definition}}
Initialization: {{Method}}
State-update or assimilation: {{Method}}
Model clock and time zone: {{Definition}}
Internal integration steps: {{By component}}
World communication step: {{Value and rationale}}
Forecast horizons: {{Values}}
Scenario branching: {{Method}}
Snapshot and restore: {{Schema and compatibility}}
Stale data and synchronization: {{Rules}}
Uncertainty propagation: {{Method}}
Numerical and material-balance checks: {{Tests}}
Reset, recalibration, and drift: {{Rules}}
15F. Statistical Estimation Technical Module
KEEP THIS MODULE IF the primary output is an estimate, interval, posterior, effect, parameter, or latent state.

Estimand implementation: {{Exact calculation}}
Statistical model: {{Likelihood, link, hierarchy, or nonparametric method}}
Estimation library and version: {{Library}}
Covariate design matrix: {{Implementation}}
Replicate and correlation structure: {{Implementation}}
Missingness and censoring: {{Method}}
Priors, if used: {{Distributions and sensitivity}}
Optimization or sampling diagnostics: {{Checks}}
Confidence or credible interval: {{Method}}
Multiplicity: {{Adjustment}}
Influence and residual diagnostics: {{Checks}}
Nonidentifiable or failed estimate: {{Status behavior}}
Simulation study: {{Bias, coverage, and failure scenarios}}
16. Risks, Decisions, and Open Questions
Technical Risk Register
Risk ID
Risk
Likelihood
Impact
Detection
Mitigation
Owner
MTS-RSK-001
{{Risk}}
Low / Medium / High
Low / Medium / High
{{Signal}}
{{Action}}
{{Owner}}

Decision Log
Decision ID
Date
Decision
Alternatives
Rationale
MRS impact
Approver
MTS-DEC-001
{{Date}}
{{Decision}}
{{Alternatives}}
{{Reason}}
None / Review
{{Name}}

Open Questions
Question ID
Question
Decision impact
Owner
Due date
Status
MTS-OQ-001
{{Question}}
{{Impact}}
{{Owner}}
{{Date}}
Open / Resolved

17. References and Glossary
References
{{Technical method, software, standard, dataset, or architecture reference}}
Biosimulant References
https://docs.biosimulant.com/runtime/create-biomodule
https://docs.biosimulant.com/runtime/model-manifest
https://docs.biosimulant.com/runtime/write-lab-manifest
https://docs.biosimulant.com/hub/publish
https://docs.biosimulant.com/developer-api
Glossary
Term
Project-specific definition
{{Term}}
{{Definition}}

Visualization delivery
{{Expected user-facing views, source outputs, labels and units, caveats, renderer/lifecycle/artifact design where applicable, executable acceptance checks, and reasons for any opt-out. Almost every scientific Lab requires a meaningful visual.}}
