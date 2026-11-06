DO NOT MODIFY - This is a template so don’t modify unless the intention is to change the template. Instead you should copy the content into a separate google doc. 
Generative MRS Example - Protein Binder Design
Model Requirements Specification: De Novo Protein Binders to IL-7R Alpha
This is a completed illustrative MRS for a research-use-only design campaign. It is not an active study, a therapeutic development plan, or a report of achieved results. Numeric targets are illustrative project requirements. Published evidence is cited.
1. Document Control
Field
Value
MRS identifier
EX-MRS-GEN-BINDER-001
Version
1.0 example
Status
Illustrative, not approved for execution
Model type
Generative with predictive filtering
Scientific owner
Protein science lead
Model owner
Computational protein design lead
Validation owner
Biophysics lead
Intended user
Protein design scientist
Last revised
2026-08-19

2. Objective and Intended Use
Generate compact de novo protein sequences predicted to fold as soluble monomers and bind a defined extracellular epitope on human interleukin-7 receptor alpha (IL-7R alpha). The model will propose a computationally filtered set from which 24 candidates will be synthesized and tested for expression, monodispersity, binding affinity, epitope competition, and selectivity.

RFdiffusion has demonstrated experimental de novo binder design to several protein targets, including IL-7R alpha, using target structure and interface hotspot conditioning [1]. That precedent establishes feasibility, not the success rate of this illustrative campaign.

The candidates are research reagents. No output may be described as therapeutic, safe, efficacious, or suitable for human or animal administration.
3. Design Target and Scope
Target: purified human IL-7R alpha extracellular domain with a frozen structure file, chain definition, residue numbering map, and construct sequence.
Desired epitope: the prespecified surface overlapping the binding site of a reference competition reagent. Exact hotspot residues are frozen in the campaign input manifest.
Candidate: one novel single-chain protein of 55 to 120 amino acids, excluding purification tags.
Intended function: bind purified target in vitro and compete with the reference reagent for the intended epitope.
Excluded goals: cellular agonism or antagonism, pharmacokinetics, immunogenicity, toxicity, developability for dosing, and activity in animals or humans.
4. Inputs and Outputs
Inputs
ID
Input
Requirement
MRS-IN-001
Target structure
Quality-reviewed coordinate file, construct sequence, biological assembly, chain identifiers, missing residues, ligands, and residue-number mapping
MRS-IN-002
Epitope specification
Approved hotspot residue list plus permitted contact surface
MRS-IN-003
Design bounds
Length 55 to 120 residues; single chain; permitted secondary-structure content; no required disulfide bond
MRS-IN-004
Sequence constraints
Standard amino acids only; prohibited motifs and composition limits from the frozen filter specification
MRS-IN-005
Reference databases
Versioned target-search database, sequence database, structure database, and model-training disclosure where available
MRS-IN-006
Randomness
Recorded random seeds and generation settings for every candidate

Outputs
ID
Output
Requirement
MRS-OUT-001
Candidate identity
Immutable identifier linking backbone, sequence, conditioning, seed, and all scores
MRS-OUT-002
Sequence and structure
Amino-acid sequence and designed three-dimensional coordinates
MRS-OUT-003
Constraint status
Pass or fail for every hard constraint with reason codes
MRS-OUT-004
Predicted quality
Fold-confidence, design-recapture, interface-confidence, clash, and composition metrics
MRS-OUT-005
Novelty and diversity
Search results, nearest known sequence, structural neighbor, and cluster assignment
MRS-OUT-006
Selection status
Generated, rejected, shortlisted, selected, synthesized, or experimentally tested


Computational scores must be described as predictions. They are not substitutes for binding, folding, specificity, or safety experiments.
5. Design Space and Constraints
Hard Constraints
No candidate released to synthesis may:

fall outside the 55 to 120 residue length range;
contain nonstandard or ambiguous residues;
contain more than one cysteine unless an approved disulfide design explicitly pairs cysteines;
contain a hydrophobic run longer than four residues according to the frozen residue list;
contain an unpaired buried polar network or unresolved severe atomic clash under the frozen structural checks;
contain a prohibited sequence motif from the safety and manufacturability filter;
fail the target-chain, hotspot, or residue-numbering integrity check; or
lack complete provenance linking sequence to the generated backbone and conditioning input.
Soft Objectives
High predicted monomer-fold confidence.
Close recapture of the designed monomer and target-bound geometry by an independent prediction workflow.
Low predicted interface error and favorable interface contact geometry.
Soluble expression potential without excessive hydrophobicity or charge imbalance.
Sequence and topology diversity across the selected set.
Low similarity to the frozen reference databases, without claiming that a database search proves absolute novelty.
6. Generation and Filtering Funnel
All counts are illustrative campaign requirements.

Generate at least 5,000 backbone designs across at least ten independent random seeds.
Generate four sequences per retained backbone using a sequence-design model, producing at least 10,000 sequence-backbone pairs after geometric prefilters.
Apply hard sequence, geometry, clash, and provenance filters.
Run an independent structure and complex prediction workflow on no fewer than 1,000 passing candidates.
Retain a computational shortlist of 120 candidates meeting the locked fold and interface thresholds.
Cluster the shortlist by sequence and predicted structure.
Select 24 candidates for synthesis using the locked ranking rule with a maximum of three candidates per cluster.

