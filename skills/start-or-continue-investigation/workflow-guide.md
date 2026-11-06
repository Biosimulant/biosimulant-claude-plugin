# Biosimulant workflow guide

Labs hold executable scientific work. Biosimulant chat sessions hold durable research questions, requirements, plans and evidence. A session either has no Lab (standalone) or works in one Lab of its own, which never changes; its `lab` summary says which. When users request a model, use the lab workflow. A lab contains executable model components described by `model.yaml`, coordinated by `lab.yaml`.

For session activity and the research notes shared by Labs and sessions, read
[Session research notes and activity](references/session-research.md). Save findings
as notes when requested; note revisions preserve interpretation and sources without
changing execution requirements or approvals.

Before creating or renaming Labs, models, or child Labs, read
[Naming and identity](references/naming.md). Keep scientific titles, stable package
identities, and instance aliases separate; preserve imported names and attribution.


Biosimulant MCP is the product interface: it authenticates, authorizes, stores
immutable work, validates changes, executes approved compute, retrieves
artifacts, records execution facts, and publishes. This skill adds optional scientific
workflow guidance. It never adds permissions or capabilities to MCP.

Inspect the connected server's live tool schemas before acting. Do not infer
that MCP is unavailable because it has no resources/templates or because the
local `biosim` command is absent. If a required tool or scope is genuinely
missing, complete the supported portion and report the exact blocker.

A folder holding `.biosimulant-project.json` is a local copy of a Lab. Before
changing that Lab, check for `lab_copy_status` in the live tool catalog and read
[Working in a local copy of a Lab](references/lab-copies.md). When the tool is
available, call it first. Otherwise report the server limitation and pause
changes to the linked Lab until the person can sync through a compatible client.
Do not bypass the missing tool with workspace writes.

For Hub or Lab discussions, read [Community discussions](references/community-discussions.md).
Read access and registered-agent reply permission are separate.

## User-facing language

Speak to the user in plain English, including progress updates. Lead with what was found, changed, or completed and what it means for their goal. Describe actions such as searching published models or checking a private lab; do not narrate MCP method names such as hub_search or workspace_get. Omit internal IDs, raw JSON, status enums, request IDs, and checksums from ordinary replies unless the user requests technical detail, troubleshooting needs them, or an exact approval requires them. Preserve these values internally for tool calls, provenance, verification, and approval binding. Use readable names and source links where available. Explain material warnings, failed checks, missing evidence, uncertainty, and next steps in everyday language. An empty draft has no computed results. Explain necessary scientific terms, preserve quantities and units, and preserve concrete execution errors and approval requirements.

For example, say “Your private lab was created successfully. It is empty, so no simulation has run yet.” Say “I found three published labs” instead of “hub_search returned three results.” These examples describe outcomes only when the tool results confirm them.

For a new scientific experiment, prefer a concise question as its name so the
results explain what was being asked. Use question-shaped result or chart titles
when they help a reader interpret the output; keep the answer and its limits
alongside them. Respect explicit user names and use descriptive titles for
operational work. Read [Naming and identity](references/naming.md) for the
existing experiment/run fields, scientific scope, and shared-title boundaries.
This guidance does not rename existing work or add fields to MCP tools.

## Start from what the user already has

Before asking for an ID or creating anything, look: `lab_list` for Labs the
user owns and their exact release references, `workspace_list` for private labs
in progress, `run_list` for runs, including those started in Studio (filter by status,
workspace, study or Lab),
`experiment_list` for studies, and `file_list` for data the user uploaded.
`account_get` reports the connected account, its scopes, whether managed
compute is on, and today's fair-use usage. Every list returns only the signed-in
user's own records, newest first, and pages with `limit` and `next_cursor`.
Continue existing work rather than duplicating it: add an arm to an existing
study, change an existing workspace, or re-read an earlier run.

For a request such as "summarize my colony CFU project", first inspect the live
inventory for `project_search` and use a broad project name/topic. It searches
owned Labs (including unpublished/private ones), active private workspaces and
their recent durable runs. Names are topic-word matches, not semantic proof;
show ambiguous candidates and inspect specifications and actual run artifacts
before reporting progress, remaining requirements or scientific results.
Follow `next_cursor` and per-Lab/workspace `run_list` history when results are
bounded. Missing scopes or tools make discovery incomplete, not empty.

If `project_search` is unavailable, use `lab_list` and `workspace_list` with
short keywords, then `run_list` for matching identities. `hub_search` searches
released packages: an empty release search never establishes that a project or
run results do not exist. New servers include `owned_work` with exact workspace
and run references after an empty first Hub search; clients with older tool
inventories can inspect these using `workspace_get` and `run_get`. If neither
route is available, disclose the discovery limitation and refresh the client's
tool inventory. Do not create a duplicate project or replace missing evidence
with recollections from another conversation.

For uploads, public dataset imports, spreadsheet inspection, or missing input
files, read [Files and datasets](references/files-and-datasets.md). Use original
bytes or source URLs and verified retained file references; never retype patient
data. Check the live schemas before assuming these tools are available.

## Current guidance from the server

