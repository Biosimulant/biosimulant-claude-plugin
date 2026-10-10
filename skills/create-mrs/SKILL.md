---
name: create-mrs
description: Create or revise a Model Requirements Specification (MRS) for a biological or computational model from scientific briefs, assay/data evidence, and intended-use decisions. Use when defining what the model must do and what evidence will establish acceptance; do not use for implementation design or an MTS.
metadata:
  version: "2026.10.04"
---

# Create MRS

Create a controlled requirements document whose source of truth is the scientific purpose, intended use, supported domain, required behavior, validation evidence, and acceptance criteria. Do not let a preferred algorithm, runtime, or existing implementation redefine those requirements.

State a concise scientific question or precise operational objective in the
purpose section, within the available inputs and intended-use limits. Reuse it
when naming a new study or explaining results. Keep acceptance criteria as
testable requirements; a question-shaped title is not evidence that they pass.
Preserve user-chosen model/project names and approved requirements rather than
renaming them for this presentation preference.

## Ground the draft

1. Read [references/suite-lifecycle.md](references/suite-lifecycle.md) for lifecycle, freeze, acceptance, and change-control rules.
2. Inspect the project for a biological brief, assay/data specification, existing MRS, validation protocol, relevant code, datasets/manifests, and decision records before asking questions.
3. Classify the model job. Read only the matching example reference(s):
   - predictive or ML: [references/examples/predictive-ml.md](references/examples/predictive-ml.md)
   - mechanistic: [references/examples/mechanistic.md](references/examples/mechanistic.md)
   - generative: [references/examples/generative.md](references/examples/generative.md)
   - optimization: [references/examples/optimization.md](references/examples/optimization.md)
   - simulation or digital twin: [references/examples/digital-twin.md](references/examples/digital-twin.md)
   - statistical estimation: [references/examples/statistical-estimation.md](references/examples/statistical-estimation.md)
   Read every applicable example for a hybrid model, but treat its numbers and scientific claims as illustrative rather than reusable facts.
4. Read [references/biosimulant-runtime.md](references/biosimulant-runtime.md) only when Biosimulant capability, delivery, or fit affects a requirement. An MRS may require a portable artifact or execution property, but it must not prescribe Biosimulant without an intended-use reason.

Prefer evidence over questions. Ask only about consequential scientific or product decisions that the available material cannot establish. Never invent owners, thresholds, sample sizes, assay behavior, citations, or approval state. Record unresolved facts as explicit open items with an owner and impact.

If the available study design cannot support the requested identification, validation, forecast, ranking, or intervention decision, stop that requested lifecycle at a read-only requirements/gap analysis. Do not create a project, workspace, revision, or prepared change merely to persist the refusal unless the user explicitly requests a durable gap-analysis record. Do not silently substitute a runnable exploratory model or weaker acceptance claim. You may propose a reduced intended use or minimum experimental design, but persistence or implementation begins only after the user explicitly accepts that changed objective.

## Create or revise

For a new MRS, run:

```bash
python3 <skill-dir>/scripts/start_mrs.py "<Model or Project Name>" --root <project-root>
```

Resolve `<skill-dir>` to the folder containing this `SKILL.md`. The command copies the protected template to `specifications/<model-slug>/mrs.md` and refuses to overwrite an existing file. The master asset is immutable; edit only the working copy.

For a revision, edit the existing MRS instead of starting from the template. Preserve its identifier lineage, increment the version according to project policy, update `Last revised` and revision history, assess approval impact, and retain decisions or superseded content needed for auditability. Changes to intended use, endpoint, domain, ground truth, required inputs, output interpretation, decision thresholds, or acceptance criteria require reapproval.

When working through the Biosimulant Agent Gateway, draft and validate the MRS with this skill, then submit its contents through `requirements_set` in `workspace_change_prepare`. The Gateway commit is an immutable storage revision, not scientific approval of the MRS. Show the prepared diff and digest before `workspace_change_apply`, and retain the MRS approval state inside the document.

## Authoring rules

- Complete the common core and retain every applicable model-type module. Delete unused modules and all template instructions from an approval candidate.
- Use stable requirement identifiers: `MRS-###` for cross-cutting acceptance requirements and the template prefixes for inputs, outputs, data quality, operations, and model-specific requirements. Do not reuse an identifier for a different requirement.
- Make every requirement observable and traceable to a verification or validation method, evidence artifact, owner, and unchanged acceptance criterion.
- Define inputs, outputs, units, timing, supported domain, uncertainty, failure/abstention behavior, provenance, and non-use explicitly.
- State whether one intended-use invocation is finite, precedes a temporal run,
  follows a temporal run, or must recur as simulated state evolves. Describe the
  scientific requirement without prescribing a Biosimulant hook or policy.
- Match partitions and evidence to the claimed generalization domain. Keep locked, external, and prospective evidence out of training, calibration, feature selection, threshold tuning, or other development decisions.
- Separate project requirements from literature facts and from example values. Cite factual scientific claims; label project-selected thresholds as requirements.
- Distinguish technical verification from scientific validation. Reproducible execution and passing software tests do not establish biological validity.
- Keep implementation choices out of the MRS unless they are genuine operational constraints. Record implementation alternatives and architecture in the MTS.
- Use `Not applicable` only with a reason. Drafts may contain explicit open items; approved documents may not contain placeholders, unresolved template choices, or unowned mandatory questions.

## Validate

Run:

```bash
python3 <skill-dir>/scripts/validate_mrs.py specifications/<model-slug>/mrs.md
```

Treat warnings as items to resolve or consciously retain in Draft/In review status. An Approved MRS must pass with no errors. Then perform a semantic review: confirm that the stated acceptance criteria answer the intended biological decision and that no implementation preference has silently become a scientific requirement.

Before presenting an MRS as approval-ready, perform a whole-document consistency
review once editing is complete. Search every section, table, revision note, constraint,
and model-type module for stale values or contradictory claims about units, time
bases, conversion factors, parameter exposure, source mutation, intended use,
approval state, and validation evidence. A validator exit of zero does not make
contradictory prose acceptable. When the source uses an undeclared time basis,
keep source time and any evaluation-time convention explicitly distinct in every
occurrence.

User authorization to approve an evaluation MRS must be represented explicitly
in the document status, approval table or receipt, date, and revision history
before an MTS treats it as approved. Authorization never permits weakening an
acceptance threshold, inventing evidence, or marking a validation result as
having passed before it is executed.


## Visualization deliverables

Before authoring, call `get_biosimulant_authoring_contract` with topic `visualization`.
The complete catalog contains timeseries, bar, scatter, heatmap, graph, table, image,
structure3d and text, including payload examples, limits and retained artifact rules.
Almost every scientific Lab needs a useful visual of actual computed outputs; choose
the type by the user's question rather than always emitting a table. Record expected
views, source outputs, units and caveats in the MRS; record render/schema, owning module,
typed wiring, lifecycle, artifact retention and executable checks in the MTS.
Implement reusable `BioModule.visualize()` and declare `lab.yaml` visualization requirements
(or a justified opt-out for infrastructure-only work). Inspect actual composed results,
check plotted values against typed outputs, and verify artifacts and reopening. Missing
or invalid required views block qualification/publication. Ad-hoc Studio chat charts
do not satisfy this contract. Historical Labs without a declaration remain compatible.
