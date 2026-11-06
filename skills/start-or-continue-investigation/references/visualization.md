# Visualization delivery

Provide a visualization when the user requests one or it helps explain computed results.
Keep typed outputs as well. File-only and infrastructure tasks need no chart or opt-out
justification. Do not generate decorative charts or invent data to satisfy a count.

Before authoring in Studio Chat or MCP, read `get_biosimulant_authoring_contract` with
`topics: ["visualization"]`. It returns the versioned catalog, payload examples, limits,
asset lifecycle and technical validation rules. Both agent surfaces share this contract.

| Render | Choose it for | Data contract |
| --- | --- | --- |
| `timeseries` | Dynamics and trajectories | `series: [{name, points: [[x, y], ...]}]`; `x_label`, `x_unit`, `y_label`, `y_unit` |
| `bar` | Categories or endpoints | `items: [{label, value, unit?}]` |
| `scatter` | Observed/predicted values, residuals | `points: [{x, y, label?, series?}]`; axis labels and units |
| `heatmap` | Spatial fields, matrices, sweeps | Rectangular `values: [[number, ...], ...]`; `x_labels`, `y_labels`, `unit` |
| `graph` | Networks | `nodes: [{id}]`, `edges: [{source, target}]` referencing those IDs |
| `table` | Exact values and metadata | `columns: [string, ...]`, `rows: [[cell, ...], ...]`, matching widths |
| `image` | Scientific images and annotated overlays | `source: {kind: "artifact", path: "outputs/annotated.png"}` and meaningful `alt`; optional `caption` |
| `structure3d` | Molecular coordinates | `format: "pdb"` or `"mmcif"`, artifact `source` |
| `text` | Interpretation, caveats, abstentions | Nonempty `text` |

Each v1 spec includes `schema_version: "1"`, `render` and a JSON-compatible `data`
mapping. Add `title`, labels, units and `description` to explain the scientific result.
When it clarifies the result, phrase a supported visual title as the question
its computed data answers, such as "How does the population change over time?".
Use captions for setup and limitations; keep axes, series names and units as
precise quantity labels. Pending, failed or unverified work must not be presented
as having answered the question. Avoid private input details in shared titles.
`biosimulant.visualization_catalog()` supplies executable examples for all nine renderers.
The catalog uses the common portable subset across local Labs Serve, Web and Desktop.
Some clients also accept richer legacy payloads; that does not make those payloads portable.
Custom renderer names require actual client registration and are outside the v1 contract.

## Implementation

Choose render types, source outputs, units, typed connections, execution lifecycle,
bounded previews and retained assets to serve the user's requested outputs. Create or
revise MRS/MTS documents only when explicitly requested; they are not prerequisites
for authoring, execution or publication.
A table is useful for exact data but should accompany a plot when a plot makes the result
clearer. Select a meaningful image overlay for image analysis, scatter for prediction
validation, heatmap for spatial/matrix data and 3D for structures.

Existing Labs may declare visualization deliverables at the top level of `lab.yaml`.
Preserve that metadata when editing a Lab, for example:

```yaml
visualization:
  schema_version: "1"
  required:
    - module: summary
      render: timeseries
      min_count: 1
```

Names are actual composed runtime aliases, including child prefixes. Preserve existing
`opt_out_reason` metadata and parent declarations for views produced by a child.
Visualization declarations and opt-out reasons are not required for new authoring,
execution or publication.

Implement `visualize()` on the result component using actual computed state. It returns one
spec or a list. It must not run inference again or advance the science. A finite downstream
analysis module uses `ExecutionPolicy.ONCE_AFTER_RUN` with real typed wiring. Temporal
modules record bounded observations during `execute`; `visualize()` reads them afterward.

## Retained images and coordinates

Emit image/structure files inside the run's output directory and reference them through
`data.source = {"kind": "artifact", "path": "outputs/annotated.png"}`. Also emit the path
through a typed file output when it is a scientific deliverable. Managed execution collects
visual-only assets using the same file types, limits and confinement as other output files,
then replaces paths with durable artifact IDs. Clients resolve IDs through the authorized
run context when the run is reopened. Web previews use temporary browser object URLs,
revoked on teardown; persisted results contain stable IDs rather than those URLs.

Small inline images must use a complete `data:image/png;base64,...` URI. Raw base64 is not
an image source. Avoid temporary paths and expiring remote links as delivered sources.
The v1 contract bounds each spec to 2 MB, each Lab to 64 visuals and chart data to 10,000
points/cells per series/matrix. Web artifact image previews are limited to 10 MB; larger
files remain downloadable. Retention limits still apply to the full artifact.

## Delivery verification

Run the actual composition and inspect results JSON: typed outputs plus grouped `visuals`.
The SDK adds a `visualization` delivery report; invalid v1 payloads and `visualize()` errors
produce bounded diagnostics while scientific outputs remain accessible. Legacy envelopes
remain compatible, with diagnostics where their payload is not portable.

Verify chosen types, nonempty data, units, plotted values against typed outputs, labels,
retained files, reopening and exports. Report invalid or missing requested visuals and
rendering errors as delivery results, preserving accessible typed outputs and files.
Artifact-backed visuals must refer to completed retained artifacts. These technical checks
do not impose a scientific qualification or publication gate.

Studio `create_visualization` creates an ad-hoc chat chart resource. It does not implement
reusable `BioModule.visualize()` behavior; use that method when the requested view must
be part of a reusable Lab.