This skill may be older than the connected server. `skill_list` and `skill_get`
return the currently published skills, checked against their published SHA-256;
read `skill_get` with name `biosimulant` when a tool, field or rule here does not
match the live schema, and prefer the live copy. The same skills are available
as MCP resources (`biosimulant://skills/{name}`) and prompts where the host
shows them.

## Session execution and authenticated approvals

For work in a Biosimulant session, read `session_resume` before proposing changes,
before execution, and after reconnecting. Its `execution_policy` is authoritative:
current revision, `local_only`, `cloud_only` or `agent_decides`, approval mode,
capabilities, and cumulative Compute maximum, spent, held and remaining amounts.
The user changes these in Studio Settings; an agent cannot grant itself a mode,
raise a cap, or reset a task by changing a request key, plan or client.

Local-only means scientific computation is local, while session records, Hub,
evidence and retained files still use online services. Verify a supported local
CLI/runtime and required device before choosing local execution. Studio currently
has no local simulation engine. Cloud-only rejects local execution; local-only
rejects managed cloud compute. When an allowed location is unavailable, state the
blocker and ask the user to change the preference; never fall back silently. In
Agent decides, choose only supported execution paths and record the choice. A
local CLI result is not a managed Run or signed Passport. A requirement for a
managed Passport cannot be claimed satisfied by local output. Biosimulant cannot
sandbox an external agent's shell or unrelated tools; bind session work through
`session_workspace_create` or the tool's supported session_id rather than using
standalone work to evade a session's limits.

Hand off allows ordinary bounded session work. Ask me requires exact action
review. Within plan permits an exact prepared operation ID and SHA-256 only when
listed in `session_plan_prepare` step `actions` and covered by the current active
step of a human-approved plan for this contract, user and OAuth client. An active
prose plan, an automatically approved plan, or supplying a digest is not consent.
Publication, sharing, hosting/lifecycle and standing run/workflow grants always
need separate authenticated human approval, including in Hand off. Mode selection
does not approve financial, account or infrastructure changes.

When preparation returns `requires_confirmation`, show `review_url` or the
`action_approvals` approval_url to the user. They review the immutable request,
revision, inputs, compute bounds and policy and choose Approve or Decline in
Biosimulant. A chat answer or exact digest alone cannot resolve this approval;
MCP OAuth tokens cannot call the first-party human approval API. Refresh after the
decision and apply only the original plan ID and digest. Declined, expired,
revoked, stale-policy or scope-mismatched actions fail closed. Protected standalone
publication/hosting targets can bind an accessible session_id during preparation.
`lab_visibility_set` and `hosting_pause`, `hosting_resume` or `hosting_withdraw` first prepare without changing anything;
repeat with the human-approved plan_id and plan_sha256 to apply the exact action.

Compute limits are cumulative: every Studio continuation shares its original
task, and external work shares its session-lifetime budget across plans and
clients. Include existing spend and reservations before selecting more arms or
retries. Unknown cost is pending, never zero. Explicit zero prohibits billable
compute. Preserve server-owned scope and budget identity in resumptions. These
are Biosimulant charges; an external agent's own provider charges are separate.

## Retained files and hosted Labs

After a run finishes, return `links.open_results` and `links.open_files` when
the server provides them, plus the saved filenames and file-delivery warnings.
If these links are absent, disclose that this server does not provide them;
use available artifact tools and never invent a destination URL. The Files page
offers previews, individual downloads and Download all.
These links require the user's normal Biosimulant access; they are not public
shares. Follow `run_artifact_list` pagination before calling an inventory complete;
if the connected client lacks that tool, disclose the limit and provide the Files
page link when returned by the server rather than claim there are no more files. Files remain in Biosimulant until
downloaded. A preview, base64 content or worker filesystem path does not establish
a local download. If the user asks to save files locally and this host can write
files, use their chosen destination or `outputs/<run-id>/`, keep filenames inside
that directory, and verify saved byte lengths and SHA-256 against artifact
metadata. Never overwrite different existing bytes; report the exact local paths
only after successful downloads. If this host cannot save files, provide the
Files-page link when available and say so. Keep temporary signed byte-download URLs out of final
replies; use the stable Files-page link for the user.

Use `dataset_list` and `dataset_get` to inspect immutable dataset versions.
`dataset_register` records owned retained file identities, source/license,
groups, and splits; registration is not scientific validation. Retain verified
Run artifacts with `file_import_from_run`, preserving their original identity
and Run provenance. Inspect the live schema for bounds and supported ZIP-member
imports rather than embedding large binary files in workspace text.

Use `hosting_get` to inspect an owned hosting state. `hosting_prepare` checks an
exact release before deployment; `hosting_execute` applies only the approved
plan. Each of `hosting_pause`, `hosting_resume` and `hosting_withdraw` prepares a human-reviewed lifecycle proposal and applies only its exact approved plan. Publishing a Hub
release, deploying hosting, and running a hosted invocation are separate actions.

