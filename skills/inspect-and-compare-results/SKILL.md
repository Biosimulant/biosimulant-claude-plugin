---
name: inspect-and-compare-results
description: Read and compare saved Biosimulant results, including values, plots, and files. Use when the user asks what a completed experiment produced or how two runs differ.
---

# Inspect and compare results

Check the connected server's available read tools and schemas. Lead with what the saved results show in plain English, then give the relevant quantities, units, and limits.

1. Find the exact completed run or runs and retrieve their settings and outcomes. Read saved artifacts, not just filenames or job status. Use verified full content or a server-verified bounded preview when supported. Preserve units and labels, and say when a preview is sampled or a requested value is unavailable.
2. Compare inputs, revisions, settings, and output values side by side. Compare like quantities only. For Boltz-2, distinguish the predicted structure, model confidence, and affinity or binding scores, using the names and units in the saved files. Treat scores as predictions and state any limitation that affects the question.
3. Link to the saved results and files in Studio when the server provides those links. Use the available execution record when relevant. Report missing or failed outputs directly and never invent values, fabricate links, or rerun to fill a gap without being asked.

Example: “Compare my two completed Boltz-2 runs. What changed in the inputs, what do the saved scores show, and where can I open the structures?”
