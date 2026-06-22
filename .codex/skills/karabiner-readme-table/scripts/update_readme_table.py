#!/usr/bin/env python3
"""Update README shortcut table from karabiner.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


START = "<!-- shortcuts-table:start -->"
END = "<!-- shortcuts-table:end -->"
HEADING = "## ショートカットキー一覧"

KEY_NAMES = {
    "japanese_eisuu": "英数",
    "japanese_kana": "かな",
    "open_bracket": "[",
    "close_bracket": "]",
    "semicolon": ";",
    "slash": "/",
    "comma": ",",
    "period": ".",
    "spacebar": "space",
    "return_or_enter": "Enter",
    "escape": "escape",
    "international3": "¥",
    "left_arrow": "←",
    "down_arrow": "↓",
    "up_arrow": "↑",
    "right_arrow": "→",
    "page_up": "page_up",
    "page_down": "page_down",
    "caps_lock": "caps_lock",
    "left_control": "control",
    "right_control": "control",
    "left_command": "command",
    "right_command": "right_command",
    "left_option": "option",
    "right_option": "option",
    "mission_control": "Mission Control",
    "launchpad": "Launchpad",
    "illumination_decrement": "illumination_decrement",
    "illumination_increment": "illumination_increment",
}

MODIFIER_NAMES = {
    "command": "英数",
    "left_command": "英数",
    "right_command": "英数",
    "option": "かな",
    "left_option": "かな",
    "right_option": "かな",
    "control": "control",
    "left_control": "control",
    "right_control": "control",
    "shift": "shift",
    "left_shift": "shift",
    "right_shift": "shift",
}

CONSUMER_KEY_NAMES = {
    "fastforward": "fastforward",
}


def key_name(key_code: str, *, from_key: bool) -> str:
    if from_key and key_code == "left_command":
        return "英数"
    if from_key and key_code == "right_command":
        return "right_英数"
    if from_key and key_code in {"left_option", "right_option"}:
        return "かな"
    if re.fullmatch(r"f\d+", key_code):
        return key_code.upper()
    return KEY_NAMES.get(key_code, key_code)


def modifier_name(modifier: str, *, physical_alias: bool = True) -> str | None:
    if modifier == "any":
        return None
    if not physical_alias and modifier in {"option", "left_option", "right_option"}:
        return "option"
    if not physical_alias and modifier in {"command", "left_command", "right_command"}:
        return "command"
    return MODIFIER_NAMES.get(modifier, modifier)


def format_from(from_def: dict) -> str:
    parts: list[str] = []
    physical_alias = from_def.get("key_code") != "international3"
    modifiers = from_def.get("modifiers", {}).get("mandatory", [])
    for modifier in modifiers:
        name = modifier_name(modifier, physical_alias=physical_alias)
        if name:
            parts.append(name)

    if "key_code" in from_def:
        parts.append(key_name(from_def["key_code"], from_key=True))
    elif "consumer_key_code" in from_def:
        parts.append(CONSUMER_KEY_NAMES.get(from_def["consumer_key_code"], from_def["consumer_key_code"]))
    else:
        parts.append("unknown")

    return " + ".join(parts)


def format_key_action(action: dict) -> str | None:
    if "shell_command" in action:
        return simplify_shell_command(action["shell_command"])
    if "set_variable" in action:
        return None
    if action.get("key_code") == "vk_none":
        return "無効化"

    parts: list[str] = []
    physical_alias = action.get("key_code") != "international3"
    for modifier in action.get("modifiers", []):
        name = modifier_name(modifier, physical_alias=physical_alias)
        if name:
            parts.append(name)

    if "key_code" in action:
        parts.append(key_name(action["key_code"], from_key=False))
    elif "consumer_key_code" in action:
        parts.append(CONSUMER_KEY_NAMES.get(action["consumer_key_code"], action["consumer_key_code"]))
    else:
        return None

    return " + ".join(parts)


def simplify_shell_command(command: str) -> str:
    if command.startswith("~/dotfiles/bin/mgv"):
        return "~/dotfiles/bin/mgv"
    return command


def format_to_parts(manipulator: dict) -> tuple[list[str], str | None]:
    actions = [format_key_action(action) for action in manipulator.get("to", [])]
    actions = [action for action in actions if action]
    if not actions:
        return [], None
    return actions, format_to_if_alone(manipulator)


def plain_to(actions: list[str], alone: str | None) -> str:
    if actions == ["無効化"]:
        return "無効化"
    separator = " → " if any(action.startswith("/") or action.startswith("~/") for action in actions) else " + "
    text = separator.join(actions)
    if alone:
        text = f"{text} (単独押しで{alone})"
    return text


def format_to_if_alone(manipulator: dict) -> str | None:
    alone_actions = manipulator.get("to_if_alone") or []
    for action in alone_actions:
        if "key_code" in action:
            return key_name(action["key_code"], from_key=False)

    from_key_code = manipulator.get("from", {}).get("key_code")
    first_to_key_code = (manipulator.get("to") or [{}])[0].get("key_code")
    if from_key_code == "japanese_kana" and first_to_key_code == "left_option":
        return "かな"
    return None


def markdown_from(text: str) -> str:
    return f"`{text}`"


def markdown_to(actions: list[str], alone: str | None) -> str:
    if actions == ["無効化"]:
        return "無効化"

    suffix = f" (単独押しで{alone})" if alone else ""
    if len(actions) == 1:
        return f"`{actions[0]}`{suffix}"

    separator = " → " if any(action.startswith("/") or action.startswith("~/") for action in actions) else " + "
    return separator.join(f"`{action}`" for action in actions) + suffix


def markdown_shortcut(text: str, *, target: bool = False) -> str:
    if text == "無効化":
        return text

    suffix = ""
    if target and " (単独押しで" in text:
        text, suffix = text.split(" (単独押しで", 1)
        suffix = f" (単独押しで{suffix}"

    if " → " in text:
        return " → ".join(f"`{part}`" for part in text.split(" → ")) + suffix
    if text.count(" + ") > 1:
        return " + ".join(f"`{part}`" for part in text.split(" + ")) + suffix
    return f"`{text}`{suffix}"


def row_description(from_text: str, to_text: str, rule_description: str) -> str:
    friendly = friendly_description(from_text, to_text)
    if friendly:
        return friendly
    app = app_name(to_text)
    if app:
        return f"{app}を起動または前面化"
    if to_text == "無効化":
        return f"{from_text}を無効化"
    if rule_description and len(rule_description) <= 40 and "alias" not in rule_description.lower():
        return rule_description
    return f"{from_text}を{to_text}に変更"


def friendly_description(from_text: str, to_text: str) -> str | None:
    mappings = {
        ("英数 + w", "無効化"): "iTerm2でcmd+wを無効化",
        ("control + [", "escape + 英数"): "Ctrl+[を押したときに、escキーと英数キーを送信する",
        ("control + ]", "escape + 英数"): "Ctrl+]を押したときに、escキーと英数キーを送信する",
        ("英数", "command (単独押しで英数)"): "英数キーをCommandキーとして使用",
        ("かな", "option (単独押しでかな)"): "かなキーをOptionキーとして使用",
        ("かな + h", "←"): "Vi Mode: 左移動",
        ("かな + j", "↓"): "Vi Mode: 下移動",
        ("かな + k", "↑"): "Vi Mode: 上移動",
        ("かな + l", "→"): "Vi Mode: 右移動",
        ("かな + shift + h", "shift + ←"): "Vi Mode: 左移動 (Shift)",
        ("かな + shift + j", "shift + ↓"): "Vi Mode: 下移動 (Shift)",
        ("かな + shift + k", "shift + ↑"): "Vi Mode: 上移動 (Shift)",
        ("かな + shift + l", "shift + →"): "Vi Mode: 右移動 (Shift)",
        ("かな + ;", "page_up"): "PageUp",
        ("かな + /", "page_down"): "PageDown",
        ("かな + ,", "control + a"): "Home",
        ("かな + .", "control + e"): "End",
        ("かな + shift + ,", "shift + control + a"): "Home (Shift)",
        ("かな + shift + .", "shift + control + e"): "End (Shift)",
        (";", "Enter"): "セミコロンをEnterに変更",
        ("shift + ;", "shift + ;"): "Shift+セミコロンの挙動は変更なし",
        ("shift + control + ;", ";"): "Shift+Ctrl+セミコロンをセミコロンに変更",
        ("英数 + 2", "F2"): "F2を英数+2に変更",
        ("英数 + 7", "F7"): "F7を英数+7に変更",
        ("英数 + 8", "F8"): "F8を英数+8に変更",
        ("¥", "option + ¥"): "¥をAlt+¥に変更",
        ("option + ¥", "¥"): "Alt+¥を¥に変更",
        ("英数 + e", "英数 + a → 英数 + c → ~/dotfiles/bin/mgv"): "英数+EでVimで編集",
        ("shift + control + space", "shift + 英数 + space + shift + control + space"): "Shift+Ctrl+SpaceをSlack MuteとSuperwhisperに変更",
        ("caps_lock", "control"): "Caps LockをControlに変更",
        ("F3", "Mission Control"): "F3をMission Controlに変更",
        ("F4", "Launchpad"): "F4をLaunchpadに変更",
        ("F5", "illumination_decrement"): "F5をキーボード輝度ダウンに変更",
        ("F6", "illumination_increment"): "F6をキーボード輝度アップに変更",
        ("F9", "fastforward"): "F9を早送りに変更",
    }
    return mappings.get((from_text, to_text))


def app_name(to_text: str) -> str | None:
    match = re.search(r"/usr/bin/open -a '([^']+)\.app'", to_text)
    if not match:
        return None
    return match.group(1)


def condition_suffix(conditions: list[dict] | None) -> str:
    if not conditions:
        return ""
    for condition in conditions:
        if condition.get("type") != "keyboard_type_if":
            continue
        keyboard_types = condition.get("keyboard_types", [])
        if set(keyboard_types) == {"ansi", "iso"}:
            return " (ANSI/ISO)"
        if keyboard_types == ["jis"]:
            return " (JIS)"
    return ""


def should_skip_manipulator(manipulator: dict) -> bool:
    actions = manipulator.get("to", [])
    if not actions:
        return True
    from_key_code = manipulator.get("from", {}).get("key_code")
    to_key_codes = [action.get("key_code") for action in actions if "key_code" in action]
    has_variable_action = any("set_variable" in action for action in actions)
    if has_variable_action and to_key_codes == [from_key_code]:
        return True
    if any("set_variable" not in action for action in actions):
        return False
    return True


def generated_rows(data: dict) -> list[tuple[str, str, str]]:
    profile = next((profile for profile in data.get("profiles", []) if profile.get("selected")), None)
    if profile is None:
        profiles = data.get("profiles", [])
        profile = profiles[0] if profiles else {}

    rows: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    for rule in profile.get("complex_modifications", {}).get("rules", []):
        rule_description = rule.get("description", "")
        for manipulator in rule.get("manipulators", []):
            if should_skip_manipulator(manipulator):
                continue
            from_text = format_from(manipulator.get("from", {}))
            to_actions, alone = format_to_parts(manipulator)
            if not to_actions:
                continue
            to_text = plain_to(to_actions, alone)
            description = row_description(from_text, to_text, rule_description) + condition_suffix(manipulator.get("conditions"))
            rendered = (description, markdown_from(from_text), markdown_to(to_actions, alone))
            identity = (from_text, to_text, condition_suffix(manipulator.get("conditions")))
            if identity in seen:
                continue
            seen.add(identity)
            rows.append(rendered)

    for modification in profile.get("simple_modifications", []):
        from_text = format_from(modification.get("from", {}))
        to_actions, alone = format_to_parts(modification)
        if not to_actions:
            continue
        to_text = plain_to(to_actions, alone)
        rendered = (row_description(from_text, to_text, ""), markdown_from(from_text), markdown_to(to_actions, alone))
        identity = (from_text, to_text, "")
        if identity not in seen:
            seen.add(identity)
            rows.append(rendered)

    for modification in profile.get("fn_function_keys", []):
        from_text = format_from(modification.get("from", {}))
        to_actions, alone = format_to_parts(modification)
        if not to_actions:
            continue
        to_text = plain_to(to_actions, alone)
        rendered = (row_description(from_text, to_text, ""), markdown_from(from_text), markdown_to(to_actions, alone))
        identity = (from_text, to_text, "")
        if identity not in seen:
            seen.add(identity)
            rows.append(rendered)

    return rows


def existing_table_index(readme: str) -> tuple[dict[tuple[str, str], str], dict[tuple[str, str], int]]:
    if START in readme and END in readme:
        return {}, {}

    descriptions: dict[tuple[str, str], str] = {}
    order: dict[tuple[str, str], int] = {}
    for line in readme.splitlines():
        if not line.startswith("|") or line.startswith("|------"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] == "説明":
            continue
        key = (normalize_cell(cells[1]), normalize_cell(cells[2]))
        descriptions[key] = cells[0]
        order.setdefault(key, len(order))
    return descriptions, order


def normalize_cell(cell: str) -> str:
    return re.sub(r"\s+", " ", cell.replace("`", "")).strip()


def render_table(rows: list[tuple[str, str, str]], readme: str) -> str:
    descriptions, order = existing_table_index(readme)
    enriched = []
    for index, (description, from_cell, to_cell) in enumerate(rows):
        key = (normalize_cell(from_cell), normalize_cell(to_cell))
        enriched.append((order.get(key, 10_000 + index), descriptions.get(key, description), from_cell, to_cell))
    enriched.sort(key=lambda row: row[0])

    lines = [
        START,
        "| 説明 | 元のキー | 変更後のキー |",
        "|------|---------|-------------|",
    ]
    lines.extend(f"| {description} | {from_cell} | {to_cell} |" for _, description, from_cell, to_cell in enriched)
    lines.append(END)
    return "\n".join(lines)


def replace_table(readme: str, table: str) -> str:
    if START in readme and END in readme:
        pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
        return pattern.sub(table, readme)

    heading_index = readme.find(HEADING)
    if heading_index == -1:
        return readme.rstrip() + f"\n\n{HEADING}\n\n{table}\n"

    after_heading_index = readme.find("\n", heading_index)
    if after_heading_index == -1:
        return readme.rstrip() + f"\n\n{table}\n"

    table_start = readme.find("| 説明 |", after_heading_index)
    if table_start == -1:
        return readme[: after_heading_index + 1] + f"\n{table}\n" + readme[after_heading_index + 1 :]

    table_end = table_start
    lines = readme[table_start:].splitlines(keepends=True)
    consumed = 0
    for line in lines:
        if not line.startswith("|"):
            break
        consumed += len(line)
    table_end += consumed
    return readme[:table_start] + table + "\n" + readme[table_end:]


def update_readme(karabiner_path: Path, readme_path: Path) -> str:
    data = json.loads(karabiner_path.read_text())
    readme = readme_path.read_text()
    table = render_table(generated_rows(data), readme)
    updated = replace_table(readme, table)
    if not updated.endswith("\n"):
        updated += "\n"
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--karabiner", type=Path, default=Path("karabiner.json"))
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--check", action="store_true", help="Exit with an error if README.md is not up to date.")
    args = parser.parse_args()

    updated = update_readme(args.karabiner, args.readme)
    current = args.readme.read_text()

    if args.check:
        if current != updated:
            print(f"{args.readme} is out of date. Run `make table`.", file=sys.stderr)
            return 1
        return 0

    if current != updated:
        args.readme.write_text(updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