For an accessible hosted release, read `hosted_release_get` for declared inputs
and bounds, then use `hosted_invocation_prepare` and, after approval of its exact
plan, `hosted_invocation_execute`. Follow `hosted_invocation_get` until terminal;
use `hosted_invocation_artifact_get` to retrieve and independently verify output
bytes. Use `hosted_invocation_cancel` when the user requests cancellation. Keep
the release title, package identity, and instance roles consistent with the
naming guide; a hosting state does not establish scientific qualification.

## Durable collaboration across sessions

For work that should resume across external chats or agents, read
[Session collaboration](references/sessions.md). Reuse the existing chat linked
to the workspace (`session_id`); do not invent a new Task entity or assume a
transcript is the authoritative contract. Keep approved requirements separate
from a revisable execution plan. Another client does not inherit execution
grants.

`session_resume`, `session_create`, `session_attach` and `session_list` report
where a session's work lives as `lab.state`: standalone (no Lab), in_lab
(`lab.lab` is the session's own Lab) or pending (an older session whose private
Lab is created on first use). When `lab.forked_from` is set, the session works
in its own private copy: every edit, run and release applies to the copy, never
the original. In a standalone session, opening a workspace, building, running
and releasing return lab_required; only the user can add a Lab, so ask them.
The sessions reference covers forks, unavailable Labs and session-bound tools.
Inspect live schemas: these capabilities may be available in staging before
production. Do not infer availability from this guidance alone.

## Workflow guidance

Honor the current session execution policy, cumulative budget, ownership and exact scoped approvals. Inspect live tool schemas. Resume existing Labs, sessions and runs before creating new ones. Keep immutable revision IDs, checksums, original inputs and attribution. Never invent input data, measured values, files or successful execution. Do not rerun saved work just to inspect it.

Biosimulant has no scientific qualification or acceptance gate. Do not require MRS/MTS, evidence, caveats, independent fixtures, domain profiles or a research-ready target for ordinary analysis, execution or publication. Do not append generic biological-validity disclaimers. Run scientific reviews, reference comparisons or benchmarks only as requested work and return their findings as data. Explicit user conditions and ordinary permissions still apply.

Technical checks remain: readable manifests, safe paths and packaging, entrypoints, dependencies, types, shapes, formats, declared units and checksums. Preserve real solver/parser/subprocess errors and useful partial outputs. File-only tasks need no chart. With runtime 0.0.38+, use `ExecutionOutcome` and `report_execution_outcome` to record an inner command failure; do not mistake a saved error report for a completed analysis.

Use the relevant references for discovery, files, model authoring, composition or publication. Use the Build or adapt a model skill when formal modeling documents are requested.

## Individually exposed lab actions

Use the specific preview/apply pair for the requested edit. These are tools in
the existing Biosimulant connection, not separate plugins. Each preview takes
`workspace_id`, `base_revision_id`, a bounded typed `changes` list, an optional
`rationale`, and an `idempotency_key`. Every entry in `changes` contains only that
action's fields; do not send a `kind` or `action` selector. Each apply takes only
the returned exact `plan_id` and `plan_sha256`.

| Edit | Preview | Apply |
| --- | --- | --- |
| `file_put` | `workspace_file_put_prepare` | `workspace_file_put_apply` |
| `file_delete` | `workspace_file_delete_prepare` | `workspace_file_delete_apply` |
| `manifest_patch` | `workspace_manifest_patch_prepare` | `workspace_manifest_patch_apply` |
| `component_add` | `workspace_component_add_prepare` | `workspace_component_add_apply` |
| `component_remove` | `workspace_component_remove_prepare` | `workspace_component_remove_apply` |
| `connection_put` | `workspace_connection_put_prepare` | `workspace_connection_put_apply` |
| `connection_delete` | `workspace_connection_delete_prepare` | `workspace_connection_delete_apply` |
| `input_bind` | `workspace_input_bind_prepare` | `workspace_input_bind_apply` |
| `evidence_pin` | `workspace_evidence_pin_prepare` | `workspace_evidence_pin_apply` |
| `requirements_set` | `workspace_requirements_set_prepare` | `workspace_requirements_set_apply` |
| `technical_spec_set` | `workspace_technical_spec_set_prepare` | `workspace_technical_spec_set_apply` |
| `caveats_set` | `workspace_caveats_set_prepare` | `workspace_caveats_set_apply` |

Read the preview's diff, blockers, expiry and `requires_confirmation`. Follow
its approval decision; knowing the digest is not human approval. Apply only with
the matching action tool. It rejects another action's plan and old batch plans.
Related files may be saved together in one `workspace_file_put_prepare` batch,
so their combined content is validated before any is applied. Do not mix action
types within a batch. After applying, use the new immutable revision as the base
of the next preview.
Save code and data through the file action, and edit the Lab's `lab.yaml` through
the manifest action rather than writing its reserved path. A preview with
blockers must not be applied; do not claim an incomplete edit is executable.

For hosting, use `hosting_pause`, `hosting_resume`, or `hosting_withdraw`.
Without plan details these only prepare the named action. A person must approve
it in Studio before the same tool receives its exact plan ID and digest.
Hosting may interrupt access or remove compute. Verify actual state with
`hosting_get`; requesting a change does not establish readiness or cleanup.
