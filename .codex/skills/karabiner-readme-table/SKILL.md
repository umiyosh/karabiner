---
name: karabiner-readme-table
description: Update the Karabiner-Elements shortcut table in README.md from karabiner.json. Use when working in this repository and changing Karabiner settings, shortcut mappings, complex_modifications, simple_modifications, fn_function_keys, assets/complex_modifications, README shortcut documentation, or the Makefile targets that validate Karabiner configuration.
---

# Karabiner README Table

## Overview

Keep README.md's "ショートカットキー一覧" table derived from the active Karabiner profile in karabiner.json. Use the bundled script instead of editing the generated table by hand.

## Workflow

1. Edit Karabiner settings in `karabiner.json` or supporting complex modification assets.
2. Run `make table` from the repository root.
3. Inspect the README diff and confirm the generated table reflects the changed shortcuts.
4. Run `make table-check` before finishing to verify README.md is current.
5. Run `make lint` when Karabiner-Elements CLI exists on the machine. If it is unavailable, report that verification gap.

## Table Generation

The generator lives at:

```bash
python3 .codex/skills/karabiner-readme-table/scripts/update_readme_table.py
```

It reads the selected profile from `karabiner.json`, derives rows from active `complex_modifications.rules[].manipulators`, `simple_modifications`, and `fn_function_keys`, then replaces only the generated table block in README.md.

Do not manually edit the block between:

```markdown
<!-- shortcuts-table:start -->
<!-- shortcuts-table:end -->
```

If generated wording is insufficient, update the generator or add clearer Karabiner metadata, then regenerate.

## Display Rules

- Display command modifiers as `英数` and option modifiers as `かな`, because this repository maps those physical keys for shortcut use.
- Preserve descriptions only when converting a legacy, unmarked table. Once the generated markers exist, treat the generator as the source of truth.
- Remove README rows that no longer correspond to active mappings in `karabiner.json`.

## Required Checks

Use these commands from the repository root:

```bash
make table
make table-check
make lint
```
