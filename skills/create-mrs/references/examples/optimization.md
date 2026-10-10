DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Optimization MRS Example - CHO Media Formulation
Model Requirements Specification: CHO Basal-Media Formulation Optimization
This is a completed illustrative MRS for research process development. It is not an active study, a manufacturing control strategy, or a report of achieved results. Numeric targets and formulation bounds are illustrative project requirements.
1. Document Control
Field
Value
MRS identifier
EX-MRS-OPT-CHO-MEDIA-001
Version
1.0 example
Status
Illustrative, not approved for execution
Model type
Constrained multi-objective optimization
Scientific owner
Cell-culture process development lead
Model owner
Bioprocess modeling lead
Validation owner
Analytical development lead
Intended user
Media-development scientist
Last revised
2026-08-19

2. Objective and Intended Use
Recommend a chemically defined basal-medium formulation for one recombinant monoclonal-antibody-producing CHO cell line in a fixed 14-day fed-batch process. The recommendation must improve product titer while maintaining viable-cell performance, metabolite control, product-quality comparability, formulation feasibility, and an acceptable raw-material cost.

The model will prioritize three formulations for confirmatory experiments. It will not authorize manufacturing use, alter the feed strategy, or claim transfer to another clone or scale.

Mixture design and automated small-scale bioreactors have been used to optimize CHO media under controlled fed-batch conditions [1]. Model-guided CHO media development can also combine multivariate data with mechanistic or metabolic evidence [2]. These sources motivate the workflow but do not set this project's success thresholds.
3. Decision Variables and Scope
Decision Variables
Eight predefined chemically defined supplement groups vary as multipliers of the reference basal formulation:

ID
Supplement group
Allowed multiplier
X1
Essential amino-acid group
0.70 to 1.30
X2
Nonessential amino-acid group
0.70 to 1.50
X3
Vitamin group
0.75 to 1.50
X4
Trace-element group
0.75 to 1.25
X5
Lipid and cholesterol group
0.75 to 1.50
X6
Iron-carrier group
0.75 to 1.25
X7
Glutamine-substitute group
0.75 to 1.25
X8
Nucleoside and precursor group
0.75 to 1.50


The exact chemical composition of each group is fixed before study execution. The optimizer may vary group multipliers but may not change group membership or introduce a new component.
Fixed Conditions
Cell clone, inoculum train, seeding density, vessel type, temperature shift, pH, dissolved oxygen, agitation, feed composition, feed schedule, glucose-control rule, harvest day, and analytical methods remain fixed. A deviation invalidates a run for primary optimization unless the deviation rule classifies it as minor before outcomes are reviewed.
4. Objectives and Constraints
Objectives
The optimizer uses a lexicographic decision rule:

Reject infeasible formulations.
Among feasible formulations, maximize day-14 monoclonal-antibody titer.
Break practically equivalent titer results using higher integral viable-cell concentration.
Break any remaining tie using lower media raw-material cost.

Formulations whose predicted titer differs by less than 3 percent are treated as practically equivalent for tie-breaking.
Hard Constraints
Calculated initial osmolality from 280 to 340 mOsm/kg, confirmed by measurement before inoculation.
Final pH after preparation from 7.00 to 7.30 before equilibration under the locked process.
No visible precipitate after sterile filtration and 72 hours at 2 to 8 degrees Celsius.
Every supplement multiplier lies within its approved bound.
Estimated raw-material cost no greater than 110 percent of the reference formulation.
Predicted day-14 viability at least 70 percent.
Predicted peak lactate no greater than 6 mmol/L and peak ammonia no greater than 5 mmol/L.

An infeasible candidate must be returned with violated constraints and distances to feasibility. It must not receive a recommendation rank.
Product-Quality Guardrails
The main charge-variant profile, aggregate percentage, and the three prespecified major glycan groups must each remain inside the 95 percent reference-process tolerance interval established from six independent reference runs. This is a research comparability rule, not a product-release specification.
5. Inputs and Outputs
Inputs
Eight formulation multipliers and derived ingredient concentrations.
Measured osmolality and prepared-medium pH.
Run identifiers, culture block, vessel position, inoculum batch, and operator.
Daily viable-cell density and viability.
Daily glucose, lactate, glutamine or substitute, and ammonia measurements.
Day-14 titer and product-quality measurements.
Frozen component cost table with currency and effective date.
Outputs
ID
Output
Requirement
MRS-OUT-001
Feasibility status
Pass or fail plus constraint margins
MRS-OUT-002
Predicted outcomes
Day-14 titer, integral viable-cell concentration, day-14 viability, peak lactate, peak ammonia, and cost
MRS-OUT-003
Prediction uncertainty
90 percent interval for each predicted biological outcome
MRS-OUT-004
Recommended formulations
Ranked top three plus two scientifically distinct backups
MRS-OUT-005
Trade-off view
Feasible Pareto set for titer, cell integral, and cost
MRS-OUT-006
Robustness report
Outcome changes under component-preparation and model uncertainty

6. Experimental Design and Data Quality
Illustrative Development Design
Platform: controlled 15 mL parallel bioreactors.
Formulations: 48 model-informed mixture or response-surface conditions across two balanced experimental blocks.
Reference controls: six reference-medium vessels distributed across blocks.
Replication: 12 selected formulations repeated in independent inoculum blocks to estimate reproducibility; technical analytical replication follows each assay's validated method.
Blinding: analytical sample identifiers mask formulation rank.
Randomization: vessel position randomized within process constraints.

