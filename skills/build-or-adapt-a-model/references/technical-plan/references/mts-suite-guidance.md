DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Model Requirements Specification Suite
Purpose
This suite provides a consistent way for computational scientists, model developers, scientific software engineers, platform engineers, validation owners, and wet-lab collaborators to define how an approved biological model will be implemented, verified, released, and maintained.

The Modeling Technical Specification (MTS) is the implementation contract for an approved Model Requirements Specification (MRS). It translates scientific and operational requirements into:

Technical architecture and component boundaries
Algorithms, equations, solvers, and model structures
Data preparation and partition controls
Input, output, unit, uncertainty, and error contracts
Training, fitting, generation, optimization, or simulation procedures
Verification tests and acceptance evidence
Reproducible environments and locked artifacts
Release, monitoring, rollback, recalibration, and retirement procedures

The MTS explains how the requirements will be satisfied. It must not silently weaken, reinterpret, or replace the MRS.
Relationship Between the MRS and MTS
Document
Main question
Source of truth for
Model Requirements Specification
What must the model do, where must it work, and what evidence will prove it?
Scientific purpose, intended use, required behavior, validation, and acceptance
Modeling Technical Specification
How will the approved requirements be implemented, tested, delivered, and maintained?
Architecture, algorithms, interfaces, implementation controls, tests, and operations


Every mandatory MRS requirement must trace to:

A technical component or implementation decision
A verification test or validation protocol
An evidence artifact
An accountable owner
The original MRS acceptance criterion

A technical implementation is not acceptable merely because it runs successfully. It must satisfy the scientific and operational requirements defined in the MRS.
Model Types
Select technical modules according to the jobs the model performs. A hybrid model may retain more than one module.

Model type
Main technical concern
Typical implementation elements
Predictive / ML
Produce reliable predictions for the intended generalization domain
Features, target transformation, architecture, loss, grouped partitions, leakage prevention, calibration, uncertainty, export, and inference
Mechanistic
Represent and numerically solve a specified biological mechanism
Equations, reactions, states, parameters, initial conditions, units, solvers, conservation, identifiability, and sensitivity
Generative
Produce valid and diverse candidates under design constraints
Conditioning, sampling, hard filters, scoring, novelty, diversity, invalid-output handling, candidate registry, and experimental funnel
Optimization
Search a feasible decision space under one or more objectives
Decision variables, objective functions, hard constraints, penalties, solver, initialization, robustness, infeasibility, and Pareto selection
Simulation / digital twin
Maintain or forecast the state of a system over time
State vector, initialization, events, model clock, integration, measurement assimilation, synchronization, snapshots, scenarios, and drift
Statistical estimation
Infer a defined quantity from noisy observations
Estimand, statistical model, likelihood, replicate structure, censoring, fitting, diagnostics, intervals, multiplicity, and failed-estimate handling


Select the technical design because it is appropriate for the requirement, data, and intended decision. Do not select a modeling technique simply because it is familiar or already available.
How to Use the Master Template
Complete and approve the MRS before treating implementation as authorized.
Copy the MTS template into the same project folder as the approved MRS.
Link the MTS to the exact MRS identifier and version it implements.
Complete every common section unless it is explicitly conditional.
Keep every applicable model-type module. Multiple modules may be retained for a hybrid model.
Delete unused modules and all instructional text marked TEMPLATE INSTRUCTION.
Map every mandatory MRS requirement to a component, test or protocol, evidence artifact, and acceptance criterion.
Give derived technical requirements stable identifiers such as MTS-DATA-001 or MTS-ARCH-001.
Record the selected algorithm, equations, solver, architecture, data process, environment, and dependency versions.
Define invalid inputs, failures, unsupported domains, abstention, and recovery behavior.
Complete the Biosimulant-fit assessment without assuming that Biosimulant must be used.
Define the model-lock contents before accessing locked validation outcomes.
Obtain technical, scientific, validation, security, operational, and intended-use approval as applicable.
Keep the approved MRS, MTS, locked artifacts, tests, validation evidence, and release decision together.
MRS-to-MTS Traceability
The traceability matrix is the backbone of the MTS.

MRS requirement
Component or design decision
Test or protocol
Evidence
Acceptance criterion
MRS identifier
Implementation responsible for satisfying it
Stable test or protocol identifier
Report, log, dataset, or review artifact
Unchanged criterion from the MRS


Traceability may group consecutive requirements only when the implementation, test, and evidence genuinely apply to every requirement in the range.

If the implementation cannot satisfy an approved requirement, do not quietly change the threshold in the MTS. Return the issue to the MRS owner for review and formal change control.
Biosimulant-Fit Assessment
Every MTS must assess whether Biosimulant is technically appropriate. There are four valid outcomes.

Outcome
Meaning
Required treatment
Native fit
The model naturally benefits from typed temporal or finite components, wiring, inspection, snapshots, scenarios, or shared delivery
Define BioModules, BioSignals, invocation policies, BioWorld timing where applicable, Lab wiring, manifests, packaging, execution, and tests
Adapter fit
The authoritative model remains in a domain-native format, but a frozen component benefits from a Biosimulant wrapper
Define the authoritative artifact, adapter, typed ports, parity tests, packaging, and limitations
External boundary
The core workflow belongs in another runtime, but a versioned import, export, scoring, or inspection boundary may be useful
Define the external stack, authoritative artifacts, exchange schema, ownership, and boundary versioning
Not suitable
Biosimulant adds no justified value for the standalone model
Name the better-suited stack, reproducibility controls, operational approach, and reassessment trigger


