DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Simulation Digital Twin MRS Example - CHO Fed-Batch Culture
Model Requirements Specification: CHO Fed-Batch Predictive Digital Twin
This is a completed illustrative MRS for research process development. It is not an active study, a validated manufacturing system, or a report of achieved results. Numeric targets are illustrative project requirements.
1. Document Control
Field
Value
MRS identifier
EX-MRS-DT-CHO-FEDBATCH-001
Version
1.0 example
Status
Illustrative, not approved for execution
Model type
Simulation / predictive digital twin
Scientific owner
Upstream process development lead
Model owner
Bioprocess modeling lead
Validation owner
Process analytics lead
Intended user
Fed-batch process scientist
Last revised
2026-08-19

2. Objective and Intended Use
Create a batch-specific computational representation of one monoclonal-antibody-producing CHO fed-batch process. The twin must initialize from the batch recipe and inoculum, update its state after daily measurements, and forecast viable-cell density, viability, extracellular metabolites, culture volume, and product titer over the next 24, 48, and 72 hours and through day 14.

The intended user will compare prespecified feed-delay and feed-volume scenarios during process development. The twin provides forecasts and uncertainty, not autonomous control instructions. Any experimental intervention requires scientist approval and protocol authorization.

Hybrid kinetic, constraint-based, and machine-learning components have been combined to predict viable-cell density, metabolites, and product titer in CHO fed-batch cultures [1]. That evidence supports feasibility but does not establish this illustrative twin's performance.
3. Asset, Scope, and Digital-Twin Semantics
Physical asset represented: one 15 mL controlled fed-batch bioreactor run of a frozen CHO clone, basal medium, feed medium, and 14-day process recipe.
Twin instance: one immutable batch identifier linked to its process events, measurements, model version, and state history.
Initialization: day-0 inoculum, medium lot, starting volume, viable-cell density, viability, initial metabolite values, process set points, and planned feed schedule.
Synchronization: state update after each accepted daily at-line measurement set and after every feed or sample-removal event.
Forecast horizon: 24, 48, and 72 hours plus end-of-run day 14.
Update cadence: at least once every 24 hours from day 0 through harvest.

This digital twin is operational and batch-specific. It may contain mechanistic equations, but it is accepted on synchronization, forecasting, scenario, and failure-handling performance. It is not accepted as proof that its internal biological mechanisms are uniquely correct.
Non-Use
The twin must not be used for autonomous feed control, manufacturing batch release, product-quality release, another cell clone, another vessel scale, perfusion culture, untested media, or prediction beyond day 14.
4. Inputs, States, Events, and Outputs
Inputs and Events
ID
Input
Unit
Timing
MRS-IN-001
Viable-cell density
10^6 cells/mL
Day 0 and daily
MRS-IN-002
Viability
percent
Day 0 and daily
MRS-IN-003
Glucose, lactate, glutamine or substitute, and ammonia
mmol/L
Day 0 and daily
MRS-IN-004
Product titer
g/L
At declared sampling days
MRS-IN-005
Temperature, pH, dissolved oxygen, and agitation
process-specific units
Time-stamped online values or daily summaries
MRS-IN-006
Feed and base additions
mL and timestamp
Every event
MRS-IN-007
Sample removals
mL and timestamp
Every event
MRS-IN-008
Batch attributes
categorical or numeric
At initialization


All values require a timestamp, unit, source instrument or assay, quality status, and batch identifier. Unit conversion occurs before state update and is recorded.
Required States
The twin must maintain viable cells, nonviable cells or viability-equivalent state, culture volume, glucose, lactate, ammonia, glutamine-equivalent substrate, and accumulated product. Additional latent metabolic or model states are permitted if their interpretation and initialization are documented.
Outputs
ID
Output
Requirement
MRS-OUT-001
Current estimated state
Value, unit, timestamp, and uncertainty for every required state
MRS-OUT-002
Forecast trajectory
Median plus central 80 and 95 percent intervals at 24, 48, and 72 hours and day 14
MRS-OUT-003
Scenario comparison
Difference from the current approved schedule for each endpoint and scenario
MRS-OUT-004
Domain and synchronization status
In domain, caution, unsupported, synchronized, stale, or update failed with reasons
MRS-OUT-005
Event and provenance log
Input versions, state updates, model version, configuration, and forecast issue time

5. Data and Generalization Plan
Illustrative Historical Dataset
Thirty complete fed-batch runs from the same clone, platform, media family, and assay methods.
At least three inoculum lots and three media or feed lots.
Planned variation in two feed-volume profiles and one feed-delay scenario.
Full process-event logs and daily cell and metabolite measurements.
Product titer measured on at least days 7, 10, 12, and 14.

Partition by complete bioreactor run. Daily rows from one run may never cross development, validation, or test partitions. The locked test set comprises the six latest eligible historical runs by start date. A further six prospective runs, including at least two non-reference feed scenarios, form the prospective validation set.

The claim is limited to future runs of the same clone and qualified small-scale process within the observed input ranges. Generalization across scale, clone, media family, or assay method requires a new MRS version.
Data Quality Gates
ID
Gate
Response
MRS-DQ-001
Batch and timestamp identity complete
Reject update if identity is ambiguous
MRS-DQ-002
Cell and metabolite assay controls pass
Retain last valid state and mark new data rejected if controls fail
MRS-DQ-003
Material-balance event log complete
Block scenario forecasts until feed and sample-removal events reconcile
MRS-DQ-004
Range and rate-of-change check
Flag implausible observations for review; do not silently clip
MRS-DQ-005
Measurement freshness
Mark twin stale when no accepted state measurement arrives for more than 30 hours

