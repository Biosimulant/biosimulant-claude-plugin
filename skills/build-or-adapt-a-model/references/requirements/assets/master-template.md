DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Model Requirements Specification Template
Model Requirements Specification: {{Model or Project Name}}
TEMPLATE INSTRUCTION: Complete the common core, keep every applicable model-type module, and delete all unused modules and instructional text before approval. A hybrid model may retain multiple modules. Replace every {{placeholder}} with project content or Not applicable plus a reason.
1. Document Control
Field
Value
MRS identifier
{{MRS identifier}}
Version
{{Version}}
Status
Draft / In review / Approved / Superseded
Owning program
{{Program}}
Model owner
{{Name and role}}
Scientific owner
{{Name and role}}
Validation owner
{{Name and role}}
Intended-use owner
{{Name and role}}
Created
{{YYYY-MM-DD}}
Last revised
{{YYYY-MM-DD}}
Related biological brief
{{Link or identifier}}
Related assay / data specification
{{Link or identifier}}
Related technical specification
{{Link or identifier, if available}}
Related validation protocol
{{Link or identifier, if available}}

Contributors and Reviewers
Role
Name
Responsibility
Wet-lab scientist
{{Name}}
Biological question, assay feasibility, and ground truth
Computational scientist
{{Name}}
Model requirements, metrics, and analysis validity
Data owner
{{Name}}
Data provenance, permissions, and quality
Engineer
{{Name}}
Interface, runtime, and reproducibility constraints
Intended user
{{Name}}
Decision workflow and usability
Independent reviewer
{{Name}}
Scientific and validation challenge

Approval
Approver
Approval scope
Decision
Date
Evidence
{{Name}}
Scientific validity
Pending / Approved / Rejected
{{Date}}
{{Link}}
{{Name}}
Data and assay readiness
Pending / Approved / Rejected
{{Date}}
{{Link}}
{{Name}}
Validation and acceptance
Pending / Approved / Rejected
{{Date}}
{{Link}}
{{Name}}
Intended use
Pending / Approved / Rejected
{{Date}}
{{Link}}

Revision History
Version
Date
Author
Material change
Approval impact
{{0.1}}
{{Date}}
{{Name}}
{{Change}}
{{None / Re-review required}}

2. Executive Summary
Biological problem: {{One-paragraph description of the real system and unmet need}}
Model job: Predictive / ML, mechanistic, generative, optimization, simulation / digital twin, statistical estimation, or a named combination
Given: {{Information available at the time of use}}
The model must: {{Observable result or action}}
So that: {{Decision, experiment, or intervention supported}}
Primary user: {{Role}}
Primary success criterion: {{One biological definition of done}}
Explicit non-use: {{A plausible use that is prohibited or unsupported}}
3. Biological Objective and Intended Use
3.1 Biological System
Organism, tissue, cell type, strain, construct, molecule, process, or ecosystem: {{Definition}}
Spatial scale: {{Molecular / cellular / tissue / organism / population / process}}
Temporal scale: {{Instantaneous, time horizon, and resolution}}
Experimental or operational context: {{Context}}
Reference condition: {{Condition against which changes are interpreted}}
3.2 Scientific Question or Hypothesis
{{State a falsifiable question or a precise estimation, prediction, simulation, design, or decision objective.}}
3.3 Intended Decision
Item
Definition
Decision supported
{{Decision}}
Decision maker
{{Role}}
Decision point
{{When in the workflow}}
Available alternatives
{{What can be selected or changed}}
Cost of false positive
{{Scientific or operational consequence}}
Cost of false negative
{{Scientific or operational consequence}}
Human review
{{Required review before action}}

