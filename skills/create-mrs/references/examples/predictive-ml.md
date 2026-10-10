DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Predictive ML MRS Example - CRISPR Guide Efficiency
Model Requirements Specification: SpCas9 Guide Activity Ranking in Primary T Cells
This is a completed illustrative MRS, not an active study or a report of achieved results. Project quantities and acceptance thresholds below are teaching requirements. Published scientific statements are cited.
1. Document Control
Field
Value
MRS identifier
EX-MRS-ML-CRISPR-001
Version
1.0 example
Status
Illustrative, not approved for execution
Model type
Predictive / ML
Scientific owner
Genome engineering lead
Model owner
Computational biology lead
Validation owner
Assay development lead
Intended user
T-cell engineering scientist
Last revised
2026-08-19


Approval in a live project would require the scientific, data, modeling, assay, and intended-use owners. This example has no operational approval.
2. Objective and Intended Use
Biological Objective
Given a candidate 20-nucleotide SpCas9 protospacer, its NGG PAM and local genomic context, predict and rank the fraction of alleles edited after a fixed ribonucleoprotein electroporation protocol in activated primary human CD3-positive T cells. The result will help scientists select three guides per gene for small-scale validation.

Guide activity varies substantially, and sequence-derived design rules can improve guide selection. Doench et al. developed Rule Set 2 from empirical guide data and showed that design rules can improve library activity [1]. The project does not assume that performance reported in immortalized cell lines transfers unchanged to primary T cells.
Intended Decision
Decision: choose three of six to ten designable guides per target gene for experimental validation.
User: a genome engineering scientist reviewing model rank, uncertainty, off-target annotation, and design constraints.
Decision point: before guide synthesis.
False-positive cost: synthesis and assay capacity spent on an inefficient guide.
False-negative cost: discarding an efficient guide and possibly concluding that a tractable gene is difficult to edit.
Human review: mandatory. The activity model does not replace off-target, transcript, isoform, or safety review.
Non-Use
The model must not be used to predict off-target cleavage, clinical editing outcomes, homology-directed repair, base-editing or prime-editing efficiency, non-SpCas9 nucleases, non-NGG PAMs, or untested delivery protocols.
3. Model Definition and Scope
Unit of prediction: one unique protospacer-locus-cell-protocol combination.
Model job: predict a continuous editing-efficiency score and rank guides within a gene.
Supported domain: NGG-PAM SpCas9 knockout guides targeting constitutively expressed exons in activated primary human T cells under the specified ribonucleoprotein protocol.
Excluded domain: guides spanning common variants in the tested donor, repetitive loci, ambiguous genome mappings, or targets with fewer than six designable guides.
Required baseline: Doench Rule Set 2 score [1] plus a simple GC-content and position baseline fitted on development data.
4. Inputs and Outputs
Inputs
ID
Input
Format
Required validation
MRS-IN-001
Protospacer
Uppercase 20-base DNA sequence
A/C/G/T only; unique guide-locus identifier
MRS-IN-002
PAM
Three-base sequence
Must match NGG on the target strand context
MRS-IN-003
Local context
Four upstream bases, protospacer, PAM, and four downstream bases
GRCh38 reference and strand recorded
MRS-IN-004
Target annotation
Gene, transcript, exon, coding position, and strand
Approved annotation release and canonical transcript flag
MRS-IN-005
Protocol context
Cas9 reagent, guide chemistry, activation, delivery, dose, and readout time
Must match a supported protocol version
MRS-IN-006
Donor metadata for validation
Donor pseudonym, sex where available, activation batch, and genotype-overlap flag
No directly identifying data


No outcome-derived feature, post-editing measurement, plate result, or guide-level replicate summary may be available to the model at inference time.
Outputs
ID
Output
Definition
MRS-OUT-001
Predicted editing efficiency
Fraction from 0 to 1 for indel-bearing alleles at 72 hours
MRS-OUT-002
Within-gene rank
Rank among all eligible guides submitted for the gene
MRS-OUT-003
Predictive interval
Central 80 percent interval reflecting model and observed donor variability
MRS-OUT-004
Domain status
Supported, caution, or unsupported, with reason codes
MRS-OUT-005
Provenance
Model version, genome build, annotation version, protocol version, and run time


Unsupported inputs must not receive an unqualified activity score. Off-target information, if displayed beside the result, must be labeled as a separate analysis.
5. Ground Truth and Data
Ground Truth
Editing efficiency is the background-corrected fraction of aligned amplicon reads containing an indel within the prespecified nuclease window at 72 hours after electroporation. Each retained sample must have at least 10,000 quality-filtered reads, an unedited control from the same donor and batch, and no sample-identity discrepancy.

The guide-level target is the median across technical replicates within a donor. Donors are biological replicates and must not be averaged before donor-level variability is recorded.
Illustrative Data Plan
Development experiment: 600 guides across 30 genes, four independent donors, and at least three electroporation batches.
Technical replication: two amplicon-library preparations per donor-guide measurement.
Locked prospective validation: 200 guides across 20 genes absent from model development, measured in three new donors and at least two new electroporation batches.
Public evidence: published datasets may support feature exploration and baseline implementation, but a public observation must not be treated as protocol-matched primary T-cell ground truth without compatibility evidence.
Quality Gates
ID
Gate
Threshold and action
MRS-DQ-001
Read depth
At least 10,000 filtered reads; otherwise repeat or exclude
MRS-DQ-002
Technical replicate agreement
Absolute difference no greater than 0.15; otherwise investigate and repeat
MRS-DQ-003
Negative control
Indel fraction no greater than 0.02; otherwise reject the affected batch
MRS-DQ-004
Donor and sample identity
Full concordance with sample manifest; any mismatch is excluded
MRS-DQ-005
Protocol completeness
All required reagent, timing, and batch metadata present

