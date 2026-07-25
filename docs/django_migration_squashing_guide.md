# Research and Guidelines: Canonical Ways to Squash Migrations in Django Projects

This document presents the research, methodology, and recommendations for squashing database migrations in complex Django projects, with specific application to InvenTree.

---

## 1. Why Squash Migrations?

In mature Django projects, the accumulation of migrations (often hundreds of files per app) causes several key problems:
- **Prolonged Startup & Test Times:** Django's migration engine has to parse every file, build the migration graph, and check for consistency. InvenTree, with 13 apps and over 650 migration files, incurs noticeable latency during testing, continuous integration (CI), and local development.
- **Slower New Setup/Provisioning:** A newly set up instance has to run all 650+ migrations sequentially to build the initial database schema. This can take several minutes.
- **Maintenance Overhead:** Resolving conflicts on branch merges gets increasingly complex as the migration history becomes a dense web of dependencies.

---

## 2. Canonical Squashing Methodologies in Django

There are two primary ways to reduce the number of migrations in a Django project.

### Methodology A: Django's Native `squashmigrations`
This is the built-in, officially supported approach.
- **Command:** `python manage.py squashmigrations <app_name> <start_migration> <end_migration>`
- **Mechanism:**
  1. Django reads the operations within the specified range and attempts to merge and optimize them (e.g., combining a `CreateModel` and successive `AddField` operations into a single optimized `CreateModel` statement).
  2. It generates a new migration file (e.g., `0001_squashed_...py`) that contains a `replaces` list pointing to the original historical migration files.
  3. During transition, Django uses the `replaces` list:
     - **For new instances:** It skips the replaced individual migrations and runs the squashed migration file directly.
     - **For existing/partially-migrated instances:** If the replaced migrations have already been applied, Django understands that they are represented by the squashed migration and marks the squashed migration as applied without running any code.
- **Limitations:**
  - **Single App Limitation:** It only operates on one app at a time.
  - **Circular Dependencies:** If apps have cross-app dependencies (e.g., a Foreign Key in `stock` points to `part`, and a field in `part` depends on a model in `stock`), squashing one app will frequently trigger `CircularDependencyError`. Manually resolving these circular loops requires breaking the squashed migration into multiple files or carefully tweaking the `dependencies` list.
  - **Optimization Failures:** It cannot easily optimize custom `RunPython` or `RunSQL` data migrations.

---

### Methodology B: Clean Reset / "Clean Slate Boundary" (NetBox & Nautobot Style)
This is the pattern preferred by prominent Django-based open-source projects like NetBox (see NetBox issues [#6471](https://github.com/netbox-community/netbox/issues/6471) and [#13647](https://github.com/netbox-community/netbox/issues/13647)).

- **Mechanism:**
  1. Establish a **hard upgrade boundary** (e.g., *"Upgrading to version 4.0 requires first being fully migrated on version 3.x"*).
  2. Fully migrate a reference database to the boundary release.
  3. Delete *all* existing migration files across *all* apps.
  4. Run `python manage.py makemigrations` to generate brand-new, clean, fully-optimized initial migrations (`0001_initial.py`) for all apps from scratch.
  5. Any crucial startup custom data migrations are manually re-introduced or consolidated.
- **Pros:**
  - Complete eradication of historical migration bloat (reduces 650+ files to ~15 files).
  - Maximizes performance. Testing and CI time drop drastically (NetBox saw test/CI migration time decrease from 84 seconds to 21 seconds).
- **Cons:**
  - Breaks direct upgrades from releases older than the boundary release. Users on older releases *must* perform a two-step upgrade (Older -> Boundary Release -> New Release).

---

### Methodology C: Hybrid / Remake Migrations (Backwards-Compatible Reset)
This methodology combines the optimized output of a clean reset with the backwards-compatibility of the native `replaces` mechanism (inspired by tools like `django-remake-migrations`).

- **Mechanism:**
  1. Delete all existing migration files.
  2. Run `python manage.py makemigrations` to generate a brand-new, optimized set of migration files (`0001_initial.py`) based on the current model schemas.
  3. Inject a custom `replaces` list into each of the new initial migrations. This `replaces` list enumerates all the deleted historical migrations for that app.
- **Pros:**
  - Cleanest possible initial state (completely optimized schema representation).
  - Keeps backwards-compatibility intact. Fully migrated existing databases will not attempt to re-run the new initial files because they recognize that they "replace" the historical ones already recorded in their `django_migrations` table.
- **Cons:**
  - Requires careful handling of cross-app dependencies during the remake step.

---

## 3. Recommended Approach for InvenTree

Given that InvenTree requires **strict backwards-compatibility** (so existing running instances can upgrade seamlessly without data loss), we recommend **Methodology C (Hybrid Remake with `replaces`)** or a **Targeted Native Squash with custom helper scripts**.

For a highly robust, low-risk implementation, we propose:

1. **Step-by-Step Native / Hybrid Consolidation:**
   - Focus on the heaviest apps: `part` (153 migrations), `stock` (126 migrations), `order` (122 migrations), and `company` (80 migrations).
   - Use our helper tool (`migration_squasher.py`) to systematically identify linear chunks of migrations that do not contain inter-app cyclic dependencies.
   - Run Django's `squashmigrations` for these apps up to a stable milestone release.
   - For custom data migrations (`RunPython`), analyze their code:
     - Data migrations that perform data cleanup (e.g., `make_empty_email_field_null`, `backfill_user_profiles`) are *no-ops* on brand new database setups because no legacy data exists.
     - Data migrations that seed necessary static values or default settings (e.g., `set_default_currency`, setting up default units or parameters) are extracted and appended to the final squashed migration so they run during fresh installations.

2. **Guidelines for Custom `RunPython` Migrations during Squashing:**
   - When squashing, Django automatically copies `RunPython` operations into the squashed file.
   - Inspect the squashed file and identify functions that are no longer needed. You can safely replace them with `migrations.RunPython.noop` to skip processing on new setups.
   - If a function *is* required on a new setup, ensure its code is fully self-contained (does not import deleted models or rely on historical model states that no longer exist).

3. **Validation Workflow:**
   - Always run:
     ```bash
     python manage.py migrate --run-syncdb
     ```
     on a fresh database to ensure the new squashed migration chain constructs the tables successfully.
   - Compare the schema (e.g., `sqlite3 /tmp/db.sqlite3 .schema`) between a database migrated with the old migrations and one migrated with the squashed migrations. They should be structurally identical.