3.4 Intended Use and Non-Use
Intended population or domain: {{Definition}}
Intended environment: {{Research, process development, manufacturing support, or another context}}
Permitted decisions: {{List}}
Prohibited decisions: {{List}}
Claims this model is not designed to support: {{List}}
4. Model Definition and Scope
4.1 Model Job
Selected type or types: {{Type list}}
Unit of prediction, estimation, simulation, generation, or optimization: {{Exact unit}}
One model invocation represents: {{Definition}}
Required operating mode: Batch / interactive / streaming / scheduled / scenario run
4.2 System Boundary
In scope
Out of scope
{{Included biology, conditions, and decisions}}
{{Excluded biology, conditions, and decisions}}

4.3 Assumptions
ID
Assumption
Basis
Consequence if false
Test or monitor
ASM-001
{{Assumption}}
{{Evidence or rationale}}
{{Impact}}
{{Check}}

4.4 Dependencies
Dependency
Owner
Required state
Failure response
{{Assay, dataset, reference model, service, or expertise}}
{{Owner}}
{{Requirement}}
{{Response}}

5. Inputs
5.1 Input Contract
ID
Input
Biological meaning
Type / format
Unit
Allowed range or vocabulary
Required?
Timing
MRS-IN-001
{{Input}}
{{Meaning}}
{{Schema}}
{{Unit}}
{{Range}}
Yes / No
{{Availability}}

5.2 Input Quality and Validation
Identity checks: {{Sample, sequence, construct, subject, batch, or sensor identity checks}}
Range and unit checks: {{Rules}}
Missing-data policy: {{Permitted missingness, imputation, rejection, and missingness indicators}}
Replicate handling: {{Biological and technical replicate rules}}
Batch and site metadata: {{Required fields}}
Outlier handling: {{Predeclared rules}}
Invalid input response: Reject / warn / continue with restricted claim, with {{required message and audit record}}
Out-of-domain response: {{Detection method and safe behavior}}
6. Outputs
6.1 Output Contract
ID
Output
Meaning
Type / format
Unit
Range
Resolution
Required uncertainty
MRS-OUT-001
{{Output}}
{{Meaning}}
{{Schema}}
{{Unit}}
{{Range}}
{{Resolution}}
{{Interval, distribution, confidence, or none with reason}}

6.2 Interpretation and Failure Responses
Interpretation guidance: {{How a user should read the output}}
Decision threshold or ranking rule: {{Rule}}
Abstention or no-result condition: {{Condition}}
Warning states: {{Conditions}}
Failed run output: {{Machine-readable status and user-facing explanation}}
Unsupported extrapolation: {{How it is marked}}
Required audit information: {{Model version, data version, time, parameters, random seed, and provenance}}
7. Data, Assay, and Evidence Specification
7.1 Data Sources
Source
Purpose
Population / system
Assay or acquisition method
Size
Provenance
Permission
Version
{{Source}}
Development / calibration / validation / monitoring
{{Definition}}
{{Method}}
{{N and unit}}
{{Origin}}
{{Basis}}
{{Version}}

7.2 Experimental Design
Experimental unit: {{Definition}}
Biological replicates: {{Number and independence definition}}
Technical replicates: {{Number and aggregation rule}}
Positive controls: {{Definition}}
Negative or vehicle controls: {{Definition}}
Reference standard: {{Definition}}
Randomization: {{Method}}
Blinding: {{Method or reason not used}}
Batch structure: {{Plates, runs, instruments, operators, sites, and dates}}
Assay dynamic range and detection limits: {{Values}}
Destructive measurements: {{Measurements and consequence}}
Expected noise and error sources: {{List}}
7.3 Data Quality Gates
ID
Gate
Threshold
Scope
Failure handling
MRS-DQ-001
{{Gate}}
{{Numeric or categorical threshold}}
{{Sample / plate / batch / dataset}}
Exclude / repeat / investigate / retain with flag

