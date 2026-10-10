DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Optimization MTS Example - CHO Media Formulation
Modeling Technical Specification: CHO Basal-Media Formulation Optimization
This is an implementation-ready illustrative technical design for research process development. It is not an implemented optimizer, manufacturing control, or report of achieved improvement.
1. Document Control
Field
Value
MTS identifier
EX-MTS-OPT-CHO-MEDIA-001
Version
1.0 example
Status
Illustrative, not approved for execution
MRS
EX-MRS-OPT-CHO-MEDIA-001
Scientific owner
Cell-culture process development lead
Model owner
Bioprocess modeling lead
Validation owner
Analytical development lead
Biosimulant fit
Adapter fit for a frozen optimizer

2. Technical Decision Summary
Fit outcome-specific Gaussian-process surrogate models in an external Python analysis pipeline using the 48-run development design. Generate a deterministic Sobol candidate pool inside the permitted formulation bounds, calculate posterior feasibility and outcome distributions, apply the MRS lexicographic decision rule, and lock the top recommendations.

Package the frozen surrogate models, transformations, constraint engine, cost table, candidate-pool generator, and ranking rule as one stateless Biosimulant adapter for repeatable scenario use. Experimental design, data curation, surrogate fitting, and confirmatory analysis remain external.
3. Architecture
flowchart LR
    A["Bioreactor and analytical data"] --> B["External QC and surrogate fitting"]
    B --> C["Locked surrogate bundle"]
    D["Bounds, constraints, and cost table"] --> E["Frozen optimizer adapter"]
    C --> E
    E --> F["Feasible candidate set and recommendations"]
    F --> G["Locked confirmatory selection manifest"]
    G --> H["Confirmatory bioreactor study"]
Components
Component
Responsibility
Technology
Data validator
Enforce run identity, reference controls, deviations, and endpoint completeness
Python and Pandera
Transform package
Convert eight multipliers to a scaled model vector and derived formulation properties
Versioned Python package
Surrogate fitter
Fit one Gaussian process per continuous outcome
scikit-learn GaussianProcessRegressor
Constraint engine
Evaluate deterministic and posterior feasibility
Pure Python with versioned rules
Candidate generator
Generate a reproducible Sobol pool and remove invalid formulations
SciPy quasi-Monte Carlo
Ranker
Apply feasibility, titer, cell-integral, and cost lexicographic rules
Pure Python
Optimizer adapter
Load frozen artifacts and return recommendations with uncertainty and margins
Custom BioModule

4. Data and Surrogate Implementation
Independent unit: complete bioreactor run.
Partition: entire inoculum and experimental block remain together.
Inputs: eight formulation multipliers plus measured osmolality, prepared-medium pH, inoculum block, and declared fixed-process metadata.
Outcomes: day-14 titer, integral viable-cell concentration, day-14 viability, peak lactate, peak ammonia, product-quality measures, and media cost.
Input transform: each multiplier scales to 0 to 1 using MRS bounds. Derived quantities use frozen ingredient and cost tables.
Outcome transform: center and scale from development runs; titer may use a declared log transform only if residual diagnostics justify it before locked validation.
Surrogate: Matérn 5/2 Gaussian process with automatic relevance determination and a white-noise term bounded by pure-error evidence.
Model fitting: ten optimizer restarts from fixed seeds. Failure to converge across restarts blocks release.
Whole-run cross-block validation selects kernel constraints and checks residual structure.
Candidate Search
Generate 262,144 Sobol points from a frozen scramble seed.
Transform points into the eight permitted multiplier ranges.
Apply deterministic bounds, osmolality, pH, precipitation, and cost rules where computable.
Predict all biological outcomes and posterior samples for retained candidates.
Keep candidates with at least 95 percent posterior feasibility under all biological constraints.
Require at least 10,000 feasible candidates or return INSUFFICIENT_FEASIBLE_SEARCH.
Treat predicted titer differences below 3 percent as practical ties.
Rank by titer, then integral viable-cell concentration, then cost.
Select three recommendations and two backups with the declared minimum formulation distance.
5. Interfaces and Failure Behavior
Input Record
{
  "surrogate_bundle": "cho-media-optimizer@1.0.0",
  "search_seed": 240819,
  "recommendation_count": 3,
  "backup_count": 2,
  "robustness_samples": 10000
}
Output Record
{
  "bundle_version": "1.0.0",
  "status": "ok",
  "feasible_candidates": 18421,
  "recommendations": [
    {
      "candidate_id": "formulation-sha256",
      "multipliers": {"X1": 1.1, "X2": 0.9, "X3": 1.2},
      "predicted_titer_relative": 1.18,
      "feasibility_probability": 0.97,
      "cost_relative": 1.06,
      "constraint_margins": {}
    }
  ]
}

