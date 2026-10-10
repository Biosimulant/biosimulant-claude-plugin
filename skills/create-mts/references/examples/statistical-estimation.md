DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Statistical Estimation MTS Example - Dose Response IC50
Modeling Technical Specification: Relative IC50 Estimation from an In-Vitro Assay
This is an implementation-ready illustrative technical design. It is not an active assay analysis or report of a compound potency estimate.
1. Document Control
Field
Value
MTS identifier
EX-MTS-EST-IC50-001
Version
1.0 example
Status
Illustrative, not approved for execution
MRS
EX-MRS-EST-IC50-001
Scientific owner
Biochemical assay lead
Technical owner
Biostatistics lead
Validation owner
Independent assay scientist
Biosimulant fit
Not suitable as a standalone Lab

2. Technical Decision Summary
Implement the analysis as a small versioned R package with a command-line entry point, an renv lockfile, explicit CSV and JSON schemas, simulation-based method tests, and a generated HTML or PDF report. Fit one four-parameter logistic curve per independent assay day, preserve censoring and failure semantics, and combine valid log10 IC50 estimates exactly as defined in the MRS.

Do not create a BioModule or Lab. A standalone three-day curve fit has no meaningful component graph, simulation clock, snapshot, or composition requirement. Biosimulant would add packaging overhead without improving the statistical analysis.
3. Architecture
flowchart LR
    A["Raw well CSV and assay metadata"] --> B["Schema and plate QC"]
    B --> C["Within-day normalization and technical-well summary"]
    C --> D["Day-level 4PL fits and diagnostics"]
    D --> E["Cross-day log IC50 summary"]
    E --> F["Machine-readable result and rendered report"]
Selected Stack
Layer
Technology
Responsibility
Package
R package with renv
Functions, tests, schemas, and versioning
Curve fitting
drc with an explicit four-parameter logistic wrapper
Day-level estimation
Data handling
readr, dplyr, and jsonlite
Typed ingestion and outputs
Tests
testthat
Unit, simulation, censoring, and regression tests
Report
Quarto rendered from locked result files
Plots, diagnostics, and interpretation
Entry point
Rscript inst/cli/estimate_ic50.R
Reproducible command-line execution


The wrapper maps package parameter names to the MRS names Top, Bottom, Hill, and IC50 and records the slope convention explicitly.
4. Input and Output Contracts
Well-Level Input
Field
Type
Rule
study_id
string
One approved study identifier
assay_day
string
Independent-day identifier
plate_id
string
Unique within study
well_id
string
Unique within plate
compound_id
string
Test, reference, vehicle, or full-inhibition control
concentration_molar
number or null
Positive for compound wells; null for non-concentration controls
raw_signal
number
Unrounded instrument value
control_role
enum
test, vehicle, full_inhibition, or reference
exclusion_status
enum
included or excluded
exclusion_reason
string or null
Required for an excluded well


Assay metadata include enzyme construct and lot, substrate and ATP concentrations, incubation time, temperature, operator, instrument, dilution preparation, and protocol version.
Machine-Readable Result
{
  "study_id": "IC50_EXAMPLE_001",
  "analysis_version": "1.0.0",
  "estimand": "geometric_mean_relative_ic50",
  "status": "quantifiable",
  "valid_assay_days": 3,
  "ic50_molar": 1.2e-8,
  "log10_ic50": -7.92,
  "confidence_interval_95_log10": [-8.10, -7.74],
  "day_level_results": [],
  "diagnostic_flags": [],
  "provenance": {}
}

Permitted primary statuses are quantifiable, left_censored, right_censored, nonmonotonic, poor_fit, invalid_plate, and insufficient_valid_days. Only quantifiable returns an unqualified finite combined IC50.
5. Statistical Implementation
Plate QC and Normalization
Verify identities, concentrations, dilution lineage, controls, and metadata.
Calculate Z-prime and control coefficients of variation from included control wells.
Reject the plate when an MRS control gate fails.
Map vehicle-control median to 100 percent activity and full-inhibition median to 0 percent.
Retain normalized values outside 0 to 100 for fitting and diagnostics.
Summarize technical wells by median within day and concentration.
Day-Level Model
For positive concentration x, fit:

y = Bottom + (Top - Bottom) / (1 + (x / IC50)^Hill)