7.4 Data Partitioning and Leakage Control
Grouping unit that must not cross partitions: {{Donor, subject, gene, sequence family, construct, plate, batch, site, or time block}}
Development partition: {{Definition}}
Validation partition: {{Definition}}
Locked test partition: {{Definition}}
External or prospective set: {{Definition}}
Duplicate and near-duplicate detection: {{Method and threshold}}
Preprocessing learned from development data only: {{List}}
8. Ground Truth or Estimand
Target quantity: {{Exact definition}}
Biological or statistical meaning: {{Meaning}}
Measurement procedure: {{Assay, sampling time, normalization, and calculation}}
Unit and reference frame: {{Definition}}
Label or endpoint window: {{Definition}}
Adjudication rule: {{How disagreements or ambiguous cases are resolved}}
Censoring, detection-limit, and missing endpoint policy: {{Rule}}
Known limitations of ground truth: {{Noise, proxy status, bias, and instability}}
9. Generalization Domain
Dimension
Represented in development
Must generalize to
Not supported
Biological entity
{{Genes, donors, sequences, strains, or other entities}}
{{Unseen domain}}
{{Excluded domain}}
Experimental batch
{{Batches}}
{{Future batches}}
{{Excluded conditions}}
Assay / instrument
{{Methods}}
{{Methods}}
{{Unsupported methods}}
Site / operator
{{Sites}}
{{Sites}}
{{Unsupported sites}}
Time
{{Period}}
{{Future period}}
{{Unsupported horizon}}


Define the evidence required for every generalization claim: {{Holdout, external dataset, prospective experiment, perturbation, or stress test}}.
10. Performance Requirements
10.1 Baselines
Baseline
Why it is credible
Evaluation data
Required comparison
{{Current method, null model, published method, or human practice}}
{{Rationale}}
{{Partition}}
{{Superiority, noninferiority, or descriptive comparison}}

10.2 Metrics and Thresholds
Requirement ID
Metric
Estimation unit
Acceptance threshold
Confidence / uncertainty rule
Key strata
MRS-PERF-001
{{Metric}}
{{Sample, group, run, or candidate}}
{{Numeric threshold}}
{{Interval or resampling rule}}
{{Predeclared strata}}

10.3 Operational Requirements
Requirement ID
Requirement
Threshold
Measurement method
MRS-OPS-001
Runtime
{{Threshold and hardware}}
{{Benchmark method}}
MRS-OPS-002
Reproducibility
{{Tolerance across reruns}}
{{Comparison}}
MRS-OPS-003
Availability or throughput
{{Threshold}}
{{Test}}

11. Validation Plan
11.1 Retrospective Computational Validation
Locked artifact: {{Model, parameters, preprocessing, dependencies, and decision thresholds}}
Locked dataset: {{Identifier and checksum}}
Analysis plan: {{Metrics, strata, confidence intervals, multiplicity, and missingness}}
Reviewer: {{Independent reviewer}}
Evidence artifact: {{Report, tables, predictions, and logs}}
11.2 External Validation
Source and independence: {{Definition}}
Compatibility checks: {{Assay, unit, endpoint, and population alignment}}
Prespecified exclusions: {{Rules}}
Required result: {{Acceptance criterion}}
11.3 Prospective Biological Validation
Study objective: {{Objective}}
Candidate or condition selection rule: {{Locked rule}}
Experimental design: {{Samples, controls, replicates, randomization, and blinding}}
Primary endpoint: {{Endpoint}}
Success criterion: {{Biological definition of done}}
Failure interpretation: {{What will and will not be concluded}}
11.4 Stress, Robustness, and Negative Controls
Input perturbations: {{Tests}}
Batch and measurement shifts: {{Tests}}
Negative controls: {{Tests}}
Ablations: {{Tests}}
Boundary and failure-mode tests: {{Tests}}
12. Acceptance and Traceability
Requirement ID
Requirement
Verification method
Evidence artifact
Owner
Acceptance criterion
Status
MRS-001
{{Requirement}}
Analysis / inspection / test / prospective experiment
{{Artifact}}
{{Owner}}
{{Criterion}}
Not tested / Pass / Fail / Waived

Definition of Done
The model is accepted only when:

{{All mandatory requirements that must pass}}
{{Permitted waivers and approval authority}}
{{Required prospective biological outcome}}
{{Documentation, reproducibility, and handoff conditions}}
13. Constraints, Risks, and Governance
13.1 Constraints
Area
Constraint
Sample and assay capacity
{{Constraint}}
Cost
{{Constraint}}
Runtime and infrastructure
{{Constraint}}
Interpretability
{{Constraint}}
Data rights and privacy
{{Constraint}}
Biosafety and ethics
{{Constraint}}
Deployment environment
{{Constraint}}

13.2 Risk Register
Risk ID
Risk
Likelihood
Impact
Detection
Mitigation
Owner
RSK-001
{{Risk}}
Low / Medium / High
Low / Medium / High
{{Signal}}
{{Action}}
{{Owner}}

13.3 Change Control
Changes to intended use, biological endpoint, supported domain, ground truth, required inputs, decision thresholds, or acceptance criteria require a new MRS version and renewed approval. Define the change authority and impact assessment process: {{Process}}.
14. Reproducibility, Deliverables, and Handoff
14.1 Reproducibility
Source code and revision: {{Repository and commit}}
Data manifest and checksums: {{Artifact}}
Environment: {{Lockfile, image, or environment specification}}
Randomness: {{Seed and nondeterminism policy}}
Configuration: {{Versioned configuration artifact}}
Rerun command or workflow: {{Reference}}
Numerical tolerance: {{Expected tolerance and platform}}
14.2 Deliverables
Deliverable
Required content
Format
Owner
Acceptance check
Model artifact
{{Weights, equations, parameters, or solver configuration}}
{{Format}}
{{Owner}}
{{Check}}
Code or pipeline
{{Content}}
{{Format}}
{{Owner}}
{{Check}}
Validation package
{{Predictions, analysis, report, and raw evidence}}
{{Format}}
{{Owner}}
{{Check}}
User interface
{{API, CLI, notebook, application, or none}}
{{Format}}
{{Owner}}
{{Check}}
Documentation
{{Model card, user guide, data dictionary, and limitations}}
{{Format}}
{{Owner}}
{{Check}}
Optional Biosimulant artifact
{{Portable Lab, package, or runtime adapter if requested}}
{{Format}}
{{Owner}}
{{Check}}

14.3 Handoff and Maintenance
Operational owner after acceptance: {{Owner}}
User training: {{Requirement}}
Monitoring inputs and outcomes: {{Signals}}
Review frequency: {{Cadence}}
Recalibration or retraining trigger: {{Trigger}}
Retirement trigger: {{Trigger}}
Incident and rollback process: {{Process}}
15. Model-Specific Modules
TEMPLATE INSTRUCTION: Keep every applicable module and delete the others. If multiple modules are retained, identify which component each requirement applies to and describe how component-level evidence supports the end-to-end acceptance criterion.
15A. Predictive / ML Module
KEEP THIS MODULE IF the model predicts a label, probability, rank, continuous outcome, event, or future state from observed features. Delete this module otherwise.

Target variable and prediction horizon: {{Definition}}
Feature availability at inference time: {{Definition}}
Training examples and sampling unit: {{Definition}}
Class balance or target distribution: {{Definition}}
Known leakage paths: {{Subjects, genes, sequence families, plates, batches, post-outcome variables, or duplicates}}
Baseline predictors: {{Simple and published baselines}}
Split strategy: {{Group-aware, temporal, external, or prospective}}
Discrimination or error metrics: {{Metrics}}
Ranking metrics: {{Metrics if ranking is intended}}
Calibration requirement: {{Metric, bins, strata, and threshold}}
Uncertainty or abstention: {{Method and required behavior}}
Interpretability requirement: {{Global and case-level explanation}}
Fairness or subgroup analysis: {{Scientifically relevant strata}}
Retraining trigger: {{Data volume, drift, assay change, or performance decline}}