The real record includes all eight multipliers and every constraint margin. An infeasible search returns violated constraints and no ranked recommendation. A missing or checksum-invalid surrogate, cost table, bounds file, or transform artifact returns EXECUTION_FAILED.
6. Biosimulant Fit and Realization
Decision
Question
Decision
Outcome
Adapter fit
Value
Reproducible execution of a frozen optimizer, typed recommendations, scenario inspection, and package provenance
Why training stays external
DOE analysis, residual review, and surrogate selection require specialized statistical workflows
Authoritative artifact
Frozen surrogate bundle, constraints, transforms, and ranking configuration
Time semantics
One-pass execution; BioWorld time has no biological meaning

model.yaml Excerpt
schema_version: "2.0"
title: "CHO Basal Media Optimizer"
description: "Runs a frozen constrained formulation optimizer."
standard: other
package: biosimulant/cho-media-optimizer
version: 1.0.0

biosim:
  entrypoint: "src.optimizer:ChoMediaOptimizer"
  communication_step: 1.0

io:
  inputs:
    - name: optimization_request
      signal_type: record
      schema:
        search_seed: integer
        recommendation_count: integer
        backup_count: integer
        robustness_samples: integer
  outputs:
    - name: recommendations
      signal_type: record
      schema:
        bundle_version: string
        status: string
        feasible_candidates: integer
        recommendations: array

runtime:
  python_version: "3.12"
  dependencies:
    packages:
      - numpy==1.26.4
      - scipy==1.12.0
      - scikit-learn==1.5.2
lab.yaml Excerpt
schema_version: "2.0"
title: "CHO Media Recommendation Lab"
description: "Generates robust recommendations from a locked surrogate bundle."
package: biosimulant/cho-media-recommendation
version: 1.0.0

io:
  inputs:
    - name: optimization_request
      maps_to: optimizer.optimization_request
  outputs:
    - name: recommendations
      maps_to: optimizer.recommendations

models:
  - path: models/cho-media-optimizer
    alias: optimizer
    parameters: {}

wiring: []

runtime:
  duration: 1.0
  communication_step: 1.0
  settle_steps: 0
Execution Commands
biosimulant labs validate ./cho-media-recommendation --strict --json
biosimulant labs run ./cho-media-recommendation --results-file recommendations.json --json --no-open
biosimulant labs package ./cho-media-recommendation --out dist
biosimulant labs validate dist/biosimulant__cho-media-recommendation-1.0.0.bsilab --json
7. MRS Traceability and Tests
MRS requirement
Technical implementation
Test or protocol
Verification evidence
MRS-OUT-001 to MRS-OUT-006
Feasibility, posterior predictions, Pareto data, ranking, and robustness records
OPT-T04 to OPT-T07
Output conformance report
MRS-DQ-001 to MRS-DQ-005
External data validator and deviation workflow
OPT-V01
Data-readiness report
MRS-OPT-001
Whole-run cross-block Gaussian-process evaluation
OPT-V02
Locked model-validation report
MRS-OPT-002
Posterior outcome status compared with held-out measured feasibility
OPT-V02
Feasibility report
MRS-OPT-003
Deterministic and posterior constraint engine
OPT-T01, OPT-T03, OPT-T04, OPT-T06
Constraint and robustness audit
MRS-OPT-004 to MRS-OPT-008
Locked selection manifest and confirmatory study
OPT-V03
Confirmatory validation report

Required Tests
OPT-T01: Validate every bound, unit, cost-table entry, and deterministic constraint.
OPT-T02: Reproduce the Sobol pool byte-for-byte from the frozen seed and generator version.
OPT-T03: Test exact and near-boundary feasibility, including conflicting constraints.
OPT-T04: Confirm that no infeasible candidate receives a rank.
OPT-T05: Confirm practical titer ties resolve through cell integral and then cost.
OPT-T06: Perturb each multiplier by plus and minus 5 percent and reproduce the 95 percent robustness rule.
OPT-T07: Compare direct Python and BioModule recommendation records exactly.
OPT-T08: Test zero feasible candidates, fewer than 10,000 feasible candidates, corrupted surrogate files, and nonconverged surrogate artifacts.
OPT-T09: Validate and run the packaged Lab in a clean CPU environment.

OPT-V01 is the data-readiness protocol, OPT-V02 is the locked cross-block retrospective validation protocol, and OPT-V03 is the confirmatory bioreactor protocol.
8. Lock, Release, and Monitoring
The lock includes curated data and partitions, transform artifact, one surrogate per outcome, fit diagnostics, constraints, cost table, Sobol seed and generator version, ranking rules, recommendation manifest, code commit, environment, and package checksums.

Release of the optimizer package requires retrospective MRS gates, deterministic search reproduction, adapter parity, and independent review. Experimental acceptance requires the separate confirmatory study.

Monitor new runs for input distance, surrogate residuals, reference-process drift, constraint violations, and changed component costs. A new clone, vessel scale, feed strategy, formulation group, product-quality rule, or primary objective requires MRS review.
9. References
Adjacent Model Requirements Specification
https://docs.biosimulant.com/runtime/create-biomodule
