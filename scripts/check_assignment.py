#!/usr/bin/env python3
import sys
import re
from pathlib import Path

ASSIGNMENT_FILE = Path("01_hardware_vs_software.md")

# Expected headings as literal text (no regex escapes here)
H1 = "# Part 1 – Hardware vs Software"
H2_SECTIONS = [
    "## Explain Hardware",
    "## Explain Software",
    "## How Do Hardware and Software Interact?",
]

MIN_WORDS = 50

def fail(msg: str) -> None:
    print(f"::error::{msg}")
    print("RESULT: FAIL")
    sys.exit(1)

def info(msg: str) -> None:
    print(msg)

def load_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"File not found: {path}")

def count_words(text: str) -> int:
    # Basic word tokenizer: sequences of letters/digits/apostrophes/hyphens
    tokens = re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)?", text)
    return len(tokens)

def list_detected_h2(md: str) -> list[str]:
    return re.findall(r"(?m)^(## .+?)\s*$", md)

def extract_section_body(md: str, section_heading: str) -> str | None:
    """
    Extracts the text body under a given '##' heading, up to the next '##' or EOF.
    We escape the heading literally to avoid regex surprises.
    """
    heading_pattern = rf"(?m)^{re.escape(section_heading)}\s*\n"
    # Find the start of the section
    m = re.search(heading_pattern, md)
    if not m:
        return None
    start = m.end()

    # Find the next '## ' after start (boundary of this section)
    next_h2 = re.search(r"(?m)^\#\#\s", md[start:])
    end = start + next_h2.start() if next_h2 else len(md)

    body = md[start:end].strip()

    # Remove horizontal rules or markdown separators if any
    body = re.sub(r"(?m)^\s*[-*_]{3,}\s*$", "", body).strip()
    return body

def main() -> None:
    md = load_file(ASSIGNMENT_FILE)

    # 1) Check H1 exists (exact match)
    if not re.search(rf"(?m)^{re.escape(H1)}\s*$", md):
        fail("Missing exact H1 heading: '# Part 1 – Hardware vs Software'")

    # 2) Check each H2 exists and has >= MIN_WORDS body
    for h2 in H2_SECTIONS:
        if not re.search(rf"(?m)^{re.escape(h2)}\s*$", md):
            detected = list_detected_h2(md)
            fail(f"Missing exact section heading: '{h2}'. Detected H2 headings: {detected}")

        body = extract_section_body(md, h2)
        if body is None:
            fail(f"Could not extract content under section: '{h2}'")

        words = count_words(body)
        if words < MIN_WORDS:
            fail(f"Section '{h2}' has {words} words; minimum required is {MIN_WORDS}.")
        else:
            info(f"Section '{h2}' OK: {words} words (≥ {MIN_WORDS}).")

    print("All checks passed.")
    print("RESULT: PASS")

if __name__ == "__main__":
    main()
