#!/usr/bin/env python3
"""PreToolUse hook: block hardcoded secrets in Write/Edit before they hit disk.

Reads the tool-call JSON on stdin. If the content being written contains a
high-confidence secret, exits with code 2 (blocks the tool) and explains why on
stderr. High precision by design: env references and placeholders are allowed.
"""
import json
import os
import re
import sys

# (label, compiled regex) — high-confidence secret signatures.
SIGNATURES = [
    ("Private key block", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained PAT", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("AWS access key id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b")),
    ("Stripe live secret key", re.compile(r"\b[sr]k_live_[0-9A-Za-z]{16,}\b")),
    ("Google service account JSON", re.compile(r'"type"\s*:\s*"service_account"')),
    ("Slack webhook URL", re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9/]+")),
]

# Assignments to secret-named variables with a real literal value.
ASSIGN = re.compile(
    r"""(?ix)
    \b(?:api[_-]?key|apikey|secret|secret[_-]?key|access[_-]?key|
       auth[_-]?token|client[_-]?secret|private[_-]?key|password|passwd|
       db[_-]?password|encryption[_-]?key)\b
    [ \t]*[:=][ \t]*
    (['"]?)(?P<val>[^\s'"]{8,})\1
    """
)

# Values that are obviously NOT real secrets (env refs / placeholders).
PLACEHOLDER = re.compile(
    r"""(?ix)
    ^(?:
        \$\{? | process\.env | os\.environ | import\.meta\.env | secrets\. |
        x{3,} | \.{3,} | < | your[_-] | my[_-] | example | changeme | change-me |
        placeholder | dummy | test | sample | fake | redacted | null | none |
        true | false | \d+ | [a-z]+\.[a-z]+ | enabled | disabled
    )
    """
)


def env_filename(path: str) -> bool:
    base = os.path.basename(path or "")
    if base == ".env":
        return True
    if base.startswith(".env."):
        suffix = base[len(".env."):]
        return suffix not in {"example", "sample", "template", "dist", "defaults"}
    return False


def scan(text: str, path: str):
    findings = []
    for label, rx in SIGNATURES:
        if rx.search(text):
            findings.append(label)
    for m in ASSIGN.finditer(text):
        val = m.group("val")
        if not PLACEHOLDER.match(val):
            findings.append(f"hardcoded secret assignment ({m.group(0).split('=')[0].split(':')[0].strip()})")
            break
    if env_filename(path):
        # A real .env with any KEY=value assignment should never be written/committed.
        if re.search(r"(?m)^\s*[A-Za-z_][A-Za-z0-9_]*\s*=\s*\S", text):
            findings.append(f"real .env file with values ({os.path.basename(path)}) — use .env.example instead")
    return findings


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # can't parse → don't block

    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input", {}) or {}
    path = ti.get("file_path", "") or ""

    chunks = []
    if "content" in ti:
        chunks.append(ti["content"])
    if "new_string" in ti:
        chunks.append(ti["new_string"])
    for edit in ti.get("edits", []) or []:
        if isinstance(edit, dict) and "new_string" in edit:
            chunks.append(edit["new_string"])
    text = "\n".join(c for c in chunks if isinstance(c, str))
    if not text and not env_filename(path):
        sys.exit(0)

    findings = scan(text, path)
    if findings:
        msg = (
            "BLOCKED by secret-scan hook (MANUAL.md §5).\n"
            f"  tool: {tool}  file: {path or '(unknown)'}\n"
            "  detected: " + "; ".join(sorted(set(findings))) + "\n"
            "  Fix: move the value to an env var / secret manager and reference it; "
            "commit only .env.example (key names, no values).\n"
            "  If client/web hardcoding is truly unavoidable, STOP and report to the "
            "operator for explicit approval with a mitigation plan."
        )
        print(msg, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
