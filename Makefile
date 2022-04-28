
.PHONY: lint
lint:
	'/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli' \
		--lint-complex-modifications \
   ./karabiner.json
