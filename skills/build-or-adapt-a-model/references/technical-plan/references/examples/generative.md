DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Generative MTS Example - Protein Binder Design
Modeling Technical Specification: De Novo Protein Binders to IL-7R Alpha
This is an implementation-ready illustrative technical design for a research-use-only campaign. It is not an implemented workflow, therapeutic plan, or report of achieved results.
1. Document Control
Field
Value
MTS identifier
EX-MTS-GEN-BINDER-001
Version
1.0 example
Status
Illustrative, not approved for execution
MRS
EX-MRS-GEN-BINDER-001
Scientific owner
Protein science lead
Technical owner
Computational protein design lead
Validation owner
Biophysics lead
Biosimulant fit
External boundary, no core Biosimulant execution

2. Technical Decision Summary
Run generation and filtering in a containerized GPU workflow using RFdiffusion, ProteinMPNN, an independent structure and complex predictor, sequence and structure search tools, and an immutable candidate registry. Use a workflow engine and GPU scheduler designed for artifact-heavy batch jobs. Do not wrap RFdiffusion or the full campaign as a BioModule in v1.

The only Biosimulant boundary considered is a later read-only result-inspection or scoring Lab after the candidate registry schema is stable. That boundary is not required for this campaign and no model.yaml or lab.yaml will be created.
3. Architecture
flowchart LR
    A["Frozen target and epitope manifest"] --> B["RFdiffusion backbone generation"]
    B --> C["ProteinMPNN sequence design"]
    C --> D["Hard-constraint filters"]
    D --> E["Independent fold and complex prediction"]
    E --> F["Novelty and diversity analysis"]
    F --> G["Locked candidate registry"]
    G --> H["Selection manifest"]
    H --> I["Expression and biophysical assays"]
    I --> J["Campaign validation report"]
Selected Stack
Layer
Technology
Responsibility
Workflow
Nextflow with an executor profile for the approved GPU environment
Stage orchestration, retries, caching, and artifact lineage
Containers
Immutable OCI images referenced by digest
Model and tool environments
Backbone generation
Locked RFdiffusion release
Target- and hotspot-conditioned backbone generation
Sequence design
Locked ProteinMPNN release
Four sequences per retained backbone
Independent prediction
Locked structure and complex-prediction environment
Fold recapture and interface metrics
Sequence search
MMseqs2 against frozen UniRef and PDB-derived sequence databases
Novelty evidence
Structure search
Declared structural search and clustering tool
Topology diversity and nearest structural neighbor
Registry
Append-only Parquet tables plus content-addressed artifact storage
Candidate identity, lineage, scores, statuses, and files
Analysis
Versioned Python package and Quarto or notebook-free report build
Frozen tables, plots, and selection report

4. Inputs and Immutable Identity
Campaign Manifest
campaign_id: IL7RA_BINDER_EXAMPLE_001
target:
  construct_sequence_sha256: "recorded-before-run"
  structure_sha256: "recorded-before-run"
  chain: A
  residue_numbering_map: target-residue-map.csv
epitope:
  hotspot_residues: ["A:100", "A:102", "A:135"]
design:
  length_min: 55
  length_max: 120
  backbones_required: 5000
  sequences_per_backbone: 4
  seeds_required: 10
databases:
  uniref_manifest: databases/uniref-manifest.json
  pdb_sequence_manifest: databases/pdb-sequence-manifest.json

The residue identifiers above are illustrative placeholders within this completed example and would be replaced by scientifically reviewed residues before execution. A campaign cannot start while the structure-to-construct map or epitope is unresolved.
Candidate Identity
candidate_id is the SHA-256 digest of the canonical campaign identifier, target checksum, generation configuration, seed, backbone coordinates, sequence, and parent identifiers. Display names never replace this identity.

The registry records every generated candidate and every stage transition. Rejected, failed, unexpressed, and untested candidates remain present.
5. Generation and Filtering Implementation
Validate target coordinates, chain, sequence correspondence, missing residues, and hotspot surface exposure.
Generate at least 5,000 backbones across ten or more seeds. Persist failed jobs and reason codes.
Apply geometry and chain-integrity checks before sequence design.
Generate four ProteinMPNN sequences per passing backbone.
Apply hard sequence, motif, composition, cysteine, hydrophobic-run, clash, and provenance filters in a frozen order.
Run independent monomer and complex prediction for at least 1,000 candidates.
Calculate fold confidence, interface confidence, design recapture, clash, and contact metrics.
Search frozen sequence and structure databases and record nearest neighbors.
Form a 120-candidate computational shortlist under locked thresholds.
Cluster the shortlist, then select 24 candidates with no more than three per cluster.
Hard-Constraint Engine
Each filter is a pure versioned function returning candidate ID, filter ID, version, pass or fail, measured value, threshold, and timestamp. A failed hard constraint cannot be overridden by a ranking score. Exceptions require a new selection-manifest version and scientific approval.
Resource and Retry Rules
GPU jobs request the resource class validated for each locked container.
Out-of-memory failures may retry once at the approved larger memory class without changing scientific parameters.
Numerical or model failures do not retry with altered seeds under the same candidate identity.
Workflow retries, cache reuse, and manual restarts remain visible in execution provenance.
Credentials and database access tokens are injected by the scheduler and never stored in the campaign manifest.
Execution Command
nextflow run workflows/binder-design.nf \
  -profile locked_gpu \
  -params-file config/IL7RA_BINDER_EXAMPLE_001.yaml \
  -with-report reports/execution.html \
  -with-trace reports/execution.tsv

