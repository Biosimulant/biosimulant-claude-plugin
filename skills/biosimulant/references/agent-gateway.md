# Authenticated Agent Gateway

Use this reference when connecting Biosimulant, selecting MCP versus local CLI, invoking Gateway tools, or interpreting Gateway errors.

## Connect a client

The production Streamable HTTP endpoint is:

```text
https://api.biosimulant.com/mcp
```

Use Claude's existing Biosimulant connector and complete browser sign-in and
consent. The consent screen must be on `studio.biosimulant.com`, and the issuer
must be `https://api.biosimulant.com`. Do not paste tokens, authorization codes,
cookies or signed download links into prompts or files.

All MCP access is authenticated. Public Hub web pages may remain anonymous, but anonymous MCP initialization, tool listing, and tool calls must fail.

## Execution surface

Use the declared authenticated Biosimulant connection for workspaces, validation,
managed compute, saved results and publication. Draft scientific documents and
code in the conversation. This Claude package does not execute local commands,
simulations, document helpers or artifact processing.

## Tools and protected scopes

| Tool | Scope | Effect |
| --- | --- | --- |
| `hub_search`, `hub_inspect` | `hub:read` | Read exact accessible Hub releases; `hub_inspect` also lists the other versions you can see and the Lab ID. |
| `lab_list` | `hub:read` | List Labs you own, released or not, with exact release references. |
| `lab_update`, `lab_visibility_set` | `packages:publish` | Rename or describe an owned Lab, list a public Lab in the Hub, or change who can see it. |
| `workspace_list`, `file_list`, `file_get` | `workspaces:read` | List private workspaces; list and read files you uploaded (bounded, SHA-256 verified). |
| `run_list`, `run_event_list` | `runs:read` | List your runs from MCP, the Developer API and Biosimulant Studio (`kind`: `managed`, `release` or `studio`); read a run's ordered log. Studio runs are read here and cancelled in Studio. |
| `experiment_list` | `runs:read` | List studies with run totals. |
| `experiment_update` | `runs:write` | Rename, re-goal, close or detach runs from a study; deletes nothing. |
| `compute_profile_list` | `runs:read` | List compute sizes and how managed runs choose theirs. |
| `run_grant_list`, `workflow_grant_list` | `runs:read` | List grants this connection created. |
| `account_get` | any | The connected account, its scopes, managed-compute state and fair-use usage. |
| `skill_list`, `skill_get` | any | The currently published Biosimulant skills. |
| `biology_search`, `biology_fetch` | `biology:read` | Search approved adapters and persist exact fetched evidence as opaque resources. |
| `workspace_get` | `workspaces:read` | Read an owned workspace revision. |
| `workspace_create`, `workspace_change_prepare`, `workspace_change_apply` | `workspaces:write` | Create private workspaces and prepare/apply immutable revisions. |
| `run_get`, `run_artifact_get` | `runs:read` | Read owned Gateway runs and artifacts. |
| `run_prepare`, `run_create`, `run_cancel` | `runs:write` | Preflight, start, or cancel free-beta managed compute. |
| `run_grant_prepare`, `run_grant_create`, `run_grant_revoke` | `runs:write` | Prepare, explicitly approve, create, or revoke an exact bounded run grant. |
| `run_grant_get` | `runs:read` | Read grant expiry, state, and remaining uses. |
| `workflow_grant_prepare`, `workflow_grant_create`, `workflow_grant_revoke` | `runs:write` plus `packages:publish` | Prepare, create after one approval, or revoke an exact run/private-publication workflow grant. |
| `workflow_grant_get` | `runs:read` | Read workflow expiry, state, exact actions, and remaining work. |
| `passport_get` | `passports:read` | Read a signed Passport for an owned exact subject. |
| `publish_prepare`, `publish_execute` | `packages:publish` | Prepare or execute an immutable private/public Hub release. |

Every tool acts for the signed-in user only. Lists return only that user's
records, and an ID that belongs to someone else is answered exactly like an ID
that does not exist. Grants are additionally bound to the connection that
created them.

The effective action is the intersection of OAuth scope, user/object authorization, host capability, feature availability, and object state. There is no subscription or credit-balance gate for Agent Gateway beta access.