Requirement ID
Predictive requirement
Acceptance criterion
MRS-ML-001
{{Requirement}}
{{Threshold on locked, leakage-controlled data}}

15B. Mechanistic Module
KEEP THIS MODULE IF explicit biological entities, interactions, reactions, transport processes, or causal mechanisms are part of what the model must represent. Delete this module otherwise.

Required entities and compartments: {{List}}
Required reactions or interactions: {{List}}
Mathematical formalism: ODE / PDE / stochastic process / rule-based / constraint-based / agent-based / other
State variables and units: {{List}}
Observables and mapping from states: {{Definition}}
Rate laws and kinetic assumptions: {{Definition}}
Initial conditions: {{Definition and source}}
Boundary conditions: {{Definition}}
Parameter sources: {{Measured, literature, fitted, or assumed}}
Conservation and physical constraints: {{Mass, charge, occupancy, nonnegativity, or other constraints}}
Parameter identifiability requirement: {{Structural and practical checks}}
Sensitivity analysis: {{Local, global, and output of interest}}
Required interventions and counterfactuals: {{Perturbations}}
Mechanisms intentionally omitted: {{List and expected consequence}}
Solver accuracy, stability, and stiffness requirements: {{Thresholds}}

Requirement ID
Mechanistic requirement
Acceptance criterion
MRS-MECH-001
{{Requirement}}
{{Structural, numerical, or experimental criterion}}

15C. Generative Module
KEEP THIS MODULE IF the model proposes new biological sequences, structures, molecules, constructs, protocols, or other candidate designs. Delete this module otherwise.

Generation target: {{Candidate type}}
Conditioning information: {{Target, motif, phenotype, geometry, or other condition}}
Design space: {{Alphabet, length, topology, composition, and permitted operations}}
Hard constraints: {{Rules that no released candidate may violate}}
Soft objectives: {{Properties to optimize or rank}}
Invalid output definition and handling: {{Definition}}
Novelty requirement: {{Reference corpus, similarity method, and threshold}}
Diversity requirement: {{Pairwise or cluster-based threshold}}
Memorization check: {{Method}}
Scoring and ranking funnel: {{Stages and locked thresholds}}
Manufacturability or experimental feasibility: {{Rules}}
Safety and prohibited sequence or structure checks: {{Rules}}
Number of raw, filtered, selected, and tested candidates: {{Counts}}
Prospective experimental hit definition: {{Assay and threshold}}

Requirement ID
Generative requirement
Acceptance criterion
MRS-GEN-001
{{Requirement}}
{{Constraint, diversity, or experimental criterion}}

15D. Optimization Module
KEEP THIS MODULE IF the model recommends the best feasible settings, formulation, schedule, allocation, intervention, or design under explicit objectives and constraints. Delete this module otherwise.

Decision variables: {{Names, units, types, and bounds}}
Fixed parameters: {{Definition}}
Objective function or functions: {{Direction, scale, and weighting}}
Hard constraints: {{Feasibility conditions}}
Soft constraints and penalties: {{Definition}}
Feasible region and known forbidden combinations: {{Definition}}
Competing objectives: {{Trade-offs and selection rule}}
Baseline policy or formulation: {{Definition}}
Optimality tolerance and stopping rule: {{Definition}}
Robustness to measurement and parameter uncertainty: {{Perturbation analysis}}
Infeasible problem response: {{Diagnostic and fallback}}
Confirmatory experiment: {{Design and biological success criterion}}

Requirement ID
Optimization requirement
Acceptance criterion
MRS-OPT-001
{{Requirement}}
{{Feasibility, improvement, or robustness criterion}}

15E. Simulation / Digital Twin Module
KEEP THIS MODULE IF the model represents the evolving state of a specific system, is initialized or updated from observations, and supports forecasts or scenario comparisons over time. Delete this module otherwise.

