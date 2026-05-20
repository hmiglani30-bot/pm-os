#!/usr/bin/env python3
"""
PM-OS Artifact Validator
========================
Checks structural rules across all pipeline artifacts.
Run from the pipeline working directory (e.g., eval-runs/ai-adoption-control-plane/).

Usage:
    python validate_artifact.py <artifact-path>          # Validate one artifact
    python validate_artifact.py --all                     # Validate all artifacts in cwd
    python validate_artifact.py --pipeline <pipeline-dir> # Validate full pipeline run

Checks:
    - Frontmatter presence and required fields
    - Word count within target range
    - Required sections present
    - FAQ count (exactly 25 for PRDs)
    - Citation/source count
    - Prototype file size
    - Artifact cross-references (lineage)
"""

import sys
import os
import re
import json
import glob
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationResult:
    artifact: str
    checks_passed: int = 0
    checks_failed: int = 0
    checks_total: int = 0
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def passed(self):
        return self.checks_failed == 0

    def add_pass(self, check_name: str):
        self.checks_passed += 1
        self.checks_total += 1

    def add_fail(self, check_name: str, detail: str):
        self.checks_failed += 1
        self.checks_total += 1
        self.errors.append(f"FAIL: {check_name} — {detail}")

    def add_warning(self, check_name: str, detail: str):
        self.warnings.append(f"WARN: {check_name} — {detail}")

    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [f"\n{'='*60}", f"  {self.artifact}: {status} ({self.checks_passed}/{self.checks_total} checks)"]
        for e in self.errors:
            lines.append(f"    {e}")
        for w in self.warnings:
            lines.append(f"    {w}")
        lines.append(f"{'='*60}")
        return "\n".join(lines)


