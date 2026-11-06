DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Statistical Estimation MRS Example - Dose Response IC50
Model Requirements Specification: Relative IC50 Estimation from an In-Vitro Assay
This is a completed illustrative MRS, not an active assay protocol or a report of an estimated compound potency. Numeric thresholds are illustrative project requirements unless attributed to a source.
1. Document Control
Field
Value
MRS identifier
EX-MRS-EST-IC50-001
Version
1.0 example
Status
Illustrative, not approved for execution
Model type
Statistical estimation
Scientific owner
Biochemical assay lead
Model owner
Biostatistics lead
Validation owner
Independent assay scientist
Intended user
Screening and medicinal chemistry scientist
Last revised
2026-08-19

2. Objective and Estimand
Estimate the relative half-maximal inhibitory concentration, or relative IC50, of an illustrative small-molecule inhibitor in a recombinant human kinase activity assay. The estimate will summarize potency under one frozen assay protocol and support compound-ranking discussions.

The relative IC50 is the concentration halfway between the fitted upper and lower response asymptotes. It is not necessarily the concentration producing exactly 50 percent absolute activity. The distinction must be preserved in output labels and reports. Four-parameter logistic models are commonly used for in-vitro concentration-response data, with diagnostic review and reduced models used only when justified [1].
Primary Estimand
The geometric mean relative IC50 across three valid independent assay days for the specified compound, enzyme construct, substrate concentration, ATP concentration, incubation time, temperature, and response-normalization procedure.
Secondary Estimates
Day-specific relative IC50.
Upper and lower asymptotes.
Hill slope.
Absolute 50 percent inhibitory concentration, only if the fitted curve crosses 50 percent normalized activity within the tested range.
Between-day variability on the log10 IC50 scale.
Non-Use
The estimate must not be interpreted as a binding affinity, dissociation constant, in-cell potency, selectivity measurement, exposure requirement, efficacy claim, or safe dose.
3. Assay Design and Observations
Experimental Unit and Replication
Independent experimental unit: one assay day using a fresh enzyme and reagent preparation.
Independent repetitions: three valid assay days performed by at least two operators.
Concentrations: ten nonzero concentrations in a half-log series plus vehicle control, selected to bracket both response asymptotes based on range-finding data.
Technical wells: three wells per concentration and control on each day.
Controls: vehicle, full-inhibition control, and a reference inhibitor concentration series on every plate.
Randomization: compound and control positions distributed to reduce edge and dispensing-order effects.
Blinding: compound identity may be known, but the analyst must run the locked fitting workflow before comparing with the expected potency range.

Technical wells on one plate are not independent biological or experimental replicates. Their median normalized activity forms one concentration-level observation for that assay day, consistent with guidance that correlated replicate wells should not be treated as independent evidence [1].
Input Contract
ID
Input
Requirement
MRS-IN-001
Compound concentration
Positive molar concentration with preparation and dilution identifiers
MRS-IN-002
Raw signal
Unrounded instrument value, well identifier, plate, and read timestamp
MRS-IN-003
Control identity
Vehicle, full inhibition, reference inhibitor, or test compound
MRS-IN-004
Assay metadata
Enzyme and substrate lots, ATP and substrate concentrations, operator, instrument, temperature, and timing
MRS-IN-005
Exclusion status
Predeclared reason, decision time, reviewer, and retained raw value

Normalization
For each valid plate, vehicle-control median maps to 100 percent activity and full-inhibition-control median maps to 0 percent activity. Normalized technical replicates are summarized by the median at each concentration. Values outside 0 to 100 percent remain available for fitting and diagnostics and must not be silently truncated.
4. Statistical Model
For concentration x greater than zero, normalized activity y is modeled using the four-parameter logistic curve:

y = Bottom + (Top - Bottom) / (1 + (x / IC50)^Hill)

where Top and Bottom are fitted asymptotes, IC50 is positive, and Hill is a positive slope magnitude for a decreasing activity curve under this parameterization.
Estimation Rules
Fit each independent assay day separately using nonlinear regression on the log10 concentration scale.
Do not log-transform zero-concentration vehicle controls. Use them as asymptote-supporting observations with the declared implementation's control handling.
Estimate Top and Bottom unless a predeclared diagnostic rule requires one asymptote to be fixed to its assay-defined value.
A three-parameter fit is permitted only when the relevant asymptote is not supported by the observed range, the fixed value is scientifically justified, and the sensitivity of IC50 to the choice is reported.
A two-parameter fit with both asymptotes fixed is not the default and requires statistical-owner approval.
Combine valid day-specific log10 IC50 values using their arithmetic mean. Exponentiation gives the geometric-mean IC50.
Calculate a two-sided 95 percent t-based confidence interval on the day-level log10 IC50 values. With only three days, report the interval and all day-specific estimates rather than implying high precision.
5. Quality Gates and Failed-Curve Handling
ID
Gate
Acceptance rule
MRS-DQ-001
Plate signal separation
Z-prime factor at least 0.5 using vehicle and full-inhibition controls
MRS-DQ-002
Control variability
Vehicle and full-inhibition control coefficient of variation each no greater than 15 percent
MRS-DQ-003
Reference inhibitor
Relative IC50 within the established assay control interval
MRS-DQ-004
Concentration integrity
Dilution and dispense records complete with no unresolved preparation deviation
MRS-DQ-005
Technical consistency
No more than one technical well excluded per concentration and only for a predeclared technical reason

