DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Predictive ML MTS Example - CRISPR Guide Efficiency
Modeling Technical Specification: SpCas9 Guide Activity Ranking in Primary T Cells
This is an implementation-ready illustrative technical design. It is not an implemented model, active study, or report of achieved performance.
1. Document Control
Field
Value
MTS identifier
EX-MTS-ML-CRISPR-001
Version
1.0 example
Status
Illustrative, not approved for execution
MRS
EX-MRS-ML-CRISPR-001
Model owner
Computational biology lead
Technical owner
ML engineering lead
Validation owner
Independent computational validation lead
Delivery owner
Scientific platform lead
Biosimulant fit
Adapter fit for frozen inference only

2. Technical Decision Summary
Train a sequence-and-context neural ensemble outside Biosimulant using PyTorch. Export five locked inference members to ONNX and package them with a versioned preprocessing artifact, conformal residual table, genome annotation manifest, and domain rules. A stateless Biosimulant adapter will perform validation, ONNX inference, calibrated interval construction, and within-gene ranking for repeatable scientific use.

Training, hyperparameter search, data partitioning, and model selection remain in the external ML workflow. Biosimulant will not orchestrate training.
3. Architecture
flowchart LR
    A["Versioned guide and assay data"] --> B["External PyTorch training pipeline"]
    B --> C["Five locked ONNX members"]
    C --> D["GuideScorer BioModule"]
    E["Guide batch and annotation"] --> D
    D --> F["Ranked guides, intervals, and domain status"]
    F --> G["Scientist review or downstream selection workflow"]
Components
Component
Responsibility
Technology
Authoritative artifact
Dataset builder
Validate assay records and create immutable gene-grouped partitions
Python, PyArrow, Pandera
Data and partition manifests
Feature builder
Encode 28-base context, PAM, transcript position, and protocol context
Versioned Python package
Preprocessing wheel and JSON configuration
Trainer
Train five ensemble members on identical partitions with different seeds
PyTorch 2.x
Training runs and checkpoints
Calibrator
Estimate conformal residual quantiles on calibration genes
NumPy and SciPy
Residual table by efficiency band
Exporter
Export and compare ONNX inference
ONNX opset 18 and ONNX Runtime
Five ONNX files and parity report
GuideScorer
Validate inputs, run ensemble, form intervals, rank, and emit provenance
Custom BioModule using ONNX Runtime
Biosimulant model package

4. Data and Training Implementation
Observation key: guide sequence, GRCh38 locus, target gene, donor, protocol version, and assay batch.
Partition key: target gene. All guides for a gene remain together.
Prospective donors and genes remain absent from every development artifact.
Exact protospacers, reverse complements, and identical loci are deduplicated before partitioning.
Sequence context is one-hot encoded in A, C, G, T order. Ambiguous bases fail input validation.
Continuous metadata are standardized using development-partition statistics stored in preprocessing.json.
Categorical protocol fields use a closed vocabulary. Unknown categories return OUT_OF_DOMAIN.
No outcome, replicate summary, or post-editing feature enters the feature table.
Model Architecture
Sequence branch: two one-dimensional convolution blocks over the 28-base context, global max pooling, and a 64-unit dense layer.
Context branch: transcript-position and protocol features passed through a 32-unit dense layer.
Fusion: concatenation followed by 64- and 32-unit dense layers with dropout.
Output: sigmoid-scaled editing-efficiency estimate from 0 to 1.
Loss: donor-weighted Huber loss so genes or donors with more measurements do not dominate.
Ensemble: five seeds selected by median gene-level Spearman correlation on validation genes.
Calibration: central 80 percent split-conformal intervals from held-out calibration genes, stratified by predicted-efficiency tercile when every stratum has sufficient calibration observations.
Locked Training Procedure
Validate the data manifest and gene-level partition manifest.
Fit preprocessing on development genes only.
Train 20 candidate configurations using grouped cross-validation.
Select one architecture and training configuration using the prespecified validation score.
Train five seed members without locked-test or prospective outcomes.
Fit conformal residuals on the calibration partition.
Export every member to ONNX.
Compare native PyTorch and ONNX outputs before release.
5. Interfaces and Failure Behavior
Input Record
{
  "protocol_version": "tcell-rnp-v1",
  "genome_build": "GRCh38",
  "guides": [
    {
      "guide_id": "GENE1_g01",
      "protospacer": "ACGTACGTACGTACGTACGT",
      "pam": "AGG",
      "context_28nt": "TTTTACGTACGTACGTACGTACGTAGGA",
      "gene": "GENE1",
      "transcript": "ENST_EXAMPLE",
      "coding_position_fraction": 0.34
    }
  ]
}
Output Record
{
  "model_version": "1.0.0",
  "protocol_version": "tcell-rnp-v1",
  "results": [
    {
      "guide_id": "GENE1_g01",
      "predicted_efficiency": 0.63,
      "interval_80": [0.44, 0.78],
      "within_gene_rank": 1,
      "domain_status": "supported",
      "reason_codes": []
    }
  ]
}

