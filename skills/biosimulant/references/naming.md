# Naming and identity

Read this before creating or renaming a Lab, an embedded model, or a child Lab.
Respect explicit user names and preserve imported scientific titles and attribution.
Naming findings request review; they are not permission to rename existing work.

## Separate scientific identity from instance role

| Field | Meaning | Example |
|---|---|---|
| Lab or model `title` | Human-readable scientific purpose or component responsibility | Plate Colony Counter; YOLOX-Tiny Colony Detector |
| Manifest `package` | Stable package identity, independent of display wording | plate-colony-counter |
| Published reference | Publisher, package and exact release version | demi/plate-colony-counter@0.1.0 |
| Entry `alias` | This instance's role inside its immediate parent Lab | detector; control; treatment |
| Port `name` | Quantity or data exposed by the component | colony_count; detections |

Choose a Lab title that describes the task or system. Add species, dataset, method,
or scientific scope when it distinguishes the intended use. Name a model for its
responsibility and, when useful, its actual method. Use Plate Colony Counter for
visible-colony detection; CFU/mL would imply a different measurement.
Do not invent an algorithm or scientific scope to make a name sound specific.

Use short lowercase hyphenated package names. Published package slugs are 2–64
characters, beginning and ending with a letter or digit. The connected account
determines the publishing namespace; never invent publisher ownership. Keep the
release version in `version`, not in the package slug. Retain an existing package
identity when its purpose is unchanged; a new scientific purpose may justify a
new identity with explicit provenance. A display-title change alone is not a new
package family. A new workspace derives an initial slug from its title: inspect
and deliberately set the manifest package before publication rather than treating
that generated slug as the final identity.

Use short descriptive aliases such as `preprocess`, `detector`, and `count`.
Aliases must start with a letter, contain only letters, digits, underscores or
hyphens, and be at most 64 characters. Prefer lowercase words with underscores
for aliases containing multiple words. Models and child Labs share one sibling
alias namespace: every explicit alias in the same parent must be unique.
Prefer roles such as `control` and `treatment` to unexplained `model1` and `model2`.
Preserve meaningful existing aliases and source-native identifiers.

## Models and nested Labs

An embedded model has its own model.yaml title and an alias in the parent's
`models` list. It does not need a separate Hub release. A nested Lab has its own
lab.yaml identity and appears in the parent's `children` list. Published child
Labs retain their exact release reference and checksum when composed.

For example, a Colony Counting Comparison Lab can contain two instances of the
same Plate Colony Counter release with aliases `control` and `treatment`. Each
child can contain a model titled YOLOX-Tiny Colony Detector with alias `detector`.
The execution scopes are `control.detector` and `treatment.detector`; `detector`
does not conflict across different children. These scope names describe runtime
identity, not a new wiring syntax: parent wiring uses each child's declared public
ports, such as `control.colony_count`. Do not reach through a child's private
internal graph. Composition changes an instance alias, not the child's title,
package, internal model names, attribution, or immutable source release.

Dates, run IDs, staging/production environment, resource provider, and qualification
state belong in their metadata fields. A dataset year that defines the scientific
domain can still be meaningful in a title. Do not add Best, Validated, Clinical
Grade, Final, or Production Ready to imply evidence the release does not have.
An imported source title containing such a term is retained with attribution and
an explanation of the actual evidence; it is not automatically rewritten.

## Questions that give results context

For new scientific studies, prefer a concise question the planned outputs can
answer. Name the input, comparison or condition when it distinguishes the work:
"How does a stricter structural similarity threshold change the hits?" or
"What changes when P2Rank returns one pocket versus three for 7L13?".
Keep the question stable while runs are pending or failed; completion status
and evidence determine whether an answer is available.

Use the fields the connected tools actually expose:

- Experiment `name`: the central question. Keep `goal` for intended use, what
  a good answer looks like, and limits; it need not repeat the question.
- Arm `label`: a short setup name such as `7L13 top-1`. Keep `rationale` for
  why that setup is worth running or what it controls for.
- Ordinary `run_prepare`: when its live schema supports `group_arm_rationale`,
  record the specific question and reason there, including for a standalone
  run. Within a study, preserve `group_id` and distinguish the setup rather
  than giving every arm an indistinguishable question title.
- Hosted invocation: its preparation schema may have no question/title field.
  Carry the question in the user-facing plan and result explanation. Do not
  put it into scientific `parameters`, alter the release title, or promise
  that it will become the hosted run's heading.
- Lab or model: retain its reusable scientific name. Put the research question
  in supported notes or specification text. A visualization's supported
  `title` or caption can state the question answered by its actual data; keep
  quantity names, labels and units precise.

For example, "How many visible colonies are detected in this plate?" can frame
a detection result, while "What is the CFU/mL?" requires additional measurement
inputs. "What are the molecular descriptors of these compounds?" does not
claim to answer "Which compound is safest?". Preserve uncertainty, caveats and
prohibited uses; a question must not imply a capability or validation the
model lacks.

Respect explicit user titles and imported names. Operational work such as
`Retain source archives, batches 1-12` can remain descriptive. Do not force
every heading into a question or append a question mark to a task name.
Summarize only the intent needed for context; keep private chat text and
sensitive input details out of shared names. Existing titles and historical
records stay as they are unless the user requests an intentional rename.
Choose wording before preparing an approval-bound plan; never substitute a
different question, scope or request into a plan that has already been approved.

## Before preparing a change

1. Look for existing Labs and workspaces; continue the same scientific identity
   when appropriate rather than creating a similarly named duplicate.
2. Select titles, package identities, and aliases separately. Keep dataset,
   architecture, version, evidence, and environment in their actual fields.
3. Check sibling alias uniqueness at every nested Lab boundary. Repeated instances
   of one package are allowed under distinct role aliases.
4. For an intentional alias rename, update wiring, io maps_to values, initial
   input keys, and other alias references in the same prepared change. Review
   dependent Labs and compatibility implications; never rewrite historical Runs.
5. Read preparation blockers and naming findings. Structural alias errors block;
   generic titles, generated aliases, and identity changes request human-readable
   review without silently changing names or claiming scientific qualification.

This policy guides new authoring and intentional renames. It does not retroactively
rename existing Labs, invalidate historical releases, or change execution behavior.
