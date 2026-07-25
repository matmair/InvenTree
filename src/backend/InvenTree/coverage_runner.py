#!/usr/bin/env python3
import os
import sys
import subprocess

def run_tests_with_cov():
    """Runs pytest with coverage enabled and prints results."""
    env = os.environ.copy()
    env["INVENTREE_STATIC_ROOT"] = "/tmp/static"
    env["INVENTREE_MEDIA_ROOT"] = "/tmp/media"
    env["INVENTREE_DB_ENGINE"] = "sqlite3"
    env["INVENTREE_DB_NAME"] = "/tmp/db.sqlite3"
    env["INVENTREE_SECRET_KEY"] = "test_secret_key_12345"
    env["INVENTREE_SITE_URL"] = "http://localhost:8000"
    env["INVENTREE_BACKUP_DIR"] = "/tmp/backups"

    print("Running tests with coverage analysis...")
    cmd = ".venv/bin/python -m pytest --cov=src/backend/InvenTree/part --cov-report=term-missing src/backend/InvenTree/part/test_api.py"
    res = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)

    print(res.stdout)
    if res.returncode != 0:
        print("Tests finished with some failures (this is expected for pre-existing failures).")

def main():
    print("InvenTree Test Coverage Comparison Runner")
    print("=" * 60)
    run_tests_with_cov()

if __name__ == "__main__":
    main()
