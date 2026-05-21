---
description: Build a single-file HTML prototype from a PRD or design spec
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[topic] [--mode vision|spec]"
---

# Build Prototype

Run the Prototype Builder skill for `$ARGUMENTS`.

1. Read the Prototype Builder skill at `skills/prototype-builder/SKILL.md` and follow its instructions exactly.
2. Determine mode:
   - `--mode vision` (default if no design spec exists): Read the PRD directly, build a vision prototype showing the product concept.
   - `--mode spec`: Read the design spec, build a production-faithful prototype matching the spec exactly.
3. Use AWS Cloudscape design system components. Single-file HTML with all CSS/JS inline.
4. Build iteratively — start with layout structure, then populate each section, then add interactivity.
5. Validate: open in browser, check JS console errors, verify all tabs/buttons/interactions work.
6. Output: `prototype-v[N].html` saved to the pipeline working directory.