Physical or biological asset represented: {{Definition}}
State variables: {{Names and units}}
Static attributes: {{Definition}}
Exogenous inputs and interventions: {{Definition}}
Initialization procedure: {{Required observations and method}}
State-update or data-assimilation procedure: {{Method and cadence}}
Simulation horizon and time step: {{Definition}}
Spatial resolution: {{Definition or not applicable}}
Forecast outputs: {{Definition}}
Scenario library: {{Required interventions and disturbances}}
Personalization or batch-specific parameters: {{Definition}}
Numerical validity checks: {{Nonnegativity, balances, solver convergence, and event handling}}
Forecast accuracy by horizon: {{Metrics and thresholds}}
Uncertainty propagation: {{Sources and required intervals}}
Synchronization, stale-data, and sensor-failure behavior: {{Rules}}
Drift, recalibration, and reset triggers: {{Rules}}
Decisions explicitly excluded from autonomous control: {{List}}

Requirement ID
Digital-twin requirement
Acceptance criterion
MRS-DT-001
{{Requirement}}
{{State, forecast, scenario, or update criterion}}

15F. Statistical Estimation Module
KEEP THIS MODULE IF the primary output is an estimate of an effect, parameter, latent state, distribution, association, or uncertainty from noisy observations. Delete this module otherwise.

Estimand: {{Exact population, treatment or exposure, endpoint, contrast, and summary measure}}
Sampling design: {{Definition}}
Statistical model: {{Likelihood, link, fixed effects, random effects, or nonparametric method}}
Covariates and adjustment set: {{Definition and rationale}}
Confounders and selection mechanisms: {{Definition}}
Replicate and hierarchical structure: {{Definition}}
Missing-data mechanism and treatment: {{Assumptions and method}}
Censoring and detection limits: {{Method}}
Prior distributions, if Bayesian: {{Definition and sensitivity}}
Point estimate and interval: {{Confidence, credible, or prediction interval}}
Model diagnostics: {{Residual, influence, convergence, calibration, or posterior checks}}
Identifiability and estimability: {{Checks and failure response}}
Multiplicity: {{Family and adjustment method}}
Sensitivity analyses: {{Alternative assumptions and models}}
Reporting rules for failed or noninformative estimates: {{Definition}}

Requirement ID
Estimation requirement
Acceptance criterion
MRS-EST-001
{{Requirement}}
{{Bias, precision, coverage, diagnostic, or reproducibility criterion}}

16. Milestones and Responsibilities
Milestone
Entry criterion
Exit criterion
Owner
Target date
Requirements approval
{{Criterion}}
Approved MRS
{{Owner}}
{{Date}}
Data readiness
{{Criterion}}
Data quality gates passed
{{Owner}}
{{Date}}
Model lock
{{Criterion}}
Versioned model and analysis plan frozen
{{Owner}}
{{Date}}
Retrospective validation
{{Criterion}}
Required evidence accepted
{{Owner}}
{{Date}}
Prospective validation
{{Criterion}}
Biological success criterion evaluated
{{Owner}}
{{Date}}
Handoff
{{Criterion}}
Deliverables accepted and owner trained
{{Owner}}
{{Date}}

17. Open Questions and Decisions
Open Questions
ID
Question
Decision impact
Owner
Due date
Status
OQ-001
{{Question}}
{{Impact}}
{{Owner}}
{{Date}}
Open / Resolved

Decision Log
ID
Date
Decision
Alternatives considered
Rationale
Approver
DEC-001
{{Date}}
{{Decision}}
{{Alternatives}}
{{Rationale}}
{{Name}}

18. References and Glossary
References
{{Primary scientific, assay, dataset, standard, or software reference}}
Glossary
Term
Project-specific definition
{{Term}}
{{Definition}}



Visualization delivery
{{Expected user-facing views, source outputs, labels and units, caveats, renderer/lifecycle/artifact design where applicable, executable acceptance checks, and reasons for any opt-out. Almost every scientific Lab requires a meaningful visual.}}