Curve Statuses
Quantifiable: both response regions sufficiently support a relative IC50 inside the tested range and diagnostics pass.
Left-censored: inhibition is already beyond the midpoint at the lowest tested nonzero concentration. Report IC50 below lowest tested concentration, not an extrapolated point estimate.
Right-censored: the curve does not reach its midpoint by the highest tested concentration. Report IC50 above highest tested concentration.
Incomplete asymptote: a reduced model may be used under the predeclared rule, with sensitivity results.
Nonmonotonic or poor fit: report no IC50 and flag the response for assay and biology review.
Invalid plate: control gate failure. Repeat the assay day; retain the failed raw data and reason.

An optimization algorithm returning a number is not evidence that the IC50 is estimable.
6. Diagnostics and Uncertainty
Each day-level fit must include:

observed and fitted concentration-response plot on a log concentration axis;
parameter estimates and covariance or profile information;
residuals versus fitted value and concentration;
convergence status and boundary warnings;
influence analysis for individual concentration levels;
asymptote support and whether the midpoint lies inside the tested range; and
sensitivity to permitted three-parameter alternatives.

The combined estimate must include all valid day-level log10 IC50 values, geometric mean, 95 percent confidence interval, between-day standard deviation, and a clear statement of the number of valid independent days.
7. Performance and Acceptance Requirements
All thresholds below are illustrative project requirements.

ID
Requirement
Acceptance criterion
MRS-EST-001
Produce valid independent estimates
Three assay days pass plate QC and yield quantifiable relative IC50 estimates
MRS-EST-002
Bound uncertainty
Width of the combined 95 percent confidence interval no greater than 0.60 log10 concentration units
MRS-EST-003
Demonstrate between-day reproducibility
Maximum minus minimum day-level log10 IC50 no greater than 0.50
MRS-EST-004
Avoid material lack of fit
No systematic residual pattern and no day with absolute standardized residual greater than 3 without an investigated technical cause
MRS-EST-005
Check estimator behavior
Parametric simulation under the fitted range gives 90 to 98 percent empirical coverage for nominal 95 percent day-level intervals
MRS-EST-006
Preserve censoring semantics
All out-of-range and nonestimable test datasets return the required bound or failure status, never an unqualified finite IC50
MRS-EST-007
Reproduce results
Reanalysis from frozen raw data, metadata, and environment matches reported log10 IC50 values within 1e-6


The project is complete only when all seven requirements pass. If the interval-width or between-day criterion fails, the output remains a study result but is not an accepted potency estimate for compound ranking.
8. Validation Plan
Freeze normalization, exclusion, model-selection, convergence, censoring, and reporting rules before the three confirmatory days.
Validate the implementation on simulated curves spanning the supported IC50, slope, asymptote, and noise ranges.
Include negative tests with flat, increasing, biphasic, nonmonotonic, left-censored, right-censored, and insufficient-asymptote data.
Run the reference inhibitor on every plate and review it before accepting the test-compound curve.
Fit each day without borrowing its result from another day.
Reproduce the final report from raw data in a clean environment.

No technical replicate may be promoted to an independent assay day to satisfy the sample count.
9. Risks and Interpretation
Risk
Required mitigation
Relative IC50 is confused with absolute 50 percent activity
Label both explicitly and report absolute IC50 only when defined and in range
Tested concentrations do not bracket the curve
Report a bound and redesign the concentration range rather than extrapolating
Technical wells inflate precision
Aggregate wells within day and base between-day uncertainty on independent days
Fixed asymptotes bias potency
Fit four parameters by default and report sensitivity when an asymptote is fixed
IC50 is mistaken for binding affinity or dose
State the assay-specific estimand and prohibited interpretations in every summary
Failed fit is hidden by automated software
Require diagnostic status, censoring semantics, and raw-data plots

10. Deliverables and Traceability
Deliverables are the raw well-level data, plate and dilution metadata, QC table, normalization output, day-level fit objects, combined estimate, diagnostics, simulation-validation report, analysis code, environment lock, and a machine-readable result record.

Requirement
Verification
Evidence artifact
Owner
MRS-IN-001 to MRS-IN-005
Schema, concentration, control, metadata, and exclusion tests
Input conformance report
Assay lead
MRS-DQ-001 to MRS-DQ-005
Plate-level QC
Assay QC report
Assay lead
MRS-EST-001 to MRS-EST-004
Frozen confirmatory analysis
Estimation report
Biostatistics lead
MRS-EST-005 to MRS-EST-006
Simulation and negative tests
Method-validation report
Independent validation owner
MRS-EST-007
Clean-environment rerun
Reproducibility log
Analysis engineer

11. References
Sittampalam GS, Coussens NP, Brimacombe K, et al., editors. Assay Guidance Manual. Assay Operations for SAR Support, Determination of EC50/IC50. National Center for Advancing Translational Sciences; updated 2017. https://www.ncbi.nlm.nih.gov/books/NBK91994/
Sebaugh JL. Guidelines for accurate EC50/IC50 estimation. Pharmaceutical Statistics. 2011;10:128-134. https://doi.org/10.1002/pst.426

