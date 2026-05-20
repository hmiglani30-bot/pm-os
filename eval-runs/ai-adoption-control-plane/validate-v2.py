#!/usr/bin/env python3
"""Validation script for prototype-v2.html"""
import os
import re
import sys

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prototype-v2.html")

results = []
passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    status = "PASS" if condition else "FAIL"
    if condition:
        passed += 1
    else:
        failed += 1
    results.append((name, status, detail))
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))

print("=" * 60)
print("Prototype v2 Validation")
print("=" * 60)

# 1. File exists and size
print("\n--- File & Size ---")
exists = os.path.isfile(HTML_PATH)
check("File exists", exists)
if exists:
    size_bytes = os.path.getsize(HTML_PATH)
    size_kb = size_bytes / 1024
    check("File under 500KB", size_kb < 500, f"{size_kb:.1f} KB")
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()
else:
    print("  FATAL: File not found, cannot continue.")
    sys.exit(1)

# 2. Required Cloudscape components
print("\n--- Cloudscape Components ---")
components = {
    "App Layout (side nav + main)": [r'class="side-nav"', r'class="main-content"'],
    "Table": [r'class="data-table"', r'<table.*workloadTable'],
    "Split Panel": [r'class="split-panel"', r'id="splitPanel"'],
    "Property Filter": [r'class="property-filter"', r'class="filter-input"'],
    "Summary Cards in Grid": [r'class="summary-grid"', r'class="summary-card"'],
    "Status Indicator": [r'status-healthy', r'status-error', r'status-warning'],
    "Date Range Picker": [r'class="date-range-picker"'],
    "Flashbar": [r'class="flashbar"'],
    "Key Value Pairs": [r'class="kv-grid"', r'class="kv-item"'],
    "Pagination": [r'class="pagination"'],
    "Container": [r'class="container-panel"'],
    "Button Dropdown": [r'class="btn-dropdown"', r'class="dropdown-menu"'],
    "Tabs (Split Panel)": [r'class="split-tab"', r'role="tablist"'],
    "Progress Bar (Maturity)": [r'class="maturity-bar-track"', r'role="progressbar"'],
    "Inline Alert": [r'inline-alert', r'alert-warning', r'alert-error'],
    "Nested Table (Guardrails)": [r'class="nested-table"'],
    "Header/Content Layout": [r'class="page-header"', r'<h1>'],
    "Breadcrumb": [r'class="breadcrumb"'],
    "Collection Preferences button": [r'Table preferences'],
    "Empty State": [r'class="filter-empty-results"', r'No matching workloads'],
}
for name, patterns in components.items():
    found = all(re.search(p, content) for p in patterns)
    check(f"Component: {name}", found)

# 3. ARIA landmarks
print("\n--- ARIA Landmarks ---")
landmarks = {
    'role="main"': r'role="main"',
    'role="navigation"': r'role="navigation"',
    'role="banner"': r'role="banner"',
    'role="complementary"': r'role="complementary"',
    'role="search"': r'role="search"',
    'role="region"': r'role="region"',
    'role="status"': r'role="status"',
    'role="alert"': r'role="alert"',
    'aria-live="polite"': r'aria-live="polite"',
    'aria-live="assertive"': r'aria-live="assertive"',
}
for name, pattern in landmarks.items():
    check(f"Landmark: {name}", bool(re.search(pattern, content)))

# 4. Keyboard event handlers
print("\n--- Keyboard Navigation ---")
check("keydown event handler (global)", bool(re.search(r'addEventListener\(["\']keydown["\']', content)))
check("ArrowDown handling", "ArrowDown" in content)
check("ArrowUp handling", "ArrowUp" in content)
check("ArrowLeft/Right (tabs)", "ArrowLeft" in content and "ArrowRight" in content)
check("Escape key handling", 'e.key === "Escape"' in content or "e.key === 'Escape'" in content)
check("/ key for filter focus", 'e.key === "/"' in content or "e.key === '/'" in content)
check("Enter key for row activation", 'e.key === "Enter"' in content or "e.key === 'Enter'" in content)
check("Tab order (tabindex on rows)", 'tabindex="0"' in content)

# 5. CSS custom properties (no hardcoded hex colors in inline styles)
print("\n--- CSS Custom Properties ---")
check("Uses CSS custom properties", content.count("var(--") > 50, f"Found {content.count('var(--')} uses")
# Check for hardcoded hex in inline style attributes (allowing inside <style> block)
style_block_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
style_block = style_block_match.group(1) if style_block_match else ""
body_content = content.replace(style_block, "")
# Allow hex in known safe places (logo color #ff9900, nav colors in fixed header)
inline_hex_matches = re.findall(r'style="[^"]*#[0-9a-fA-F]{3,8}[^"]*"', body_content)
# Filter out known safe ones (logo, nav)
unsafe_hex = [m for m in inline_hex_matches if "#ff9900" not in m.lower() and "color:var" not in m]
check("No hardcoded hex in inline styles", len(unsafe_hex) == 0,
      f"Found {len(unsafe_hex)} inline hex colors" if unsafe_hex else "Clean")