def extract_frontmatter(content: str) -> Optional[dict]:
    """Extract YAML-like frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            fm[key.strip()] = val.strip()
    return fm


def count_words(content: str) -> int:
    """Count words in content, excluding frontmatter and code blocks."""
    # Remove frontmatter
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove markdown tables' pipes
    content = re.sub(r'\|', ' ', content)
    return len(content.split())


def find_sections(content: str) -> list:
    """Find all markdown headers (## and ###)."""
    return re.findall(r'^#{1,4}\s+(.+)$', content, re.MULTILINE)


def count_faqs(content: str) -> int:
    """Count FAQ entries (lines starting with **Q or bold question pattern)."""
    return len(re.findall(r'^\*\*Q\d+:', content, re.MULTILINE))


def count_citations(content: str) -> int:
    """Count citation references ([N], Source:, etc.)."""
    bracket_refs = len(re.findall(r'\[\d+\]', content))
    source_lines = len(re.findall(r'^## Sources', content, re.MULTILINE))
    numbered_sources = len(re.findall(r'^\d+\.\s+\*\*', content, re.MULTILINE))
    return bracket_refs + numbered_sources


# ─── Artifact-specific validators ────────────────────────────────

def validate_research(path: str, content: str) -> ValidationResult:
    r = ValidationResult(artifact=os.path.basename(path))
    fm = extract_frontmatter(content)

    # Frontmatter
    if fm:
        r.add_pass("frontmatter_exists")
        for field_name in ["artifact", "version", "topic"]:
            if field_name in fm:
                r.add_pass(f"frontmatter_{field_name}")
            else:
                r.add_fail(f"frontmatter_{field_name}", f"Missing '{field_name}' in frontmatter")
    else:
        r.add_fail("frontmatter_exists", "No frontmatter block found")

    # Word count (target: 6,000-10,000)
    wc = count_words(content)
    if 6000 <= wc <= 10000:
        r.add_pass(f"word_count ({wc})")
    elif wc < 6000:
        r.add_fail("word_count", f"{wc} words — below 6,000 minimum")
    else:
        r.add_warning("word_count", f"{wc} words — above 10,000 target")

    # Required sections
    sections = find_sections(content)
    sections_lower = [s.lower() for s in sections]
    required = ["competitor", "quantitative", "opportunity", "interaction pattern"]
    for req in required:
        if any(req in s for s in sections_lower):
            r.add_pass(f"section_{req}")
        else:
            r.add_fail(f"section_{req}", f"Missing section containing '{req}'")

    # Citations
    cite_count = count_citations(content)
    if cite_count >= 10:
        r.add_pass(f"citations ({cite_count})")
    else:
        r.add_fail("citations", f"Only {cite_count} citations — minimum 10")

    return r


def validate_prd(path: str, content: str) -> ValidationResult:
    r = ValidationResult(artifact=os.path.basename(path))
    fm = extract_frontmatter(content)

    # Frontmatter
    if fm:
        r.add_pass("frontmatter_exists")
        for field_name in ["artifact", "version", "topic"]:
            if field_name in fm:
                r.add_pass(f"frontmatter_{field_name}")
            else:
                r.add_fail(f"frontmatter_{field_name}", f"Missing '{field_name}' in frontmatter")
    else:
        r.add_fail("frontmatter_exists", "No frontmatter block found")

    # Word count (target: 5,500-8,000)
    wc = count_words(content)
    if 5500 <= wc <= 8000:
        r.add_pass(f"word_count ({wc})")
    elif wc < 5500:
        r.add_fail("word_count", f"{wc} words — below 5,500 minimum")
    else:
        r.add_warning("word_count", f"{wc} words — above 8,000 target")

    # Required sections
    sections = find_sections(content)
    sections_lower = [s.lower() for s in sections]
    required_keywords = ["decision", "persona", "jobs to be done", "problem depth",
                         "solution", "success metric", "faq", "dependencies", "risk"]
    for req in required_keywords:
        if any(req in s for s in sections_lower):
            r.add_pass(f"section_{req}")
        else:
            r.add_fail(f"section_{req}", f"Missing section containing '{req}'")

    # FAQ count (exactly 25)
    faq_count = count_faqs(content)
    if faq_count == 25:
        r.add_pass(f"faq_count ({faq_count})")
    elif faq_count == 0:
        # Try alternate FAQ format
        alt_count = len(re.findall(r'^\*\*Q:', content, re.MULTILINE))
        alt_count += len(re.findall(r'^###.*\?', content, re.MULTILINE))
        if alt_count >= 20:
            r.add_warning("faq_count", f"Found {alt_count} FAQ-like entries (alternate format)")
        else:
            r.add_fail("faq_count", f"Found {faq_count} FAQs — expected exactly 25")
    else:
        r.add_fail("faq_count", f"Found {faq_count} FAQs — expected exactly 25")

    # Solution Lineage table
    if "solution lineage" in content.lower() or "from opportunity" in content.lower():
        r.add_pass("solution_lineage_table")
    else:
        r.add_fail("solution_lineage_table", "Missing Solution Lineage table")

    # Dual-scope boundary
    if "eng v1" in content.lower() and "proto v1" in content.lower():
        r.add_pass("dual_scope_boundary")
    elif "v1" in content.lower() and "v2" in content.lower():
        r.add_warning("dual_scope_boundary", "Has v1/v2 scope but missing Eng v1 / Proto v1 distinction")
    else:
        r.add_fail("dual_scope_boundary", "Missing dual-scope boundary table")

    # Citations
    cite_count = count_citations(content)
    if cite_count >= 5:
        r.add_pass(f"citations ({cite_count})")
    else:
        r.add_fail("citations", f"Only {cite_count} citations — minimum 5")

    return r


def validate_gandalf(path: str, content: str) -> ValidationResult:
    r = ValidationResult(artifact=os.path.basename(path))
    fm = extract_frontmatter(content)

    if fm:
        r.add_pass("frontmatter_exists")
    else:
        r.add_fail("frontmatter_exists", "No frontmatter block found")

    # Check for score table
    if re.search(r'rubric.*\d', content, re.IGNORECASE) or re.search(r'\|\s*\d+\s*\|.*\|\s*[0-5]\s*\|', content):
        r.add_pass("score_table")
    else:
        r.add_fail("score_table", "Missing rubric score table")

    # Check question count (should have 12 questions evaluated)
    question_refs = len(re.findall(r'Q\d{1,2}[:\s]|#\s*\d{1,2}[\.\s]', content))
    if question_refs >= 10:
        r.add_pass(f"question_coverage ({question_refs} refs)")
    else:
        r.add_fail("question_coverage", f"Only {question_refs} question references — expected 12")

    # Check for verdict
    if re.search(r'verdict|pass|fail|moved forward', content, re.IGNORECASE):
        r.add_pass("verdict_present")
    else:
        r.add_fail("verdict_present", "Missing verdict section")

    return r


def validate_design_spec(path: str, content: str) -> ValidationResult:
    r = ValidationResult(artifact=os.path.basename(path))
    fm = extract_frontmatter(content)

    if fm:
        r.add_pass("frontmatter_exists")
    else:
        r.add_fail("frontmatter_exists", "No frontmatter block found")

    # Word count (target: 4,000-8,000)
    wc = count_words(content)
    if 4000 <= wc <= 8000:
        r.add_pass(f"word_count ({wc})")
    elif wc < 4000:
        r.add_fail("word_count", f"{wc} words — below 4,000 minimum")
    else:
        r.add_warning("word_count", f"{wc} words — above 8,000 target")

    # Required sections
    sections_lower = [s.lower() for s in find_sections(content)]
    for req in ["cloudscape", "navigation", "demo script", "layout"]:
        if any(req in s for s in sections_lower):
            r.add_pass(f"section_{req}")
        else:
            r.add_fail(f"section_{req}", f"Missing section containing '{req}'")

    return r


def validate_prototype(path: str) -> ValidationResult:
    r = ValidationResult(artifact=os.path.basename(path))

    # File size (< 500 KB)
    size_bytes = os.path.getsize(path)
    size_kb = size_bytes / 1024
    if size_kb < 500:
        r.add_pass(f"file_size ({size_kb:.0f} KB)")
    else:
        r.add_fail("file_size", f"{size_kb:.0f} KB — exceeds 500 KB limit")

    # Read content
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Cloudscape CSS present
    if "cloudscape" in content.lower() or "awsui" in content.lower():
        r.add_pass("cloudscape_css")
    else:
        r.add_fail("cloudscape_css", "No Cloudscape/awsui references found")

    # React present
    if "react" in content.lower():
        r.add_pass("react_included")
    else:
        r.add_warning("react_included", "No React references found")

    # Dark mode toggle
    if "dark" in content.lower() and ("mode" in content.lower() or "theme" in content.lower()):
        r.add_pass("dark_mode")
    else:
        r.add_warning("dark_mode", "No dark mode toggle detected")

    # No console.error calls (basic check)
    if "console.error" not in content:
        r.add_pass("no_console_errors")
    else:
        r.add_warning("no_console_errors", "Found console.error calls — verify they're error handlers, not bugs")

    # Check for realistic data (not "Service A", "Item 1")
    placeholder_patterns = ["Service A", "Service B", "Item 1", "Lorem ipsum", "placeholder"]
    found_placeholders = [p for p in placeholder_patterns if p in content]
    if not found_placeholders:
        r.add_pass("realistic_data")
    else:
        r.add_fail("realistic_data", f"Found placeholder data: {', '.join(found_placeholders)}")

    return r


def validate_launch_readiness(path: str, content: str) -> ValidationResult:
    r = ValidationResult(artifact=os.path.basename(path))
    fm = extract_frontmatter(content)

    if fm:
        r.add_pass("frontmatter_exists")
    else:
        r.add_fail("frontmatter_exists", "No frontmatter block found")

    # Word count (target: 3,000-5,000)
    wc = count_words(content)
    if 3000 <= wc <= 5000:
        r.add_pass(f"word_count ({wc})")
    elif wc < 3000:
        r.add_fail("word_count", f"{wc} words — below 3,000 minimum")
    else:
        r.add_warning("word_count", f"{wc} words — above 5,000 target")

    # Required sections (14 sections per SKILL.md)
    sections_lower = [s.lower() for s in find_sections(content)]
    required_keywords = ["engineering spec", "acceptance criteria", "sprint",
                         "rollout", "rollback", "monitoring", "security",
                         "tech debt", "success metric", "risk"]
    for req in required_keywords:
        if any(req in s for s in sections_lower):
            r.add_pass(f"section_{req}")
        else:
            r.add_fail(f"section_{req}", f"Missing section containing '{req}'")

    # GIVEN/WHEN/THEN acceptance criteria
    gwt_count = len(re.findall(r'GIVEN|WHEN|THEN', content))
    if gwt_count >= 6:  # At least 2 full criteria
        r.add_pass(f"given_when_then ({gwt_count} keywords)")
    else:
        r.add_fail("given_when_then", f"Only {gwt_count} GIVEN/WHEN/THEN keywords — need structured ACs")

    return r


# ─── Artifact type detection ─────────────────────────────────────

def detect_artifact_type(path: str) -> str:
    """Detect artifact type from filename."""
    basename = os.path.basename(path).lower()
    if basename.endswith('.html'):
        return 'prototype'
    if 'research' in basename:
        return 'research'
    if 'prd' in basename:
        return 'prd'
    if 'gandalf' in basename:
        return 'gandalf'
    if 'design-spec' in basename or 'design_spec' in basename:
        return 'design_spec'
    if 'launch-readiness' in basename or 'launch_readiness' in basename:
        return 'launch_readiness'
    if 'prototype-notes' in basename:
        return 'prototype_notes'
    return 'unknown'


def validate_file(path: str) -> Optional[ValidationResult]:
    """Validate a single artifact file."""
    artifact_type = detect_artifact_type(path)

    if artifact_type == 'prototype':
        return validate_prototype(path)

    if not os.path.exists(path):
        r = ValidationResult(artifact=path)
        r.add_fail("file_exists", "File not found")
        return r

    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    validators = {
        'research': validate_research,
        'prd': validate_prd,
        'gandalf': validate_gandalf,
        'design_spec': validate_design_spec,
        'launch_readiness': validate_launch_readiness,
    }

    validator = validators.get(artifact_type)
    if validator:
        return validator(path, content)
    else:
        r = ValidationResult(artifact=os.path.basename(path))
        r.add_warning("type_detection", f"Unknown artifact type for '{os.path.basename(path)}' — skipping")
        return r


def validate_pipeline(pipeline_dir: str) -> list:
    """Validate all artifacts in a pipeline directory."""
    results = []
    patterns = ["research-v*.md", "prd-v*.md", "gandalf-evaluation-v*.md",
                "design-spec-v*.md", "prototype-v*.html", "launch-readiness-v*.md"]

    for pattern in patterns:
        matches = sorted(glob.glob(os.path.join(pipeline_dir, pattern)))
        if matches:
            # Validate the latest version of each artifact type
            latest = matches[-1]
            result = validate_file(latest)
            if result:
                results.append(result)
        else:
            r = ValidationResult(artifact=pattern)
            r.add_warning("artifact_missing", f"No files matching '{pattern}' found")
            results.append(r)

    return results


# ─── Main ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == '--all' or sys.argv[1] == '--pipeline':
        pipeline_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
        results = validate_pipeline(pipeline_dir)
    else:
        result = validate_file(sys.argv[1])
        results = [result] if result else []

    # Print results
    total_passed = 0
    total_failed = 0
    for r in results:
        print(r.summary())
        total_passed += r.checks_passed
        total_failed += r.checks_failed

    # Final summary
    total = total_passed + total_failed
    print(f"\n{'='*60}")
    print(f"  TOTAL: {total_passed}/{total} checks passed across {len(results)} artifacts")
    if total_failed > 0:
        print(f"  {total_failed} checks FAILED")
        sys.exit(1)
    else:
        print("  ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == '__main__':
    main()
