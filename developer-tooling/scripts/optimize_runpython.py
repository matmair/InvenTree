#!/usr/bin/env python3
import os
import sys
import glob
import re
import ast
import subprocess

# Functions that perform seeding or insert default settings (must be preserved on fresh setups)
SEED_ALLOWLIST = {
    "add_default_reference",
    "set_default_currency",
    "set_currencies",
    "migrate_userthemes",
    "update_news_feed_urls",
    "update_image_attachments",
    "update_global_setting",
    "set_key",
    "set_testable",
    "set_template",
    "update_templates",
    "add_part_links",
    "set_creation_date"
}

class RunPythonOptimizer(ast.NodeTransformer):
    """AST transformer to optimize Django RunPython operations, preserving allowed seed functions."""

    def visit_Call(self, node):
        self.generic_visit(node)
        # Check if it is a migrations.RunPython call
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == "migrations" and node.func.attr == "RunPython":
                # Find 'code' keyword argument
                code_kw = None
                for kw in node.keywords:
                    if kw.arg == "code":
                        code_kw = kw.value

                # If code is positional, first argument is code
                if not code_kw and node.args:
                    code_kw = node.args[0]

                # Evaluate if the code represents a seed function in SEED_ALLOWLIST
                preserve_code = False
                if code_kw:
                    func_name = None
                    if isinstance(code_kw, ast.Attribute):
                        func_name = code_kw.attr
                    elif isinstance(code_kw, ast.Name):
                        func_name = code_kw.id
                    elif isinstance(code_kw, ast.Call) and isinstance(code_kw.func, ast.Name) and code_kw.func.id == "get_migration_func":
                        if len(code_kw.args) > 1 and isinstance(code_kw.args[1], ast.Constant):
                            func_name = code_kw.args[1].value

                    if func_name and func_name in SEED_ALLOWLIST:
                        preserve_code = True

                if not preserve_code:
                    noop_node = ast.Attribute(
                        value=ast.Attribute(
                            value=ast.Name(id="migrations", ctx=ast.Load()),
                            attr="RunPython",
                            ctx=ast.Load()
                        ),
                        attr="noop",
                        ctx=ast.Load()
                    )
                    node.args = [noop_node]
                    node.keywords = [
                        ast.keyword(arg="reverse_code", value=noop_node)
                    ]
        return node

def optimize_report_app_operations(tree):
    """Filters out the seven obsolete CreateModel/DeleteModel operations and their intervening noop RunPython in report app."""
    obsolete_models = {
        "BillOfMaterialsReport",
        "BuildReport",
        "PurchaseOrderReport",
        "ReturnOrderReport",
        "SalesOrderReport",
        "StockLocationReport",
        "TestReport"
    }

    # Locate the Migration class definition and its operations list
    for body_node in tree.body:
        if isinstance(body_node, ast.ClassDef) and body_node.name == "Migration":
            for class_node in body_node.body:
                if isinstance(class_node, ast.Assign):
                    for target in class_node.targets:
                        if isinstance(target, ast.Name) and target.id == "operations":
                            if isinstance(class_node.value, ast.List):
                                old_ops = class_node.value.elts
                                new_ops = []
                                runpython_noop_count = 0

                                for op in old_ops:
                                    if isinstance(op, ast.Call) and isinstance(op.func, ast.Attribute):
                                        # Check if it is CreateModel with an obsolete model
                                        if op.func.attr == "CreateModel":
                                            # Find name keyword
                                            model_name = None
                                            for kw in op.keywords:
                                                if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                                                    model_name = kw.value.value
                                            if model_name in obsolete_models:
                                                # Skip creating obsolete model
                                                continue

                                        # Check if it is DeleteModel with an obsolete model
                                        elif op.func.attr == "DeleteModel":
                                            model_name = None
                                            for kw in op.keywords:
                                                if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                                                    model_name = kw.value.value
                                            if model_name in obsolete_models:
                                                # Skip deleting obsolete model
                                                continue

                                        # Skip the intervening RunPython noop between creation and deletion of obsolete reports
                                        elif op.func.attr == "RunPython":
                                            if runpython_noop_count == 0:
                                                runpython_noop_count += 1
                                                continue

                                    new_ops.append(op)
                                class_node.value.elts = new_ops
                                print(f"  -> Report app operations optimized. Removed obsolete model operations. Reduced list from {len(old_ops)} to {len(new_ops)}.")
            break

