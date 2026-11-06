# Working in a local copy of a Lab

A folder with `.biosimulant-project.json` is a local copy of a Lab (`hub_id`,
`environment`, `base_version`, a sha256 per file). `.biosimulant/status.json`,
when present, is VS Code's current view of the copy. Never edit either file.

## Before and after your work

Check the live tool catalog first. If `lab_copy_status` is unavailable, report
that this server cannot inspect the linked copy and pause changes to the Lab.
Ask the person to sync through a compatible client; never guess copy state or
substitute workspace writes. If only `lab_copy_propose` is missing, keep the
local edits and ask the person to Sync in VS Code rather than publish them by
another route.

Call `lab_copy_status` with the Lab id (`hub_id`), the base version, the link
file's `files` as `base_files`, and the current sha256 of each file as `files`
(skip `.git`, `.biosimulant/`, `node_modules`, virtualenvs, caches and secrets).
Do it before you start and before you finish. Its `next` says what to do.

## What you may do

- Edit the Lab's files in the folder: yes.
- Lab ahead and nothing changed here: tell the person; get the latest only with
  their OK, or ask them to press Get latest / Sync in VS Code.
- Lab ahead and different files changed on each side: tell the person which
  files came in; they Sync in VS Code.
- The same file changed on both sides (`conflicts`): reconcile with the person
  (below). Never pick a side yourself.
- Propose a new version only after the person agrees, with `lab_copy_propose`
  (`base_version` from the link file) or by asking them to Sync in VS Code. A
  person approves every proposal; keep the returned id for `lab_copy_status`.
- Never publish or write this Lab's files through the workspace tools while a
  copy exists, never edit the link file, never unlink or relink.
- `github_source` set: the way back is git (commit, push, pull request), not a
  proposal.
- `draft_ahead`: someone has unpublished edits in Studio; say so and ask the
  person how to proceed.
- A pending proposal: don't propose again; wait for its decision. Declined: read
  the feedback, revise here, ask before proposing again.

## Runs use the Lab, not the folder

A cloud run executes the Lab's version or a session workspace, not local files.
To run local edits, put them in the session's workspace first and say that the
run uses your local edits as a draft; report which revision ran.

## Reconciling a conflict with the person

1. Get the base (the Lab file at `base_version`), the Lab's latest, and the local file.
2. Explain the difference in plain words.
3. Offer a merged version with a diff, beside "keep mine" and "use the Lab's".
4. Apply the person's choice only after backing up the local file to
   `.biosimulant/backups/<time>/`.
5. Record what came in and what the person chose with `session_progress_update`.
