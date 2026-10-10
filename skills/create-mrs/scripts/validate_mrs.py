#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from spec_utils import (
    Issue,
    MRS_ID_RE,
    document_status,
    duplicate_definition_ids,
    field_value,
    malformed_ids,
    missing_sections,
    render_report,
    unresolved_markers,
)


REQUIRED_SECTIONS = (
    "Document Control",
    "Executive Summary",
    "Biological Objective and Intended Use",
    "Model Definition and Scope",
    "Inputs",
    "Outputs",
    "Data, Assay, and Evidence Specification",
    "Ground Truth or Estimand",
    "Generalization Domain",
    "Performance Requirements",
    "Validation Plan",
    "Acceptance and Traceability",
    "Constraints, Risks, and Governance",
    "Reproducibility, Deliverables, and Handoff",
    "Milestones and Responsibilities",
    "Open Questions and Decisions",
    "References and Glossary",
)

MODULES = {
    "predictive": "Predictive / ML Module",
    "machine learning": "Predictive / ML Module",
    "mechanistic": "Mechanistic Module",
    "generative": "Generative Module",
    "optimization": "Optimization Module",
    "simulation": "Simulation / Digital Twin Module",
    "digital twin": "Simulation / Digital Twin Module",
    "statistical estimation": "Statistical Estimation Module",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate structural invariants of an MRS Markdown file.")
    parser.add_argument("document")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    path = Path(args.document).expanduser().resolve()
    if not path.is_file():
        parser.error(f"document not found: {path}")
    text = path.read_text(encoding="utf-8")
    status = document_status(text)
    approved = status == "approved"
    draft_level = "error" if approved else "warning"
    issues: list[Issue] = []

    if status is None:
        issues.append(Issue("warning", "status", "Status is missing, unresolved, or not one of Draft/In review/Approved/Superseded."))
    for section in missing_sections(text, REQUIRED_SECTIONS):
        issues.append(Issue("error", "section", f"Missing required section: {section}"))
    for marker in unresolved_markers(text):
        issues.append(Issue(draft_level, "unresolved", f"Document contains {marker}."))

    identifiers = set(MRS_ID_RE.findall(text))
    if not identifiers:
        issues.append(Issue(draft_level, "identifiers", "No concrete MRS requirement identifiers were found."))
    for token in malformed_ids(text, MRS_ID_RE, "MRS"):
        issues.append(Issue(draft_level, "identifier-format", f"Malformed or unresolved identifier: {token}"))
    for token in duplicate_definition_ids(text, MRS_ID_RE):
        issues.append(Issue(draft_level, "duplicate-id", f"Identifier appears to be defined more than once outside traceability: {token}"))

    retained = [heading for heading in set(MODULES.values()) if heading.casefold() in text.casefold()]
    if not retained:
        issues.append(Issue(draft_level, "model-module", "No model-specific module is retained."))
    selected = field_value(text, "Selected type or types")
    if selected and "{{" not in selected:
        folded = selected.casefold()
        for keyword, heading in MODULES.items():
            if keyword in folded and heading.casefold() not in text.casefold():
                issues.append(Issue(draft_level, "model-module", f"Declared model type '{keyword}' lacks its model-specific module."))

    if approved and ("Pending" in text or "Rejected" in text):
        issues.append(Issue("error", "approval", "Approved document still contains a Pending or Rejected approval/decision."))
    if approved and field_value(text, "MRS identifier") is None:
        issues.append(Issue("error", "document-control", "Approved document has no MRS identifier."))
    version = field_value(text, "Version")
    if approved and version is None:
        issues.append(Issue("error", "document-control", "Approved document has no version."))
    if approved and field_value(text, "Last revised") is None:
        issues.append(Issue("error", "document-control", "Approved document has no Last revised date."))
    if "Revision History" not in text:
        issues.append(Issue("error", "revision-history", "Revision History is missing."))
    elif approved and version:
        revision_window = text.split("Revision History", 1)[1].split("2. Executive Summary", 1)[0]
        if version not in revision_window:
            issues.append(Issue("error", "revision-history", f"Revision History does not contain the approved document version {version}."))

    issues.append(Issue("info", "semantic-review", "Validator cannot prove scientific sufficiency or that acceptance criteria match the intended biological decision; perform a human/agent semantic review."))
    return render_report(path, issues, as_json=args.as_json)


if __name__ == "__main__":
    raise SystemExit(main())
