#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from spec_utils import (
    Issue,
    MRS_ID_RE,
    MTS_ID_RE,
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
    "Technical Decision Summary",
    "Scope, Boundaries, and Assumptions",
    "MRS Traceability",
    "Architecture and Data Flow",
    "Data Implementation",
    "Input, Output, and Error Contracts",
    "Model Method and Uncertainty",
    "Biosimulant Fit Assessment",
    "Verification and Test Design",
    "Reproducibility, Security, Performance, and Cost",
    "Model Lock, Release, and Operations",
    "Risks, Decisions, and Open Questions",
    "References and Glossary",
)

MODEL_MODULES = (
    "Predictive / ML Technical Module",
    "Mechanistic Technical Module",
    "Generative Technical Module",
    "Optimization Technical Module",
    "Simulation / Digital Twin Technical Module",
    "Statistical Estimation Technical Module",
)

FIT_OUTCOMES = {
    "native fit": "native",
    "adapter fit": "adapter",
    "external boundary": "external",
    "not suitable": "not-suitable",
}


def fit_outcome(text: str) -> str | None:
    for label in ("Biosimulant fit", "Outcome"):
        value = field_value(text, label)
        if value is None:
            continue
        normalized = value.casefold().strip()
        if normalized in FIT_OUTCOMES:
            return FIT_OUTCOMES[normalized]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate structural and MRS-traceability invariants of an MTS Markdown file.")
    parser.add_argument("document")
    parser.add_argument("--mrs", help="Approved MRS implemented by this MTS")
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

    if not set(MTS_ID_RE.findall(text)):
        issues.append(Issue(draft_level, "identifiers", "No concrete derived MTS identifiers were found."))
    for token in malformed_ids(text, MTS_ID_RE, "MTS"):
        issues.append(Issue(draft_level, "identifier-format", f"Malformed or unresolved identifier: {token}"))
    for token in duplicate_definition_ids(text, MTS_ID_RE):
        issues.append(Issue(draft_level, "duplicate-id", f"Identifier appears to be defined more than once outside traceability: {token}"))

    if not any(heading.casefold() in text.casefold() for heading in MODEL_MODULES):
        issues.append(Issue(draft_level, "model-module", "No model-specific technical module is retained."))

    outcome = fit_outcome(text)
    if outcome is None:
        issues.append(Issue(draft_level, "biosimulant-fit", "Exactly one concrete Biosimulant fit outcome is required."))
    else:
        has_realization = "Biosimulant Realization".casefold() in text.casefold()
        has_external = "External or Not-Suitable Delivery".casefold() in text.casefold()
        if outcome in {"native", "adapter"} and not has_realization:
            issues.append(Issue(draft_level, "biosimulant-fit", "Native/adapter fit requires the Biosimulant Realization section."))
        if outcome in {"external", "not-suitable"} and not has_external:
            issues.append(Issue(draft_level, "biosimulant-fit", "External/not-suitable fit requires the External or Not-Suitable Delivery section."))
        if approved and outcome in {"native", "adapter"} and has_external:
            issues.append(Issue("error", "conditional-section", "Approved native/adapter MTS still retains the external/not-suitable conditional section."))
        if approved and outcome in {"external", "not-suitable"} and has_realization:
            issues.append(Issue("error", "conditional-section", "Approved external/not-suitable MTS still retains the Biosimulant realization conditional section."))

    if args.mrs:
        mrs_path = Path(args.mrs).expanduser().resolve()
        if not mrs_path.is_file():
            parser.error(f"MRS not found: {mrs_path}")
        mrs_text = mrs_path.read_text(encoding="utf-8")
        if document_status(mrs_text) != "approved":
            issues.append(Issue("error", "mrs-gate", "A full MTS requires an MRS whose document Status is Approved."))
        mrs_identifier = field_value(mrs_text, "MRS identifier")
        mrs_version = field_value(mrs_text, "Version")
        if not mrs_identifier or "{{" in mrs_identifier:
            issues.append(Issue("error", "mrs-gate", "The source MRS has no concrete identifier."))
        elif mrs_identifier not in text:
            issues.append(Issue("error", "mrs-link", f"MTS does not reference source MRS identifier {mrs_identifier}."))
        if not mrs_version or "{{" in mrs_version:
            issues.append(Issue("error", "mrs-gate", "The source MRS has no concrete version."))
        elif mrs_version not in text:
            issues.append(Issue("error", "mrs-link", f"MTS does not reference source MRS version {mrs_version}."))
        source_ids = set(MRS_ID_RE.findall(mrs_text))
        mapped_ids = set(MRS_ID_RE.findall(text))
        for requirement_id in sorted(source_ids - mapped_ids):
            issues.append(Issue("error", "traceability", f"MRS requirement is missing from MTS traceability: {requirement_id}"))
    else:
        issues.append(Issue("error" if approved else "warning", "mrs-gate", "Pass --mrs with the approved source MRS to validate linkage and requirement coverage."))

    if approved and ("Pending" in text or "Rejected" in text):
        issues.append(Issue("error", "approval", "Approved document still contains a Pending or Rejected approval/decision."))
    if approved and field_value(text, "MTS identifier") is None:
        issues.append(Issue("error", "document-control", "Approved document has no MTS identifier."))
    version = field_value(text, "Version")
    if approved and version is None:
        issues.append(Issue("error", "document-control", "Approved document has no version."))
    if approved and field_value(text, "Last revised") is None:
        issues.append(Issue("error", "document-control", "Approved document has no Last revised date."))
    if "Revision History" not in text:
        issues.append(Issue("error", "revision-history", "Revision History is missing."))
    elif approved and version:
        revision_window = text.split("Revision History", 1)[1].split("2. Technical Decision Summary", 1)[0]
        if version not in revision_window:
            issues.append(Issue("error", "revision-history", f"Revision History does not contain the approved document version {version}."))

    issues.append(Issue("info", "semantic-review", "Validator checks identifier coverage, not semantic fidelity. Compare every acceptance criterion and grouped mapping with the approved MRS before approval."))
    return render_report(path, issues, as_json=args.as_json)


if __name__ == "__main__":
    raise SystemExit(main())
