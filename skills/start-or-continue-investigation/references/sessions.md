# Durable session collaboration

Use the connected server's live schema. The existing Biosimulant chat is the durable container; the external agent keeps reasoning and orchestration. These tools start no internal reasoning agent.

1. Find the relevant chat with `session_list` or the workspace's `session_id`. Use `session_create` only for new work: omit `lab_id` to create a private Lab, pass `standalone: true` to start with no Lab, or pass `lab_id` to work in an editable Lab. Add `fork: true` to work in a private copy of `lab_id`; Hub and view-only Labs must be forked. `session_attach` maps this client's opaque conversation ID to the chat without granting permissions.
2. Call `session_resume` before writes and after reconnecting. Its approved contract, current plan, pinned advisory guidance, exact revisions, resources, approvals, blockers and execution_policy (revision, location, capabilities, approval mode and cumulative currency budget) are the authoritative context. Preserve the returned sequence cursor. Its `lab` summary says where the session's work lives (see below).
3. Use `session_contract_prepare` to propose goal, intended use, scope and optional run-count cap. Sessions carry no acceptance criteria. Guidance snapshots are advisory and checksum-pinned. The human reviews the exact proposal in Biosimulant before `session_change_apply`.
4. `session_plan_prepare` proposes ordered steps with earlier-step dependencies. Apply only its own exact approval. For Within plan, include each ordinary future action as a prepared plan_id and plan_sha256 in the step actions list. Only authenticated human approval covers these exact bindings; protected actions remain separately reviewed. A plan revision cannot change requirements. Contract revisions invalidate old plans.
5. Start a step with `session_progress_update`. Governed Gateway workspace edits and managed runs require this client/user's approved current plan and active step. Keep using normal workspace prepare/apply, run approvals and execution grants. An active prose plan grants no compute or release authority; exact action coverage never bypasses wallet, cumulative task limits or protected approvals.
6. Research-only chats need no workspace. Use `session_workspace_create` only when files or a Lab are needed; it reuses the same chat and the session's own Lab, and allocates no compute. In a standalone session it returns lab_required.
7. `session_completion_check` completes the session when every step of the plan for the current contract is done, and otherwise lists what remains. Skips and failures do not complete it. It does not certify scientific validity, and publication does not depend on it; publication still requires its normal approval.

## Where a session's work lives

`session_resume`, `session_create`, `session_attach` and `session_list` report `lab.state`:

- standalone: no Lab. The session can answer, research and plan. `session_workspace_create`, building, running and releasing return lab_required. Only the user can add a Lab, with Add to a Lab in Biosimulant; ask them, and never say work was saved to a Lab.
- in_lab: `lab.lab` is the session's own Lab. Every edit, run and release goes there.
- pending: an older session whose private Lab is created on first use. Do not describe it as an existing Lab before then.

When `lab.forked_from` is set, the session works in its own private copy of that Lab. Every edit, run and release applies to the copy, never to the original. Run the copy's workspace revision, never the original's published version.

If the session's Lab is deleted or no longer editable (`lab.lab.available` is false), Lab work returns session_lab_unavailable. The session never moves to another Lab; suggest a new session.

With `session_id`, `lab_visibility_set` and `hosting_prepare` act only on the session's own Lab and otherwise return lab_not_session_lab. Call them without `session_id` to act on another Lab you own.

`workspace_create` with `source_ref` always forks into a new private Lab. Workspace summaries include `lab_id` and `forked_from_lab_id`, `lab_list` items include `lifecycle` and `forked_from_lab_id`, and `publish_prepare` shows `target_lab_id`, the Lab a release goes into.

Use stable idempotency keys and returned digests. If state is stale, refresh and prepare again rather than overriding the conflict. A shared chat allows authorized clients to read and propose their own plan, not to inherit another client's grant. Multiple clients share the server-enforced lifetime workspace run cap; failed and deleted runs consume slots. This cap is not a currency-spend authorization and does not cover unrelated release runs or hosting.

Archive preserves scientific records and stops external writes until unarchived. Soft deletion retains records while making the chat inaccessible. General methodological guidance is advisory; approved session requirements and server permissions govern service operations. Biosimulant cannot control unrelated tools or the external host's chat.

Execution preferences and approval modes are configured by the user in Studio. Follow
the parent skill's Session execution and authenticated approvals section. Every
continuation retains the original Studio task Compute identity; external work uses
the session-lifetime budget across clients and plan revisions. Preparation returns
human review URLs when needed. A chat answer, digest, plan revision or connection
restart cannot reset the budget or replace a first-party human approval.