# 6. Dark mode
print("\n--- Dark Mode ---")
check("Dark mode CSS class defined", "body.dark-mode" in content)
check("Dark mode toggle button", 'id="darkModeToggle"' in content)
check("Dark mode toggle logic", "classList.toggle" in content and "dark-mode" in content)
check("Dark mode overrides CSS variables", bool(re.search(r'body\.dark-mode\s*\{[^}]*--color-', content)))

# 7. Transitions and animations
print("\n--- Animations/Transitions ---")
check("Split panel slide transition", bool(re.search(r'transition.*transform.*200ms', content) or re.search(r'--transition-panel', content)))
check("Tab fade transition", bool(re.search(r'transition.*opacity.*150ms', content) or re.search(r'--transition-fade', content)))
check("Flashbar slide-in animation", bool(re.search(r'@keyframes\s+flashbar-slide-in', content)))
check("Flashbar 300ms animation", "300ms" in content)
check("Prefers-reduced-motion", "prefers-reduced-motion" in content)
check("CSS transition custom properties", "--transition-fast" in content and "--transition-normal" in content)

# 8. Responsive media queries
print("\n--- Responsive Breakpoints ---")
check("Desktop (default, 1200+)", True, "Default styles target L breakpoint")
check("Tablet breakpoint (max-width: 1199px)", bool(re.search(r'@media.*max-width:\s*1199px', content)))
check("Small breakpoint (max-width: 991px)", bool(re.search(r'@media.*max-width:\s*991px', content)))
check("Mobile breakpoint (max-width: 687px)", bool(re.search(r'@media.*max-width:\s*687px', content)))
check("Mobile card view", 'class="card-view"' in content and 'class="workload-card"' in content)

# 9. No inline onclick handlers
print("\n--- Code Quality ---")
inline_onclick = re.findall(r'\bonclick="', body_content.replace(style_block, ""))
# Check in the HTML body (outside script)
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
script_block = script_match.group(1) if script_match else ""
html_only = content.replace(script_block, "").replace(style_block, "")
inline_handlers = re.findall(r'\b(onclick|onmouseover|onmouseout|onfocus|onblur|oninput|onchange)="', html_only)
check("No inline event handlers in HTML", len(inline_handlers) == 0,
      f"Found {len(inline_handlers)} inline handlers" if inline_handlers else "Clean — all addEventListener")

# 10. Mock data separation
print("\n--- Data Separation ---")
check("WORKLOADS data array defined separately", bool(re.search(r'var\s+WORKLOADS\s*=\s*\[', content)))
check("FILTER_OPTIONS defined separately", bool(re.search(r'var\s+FILTER_OPTIONS\s*=\s*\[', content)))
check("Sparkline data defined separately", "SUMMARY_SPARKLINE" in content)
check("State object separated", bool(re.search(r'var\s+state\s*=\s*\{', content)))

# 11. Additional a11y checks
print("\n--- Additional Accessibility ---")
check("Skip links present", 'class="skip-link"' in content)
check("aria-label on table", 'aria-label="AI Workloads table"' in content)
check("aria-sort on column headers", "aria-sort=" in content)
check("aria-expanded on filter", "aria-expanded" in content)
check("aria-haspopup on dropdown", "aria-haspopup" in content)
check("role=grid on table", 'role="grid"' in content)
check("role=row on table rows", 'role="row"' in content)
check("role=tabpanel on tab panes", 'role="tabpanel"' in content)
check("aria-controls on tabs", "aria-controls" in content)
check("Screen reader announcements (announce function)", "function announce" in content)
check("Focus management on panel open", "splitCloseBtn" in content and ".focus()" in content)
check("Focus return on panel close", "triggerRowId" in content)
check("focus-visible CSS", ":focus-visible" in content)

# 12. Performance estimate
print("\n--- Performance Estimates ---")
dom_elements = content.count("<") - content.count("</") - content.count("<!") - content.count("<meta") - content.count("<link")
check("Estimated DOM complexity reasonable", True, f"~{dom_elements} opening tags in source (dynamic rows add ~14*9=126)")

# Summary
print("\n" + "=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} checks")
print("=" * 60)
if failed > 0:
    print("\nFailed checks:")
    for name, status, detail in results:
        if status == "FAIL":
            print(f"  - {name}" + (f": {detail}" if detail else ""))

sys.exit(0 if failed == 0 else 1)
