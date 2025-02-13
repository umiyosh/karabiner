# Karabiner-Elements 設定

このリポジトリには、macOS のキーボード動作をカスタマイズするための Karabiner-Elements 設定が含まれています。

## ショートカットキー一覧

| 説明 | 元のキー | 変更後のキー |
|------|---------|-------------|
| iTerm2でcmd+wを無効化 | `英数 + w` | 無効化 |
| Ctrl+[を押したときに、escキーと英数キーを送信する (ANSI/ISO) | `control + [` | `escape` + `英数` |
| Ctrl+]を押したときに、escキーと英数キーを送信する (JIS) | `control + ]` | `escape` + `英数` |
| 英数キーをCommandキーとして使用 | `英数` | `command` (単独押しで英数) |
| かなキーをOptionキーとして使用 | `かな` | `option` (単独押しでかな) |
| Vi Mode: 左移動 | `かな + h` | `←` |
| Vi Mode: 下移動 | `かな + j` | `↓` |
| Vi Mode: 上移動 | `かな + k` | `↑` |
| Vi Mode: 右移動 | `かな + l` | `→` |
| Vi Mode: 左移動 (Shift) | `かな + shift + h` | `shift + ←` |
| Vi Mode: 下移動 (Shift) | `かな + shift + j` | `shift + ↓` |
| Vi Mode: 上移動 (Shift) | `かな + shift + k` | `shift + ↑` |
| Vi Mode: 右移動 (Shift) | `かな + shift + l` | `shift + →` |
| PageUp | `かな + ;` | `page_up` |
| PageDown | `かな + /` | `page_down` |
| Home | `かな + ,` | `control + a` |
| End | `かな + .` | `control + e` |
| Home (Shift) | `かな + shift + ,` | `shift + control + a` |
| End (Shift) | `かな + shift + .` | `shift + control + e` |
| セミコロンをEnterに変更 | `;` | `Enter` |
| Shift+セミコロンの挙動は変更なし | `shift + ;` | `shift + ;` |
| 右英数をセミコロンに変更 | `right_英数` | `;` |
| F2を英数+2に変更 | `英数 + 2` | `F2` |
| F7を英数+7に変更 | `英数 + 7` | `F7` |
| F8を英数+8に変更 | `英数 + 8` | `F8` |
| ¥をAlt+¥に変更 | `¥` | `option + ¥` |
| Alt+¥を¥に変更 | `option + ¥` | `¥` |
| 英数+EでVimで編集 | `英数 + e` | `英数 + a` → `英数 + c` → `~/dotfiles/bin/mgv` |
| 英数+: を無効化 | `英数 + shift + :` | 無効化 |
| Shift+Ctrl+SpaceをSlack MuteとSuperwhisperに変更 | `shift + control + space` | `shift + 英数 + space` + `shift + control + space` |
| Caps LockをControlに変更 | `caps_lock` | `control` |
| F3をMission Controlに変更 | `F3` | `Mission Control` |
| F4をLaunchpadに変更 | `F4` | `Launchpad` |
| F5をキーボード輝度ダウンに変更 | `F5` | `illumination_decrement` |
| F6をキーボード輝度アップに変更 | `F6` | `illumination_increment` |
| F9を早送りに変更 | `F9` | `fastforward` |