Invalid sequence, PAM, genome build, or required metadata returns INVALID_INPUT and no score for that guide.
An unknown protocol or unsupported annotation returns OUT_OF_DOMAIN and no unqualified score.
A failed ensemble member returns EXECUTION_FAILED; the adapter does not silently average fewer members.
Off-target analysis is excluded and never inferred from the activity score.
6. Biosimulant Fit and Realization
Decision
Question
Decision
Outcome
Adapter fit
Why Biosimulant adds value
Versioned inference packaging, typed inputs and outputs, reproducible local runs, and composition with future guide-selection workflows
Why it is not native
The model is single-pass inference and its training workflow is better served by ML tooling
Authoritative artifact
ONNX ensemble, preprocessing artifact, and conformal table
Unsupported Biosimulant use
Training, hyperparameter search, or prospective assay orchestration

model.yaml Excerpt
schema_version: "2.0"
title: "Primary T-Cell SpCas9 Guide Scorer"
description: "Scores and ranks protocol-matched SpCas9 guides."
standard: onnx
package: biosimulant/tcell-guide-scorer
version: 1.0.0

biosim:
  entrypoint: "src.guide_scorer:GuideScorer"
  communication_step: 1.0

io:
  inputs:
    - name: guide_batch
      signal_type: record
      schema:
        protocol_version: string
        genome_build: string
        guides: array
  outputs:
    - name: ranked_guides
      signal_type: record
      schema:
        model_version: string
        results: array

runtime:
  python_version: "3.12"
  dependencies:
    packages:
      - onnxruntime==1.18.1
      - numpy==1.26.4
lab.yaml Excerpt
schema_version: "2.0"
title: "Primary T-Cell Guide Ranking"
description: "One-pass validated guide scoring and ranking."
package: biosimulant/tcell-guide-ranking
version: 1.0.0

io:
  inputs:
    - name: guide_batch
      maps_to: scorer.guide_batch
  outputs:
    - name: ranked_guides
      maps_to: scorer.ranked_guides

models:
  - path: models/tcell-guide-scorer
    alias: scorer
    parameters: {}

wiring: []

runtime:
  duration: 1.0
  communication_step: 1.0
  settle_steps: 0

The adapter executes once. Model time has no biological interpretation in this Lab.
Execution Commands
biosimulant labs validate ./tcell-guide-ranking --strict --json
biosimulant labs run ./tcell-guide-ranking --results-file ranked-guides.json --json --no-open
biosimulant labs package ./tcell-guide-ranking --out dist
biosimulant labs validate dist/biosimulant__tcell-guide-ranking-1.0.0.bsilab --json
7. MRS Traceability and Tests
MRS requirement
Technical implementation
Test or protocol
Verification evidence
MRS-IN-001 to MRS-IN-006
Closed input schema, GRCh38 manifest, protocol vocabulary, and no outcome-derived features
ML-T01, ML-T02
Schema, boundary, and feature-lineage tests
MRS-OUT-001 to MRS-OUT-005
Ensemble mean, conformal interval, within-gene rank, domain codes, and provenance
ML-T03 to ML-T07
Golden output fixtures and result-schema tests
MRS-DQ-001 to MRS-DQ-005
Dataset builder enforces assay QC before partitioning
ML-V01
Data-readiness report
MRS-ML-001 to MRS-ML-006
Gene-grouped evaluation, Rule Set 2 baseline, calibration, and strata reports
ML-V02
Locked validation report
MRS-OPS-001
Batched ONNX inference
ML-V04
Reference CPU benchmark
MRS-OPS-002
Frozen artifacts and deterministic stable sort
ML-T04, ML-T05
Three-run equality test
Prospective definition of done
Locked selection manifest generated by this package
ML-V03
Blinded prospective assay report

Required Technical Tests
ML-T01: Reject ambiguous bases, invalid PAMs, duplicate guide identifiers, unknown protocols, and inconsistent gene annotations.
ML-T02: Prove that donors and target genes do not cross partition manifests.
ML-T03: Compare PyTorch and ONNX outputs for 10,000 reference guides with maximum absolute difference no greater than 1e-5.
ML-T04: Prove identical ranking for tied values using guide identifier as the documented stable tie-breaker.
ML-T05: Reproduce ensemble outputs and interval lookups in a clean CPU environment.
ML-T06: Validate and run the .bsilab package locally.
ML-T07: Compare direct ONNX inference with BioModule output for every golden fixture.

ML-V01 is the assay data-readiness protocol, ML-V02 is the locked retrospective validation protocol, ML-V03 is the blinded prospective assay protocol, and ML-V04 is the reference-CPU benchmark protocol.
8. Lock, Release, and Monitoring
The lock contains the five ONNX files, preprocessing JSON, conformal table, annotation manifest, protocol vocabulary, code commit, environment lock, partition manifest, Rule Set 2 implementation, test fixtures, and model card.

Release requires all MRS computational gates, ONNX parity, package validation, clean-environment reproduction, and independent review. Prospective biological acceptance remains separate.

Monitor protocol-version frequency, out-of-domain rate, prediction distribution, eventual assay residuals, runtime, and failed ensemble calls. A new assay protocol, genome build, material calibration failure, or sustained performance decline requires review and potentially a new MRS version.
9. References
Adjacent Model Requirements Specification
https://docs.biosimulant.com/runtime/add-onnx-model
https://docs.biosimulant.com/runtime/model-manifest
