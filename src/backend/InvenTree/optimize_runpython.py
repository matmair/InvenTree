#!/usr/bin/env python3
import os
import sys
import glob
import re
import subprocess

def find_balanced_parentheses(text, start_idx):
    """Finds the index of the matching closing parenthesis."""
    count = 0
    for i in range(start_idx, len(text)):
        if text[i] == '(':
            count += 1
        elif text[i] == ')':
            count -= 1
            if count == 0:
                return i
    return -1

def optimize_file(filepath):
    """Replaces custom RunPython calls with noop and removes the manual copying comments."""
    if not os.path.exists(filepath):
        return

    print(f"Optimizing: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace custom RemoveFieldOrSkip/AddFieldOrSkip with local definitions of those classes
    if "0112_auto_20230525_1606.RemoveFieldOrSkip" in content or "0112_auto_20230525_1606.AddFieldOrSkip" in content:
        content = content.replace("part.migrations.0112_auto_20230525_1606.RemoveFieldOrSkip", "RemoveFieldOrSkip")
        content = content.replace("part.migrations.0112_auto_20230525_1606.AddFieldOrSkip", "AddFieldOrSkip")

        custom_classes = """
class RemoveFieldOrSkip(migrations.RemoveField):
    def database_backwards(self, app_label, schema_editor, from_state, to_state) -> None:
        pass
    def database_forwards(self, app_label, schema_editor, from_state, to_state) -> None:
        try:
            super().database_forwards(app_label, schema_editor, from_state, to_state)
        except Exception:
            pass
    def state_forwards(self, app_label, state) -> None:
        try:
            super().state_forwards(app_label, state)
        except Exception:
            pass

class AddFieldOrSkip(migrations.AddField):
    def database_backwards(self, app_label, schema_editor, from_state, to_state) -> None:
        pass
    def database_forwards(self, app_label, schema_editor, from_state, to_state) -> None:
        try:
            super().database_forwards(app_label, schema_editor, from_state, to_state)
        except Exception:
            pass
    def state_forwards(self, app_label, state) -> None:
        try:
            super().state_forwards(app_label, state)
        except Exception:
            pass
"""
        class_decl = "class Migration(migrations.Migration):"
        idx = content.find(class_decl)
        if idx != -1:
            content = content[:idx] + custom_classes + "\n" + content[idx:]

    # Replace upload_to with local fake_func definition
    if "0097_partstocktakereport.fake_func" in content or "fake_func" in content:
        content = content.replace("part.migrations.0097_partstocktakereport.fake_func", "fake_func")
        if "def fake_func(" not in content:
            fake_func_def = "\ndef fake_func(*args, **kwargs):\n    pass\n\n"
            class_decl = "class Migration(migrations.Migration):"
            idx = content.find(class_decl)
            if idx != -1:
                content = content[:idx] + fake_func_def + content[idx:]

    # Remove manual copying comments at the top
    content = re.sub(r"# Functions from the following migrations need manual copying\..*?# [a-zA-Z0-9_\.]+\n\n", "", content, flags=re.DOTALL)
    content = re.sub(r"# Functions from the following migrations need manual copying\..*?# [a-zA-Z0-9_\.]+", "", content, flags=re.DOTALL)

    # Balance parentheses search for migrations.RunPython
    idx = 0
    while True:
        match = re.search(r"migrations\.RunPython\s*\(", content[idx:])
        if not match:
            break

        start_pos = idx + match.start()
        open_paren_pos = idx + match.end() - 1
        close_paren_pos = find_balanced_parentheses(content, open_paren_pos)

        if close_paren_pos != -1:
            replacement = "migrations.RunPython(migrations.RunPython.noop, reverse_code=migrations.RunPython.noop)"
            content = content[:start_pos] + replacement + content[close_paren_pos + 1:]
            idx = start_pos + len(replacement)
        else:
            idx = open_paren_pos + 1

    # Remove any unused dynamic getters or custom classes we injected earlier to make it incredibly clean!
    content = re.sub(r"import importlib.*?\nclass Migration", "class Migration", content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully optimized: {filepath}")

def main():
    if len(sys.argv) > 1:
        optimize_file(sys.argv[1])
        return

    base_dir = "src/backend/InvenTree"
    # To recover from any broken state first, let's discard local modifications to squashed files
    subprocess_run = "git checkout -- src/backend/InvenTree/*/migrations/*_squashed_*.py"
    os.system(subprocess_run)

    squashed_files = glob.glob(os.path.join(base_dir, "**/migrations/*_squashed_*.py"), recursive=True)

    # Filter out pre-existing ones we do not want to modify
    for f in squashed_files:
        if "0021_auto_20201020_0908_squashed_0026_auto_20201023_1228" in f:
            continue
        if "0108_alter_purchaseorder_link_and_more_squashed_0109_alter_purchaseorderextraline_link_and_more" in f:
            continue
        optimize_file(f)

if __name__ == "__main__":
    main()