6. Partitioning and Generalization
The primary generalization claim is to genes and donors not seen during development under the same protocol.

All guides for one gene must remain in one partition.
Exact protospacers, reverse complements, and guides targeting the same genomic locus must not cross partitions.
Donors used for the prospective set must not contribute development data.
Hyperparameters, preprocessing, feature selection, calibration, and decision thresholds must be determined without the locked test or prospective outcomes.
Results must be reported per gene, per donor, and per batch, not only as a pooled guide-level score.

A random guide-row split is prohibited because it would not test the stated gene-level generalization claim. Gene-aware validation has precedent in early sgRNA activity modeling [2], and leave-cell-type-out evaluation has been used to expose context generalization limits [3].
7. Performance and Acceptance Requirements
All thresholds in this section are illustrative project requirements, not claims from the cited studies.

ID
Requirement
Acceptance criterion
MRS-ML-001
Rank unseen guides within held-out genes
Median per-gene Spearman correlation at least 0.50; lower bound of the gene-bootstrap 95 percent interval at least 0.35
MRS-ML-002
Enrich efficient guides
Top-ranked quintile contains at least twice the prevalence of guides with editing efficiency at least 0.50 compared with the complete eligible set
MRS-ML-003
Improve the published sequence baseline
Median per-gene Spearman correlation exceeds Rule Set 2 by at least 0.05 on the locked test set
MRS-ML-004
Provide calibrated magnitudes
Mean absolute calibration error no greater than 0.10 across ten prespecified prediction bins, with donor-stratified plots
MRS-ML-005
Quantify uncertainty
Central 80 percent predictive intervals contain 70 to 90 percent of donor-level outcomes overall and in each prespecified efficiency tercile
MRS-ML-006
Preserve subgroup visibility
Report all primary metrics by donor, gene-expression band, GC-content band, and electroporation batch; no stratum with at least 30 guides may have negative median rank correlation without investigation
MRS-OPS-001
Batch throughput
Score 10,000 valid guides in less than five minutes on the declared CPU reference environment
MRS-OPS-002
Deterministic ranking
Same model, inputs, and configuration return identical ranks across three reruns

Prospective Biological Definition of Done
For the 20 unseen genes, at least 70 percent of genes must have one or more model-selected guides with median editing efficiency of at least 0.50 across the three new donors. The selected set must also achieve at least a 1.5-fold higher hit rate than three guides per gene chosen by the Rule Set 2 baseline. Both criteria must pass.
8. Validation Plan
Lock code, model, feature pipeline, baseline implementations, thresholds, genome annotation, and the analysis plan.
Run the locked gene-held-out test once and calculate gene-bootstrap confidence intervals.
Review calibration, residuals, failures, and performance strata before any prospective selection.
Select prospective guides using the locked ranking rule without seeing outcomes.
Randomize guide positions across assay plates and blind the assay analyst to model rank until the result table is frozen.
Report all attempted guides, assay exclusions, and missing outcomes. Excluded measurements do not silently reduce the prospective denominator.

Negative controls include sequence-shuffled feature checks, label permutation, a GC-only model, and removal of protocol-context features. A large performance increase under an invalid split must be documented as leakage evidence, not model capability.
9. Risks and Failure Behavior
Risk
Mitigation
Protocol or cell-state shift changes sequence-activity relationships
Version the protocol, show domain status, and require prospective recalibration after a material assay change
Gene-level features leak outcomes
Restrict features to information available before testing and evaluate with gene-grouped splits
Donor variability is hidden by pooled metrics
Retain donor-level observations and report donor-stratified performance
A high activity score is mistaken for a safety assessment
Keep activity and off-target outputs separate and require human review
Model confidence is overinterpreted
Use empirically checked predictive intervals and abstain outside the supported domain

10. Deliverables and Traceability
Required deliverables are versioned code, model artifact, input schema, model card, data manifest with checksums, baseline implementations, locked predictions, validation report, prospective selection manifest, and reproducible environment. A portable Biosimulant Lab may be supplied as an optional execution artifact.

Requirement
Verification
Evidence artifact
Owner
MRS-IN-001 to MRS-IN-006
Schema and boundary tests
Input conformance report
Engineering lead
MRS-OUT-001 to MRS-OUT-005
Output-schema, range, status, and provenance tests
Output conformance report
Engineering lead
MRS-DQ-001 to MRS-DQ-005
Assay QC analysis
Data readiness report
Assay lead
MRS-ML-001 to MRS-ML-006
Locked retrospective analysis
Validation report and prediction table
Validation lead
Prospective definition of done
Blinded prospective experiment
Frozen assay report and selection manifest
Scientific owner
MRS-OPS-001 to MRS-OPS-002
Reference-environment benchmark
Reproducibility report
Model owner

11. References
Doench JG, Fusi N, Sullender M, et al. Optimized sgRNA design to maximize activity and minimize off-target effects of CRISPR-Cas9. Nature Biotechnology. 2016;34:184-191. https://doi.org/10.1038/nbt.3437
Doench JG, Hartenian E, Graham DB, et al. Rational design of highly active sgRNAs for CRISPR-Cas9-mediated gene inactivation. Nature Biotechnology. 2014;32:1262-1267. https://doi.org/10.1038/nbt.3026
Chuai G, Ma H, Yan J, et al. DeepCRISPR: optimized CRISPR guide RNA design by deep learning. Genome Biology. 2018;19:80. https://doi.org/10.1186/s13059-018-1459-4

