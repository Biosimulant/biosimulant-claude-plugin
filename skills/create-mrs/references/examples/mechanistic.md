DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Mechanistic MRS Example - MAPK ERK Signaling
Model Requirements Specification: MAPK/ERK Cascade with Negative Feedback
This is a completed illustrative MRS, not an active study or a report of achieved results. Project quantities and acceptance thresholds below are teaching requirements. Published scientific statements are cited.
1. Document Control
Field
Value
MRS identifier
EX-MRS-MECH-ERK-001
Version
1.0 example
Status
Illustrative, not approved for execution
Model type
Mechanistic, deterministic ODE
Scientific owner
Signaling biology lead
Model owner
Systems biology lead
Validation owner
Quantitative assay lead
Intended user
Experimental signaling scientist
Last revised
2026-08-19

2. Objective and Intended Use
Build a reduced mechanistic model of the Ras/Raf-MEK-ERK kinase cascade that represents double phosphorylation of MEK and ERK and inhibitory feedback from active ERK to upstream cascade activation. The model must reproduce dose-dependent phospho-ERK time courses in a defined epithelial-cell assay and support prespecified in-silico perturbations of feedback strength and kinase activity.

Negative feedback combined with cascade ultrasensitivity can produce oscillatory MAPK behavior under some parameter regimes [1]. Oscillation is therefore a behavior to test, not an acceptance requirement or an assumed property of the experimental system.

The model is intended for hypothesis refinement and experiment design. It is not a complete EGFR network, a clinical model, or proof that one molecular feedback route uniquely explains an observed time course.
3. Biological Scope
Required Representation
One upstream stimulus state representing receptor/Ras-dependent activation of Raf.
Inactive and active Raf.
Unphosphorylated, singly phosphorylated, and doubly phosphorylated MEK.
Unphosphorylated, singly phosphorylated, and doubly phosphorylated ERK.
Phosphatase-mediated dephosphorylation at the MEK and ERK tiers.
A saturable inhibitory effect of active ERK on upstream Raf activation.
Nonnegative state variables and conserved total abundance within each kinase tier unless an explicit synthesis or degradation term is added in a future MRS version.
Excluded Representation
Receptor trafficking, detailed Ras nucleotide cycling, pathway crosstalk, transcriptional feedback, protein synthesis and degradation, subcellular localization, cell-cycle effects, and cell-to-cell stochasticity are excluded. Conclusions must be limited accordingly.
Unit of Simulation
One well-level population-average signaling response for one stimulus condition. The model does not represent individual cells.
4. Inputs, States, and Outputs
Inputs
ID
Input
Unit
Range
Meaning
MRS-IN-001
EGF concentration
ng/mL
0, 0.1, 1, 10, or 100
Experimental stimulus condition
MRS-IN-002
Upstream activation function
dimensionless
0 to 1
Mapping from EGF condition to effective cascade input
MRS-IN-003
Total Raf, MEK, and ERK abundance
nM
Assay-derived positive values
Conserved kinase pools
MRS-IN-004
Initial phosphorylated fractions
fraction
0 to 1
Basal state before stimulation
MRS-IN-005
Kinetic parameters
parameter-specific
Positive values
Activation, phosphorylation, dephosphorylation, and feedback terms


The EGF-to-upstream-input mapping is an empirical boundary condition, not a claim that the model represents receptor biochemistry.
Outputs
ID
Output
Unit
Resolution
MRS-OUT-001
Doubly phosphorylated ERK fraction
fraction of total ERK
Every 0.1 minute internally; reported at assay times
MRS-OUT-002
Doubly phosphorylated MEK fraction
fraction of total MEK
Every 0.1 minute internally
MRS-OUT-003
Active Raf fraction
fraction of total Raf
Every 0.1 minute internally
MRS-OUT-004
Peak amplitude and time
fraction and minutes
Per stimulus condition
MRS-OUT-005
Integrated ERK activity
fraction-minutes
0 to 120 minutes
MRS-OUT-006
Sensitivity and uncertainty summary
dimensionless or parameter-specific
For all decision-relevant outputs

