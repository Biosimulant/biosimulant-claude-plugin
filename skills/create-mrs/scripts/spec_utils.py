from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


MRS_ID_RE = re.compile(r"\bMRS-(?:[A-Z]+-)?\d{3}\b")
MTS_ID_RE = re.compile(r"\bMTS-(?:[A-Z]+-)?\d{3}\b")


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"level": self.level, "code": self.code, "message": self.message}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_line(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^#{1,6}\s+", "", value)
    value = re.sub(r"^[-*+]\s+", "", value)
    return value.strip().strip("|").strip()


def field_value(text: str, label: str) -> str | None:
    escaped = re.escape(label)
    table = re.search(
        rf"(?im)^\s*\|\s*{escaped}\s*\|\s*([^|\n]+)", text
    )
    if table:
        return clean_line(table.group(1))
    colon = re.search(
        rf"(?im)^\s*(?:[-*]\s+)?{escaped}\s*:\s*(.+?)\s*$", text
    )
    if colon:
        return clean_line(colon.group(1))

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if clean_line(line).casefold() != label.casefold():
            continue
        for candidate in lines[index + 1 :]:
            value = clean_line(candidate)
            if not value or re.fullmatch(r":?-{3,}:?", value):
                continue
            return value
    return None


def document_status(text: str) -> str | None:
    value = field_value(text, "Status")
    if value is None:
        return None
    normalized = value.casefold().strip()
    if normalized == "approved":
        return "approved"
    if normalized in {"draft", "in review", "superseded"}:
        return normalized
    return None


def unresolved_markers(text: str) -> list[str]:
    checks = {
        "template placeholders": r"\{\{[^{}]+\}\}",
        "template instructions": r"TEMPLATE INSTRUCTION|KEEP THIS MODULE IF|DO NOT MODIFY",
        "unresolved choices": r"Draft\s*/\s*In review\s*/\s*Approved|Pending\s*/\s*Approved\s*/\s*Rejected|Native fit\s*/\s*Adapter fit\s*/\s*External boundary\s*/\s*Not suitable",
        "open drafting markers": r"(?im)(?:\bTODO\b|\bTBD\b|\[OPEN(?::|\]))",
    }
    return [label for label, pattern in checks.items() if re.search(pattern, text)]


def missing_sections(text: str, sections: Iterable[str]) -> list[str]:
    folded = text.casefold()
    return [section for section in sections if section.casefold() not in folded]


def malformed_ids(text: str, valid_pattern: re.Pattern[str], prefix: str) -> list[str]:
    candidates = set(re.findall(rf"\b{re.escape(prefix)}-[A-Z0-9-]+\b", text))
    return sorted(token for token in candidates if valid_pattern.fullmatch(token) is None)


def duplicate_definition_ids(text: str, valid_pattern: re.Pattern[str]) -> list[str]:
    lines = text.splitlines()
    definitions: dict[str, int] = {}
    reference_words = (
        "traceability",
        "deliverable",
        "references",
        "mrs mapping",
        "source mrs id",
        "verification and test",
    )
    for index, line in enumerate(lines):
        token = clean_line(line)
        if valid_pattern.fullmatch(token) is None:
            continue
        context = " ".join(clean_line(item).casefold() for item in lines[max(0, index - 12) : index])
        if any(word in context for word in reference_words):
            continue
        definitions[token] = definitions.get(token, 0) + 1
    return sorted(token for token, count in definitions.items() if count > 1)


def render_report(path: Path, issues: list[Issue], *, as_json: bool) -> int:
    errors = sum(issue.level == "error" for issue in issues)
    warnings = sum(issue.level == "warning" for issue in issues)
    if as_json:
        print(
            json.dumps(
                {
                    "path": str(path),
                    "valid": errors == 0,
                    "errors": errors,
                    "warnings": warnings,
                    "issues": [issue.to_dict() for issue in issues],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        for issue in issues:
            print(f"{issue.level.upper()} [{issue.code}] {issue.message}")
        print(f"{path}: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0