Only native-fit and adapter-fit outcomes require BioModule, BioSignal, BioWorld, model.yaml, lab.yaml, Lab packaging, and Biosimulant execution details.

Biosimulant should not be forced into GPU-native generation pipelines, one-off statistical analyses, specialized scientific runtimes, or file-oriented workflows when it does not improve composition, inspection, reuse, provenance, or delivery.

Platform fit does not demonstrate scientific correctness. Scientific validity remains governed by the MRS and its validation evidence.
Technical Quality Rules
Begin with the approved MRS, not with a preferred algorithm or platform.
Preserve the scientific meaning, units, ranges, time bases, and coordinate systems of every input and output.
Separate authoritative scientific artifacts from adapters, packages, and presentation layers.
Enforce donor, gene, sequence-family, batch, plate, site, and time partitions before preprocessing or model fitting.
Prevent locked validation and prospective outcomes from entering training, calibration, feature selection, or threshold tuning.
Version data manifests, preprocessing, equations, parameters, weights, thresholds, dependencies, and environments.
Define randomness, seeds, determinism limits, numerical tolerances, and acceptable cross-runtime differences.
Treat uncertainty as part of the output contract.
Define machine-readable statuses for invalid input, out-of-domain input, failed execution, nonidentifiable estimates, infeasible searches, and abstention.
Test scientific invariants in addition to software correctness.
Include unit, integration, numerical, scientific-behavior, regression, performance, and acceptance tests as applicable.
Keep external training, calibration, generation, or fitting workflows explicit when the released model contains only frozen inference or simulation artifacts.
Define model-lock contents before validation.
Define release, monitoring, rollback, recalibration, revalidation, and retirement procedures.
Do not claim that successful packaging, reproducible execution, or passing software tests proves biological validity.
Verification and Validation
The MTS should distinguish technical verification from scientific validation.
Technical Verification
Technical verification asks whether the implementation behaves as designed. It may include:

Schema and boundary tests
Unit and conversion tests
Component and integration tests
Solver and numerical-stability tests
Native-runtime and adapter-parity tests
Snapshot and restore tests
Determinism and seed-reproduction tests
Failure-injection tests
Performance and cost benchmarks
Clean-environment reproduction
Package validation and execution
Scientific Validation
Scientific validation asks whether the locked model satisfies the MRS. It may include:

Locked retrospective validation
External-dataset validation
Held-out perturbation validation
Calibration and uncertainty evaluation
Prospective biological experiments
Confirmatory optimization studies
Identifiability and sensitivity analysis
Assay and estimand validation

Passing technical verification is necessary but does not replace scientific validation.
Model Lock and Release
Before locked validation, freeze every artifact that can affect the result:

Source revision
Equations or architecture
Parameters, weights, and thresholds
Preprocessing and feature definitions
Data and partition manifests
Solver and numerical configuration
Random seeds or sampling rules
Environment and dependency lock
Input and output schemas
Domain and failure rules
Adapter and package versions
Validation protocol and analysis plan

Release requires:

Complete MRS traceability
Passing mandatory technical tests
Passing required MRS validation gates
Reproduction in the declared environment
Approved interpretation and limitations
Monitoring and operational ownership
A rollback or withdrawal procedure
Monitoring and Change Control
Monitor the properties relevant to the model type and intended use, such as:

Input-domain drift
Outcome performance
Calibration or interval coverage
Failure, abstention, and out-of-domain rates
Solver or numerical warnings
Constraint violations
Scenario or branch failures
Reference-control behavior
Runtime, throughput, memory, and cost
Dependency and environment compatibility

Return to the MTS when the requirement is unchanged but the implementation, architecture, fitting method, packaging, or operational process changes.

Return to the MRS when the intended use, supported domain, biological endpoint, required inputs, output interpretation, acceptance criteria, or permitted decision changes.

Material changes require an impact assessment, a new model version, and validation proportional to the risk.
Status of the Examples
The six paired examples are implementation-ready technical specifications for illustrative projects. They demonstrate:

Direct traceability to adjacent MRS requirements
Appropriate architecture and model-specific methods
Input, output, uncertainty, and error contracts
Diagrams, schemas, commands, and tests
Biosimulant native, adapter, external, and not-suitable decisions
Model-lock, release, monitoring, and change-control procedures

They do not provide runnable model repositories and are not reports that the specified models were built, validated, released, or scientifically successful.

Project-specific algorithms, thresholds, sample counts, resource limits, and acceptance targets are illustrative requirements unless explicitly supported by a cited source.
Relationship to Other Documents
Artifact
Main question
Biological Brief
Why does the scientific problem matter?
Assay / Data Specification
How will observations and ground truth be generated and governed?
Model Requirements Specification
What must the model do, where must it work, and what evidence will prove it?
Modeling Technical Specification
How will the approved requirements be implemented, verified, delivered, and maintained?
Validation Protocol
Exactly how will the locked model and prospective experiment be executed and analyzed?
Verification Report
Did the implementation pass its technical tests?
Validation Report
Did the locked model satisfy the MRS acceptance criteria?
Release Record
What was approved, delivered, and placed under monitoring?
Change or Retirement Record
What changed, why was it revalidated, or why was it withdrawn?


These may be separate controlled documents or linked sections. The MRS remains the source of truth for model acceptance, while the MTS remains the source of truth for the approved technical implementation.