The workflow revision, executor profile, parameter-file checksum, and container digests are captured before execution. Resume is permitted only against the same locked campaign inputs.
6. Output and Exchange Contracts
Candidate Registry Record
{
  "candidate_id": "sha256:example",
  "campaign_id": "IL7RA_BINDER_EXAMPLE_001",
  "parent_backbone_id": "sha256:example-backbone",
  "sequence": "AMINOACIDSEQUENCE",
  "length": 78,
  "status": "shortlisted",
  "hard_constraints_passed": true,
  "sequence_cluster": "seq-07",
  "structure_cluster": "struct-03",
  "nearest_sequence_identity": 0.31,
  "artifact_checksums": {
    "designed_structure": "sha256:example",
    "predicted_complex": "sha256:example"
  }
}
Experimental Handoff
The locked selection manifest contains exactly 24 candidate IDs, sequences, purification-tag instructions, selection strata, randomized assay codes, and checksums. Experimental teams receive assay codes and required constructs, not mutable computational ranks.

Assay results return through a separate immutable table keyed by assay code and preparation identifier. The join key is revealed only after the assay result table is frozen.
7. Biosimulant Fit Assessment
Question
Decision
Outcome
External boundary
Why the core remains external
The campaign is a file- and artifact-heavy GPU batch pipeline with native workflow scheduling, caching, and retry needs
Biosimulant value in v1
No value sufficient to justify wrapping the core generation workflow
Possible future boundary
A read-only Lab that loads a locked candidate registry and exposes scoring, cluster inspection, or composition with another validated model
Reassessment trigger
Repeated use of a stable candidate-review contract across multiple campaigns


If a future result-inspection Lab is built, the candidate-registry schema remains authoritative. Biosimulant may read the registry but must not alter campaign status, candidate identity, or locked selection evidence.
8. MRS Traceability and Tests
MRS requirement
Technical implementation
Test or protocol
Verification evidence
MRS-IN-001 to MRS-IN-006
Frozen target, epitope, bounds, database, and seed manifests
GEN-T01
Campaign-input conformance report
MRS-OUT-001 to MRS-OUT-006
Append-only candidate registry and content-addressed artifacts
GEN-T03, GEN-T06, GEN-T07
Registry validation report
MRS-GEN-001
Pure hard-filter functions and immutable stage denominators
GEN-T03
Constraint audit
MRS-GEN-002
Sequence and structure clustering before selection
GEN-T05
Diversity report
MRS-GEN-003
Frozen-database search with exceptions recorded
GEN-T04
Novelty report
MRS-GEN-004
Expression and size-exclusion result tables
GEN-V01
Protein-production report
MRS-GEN-005 to MRS-GEN-008
Locked binding, affinity, competition, and selectivity analyses
GEN-V02
Blinded biophysical validation report
MRS-OPS-001
Content-addressed lineage and container digests
GEN-T02, GEN-T08
Reproducibility report

Required Technical Tests
GEN-T01: Reject a target checksum mismatch, chain mismatch, unresolved hotspot, or inconsistent residue map.
GEN-T02: Re-run a representative generation subset from frozen seeds and confirm identity under the declared determinism limits.
GEN-T03: Unit-test every hard filter at its boundary and preserve failed candidates.
GEN-T04: Verify that sequence and structure database manifests are immutable during a campaign.
GEN-T05: Prove that no selected cluster contributes more than three candidates and minimum cluster counts are met.
GEN-T06: Rebuild the selection report only from the registry and frozen configuration.
GEN-T07: Inject failed, cancelled, and out-of-memory jobs and verify correct denominators and reason codes.
GEN-T08: Reproduce the complete 24-candidate handoff manifest in a clean analysis environment.

GEN-V01 is the locked expression and size-exclusion protocol. GEN-V02 is the blinded binding, affinity, epitope-competition, and selectivity protocol. Their numeric acceptance rules remain those in the adjacent MRS.
9. Lock, Release, and Monitoring
The campaign lock includes target and epitope manifests, all container digests, model checkpoints or release identities, workflow revision, filter specification, database manifests, candidate registry, selection rules, analysis environment, and prospective assay protocol.

The computational release is the locked selection manifest, not a claim of binding. Biological acceptance occurs only after the experimental MRS gates pass.

Monitor failed-stage rates, hard-constraint yield, cluster diversity, database-search coverage, expression yield, binding hit rate, and any deviation from the frozen assay protocol. A changed target construct, epitope, generator, ranking funnel, or hit definition requires impact review and a new campaign version.
10. References
Adjacent Model Requirements Specification
https://www.nature.com/articles/s41586-023-06415-8
https://www.nature.com/articles/s41586-022-04654-9

