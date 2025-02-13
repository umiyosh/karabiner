
.PHONY: lint
lint:
	'/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli' \
		--lint-complex-modifications \
   ./karabiner.json

# update readme
.PHONY: table
table:
	cat karabiner.json|sgpt --code "Readme.mdにたいしkarabiner.jsonよりREADME.mdのショートカットキー一覧表をmd形式で更新してください.optionとcommandは英数・かなにいれかえてるので それも意識すること"