The development design must support estimation of important nonlinear effects and selected interactions while retaining pure-error information. A model that cannot distinguish lack of fit from run noise is not adequate for optimization.
Quality Gates
ID
Gate
Rule
MRS-DQ-001
Reference-run control
Reference titer and peak viable-cell density within established process-control limits
MRS-DQ-002
Inoculum
Viability at least 95 percent and seeding density within 10 percent of target
MRS-DQ-003
Process deviations
pH, dissolved oxygen, temperature, agitation, and feed deviations reviewed before outcome unblinding
MRS-DQ-004
Medium preparation
Measured osmolality and pH recorded; no visible precipitate
MRS-DQ-005
Endpoint completeness
Titer and primary product-quality results available or a documented assay failure recorded


Bioreactor runs, not analytical replicate wells, are the independent experimental units.
7. Optimization and Robustness Requirements
The surrogate outcome models must be validated using whole-run holdouts, not individual daily measurement rows.
Preprocessing and hyperparameters are fitted without confirmatory-run outcomes.
The search method must respect all hard constraints during recommendation.
The optimizer must examine at least 10,000 feasible candidate formulations or use a convergence demonstration appropriate to the selected algorithm.
Stability must be tested for independent optimization seeds and reasonable changes to surrogate-model hyperparameters.
Robustness must be evaluated under independent plus or minus 5 percent preparation error for every supplement multiplier and under the predictive-outcome distributions.
A robust recommendation must remain feasible in at least 95 percent of 10,000 uncertainty simulations.
The top three recommendations must not be trivial numerical duplicates. Any pair must differ by at least 0.10 in one supplement multiplier.
8. Performance and Acceptance Requirements
All thresholds are illustrative project requirements.

ID
Requirement
Acceptance criterion
MRS-OPT-001
Predict held-out titer
Cross-block whole-run normalized RMSE no greater than 0.15 and no material block-specific residual trend
MRS-OPT-002
Predict feasibility outcomes
At least 90 percent balanced accuracy for day-14 viability and metabolite constraint status on held-out runs
MRS-OPT-003
Return only feasible recommendations
Every recommended formulation passes all deterministic constraints and has at least 95 percent simulated feasibility probability
MRS-OPT-004
Improve titer prospectively
At least two of three confirmatory formulations improve mean day-14 titer by at least 15 percent relative to concurrent reference controls
MRS-OPT-005
Preserve viable-cell performance
Successful formulations do not reduce integral viable-cell concentration by more than 5 percent and retain day-14 viability of at least 70 percent
MRS-OPT-006
Preserve product-quality comparability
Successful formulations keep every stated product-quality measure within the reference tolerance interval
MRS-OPT-007
Respect cost
Successful formulations cost no more than 110 percent of reference basal medium
MRS-OPT-008
Demonstrate reproducibility
The titer improvement for a successful formulation is positive in each of three independent inoculum blocks

9. Confirmatory Validation
Prepare the top three locked formulations, two diverse backups, and the reference formulation from new stock solutions. Test each in three independent inoculum blocks. Randomize vessel positions and blind analytical identifiers. No model update is allowed after the selection manifest is frozen.

The primary analysis compares each recommendation with concurrent reference controls using block-aware estimates and confidence intervals. All attempted runs remain visible. A failed vessel may be excluded only under a predeclared process-deviation rule unrelated to the formulation outcome.

The project succeeds when at least two formulations satisfy MRS-OPT-004 through MRS-OPT-008. If one formulation succeeds, it is a promising result but does not satisfy the portfolio requirement.
10. Risks and Failure Behavior
Risk
Mitigation
Apparent improvement is a block or vessel-position effect
Balance, randomize, retain block metadata, and validate in new inoculum blocks
Optimizer exploits surrogate error at the edge of the design space
Use uncertainty-aware feasibility, distance-to-data reporting, and confirmatory experiments
Component groups hide antagonistic ingredients
Freeze group composition for this MRS and identify deconvolution as a separate follow-on study
Titer improvement harms product quality
Treat quality ranges as hard guardrails rather than secondary scores
Preparation variability makes the optimum fragile
Require plus or minus 5 percent robustness simulation and new-stock confirmation
Small-scale result is assumed to transfer to production scale
Limit claim to the specified small-scale platform and require a separate scale-down qualification and scale-up MRS

11. Deliverables and Traceability
Deliverables are the formulation and cost schema, experimental design, raw and curated run data, quality report, surrogate models, optimization configuration, feasible candidate set, selection manifest, robustness report, confirmatory assay package, and final recommendation report. A Biosimulant Lab may optionally package the optimization workflow.

Requirement
Verification
Evidence artifact
Owner
MRS-OUT-001 to MRS-OUT-006
Feasibility, outcome, uncertainty, ranking, Pareto, and robustness output tests
Output conformance report
Model owner
MRS-DQ-001 to MRS-DQ-005
Data-readiness review
QC and deviation report
Process development lead
MRS-OPT-001 to MRS-OPT-003
Locked retrospective and robustness analysis
Model validation report
Validation owner
MRS-OPT-004 to MRS-OPT-008
Confirmatory bioreactor study
Frozen experiment and analytical report
Scientific owner

12. References
Grimm C, Kusser W, Lee B, et al. Media optimization for CHO fed-batch processes using a DoE approach in automated high-throughput single-use ambr15 bioreactors. BMC Proceedings. 2015;9(Suppl 9):P15. https://doi.org/10.1186/1753-6561-9-S9-P15
Hong JK, Choi DH, Park SY, et al. Data-driven and model-guided systematic framework for media development in CHO cell culture. Metabolic Engineering. 2022;73:114-123. https://doi.org/10.1016/j.ymben.2022.07.003

