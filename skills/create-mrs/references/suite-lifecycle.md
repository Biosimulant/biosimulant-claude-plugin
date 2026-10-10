Biosimulant Model Specification Suite and Lifecycle
Purpose
This suite gives wet-lab scientists, computational scientists, model developers, engineers, validation owners, and intended users one path from a biological question to an accepted, reproducible, monitored model.

Every completed example keeps two documents together:

mrs: the Model Requirements Specification defines what the model must do, where it must work, and what evidence will prove it.
mts: the Modeling Technical Specification defines how the approved requirements will be implemented, verified, delivered, and maintained.

The MRS remains the source of truth for acceptance. The MTS may choose any scientifically and operationally credible implementation that satisfies it.
Files
Reusable Templates
Generic MRS Template - Model Requirements Specification template
Generic MTS Template -  Modeling Technical Specification template

Completed Paired Examples
Model and project
Biosimulant fit decision
Predictive / ML: CRISPR guide activity
Adapter fit for frozen inference
Mechanistic: MAPK/ERK signaling
Adapter fit through SBML or a custom ODE module
Generative: protein binder design
External generation workflow with a defined boundary
Optimization: CHO media formulation
Adapter fit for the frozen optimizer
Simulation / digital twin: CHO fed-batch culture
Native fit
Statistical estimation: concentration-response IC50
Not suitable as a standalone Lab

How to Use the Suite
Copy both templates into one project folder as mrs and mts.
Complete and approve the MRS before treating implementation as authorized.
Keep every applicable model-type module in both documents and delete unused modules.
Give each testable requirement a stable MRS-* identifier.
Map every requirement to a component, implementation decision, test, and evidence artifact in the MTS.
Perform the Biosimulant fit assessment. Do not assume Biosimulant is the correct runtime.
Freeze the model and validation protocol before accessing locked test or prospective outcomes.
Record acceptance against the MRS, not against whether the chosen implementation was completed.
Keep the approved MRS, MTS, validation evidence, model artifact, environment, and decision log together for the model version.
Full Model Lifecycle
flowchart TD
    A["Biological Brief"] --> B["Assay and Data Specification"]
    B --> C["Model Requirements Specification"]
    C --> D{"MRS approved?"}
    D -->|No| C
    D -->|Yes| E["Modeling Technical Specification and platform-fit decision"]
    E --> F{"Data and assay ready?"}
    F -->|No| B
    F -->|Yes| G["Build and verification"]
    G --> H["Model lock and validation-protocol freeze"]
    H --> I["Retrospective and external validation"]
    I --> J{"Computational gates pass?"}
    J -->|No| N["Failure analysis"]
    J -->|Yes| K["Prospective biological validation"]
    K --> L{"MRS acceptance criteria met?"}
    L -->|No| N
    L -->|Yes| M["Release and handoff"]
    N --> O{"Requirements changed?"}
    O -->|Yes| C
    O -->|No, implementation issue| E
    M --> P["Monitor and maintain"]
    P --> Q{"Change, drift, or failure?"}
    Q -->|Recalibrate or rebuild| E
    Q -->|Intended use changed| C
    Q -->|Retire| R["Retirement and archival"]
Lifecycle Stages and Gates
Stage
Primary artifact
Accountable owner
Entry gate
Exit gate
1. Biological Brief
Biological Brief
Scientific owner
A decision-relevant biological problem has been identified
Objective, intended decision, users, value, and exclusions are clear
2. Assay and Data Specification
Assay / Data Specification
Assay and data owners
The biological objective requires measurable evidence
Ground truth, units, controls, replication, metadata, quality gates, provenance, and access are executable
3. Model requirements
Approved mrs.md
Scientific and intended-use owners
Biological and evidence definitions are stable enough to specify
Inputs, outputs, domain, performance, validation, constraints, and biological definition of done are approved
4. Technical design
Approved mts.md
Model owner
MRS is approved
Architecture, data flow, implementation, uncertainty, tests, delivery, and platform fit trace to the MRS
5. Data readiness
Data-readiness report
Data owner
Assay and technical design are approved
Required data exist, permissions and versions are recorded, and quality and leakage gates pass
6. Build and verification
Development model and verification report
Model owner
Data and environment are ready
Code, equations, interfaces, numerical behavior, scientific invariants, and reproducibility tests pass
7. Model lock
Locked model and validation protocol
Validation owner
Candidate implementation passes verification
Code, parameters, weights, preprocessing, thresholds, environment, datasets, and analysis plan are frozen
8. Retrospective and external validation
Validation report
Independent validation owner
Model and protocol are locked
Required metrics, strata, baselines, robustness, and uncertainty gates pass on untouched evidence
9. Prospective validation
Prospective protocol and report
Scientific owner
Computational validation passes
Prespecified biological outcomes are evaluated without post-selection changes
10. Acceptance
Acceptance and traceability record
Intended-use owner
All mandatory evidence is available
Every MRS requirement is pass, fail, or formally waived and the release decision is recorded
11. Release and handoff
Versioned delivery package
Operational owner
Acceptance is granted
Users can run, interpret, reproduce, monitor, and safely reject unsupported results
12. Monitoring and change control
Monitoring record and change requests
Operational and model owners
Model is in intended use
Drift, failures, new data, assay changes, and user feedback are reviewed at the approved cadence
13. Retirement
Retirement and archive record
Intended-use owner
Replacement, invalidation, or end of need is confirmed
Access is withdrawn, dependencies are recorded, and artifacts and evidence remain auditable

