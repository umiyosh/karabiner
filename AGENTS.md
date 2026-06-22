# AGENTS.md

## Conversation

- 常に日本語で会話する。

## Karabiner README Table

- `karabiner.json`、`assets/complex_modifications/*.json`、またはショートカット挙動に関わる設定を変更した場合は、必ず `$karabiner-readme-table` を使う。
- 設定変更後は `make table` を実行し、README.md の `ショートカットキー一覧` を `karabiner.json` から再生成する。
- README.md の `<!-- shortcuts-table:start -->` から `<!-- shortcuts-table:end -->` までを手で編集しない。表示文言の改善が必要なら生成スクリプトを直してから再生成する。
- 完了前に `make table-check` を実行し、README.md が最新であることを確認する。
- Karabiner-Elements CLI が利用できる環境では `make lint` も実行する。CLIが無い場合は、その未検証点を報告する。