Estimate all four parameters by default.
Require positive IC50 and Hill under this decreasing-activity parameterization.
Use vehicle observations to support the upper asymptote without applying log10 to zero concentration.
Permit a fixed Top or Bottom only under the predeclared incomplete-asymptote rule.
Record convergence, covariance or profile information, residuals, influence, boundary warnings, asymptote support, and whether the midpoint lies inside the tested range.
Across-Day Summary
Require three independent quantifiable assay days.
Calculate the arithmetic mean of the three log10 IC50 estimates.
Exponentiate for the geometric-mean IC50.
Calculate the two-sided t-based 95 percent interval on day-level log10 IC50 values.
Report every day-level estimate and between-day standard deviation.
Do not substitute technical wells for independent days.
6. Biosimulant Fit Assessment
Question
Decision
Outcome
Not suitable
Selected alternative
Versioned R package and generated report
Why it is better
Direct statistical semantics, small execution surface, mature diagnostics, and no artificial simulation clock
Biosimulant boundary
None in v1
Reassessment trigger
The estimator becomes one validated component in a larger composed screening or decision workflow


If future composition is justified, the locked R result JSON may become the exchange boundary. That later project must assess whether to call the package externally or wrap it, and must not alter the estimator semantics.
7. Execution and Reproducibility
Rscript -e 'renv::restore(prompt = FALSE)'
Rscript inst/cli/estimate_ic50.R \
  --wells data/wells.csv \
  --metadata data/assay-metadata.json \
  --config config/analysis.yaml \
  --output results/ic50-result.json
Rscript -e 'testthat::test_local()'
quarto render report/ic50-report.qmd

The release records the source commit, R version, renv.lock, input checksums, analysis configuration, package version, random seeds for simulation checks, JSON result checksum, and rendered-report checksum.
8. MRS Traceability and Tests
MRS requirement
Technical implementation
Test or protocol
Verification evidence
MRS-IN-001 to MRS-IN-005
Well and metadata schemas with dilution and exclusion lineage
EST-T04
Input conformance report
MRS-DQ-001 to MRS-DQ-005
Plate-QC and reference-inhibitor functions
EST-T04
Assay QC report
MRS-EST-001
Independent-day status gate
EST-T05, EST-V01
Confirmatory estimation report
MRS-EST-002 to MRS-EST-004
Locked across-day summary and diagnostic functions
EST-T01, EST-T03, EST-T06, EST-V01
Estimation and diagnostic report
MRS-EST-005
Parametric simulation suite
EST-T02
Coverage report
MRS-EST-006
Explicit censoring and failed-fit state machine
EST-T03, EST-T09
Negative-test report
MRS-EST-007
renv clean rerun and checksum comparison
EST-T08
Reproducibility log

Required Tests
EST-T01: Recover known 4PL parameters across the supported concentration, slope, asymptote, and noise ranges.
EST-T02: Simulate at least 10,000 eligible day-level datasets for interval-coverage evaluation.
EST-T03: Test flat, increasing, nonmonotonic, biphasic, left-censored, right-censored, and incomplete-asymptote curves.
EST-T04: Test a failed Z-prime, failed reference inhibitor, missing concentration, duplicated well, and invalid exclusion.
EST-T05: Confirm technical wells do not increase the independent-day count.
EST-T06: Confirm normalized values are not clipped.
EST-T07: Compare fixed-asymptote sensitivity with the default 4PL when the exception rule is used.
EST-T08: Reproduce the JSON result and report from raw inputs in a clean environment.
EST-T09: Verify that every nonquantifiable state omits an unqualified finite combined IC50.

EST-V01 is the frozen three-day confirmatory analysis protocol. Its precision, reproducibility, and diagnostic gates remain those in the adjacent MRS.
9. Lock, Release, and Monitoring
The lock contains raw inputs, metadata, exclusion table, QC configuration, analysis configuration, package source, renv.lock, test fixtures, simulation seeds, JSON schema, result, diagnostics, and report.

Release requires all method tests, assay QC, three valid days, MRS precision and reproducibility gates, independent code review, and report review by the assay scientist.

Monitor reference-inhibitor control charts, plate invalidation rate, censoring rate, fit failures, between-day variation, and protocol changes. A changed enzyme construct, substrate or ATP condition, normalization, estimand, or ranking use requires MRS review.
10. References
Adjacent Model Requirements Specification
https://www.ncbi.nlm.nih.gov/books/NBK91994/
https://doi.org/10.1002/pst.426