The ranking score, filter order, and thresholds are frozen before experimental results are available. Failed or unexpressed candidates remain in campaign denominators.
7. Novelty, Diversity, and Memorization Checks
Search every selected sequence against a frozen UniRef and Protein Data Bank sequence set using a documented alignment method.
Report the nearest hit, identity, aligned coverage, and E-value.
Require selected candidates to have less than 50 percent identity over at least 80 percent of candidate length to any non-target reference sequence, unless the scientific owner documents why a known motif is intentional.
Cluster selected candidates at 40 percent pairwise sequence identity and by a declared structural-similarity method.
At least eight sequence clusters and four predicted topology clusters must be represented among the 24 synthesized candidates.
Compare candidates with accessible training examples or model-provided nearest neighbors where available. If the generator's training corpus is unavailable, state that memorization cannot be excluded completely.
8. Experimental Validation
Assays
Expression: standardized small-scale expression and purification with yield reported in mg/L of clarified culture.
Monodispersity: analytical size-exclusion chromatography with aggregate or oligomer fraction reported.
Primary binding: biolayer interferometry against purified IL-7R alpha, including reference binder, irrelevant protein, and no-analyte controls.
Affinity confirmation: concentration series with global kinetic fit for candidates passing the primary screen.
Epitope confirmation: competition biolayer interferometry against the reference epitope reagent.
Selectivity: binding test against two prespecified structurally or functionally related receptor ectodomains and one unrelated protein.

Each binding experiment uses at least three independently prepared analyte dilutions. A second protein preparation is required to confirm any candidate counted toward the final biological success criterion.
Hit Definitions
Expressed candidate: soluble purified yield at least 2 mg/L.
Monomeric candidate: monomer peak area at least 80 percent by the declared size-exclusion method.
Binding hit: confirmed equilibrium dissociation constant no greater than 1 micromolar with interpretable sensorgrams and reference-subtracted response.
High-affinity hit: confirmed equilibrium dissociation constant no greater than 100 nanomolar.
Epitope-confirmed hit: binding response is reduced at least 70 percent by saturating reference competitor under the locked assay conditions.
Selective hit: no quantifiable binding to the three negative-control proteins at ten times the candidate concentration used for the target test.
9. Acceptance Requirements
All thresholds are illustrative project requirements.

ID
Requirement
Acceptance criterion
MRS-GEN-001
Produce valid designs
At least 95 percent of candidates released to the independent prediction stage pass all machine-checkable hard constraints
MRS-GEN-002
Preserve selection diversity
The 24 synthesized candidates represent at least eight sequence clusters and four structure clusters, with no more than three candidates per cluster
MRS-GEN-003
Document novelty
Every synthesized candidate has a complete frozen-database search report and satisfies the stated identity rule or has an approved exception
MRS-GEN-004
Achieve expression and monodispersity
At least 12 of 24 candidates meet both the expressed and monomeric definitions
MRS-GEN-005
Achieve binding
At least three of 24 candidates are confirmed binding hits
MRS-GEN-006
Achieve high affinity
At least one of 24 candidates is a confirmed high-affinity hit
MRS-GEN-007
Confirm intended epitope
At least one binding hit also meets the epitope-confirmed definition
MRS-GEN-008
Demonstrate tested selectivity
Every candidate presented as a final hit passes the stated negative-target panel
MRS-OPS-001
Preserve reproducibility
Every selected candidate can be regenerated or retrieved with identical sequence, coordinates, inputs, settings, and provenance


The campaign succeeds only if MRS-GEN-005, MRS-GEN-006, MRS-GEN-007, and MRS-GEN-008 all pass. Computational success without experimental binding does not satisfy the MRS.
10. Risks and Failure Behavior
Risk
Mitigation
Predicted fold or interface quality does not translate to experimental binding
Treat predictions as filters and retain prospective experimental success as the primary endpoint
Many similar candidates inflate apparent hit rate
Cluster before selection and limit candidates per cluster
Database novelty is mistaken for functional or legal novelty
Report search scope and avoid patent, freedom-to-operate, or absolute novelty claims
Sensor artifacts appear as binding
Require reference subtraction, concentration dependence, interpretable kinetics, and independent preparation confirmation
Binding is mistaken for desired biological activity
Keep cell signaling and therapeutic claims out of scope
Target structure or numbering is wrong
Freeze and review the construct-to-structure residue map before generation


Invalid generator outputs receive a failed status and remain in validity-rate calculations. A candidate with missing provenance cannot advance, irrespective of predicted quality.
11. Deliverables and Traceability
Deliverables are the target and epitope manifest, frozen design specification, generator and filter configurations, candidate registry, complete score table, database manifests, selection report, synthesis manifest, raw and analyzed assay data, final validation report, and reproducible environment. A Biosimulant Lab is an optional packaging artifact.

Requirement
Verification
Evidence artifact
Owner
MRS-IN-001 to MRS-IN-006
Target, epitope, design-bound, database, and provenance checks
Campaign input conformance report
Scientific owner
MRS-OUT-001 to MRS-OUT-006
Candidate-registry schema and lifecycle tests
Candidate registry validation report
Engineering lead
MRS-GEN-001 to MRS-GEN-003
Registry and frozen-filter analysis
Computational campaign report
Model owner
MRS-GEN-004
Expression and size-exclusion assays
Protein production report
Protein science lead
MRS-GEN-005 to MRS-GEN-008
Blinded biophysical assays
Binding, competition, and selectivity report
Biophysics lead
MRS-OPS-001
Provenance replay
Reproducibility report
Engineering lead

12. References
Watson JL, Juergens D, Bennett NR, et al. De novo design of protein structure and function with RFdiffusion. Nature. 2023;620:1089-1100. https://doi.org/10.1038/s41586-023-06415-8
Dauparas J, Anishchenko I, Bennett N, et al. Robust deep learning-based protein sequence design using ProteinMPNN. Science. 2022;378:49-56. https://doi.org/10.1126/science.add2187