Required Freezes
Requirements Freeze
Approve the MRS before optimizing the model. If the intended use, endpoint, supported domain, or biological success criterion changes, version and reapprove the MRS.
Model Freeze
Freeze code, equations or architecture, parameters or weights, feature and preprocessing pipeline, thresholds, dependency environment, and model version before locked validation.
Validation Freeze
Freeze exclusions, candidate-selection rules, metrics, strata, confidence-interval method, statistical analysis, assay protocol, and success criteria before opening locked test outcomes or starting prospective experiments.
Failure and Change Rules
Do not repeatedly tune against the locked test set or prospective experiment.
Classify failure as requirements, assay, data, implementation, model capability, domain shift, or operational failure.
Return to the MTS when the requirement is unchanged but the implementation failed.
Return to the MRS when intended use, supported domain, endpoint, required inputs, output interpretation, or acceptance criteria change.
Create a new locked validation set or prospective protocol after a material model revision.
Preserve failed results and attempted candidates. Do not silently redefine denominators or exclusions.
Lightweight and Full Paths
Lightweight Path
Use a shortened MRS and MTS for a low-risk, bounded model such as a single 4PL concentration-response fit. The documents may be concise, but they must still define the estimand, data rules, diagnostics, uncertainty, failed-fit behavior, reproducibility, and acceptance.
Full Path
Use the complete lifecycle for models that select costly experiments, generate new biological candidates, combine multiple components, update over time, support consequential decisions, or operate across teams and environments.

The rigor should scale with scientific and operational consequence, not with whether the implementation uses machine learning.
Biosimulant Context
Biosimulant exists to make heterogeneous biological models easier to compose, package, execute, inspect, and share. It does not replace SBML, CellML, NeuroML, ONNX, scientific Python, statistical software, or specialized workflow systems.

The current technical concepts are:

BioModule: one runnable component with declared inputs and outputs.
Model package: a BioModule source tree described by model.yaml.
BioSignal: a typed value exchanged across named ports.
BioWorld: the local communication-step orchestration kernel.
Lab: a versioned graph of models, public inputs and outputs, wiring, and runtime settings described by lab.yaml.
Studio: the web and desktop workbench for composing and inspecting Labs.
Hub: the registry for versioned Labs and model packages.
Developer API: managed execution for accessible, versioned Hub Labs.
Fit Outcomes
Outcome
Meaning
Required technical treatment
Native fit
The model is naturally expressed as one or more typed temporal or finite components
Specify BioModules, signals, invocation policy, world timing where applicable, Lab wiring, state, packaging, and execution
Adapter fit
The scientific model is built in a domain stack, but a frozen component benefits from a Biosimulant wrapper
Keep the authoritative artifact in its domain format and specify the adapter, ports, packaging, tests, and limitations
External boundary
The core workflow belongs in another runtime, but an import, export, scoring, inspection, or composition boundary is useful
Specify the external stack and the versioned exchange contract; do not wrap the core merely for uniformity
Not suitable
Biosimulant provides no justified value for the standalone model
Name the selected alternative, reproducibility controls, and conditions that could justify future integration

Suitability Questions
Use Biosimulant when the answer to several of these questions is yes:

Does the workflow contain reusable components with stable typed interfaces?
Do components exchange signals, execute at defined run phases, or advance through simulation time?
Is explicit wiring, state inspection, snapshotting, or scenario branching valuable?
Should the same versioned model or Lab run locally, in CI, through a workbench, or as a managed job?
Would packaging and provenance materially improve reuse?

Prefer another tool when the work is primarily a one-off statistical analysis, model training pipeline, file-oriented ETL workflow, specialized HPC scheduler, or domain workflow whose native runtime already provides the correct execution and validation semantics.

Scientific correctness, model validation, and biological usefulness remain responsibilities of the project, irrespective of platform fit.
Biosimulant Technical References
Create and test a BioModule
Write a model manifest
Write a Lab manifest
Package and publish
Developer API
Quality Rules
Start from the biological decision and MRS, not from a preferred technology.
Keep scientific requirements separate from implementation choices.
Match data partitions to the claimed generalization domain.
Trace each MRS requirement to a component and verification artifact.
Use explicit units, time bases, coordinate systems, schemas, and failure statuses.
Treat uncertainty as part of the output contract.
Keep literature results separate from project-specific thresholds.
Do not claim that packaging, execution, or reproducibility proves biological validity.
Do not force Biosimulant into a workflow that is better served by another tool.
Status of the Examples
The paired examples are implementation-ready design documents for illustrative projects. They are not active commissioned studies, validated products, manufacturing controls, clinical systems, or reports that the stated outcomes have been achieved.