def optimize_part_block_2_operations(tree):
    """Replaces RemoveFieldOrSkip/AddFieldOrSkip with standard migrations operations in part block 2."""
    for body_node in tree.body:
        if isinstance(body_node, ast.ClassDef) and body_node.name == "Migration":
            for class_node in body_node.body:
                if isinstance(class_node, ast.Assign):
                    for target in class_node.targets:
                        if isinstance(target, ast.Name) and target.id == "operations":
                            if isinstance(class_node.value, ast.List):
                                old_ops = class_node.value.elts
                                new_ops = []
                                for op in old_ops:
                                    # Skip RemoveFieldOrSkip entirely
                                    if isinstance(op, ast.Call) and isinstance(op.func, ast.Name) and op.func.id == "RemoveFieldOrSkip":
                                        continue

                                    # Rewrite AddFieldOrSkip to migrations.AddField
                                    if isinstance(op, ast.Call) and isinstance(op.func, ast.Name) and op.func.id == "AddFieldOrSkip":
                                        op.func = ast.Attribute(
                                            value=ast.Name(id="migrations", ctx=ast.Load()),
                                            attr="AddField",
                                            ctx=ast.Load()
                                        )
                                    new_ops.append(op)
                                class_node.value.elts = new_ops
                                print(f"  -> Part block 2 operations optimized. Removed RemoveFieldOrSkip and converted AddFieldOrSkip to AddField.")
            break

def optimize_file(filepath):
    """Optimizes RunPython blocks and class/function references using Python AST parsing."""
    if not os.path.exists(filepath):
        return

    print(f"Optimizing: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Balanced check for fake_func
    if "0097_partstocktakereport.fake_func" in content:
        content = content.replace("part.migrations.0097_partstocktakereport.fake_func", "fake_func")
        if "def fake_func(" not in content:
            fake_func_def = "\ndef fake_func(*args, **kwargs):\n    pass\n\n"
            class_decl = "class Migration(migrations.Migration):"
            idx = content.find(class_decl)
            if idx != -1:
                content = content[:idx] + fake_func_def + content[idx:]

    # Parse to AST and transform
    tree = ast.parse(content)

    # Apply specialized report app optimization if this is the report squashed file
    if "report" in filepath and "_squashed_" in filepath:
        optimize_report_app_operations(tree)

    # Apply specialized part block 2 optimization if this is the part block 2 squashed file
    if "part" in filepath and "0061_" in filepath and "_squashed_" in filepath:
        optimize_part_block_2_operations(tree)
        # Remove RemoveFieldOrSkip and AddFieldOrSkip class definitions from module body
        tree.body = [
            node for node in tree.body
            if not (isinstance(node, ast.ClassDef) and node.name in {"RemoveFieldOrSkip", "AddFieldOrSkip"})
        ]
        print("  -> Removed RemoveFieldOrSkip and AddFieldOrSkip class definitions from module body.")

    transformer = RunPythonOptimizer()
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)

    # Emit deterministically
    content = ast.unparse(transformed_tree)

    # Clean up any residual get_migration_func block between boundaries if it is unused
    if "get_migration_func" in content:
        if not re.search(r"get_migration_func\s*\(", content):
            content = re.sub(r"def get_migration_func.*?return lambda apps, schema_editor: None", "", content, flags=re.DOTALL)
            content = content.replace("import importlib", "")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully optimized: {filepath}")

def main():
    if len(sys.argv) > 1:
        optimize_file(sys.argv[1])
        return

    base_dir = "src/backend/InvenTree"
    squashed_files = glob.glob(os.path.join(base_dir, "**/migrations/*_squashed_*.py"), recursive=True)

    target_files = []
    for f in squashed_files:
        if "0021_auto_20201020_0908_squashed_0026_auto_20201023_1228" in f:
            continue
        if "0108_alter_purchaseorder_link_and_more_squashed_0109_alter_purchaseorderextraline_link_and_more" in f:
            continue
        target_files.append(f)

    if "--reset" in sys.argv and target_files:
        print("Reset flag detected. Reverting local changes on squashed files first...")
        subprocess.run(["git", "checkout", "--"] + target_files, shell=False)

    for f in target_files:
        optimize_file(f)

if __name__ == "__main__":
    main()