Compatibility profiles are distributed with the pinned `biosimulant` runtime,
not through Agent Gateway tools. Do not run local compatibility commands from this plugin. Managed runs enforce the same declarations
through their pinned runtime and record the used profile digests in provenance.

Searchable biology source IDs currently exposed by the Gateway schema are `pubmed`, `europe_pmc`, `uniprot`, `ols`, `reactome`, `biomodels`, `physiome`, `chembl`, `pubchem`, `cellosaurus`, and `clinvar`. Select one to three per search. Never supply arbitrary URLs, headers, credentials, or unsupported source parameters.

## Durable operation pattern

1. Read or inspect the exact subject.
2. Draft bounded content locally in the agent context.
3. Call the relevant `*_prepare` tool with an idempotency key.
4. Show the returned base revision, normalized diff/request, validation findings, blockers, expiry, side effects, compute bounds when applicable, and `plan_sha256`.
5. Obtain explicit approval for that exact plan.
6. Call the paired apply/create/execute tool with the unmodified plan ID and digest.
7. Save the durable resource ID and read it back.

Never interpret preparation as execution or approval. When several exact plans
are ready together, show them together and obtain one consolidated user answer.
Re-prepare after a stale base, changed input, changed compute bound, changed
version/visibility, expired plan, or digest mismatch. Replaying an already
executed plan should return the same resource rather than duplicate a revision,
run, charge, grant, or release.

For exact managed runs that should privately publish after successful
verification, prepare each run and private publication, then bundle up to ten
pairs with `workflow_grant_prepare`. After one explicit approval, call
`workflow_grant_create`, execute the listed runs with its ID, and publish each
private release only with the matching completed run ID. The server requires a
durable, checksummed, non-empty results artifact and rejects public releases,
changed scope, expiry, revocation, or reuse. Use a standalone run grant when no
private publication is intended. Never silently downgrade to direct execution
when a requested grant fails.

For an uninterrupted final managed run, prepare the exact run first, then use
`run_grant_prepare` with `max_runs: 1` and a short lifetime. Show and obtain one
explicit approval for that grant plan before `run_grant_create`. The returned
grant authorizes only its exact revision, scientific request, quality profile,
compute bounds, user, and OAuth client. Pass it to `run_create`, or to a later
identical `run_prepare` when the original operation plan expired. A matching
grant makes `requires_confirmation` false; expiry, revocation, exhaustion, or
any scope change fails closed. Use `run_grant_revoke` whenever the remaining
authorization is no longer needed.

## Responses and recovery

Successful tools return a versioned envelope with `request_id`, `data`, `warnings`, `next_actions`, and `links`. Expected failures return a typed code, retryability, field, details, and resolution. Preserve the request ID when reporting a defect.

- Authentication or scope failure: reconnect and consent to the needed scope; do not seek a token elsewhere.
- Stale or expired plan: read the current subject and prepare again.
- Validation or evidence blocker: fix the underlying scientific or technical issue; do not weaken the gate.
- Capacity, timeout, or rate limit: report the typed limit and retry only when the response says it is retryable.
- Host action unavailable: stop at the supported read/preparation boundary and provide the returned Studio link when available.

During the authenticated free beta, Gateway managed runs return `billing_mode: free_beta` and `user_charge: 0`. They require direct exact approval or coverage by a previously approved active exact-scope grant because they consume infrastructure. The service may enforce runtime timeouts, concurrency, rate limits, provider capacity, and emergency compute shutdown.

## The Developer API is the same service

Programs use `https://api.biosimulant.com/v1` with an API key
(`Authorization: Bearer bsk_live_...`). Each MCP tool above, except the grant
tools, has a REST route running the same operation for the key's owner, with the
same scopes and the same response envelope; each `next_actions` entry carries its
REST equivalent under `http`. Plans work the same way: `POST /v1/run-plans` and
`POST /v1/runs` with `plan_id` and `plan_sha256`, `POST /v1/workspaces/{id}/change-plans`
and `POST /v1/workspace-revisions`, `POST /v1/experiment-plans` and
`POST /v1/experiments`, `POST /v1/publication-plans` and `POST /v1/publications`.
Grants are MCP-only because an API key already carries its owner's authority.
Runs, studies, workspaces and files created on either surface appear on both.

