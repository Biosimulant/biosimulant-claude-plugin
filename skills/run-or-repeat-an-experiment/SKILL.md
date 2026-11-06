---
name: run-or-repeat-an-experiment
description: Prepare or repeat a Biosimulant computational experiment using a known lab, inputs, and settings. Use for new runs, reruns, or comparisons that require fresh compute and explicit approval.
---

# Run or repeat an experiment

Check the connected server's tool schemas and current session policy. Explain the setup and approval in plain English, using exact quantities and units.

1. Resolve the exact lab and revision. For a repeat, retrieve the original run and use its saved inputs, parameters, and bounds. Show any requested changes or missing files. If the same setup cannot be recreated, explain the difference before preparing a substitute.
2. Prepare the plan through the connected service. Show the inputs, settings, compute limits, cost or pending estimate, expiry, and blockers. Follow the server's current approval rules and show its Studio review link when provided. If asked to prepare or wait for approval, stop at the plan. A chat response, plan ID, or hash by itself does not resolve a required Studio approval. A changed or expired plan needs a fresh review.
3. When authorized to execute, use the exact approved plan and check the resulting run through its terminal outcome. Report the actual completion or failure and link to saved results and files when the server provides them. An inspection request never needs a fresh run.

Example: “Prepare a rerun of my saved Boltz-2 experiment. Show me the inputs, settings, and estimated cost before I approve it.”