5. Experimental Evidence and Observables
Illustrative Assay Plan
System: one authenticated human epithelial cell line under a frozen culture and serum-starvation protocol.
Stimuli: 0, 0.1, 1, 10, and 100 ng/mL EGF.
Sampling times: 0, 2, 5, 10, 15, 30, 60, and 120 minutes.
Replication: three independent culture days as biological replicates, with two technical assay replicates per lysate.
Readouts: phospho-ERK1/2, total ERK1/2, phospho-MEK1/2, and total MEK1/2 measured by a quantitative immunoassay with an internal reference sample on every plate.
Perturbation validation: one MEK-inhibitor condition and one feedback-attenuation condition selected before the validation protocol is locked.

The primary observable is the background-corrected phospho-ERK to total-ERK ratio, normalized to the plate reference sample. A measurement below the lower limit of quantification remains left-censored and must not be silently replaced with zero.
Quality Gates
ID
Gate
Acceptance rule
MRS-DQ-001
Technical replicate agreement
Coefficient of variation no greater than 20 percent when both values are quantifiable
MRS-DQ-002
Plate reference stability
Reference-sample value within 20 percent of the study median
MRS-DQ-003
Total-protein stability
Total ERK and total MEK each remain within 20 percent of their condition baseline over 120 minutes
MRS-DQ-004
Negative control
Vehicle phospho-ERK response remains within the predeclared basal range
MRS-DQ-005
Cell-line and protocol identity
Authentication, passage range, starvation period, and stimulus preparation recorded

6. Mathematical and Parameter Requirements
Formalism: deterministic ordinary differential equations with differentiable rate laws.
Phosphorylation: each MEK and ERK phosphorylation step must be represented separately. Lumping is permitted only if an identifiability analysis shows no loss for the prespecified outputs and the scientific owner approves the reduced interpretation.
Feedback: active ERK must reduce effective upstream activation through an explicit monotone inhibitory term.
Kinetics: rate laws must be stated and dimensionally consistent. Michaelis-Menten or effective saturable terms require a documented quasi-steady-state interpretation.
Initial conditions: estimated from time-zero observables where possible; unobserved basal state fractions must be bounded and included in uncertainty analysis.
Parameters: each parameter must be labeled measured, literature-derived, fitted, or assumed. Literature values transferred across systems require a sensitivity range rather than false precision.
Conservation: Raf, MEK, and ERK tier totals must be conserved to a relative residual of at most 1e-8 during a simulation.
Numerical behavior: states must remain nonnegative, integration must complete without an unhandled warning, and halving solver tolerances must change phospho-ERK output by less than 0.1 percent of total ERK.
7. Calibration, Identifiability, and Generalization
Calibration uses three of the five EGF doses and six of the eight time points selected before outcomes are examined. The remaining doses and time points form an interpolation and response-shape test. The inhibitor and feedback-attenuation conditions are withheld for perturbation validation.

Biological culture day is the resampling unit. Technical replicates are summarized within lysate and do not count as independent samples.

Structural identifiability must be assessed for the selected parameterization or justified using a documented reduced parameterization.
Practical identifiability must be assessed using profile likelihood or an equivalent method.
Parameters that are not practically identifiable must not receive narrow point claims. They may be fixed from evidence, grouped into identifiable combinations, or propagated as uncertainty.
Global sensitivity analysis must cover the stated parameter ranges and report effects on peak phospho-ERK, peak time, and 0 to 120 minute integrated activity.
The model may claim generalization only to held-out EGF doses and the two prespecified perturbations in the same cell line and protocol.
8. Performance and Acceptance Requirements
All thresholds are illustrative project requirements.

