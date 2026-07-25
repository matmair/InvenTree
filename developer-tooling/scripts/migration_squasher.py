#!/usr/bin/env python3
import os
import sys
import glob
import re

BUILTIN_APPS = [
    "build",
    "common",
    "company",
    "importer",
    "machine",
    "order",
    "part",
    "report",
    "stock",
    "users",
    "plugin",
    "InvenTree",
    "generic"
]

def get_migrations_info():
    """Finds all built-in apps and counts their migrations."""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src", "backend", "InvenTree")
    apps_info = {}
    total_files = 0

    for app in BUILTIN_APPS:
        m_dir = os.path.join(base_dir, app, "migrations")
        if not os.path.exists(m_dir):
            continue
        py_files = glob.glob(os.path.join(m_dir, "[0-9]*.py"))
        count = len(py_files)
        apps_info[app] = {
            "path": m_dir,
            "count": count,
            "files": sorted([os.path.basename(f)[:-3] for f in py_files])
        }
        total_files += count

    return apps_info, total_files

def fix_squashed_migration(filepath, app_name):
    """Post-processes a squashed migration file to resolve syntax errors with leading zero numbers."""
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return False

    print(f"Post-processing squashed migration file: {filepath} for app: {app_name}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

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

    dynamic_getter = f"""
import importlib

def get_migration_func(migration_name, func_name):
    try:
        mod = importlib.import_module(f"{app_name}.migrations.{{migration_name}}")
        return getattr(mod, func_name)
    except (ImportError, AttributeError):
        return lambda apps, schema_editor: None
"""

    # Inject dynamic getter and custom classes right before "class Migration"
    insertion_point = content.find("class Migration(migrations.Migration):")
    if insertion_point != -1:
        content = content[:insertion_point] + dynamic_getter + custom_classes + "\n" + content[insertion_point:]

    # Replace references to operations subclasses (only when app_name is "part")
    if app_name == "part":
        content = content.replace("part.migrations.0112_auto_20230525_1606.RemoveFieldOrSkip", "RemoveFieldOrSkip")
        content = content.replace("part.migrations.0112_auto_20230525_1606.AddFieldOrSkip", "AddFieldOrSkip")

    # Replace references like app_name.migrations.0034_auto_20200404_1238.create_thumbnails
    escaped_app_name = re.escape(app_name)
    pattern = rf"{escaped_app_name}\.migrations\.([0-9a-zA-Z_]+)\.([a-zA-Z0-9_]+)"

    def replacer(match):
        migration_name = match.group(1)
        func_name = match.group(2)
        return f'get_migration_func("{migration_name}", "{func_name}")'

    content = re.sub(pattern, replacer, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully processed and resolved syntax errors in {filepath}")
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "fix":
        if len(sys.argv) < 4:
            print("Error: fix command requires both <filepath> and <app_name> arguments.")
            print("Usage: python migration_squasher.py fix <filepath> <app_name>")
            sys.exit(1)
        filepath = sys.argv[2]
        app_name = sys.argv[3]
        if app_name not in BUILTIN_APPS:
            print(f"Error: app_name '{app_name}' is not in BUILTIN_APPS.")
            sys.exit(1)
        fix_squashed_migration(filepath, app_name)
        return

    print("InvenTree Django Migration Analyzer & Squasher Helper Tool")
    print("=" * 60)

    apps_info, total_files = get_migrations_info()
    print(f"Detected {len(apps_info)} apps with a total of {total_files} migration files.\n")

    print(f"{'App':<20} | {'Migration Count':<15} | {'Path'}")
    print("-" * 60)
    for app, info in sorted(apps_info.items(), key=lambda x: x[1]['count'], reverse=True):
        print(f"{app:<20} | {info['count']:<15} | {info['path']}")
    print("-" * 60)

if __name__ == "__main__":
    main()
