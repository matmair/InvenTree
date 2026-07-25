#!/usr/bin/env python3
import os
import sys
import tempfile
import subprocess

def run_tests_with_cov():
    """Runs pytest with coverage enabled in an isolated temporary directory and prints results."""
    with tempfile.TemporaryDirectory() as tmpdir:
        static_dir = os.path.join(tmpdir, "static")
        media_dir = os.path.join(tmpdir, "media")
        db_path = os.path.join(tmpdir, "db.sqlite3")
        backup_dir = os.path.join(tmpdir, "backups")

        # Create necessary directories
        os.makedirs(static_dir, exist_ok=True)
        os.makedirs(media_dir, exist_ok=True)
        os.makedirs(backup_dir, exist_ok=True)

        env = os.environ.copy()
        env["INVENTREE_STATIC_ROOT"] = static_dir
        env["INVENTREE_MEDIA_ROOT"] = media_dir
        env["INVENTREE_DB_ENGINE"] = "sqlite3"
        env["INVENTREE_DB_NAME"] = db_path
        env["INVENTREE_SECRET_KEY"] = "test_secret_key_12345"
        env["INVENTREE_SITE_URL"] = "http://localhost:8000"
        env["INVENTREE_BACKUP_DIR"] = backup_dir

        # 1. Run migrations to verify they work and to initialize the database
        print("Verifying and applying squashed database migrations...")
        migrate_cmd = [
            sys.executable, "src/backend/InvenTree/manage.py", "migrate", "--noinput"
        ]
        migrate_res = subprocess.run(migrate_cmd, env=env, capture_output=True, text=True)
        if migrate_res.returncode != 0:
            print("Migration failed!")
            print(migrate_res.stdout)
            print(migrate_res.stderr)
            sys.exit(migrate_res.returncode)
        print("Database migrations applied successfully!")

        # 2. Run pytest with coverage
        print(f"Running tests with coverage analysis in isolated directory: {tmpdir}...")

        cmd = [
            sys.executable, "-m", "pytest",
            "--cov=src/backend/InvenTree/part",
            "--cov-report=term-missing",
            "src/backend/InvenTree/part/test_api.py"
        ]

        res = subprocess.run(cmd, env=env, capture_output=True, text=True)

        print(res.stdout)
        if res.stderr:
            print("Errors/Warnings in STDERR:")
            print(res.stderr)

        if res.returncode != 0:
            print(f"Tests failed with exit code: {res.returncode}")
            sys.exit(res.returncode)
        else:
            print("All tests passed successfully under coverage!")

def main():
    print("InvenTree Test Coverage Comparison Runner")
    print("=" * 60)
    run_tests_with_cov()

if __name__ == "__main__":
    main()