ID
Requirement
Acceptance criterion
MRS-MECH-001
Preserve kinase pools and nonnegativity
Conservation residual at most 1e-8 and no state below -1e-10 nM in every validation simulation
MRS-MECH-002
Reproduce held-out phospho-ERK trajectories
Normalized RMSE no greater than 0.15 across held-out EGF dose-time observations
MRS-MECH-003
Reproduce response timing
Median absolute peak-time error no greater than five minutes across quantifiable stimulated conditions
MRS-MECH-004
Reproduce response magnitude
Median absolute peak-amplitude error no greater than 20 percent of the observed dynamic range
MRS-MECH-005
Predict MEK-inhibitor direction
Correctly predicts a decrease in phospho-ERK area under the curve, and predicted magnitude lies within the biological-replicate 95 percent interval
MRS-MECH-006
Predict feedback-attenuation response
Correctly predicts the prespecified direction of change for peak or duration; exact endpoint is fixed before unblinding
MRS-MECH-007
Qualify parameter claims
Every decision-relevant parameter is identifiable, fixed with evidence, or reported as a bounded nonidentifiable set
MRS-MECH-008
Demonstrate numerical robustness
Tightening tolerances and changing between two validated stiff solvers changes primary outputs by less than 0.5 percent


Oscillation is reported if it occurs, including parameter region and numerical checks. It is neither forced during calibration nor counted as success without corresponding experimental evidence.
9. Validation and Negative Controls
Freeze equations, units, parameter bounds, observation mapping, calibration conditions, and solver settings.
Calibrate without held-out dose-time observations or perturbation results.
Run posterior or profile-prediction intervals for held-out conditions.
Evaluate all acceptance requirements using the frozen analysis.
Compare against two baselines: linear interpolation by dose and an otherwise identical cascade without ERK-mediated feedback.
Test time-label permutation, unit conversion, zero-stimulus behavior, extreme but permitted inputs, and independent reruns.

The feedback model must provide materially better held-out perturbation prediction than the no-feedback baseline to support a claim that feedback is needed. Similar fits to unperturbed time courses alone do not establish mechanism uniqueness.
10. Risks, Deliverables, and Traceability
Risk
Required mitigation
Multiple parameter sets fit the same observable
Profile parameters, propagate uncertainty, and restrict mechanistic claims
Normalized immunoassay values are treated as absolute concentration
Keep an explicit observation model and preserve assay units
Omitted pathway crosstalk drives perturbation results
Record model discrepancy and prohibit claims beyond the represented cascade
Numerical oscillation is mistaken for biology
Require solver, tolerance, and step-size robustness plus experimental evidence
Population-average data hide cell heterogeneity
State the well-average scope and do not infer single-cell behavior


Deliverables are the equation and unit specification, parameter provenance table, executable model, solver configuration, calibration data manifest, fitted parameter ensembles, sensitivity and identifiability reports, locked validation report, and user limitations guide. SBML and a portable Biosimulant package are optional exchange artifacts, not scientific acceptance criteria.

Requirement
Verification
Evidence artifact
Owner
MRS-IN-001 to MRS-IN-005
Unit, range, initial-state, and parameter-provenance review
Input and parameter conformance report
Systems biology lead
MRS-OUT-001 to MRS-OUT-006
Output-unit, time-grid, summary, and uncertainty tests
Output conformance report
Model owner
MRS-DQ-001 to MRS-DQ-005
Assay QC
Data readiness report
Assay lead
MRS-MECH-001 and MRS-MECH-008
Numerical test suite
Solver verification report
Model owner
MRS-MECH-002 to MRS-MECH-006
Locked holdout and perturbation analysis
Validation report
Validation owner
MRS-MECH-007
Identifiability review
Profile and parameter provenance report
Systems biology lead

11. References
Kholodenko BN. Negative feedback and ultrasensitivity can bring about oscillations in the mitogen-activated protein kinase cascades. European Journal of Biochemistry. 2000;267:1583-1588. https://doi.org/10.1046/j.1432-1327.2000.01197.x
BioModels. Kholodenko 2000 MAPK cascade model, BIOMD0000000010. https://www.ebi.ac.uk/biomodels/BIOMD0000000010