6. State Update, Simulation, and Scenario Requirements
State updates must reconcile measured concentrations with culture volume, feed additions, and sample removals.
The update method must preserve nonnegative mass and cell states.
The same observations and prior state must yield the same updated state within the declared numerical tolerance.
Measurement uncertainty must be included in state updates; an assay value is not treated as error-free truth.
A rejected measurement must remain visible with its reason and must not overwrite the last accepted state.
Forecast intervals must propagate parameter, state, and residual uncertainty.
Simulations must complete on the declared reference CPU environment before the next scheduled decision point.
Required Scenario Library
For a synchronized twin, users may run:

the approved reference feed schedule;
a single feed delayed by six hours;
a single feed volume reduced by 10 percent;
a single feed volume increased by 10 percent, provided the resulting volume and osmolality remain inside experimental limits; and
no further feed, clearly labeled as a stress scenario rather than an operational recommendation.

The interface must reject a scenario outside permitted bounds and report the violated condition.
7. Performance and Acceptance Requirements
Metrics are calculated per held-out run and summarized across runs. Concentration errors are normalized by the prespecified assay-relevant range to avoid unstable percentage errors near zero. All thresholds are illustrative project requirements.

ID
Requirement
Acceptance criterion
MRS-DT-001
Forecast viable-cell density
Median 24-hour normalized RMSE no greater than 0.10 and 72-hour normalized RMSE no greater than 0.20 on locked runs
MRS-DT-002
Forecast metabolites
Median 48-hour normalized RMSE no greater than 0.20 for glucose, lactate, and ammonia; each analyte also reported separately
MRS-DT-003
Forecast product
Day-14 titer median absolute percentage error no greater than 12 percent
MRS-DT-004
Quantify uncertainty
Central 80 percent intervals cover 70 to 90 percent of eligible locked observations overall, with endpoint-specific coverage reported
MRS-DT-005
Add value through synchronization
Daily state updates reduce next-48-hour RMSE by at least 15 percent relative to the same model run open-loop from day 0
MRS-DT-006
Preserve balances and valid states
No negative physical state and relative material-balance residual no greater than 1 percent after accounting for declared assay and event uncertainty
MRS-DT-007
Predict scenario direction
Correct direction for the prespecified endpoint in at least five of six prospective scenario runs; endpoint and direction are frozen before unblinding
MRS-DT-008
Handle stale or failed data safely
All stale, rejected, missing-event, and out-of-domain test cases produce the required state and no unqualified forecast
MRS-OPS-001
Meet decision timing
State update plus five scenarios completes in less than two minutes on the declared reference CPU environment
MRS-OPS-002
Reproduce forecasts
Three reruns match within 1e-6 relative tolerance for deterministic outputs and within declared Monte Carlo error for interval estimates

8. Validation Plan
Freeze equations or learned components, parameters, state-update logic, process ranges, scenario definitions, random seeds, and the analysis plan.
Replay historical runs in time order, revealing only information available at each forecast issue time.
Evaluate the locked six-run test once, including forecast horizon curves and calibration.
Conduct six prospective runs with the selected feed scenarios. Analysts receive scenario codes, not expected directions.
Compare the synchronized twin with three baselines: last observation carried forward, historical mean trajectory aligned by process day, and open-loop model from day 0.
Run failure injection for missing measurements, duplicate timestamps, unit errors, delayed feed events, impossible negative values, stale data, and solver failure.

The prospective study succeeds only if MRS-DT-001 through MRS-DT-008 pass. Failure of one metabolite endpoint triggers a scoped limitations review rather than silent averaging with stronger endpoints.
9. Risks and Operational Behavior
Risk
Required mitigation
Measurement update overfits assay noise
Include assay uncertainty and compare synchronized with open-loop forecasts
A batch moves outside the development domain
Show caution or unsupported status and prohibit unqualified scenario results
Event log and concentration measurements disagree
Reconcile volume and mass before updating the state
Forecast interval is interpreted as guaranteed containment
Document empirical coverage and model limitations
Scenario comparison is treated as autonomous control
Require explicit human review and keep write access to process controls out of scope
Internal mechanism is treated as biological proof
Accept the twin on forecast and scenario evidence and limit mechanistic claims

10. Deliverables and Traceability
Deliverables are the state and event schema, data manifest, model artifact, state-update implementation, scenario library, replay harness, test predictions, calibration report, failure-injection report, prospective validation report, user guide, and versioned environment. A Biosimulant Lab is an optional portable interface.

Requirement
Verification
Evidence artifact
Owner
MRS-IN-001 to MRS-IN-008
Schema, unit, identity, timing, and event-reconciliation tests
Input conformance report
Process analytics lead
MRS-OUT-001 to MRS-OUT-005
State, forecast, interval, status, and provenance tests
Output conformance report
Engineering lead
MRS-DQ-001 to MRS-DQ-005
Data and failure tests
Input-quality report
Process analytics lead
MRS-DT-001 to MRS-DT-007
Time-ordered retrospective and prospective analysis
Twin validation report
Validation owner
MRS-DT-008
Failure injection
Safety-behavior test report
Engineering lead
MRS-OPS-001 to MRS-OPS-002
Reference-environment benchmark
Performance and reproducibility report
Model owner

11. References
Richelle A, Andersson D, Antonakoudis A, et al. A Hybrid Modeling Framework for Predictive Digital Twins of CHO Cell Culture. Computational and Structural Biotechnology Journal. 2026;35(1):0078. https://doi.org/10.34133/csbj.0078
Justice C, Brix A, Freimark D, et al. Process control in cell culture technology using dielectric spectroscopy. Biotechnology Advances. 2011;29:391-401. https://doi.org/10.1016/j.biotechadv.2011.03.002

