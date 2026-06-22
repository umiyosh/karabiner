
.PHONY: lint
lint:
	'/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli' \
		--lint-complex-modifications \
   ./karabiner.json

.PHONY: table
table:
	python3 .codex/skills/karabiner-readme-table/scripts/update_readme_table.py

.PHONY: table-check
table-check:
	python3 .codex/skills/karabiner-readme-table/scripts/update_readme_table.py --check
