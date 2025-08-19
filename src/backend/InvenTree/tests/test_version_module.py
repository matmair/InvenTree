"""Test suite for the version module in InvenTree backend."""

import os
import importlib
import types
from datetime import datetime as dt, timedelta as td

import sys

import pytest

# We import the module under test after preparing environment or monkeypatch as needed in tests
MODULE_PATH = "src.backend.InvenTree.InvenTree.test_version".replace("/", ".").replace("\\\\", ".")


def reload_module(monkeypatch, extra_patches=None):
    """Reload module under test with optional extra patches applied before import.

    Ensures top-level import side effects (e.g., dulwich presence) are stabilized.
    """
    if extra_patches:
        for func in extra_patches:
            func()
    # Remove from sys.modules to re-execute top-level code paths
    if MODULE_PATH in sys.modules:
        del sys.modules[MODULE_PATH]
    return importlib.import_module(MODULE_PATH)


class DummyCommit:
    """Dummy commit object for testing."""

    def __init__(self, hexstr="abcdef1234567", ts=1700000000, tz=0):
        """Initialize DummyCommit with hex string, timestamp, and timezone."""
        self._hex = hexstr
        self.commit_time = ts
        self.commit_timezone = tz

    def sha(self):
        """Return object with hexdigest method returning the hex string."""
        class _S:
            def __init__(self, h): self._h = h
            def hexdigest(self): return self._h
        return _S(self._hex)


def test_inventreeVersion_and_tuple_and_dev_detection(monkeypatch):
    """Test inventreeVersion, inventreeVersionTuple, and development detection."""
    # Force a specific SW version
    def patch_version():
        mod = types.SimpleNamespace()
        return mod
    mod = reload_module(monkeypatch)
    # Set to a development version
    mod.INVENTREE_SW_VERSION = "1.2.3 dev"
    assert mod.inventreeVersion() == "1.2.3 dev"
    assert mod.inventreeVersionTuple() == [1, 2, 3]
    assert mod.isInvenTreeDevelopmentVersion() is True

    # Set to a release version
    mod.INVENTREE_SW_VERSION = "2.10.0"
    assert mod.inventreeVersion() == "2.10.0"
    assert mod.inventreeVersionTuple() == [2, 10, 0]
    assert mod.isInvenTreeDevelopmentVersion() is False


def test_inventreeDocs_and_urls(monkeypatch):
    """Test inventreeDocsVersion, inventreeDocUrl, inventreeAppUrl, and inventreeGithubUrl."""
    mod = reload_module(monkeypatch)
    # Dev version -> docs "latest"
    mod.INVENTREE_SW_VERSION = "0.18.0 dev"
    assert mod.inventreeDocsVersion() == "latest"
    assert mod.inventreeDocUrl().endswith("/en/latest")

    # Release version -> returns exact version (no cover in code originally)
    mod.INVENTREE_SW_VERSION = "0.18.0"
    # inventreeDocsVersion will return INVENTREE_SW_VERSION
    assert mod.inventreeDocsVersion() == "0.18.0"
    assert mod.inventreeDocUrl().endswith("/en/0.18.0")

    # Static URLs
    assert mod.inventreeAppUrl() == "https://docs.inventree.org/app/"
    assert mod.inventreeGithubUrl() == "https://github.com/InvenTree/InvenTree/"


def test_checkMinPythonVersion_accepts_39_plus(monkeypatch, capsys):
    """Test checkMinPythonVersion accepts Python >= 3.9."""
    mod = reload_module(monkeypatch)
    # Simulate Python 3.11
    monkeypatch.setattr(sys, "version_info", types.SimpleNamespace(major=3, minor=11, micro=0))
    monkeypatch.setattr(sys, "version", "3.11.0 (main, Jan  1 2024, 00:00:00)")
    monkeypatch.setattr(sys, "executable", "/usr/bin/python3.11")
    # Should not raise
    mod.checkMinPythonVersion()
    out = capsys.readouterr().out
    assert "Python version 3.11.0" in out
    assert "/usr/bin/python3.11" in out


@pytest.mark.parametrize(
    "major,minor,should_raise",
    [
        (2, 7, True),   # Python2 -> raise
        (3, 8, True),   # 3.8 -> raise
        (3, 9, False),  # 3.9 -> ok
        (3, 10, False), # 3.10 -> ok
    ],
)
def test_checkMinPythonVersion_version_boundaries(monkeypatch, major, minor, should_raise):
    """Test checkMinPythonVersion raises or accepts based on version boundaries."""
    mod = reload_module(monkeypatch)
    monkeypatch.setattr(sys, "version_info", types.SimpleNamespace(major=major, minor=minor, micro=0))
    monkeypatch.setattr(sys, "version", f"{major}.{minor}.0 (mock)")
    monkeypatch.setattr(sys, "executable", "/usr/bin/pythonX")
    if should_raise:
        with pytest.raises(RuntimeError) as exc:
            mod.checkMinPythonVersion()
        assert "InvenTree requires Python 3.9 or above" in str(exc.value)
    else:
        mod.checkMinPythonVersion()  # no exception


def test_inventreeApiVersion_and_text_parsing(monkeypatch):
    """Test parse_version_text, inventreeApiText, and version data parsing."""
    # Patch API constants to a controlled small sample
    SAMPLE_TEXT = """
v3 -> 2024-06-01: https://github.com/InvenTree/InvenTree/releases/tag/v3
- Added endpoints for widgets
- Fixed bug A

v2 -> 2024-05-01: https://github.com/InvenTree/InvenTree/releases/tag/v2
- Improvements

v1
- Initial
""".lstrip("\n")

    def apply_patches():
        pass

    mod = reload_module(monkeypatch)
    # Set constants and re-parse
    mod.INVENTREE_API_VERSION = 3
    mod.INVENTREE_API_TEXT = SAMPLE_TEXT
    parsed = mod.parse_version_text()
    assert isinstance(parsed, dict)
    # v3 entry
    assert "v3" in parsed
    assert parsed["v3"]["version"] == "v3"
    assert parsed["v3"]["date"] == "2024-06-01"
    assert parsed["v3"]["gh"].startswith("https://github.com/")
    assert parsed["v3"]["latest"] is True  # latest should match current API version
    assert "- Added endpoints for widgets" in parsed["v3"]["text"][0]
    # v2 entry
    assert parsed["v2"]["date"] == "2024-05-01"
    assert parsed["v2"]["latest"] is False
    # v1 without details in header (date, gh)
    assert parsed["v1"]["date"] == ""
    assert parsed["v1"]["gh"] is None
    # Set preprocessed cache and fetch slices
    mod.INVENTREE_API_TEXT_DATA = parsed

    # Fetch default 10 versions from start_version computed as API_VERSION - versions + 1
    res = mod.inventreeApiText(versions=2)  # Given API_VERSION=3 -> start 2..3
    assert list(res.keys()) == ["v2", "v3"]
    assert res["v3"]["latest"] is True
    assert res["v2"]["latest"] is False

    # Explicit start version
    res2 = mod.inventreeApiText(versions=2, start_version=1)
    assert list(res2.keys()) == ["v1", "v2"]


def test_inventreePython_and_django_version(monkeypatch):
    """Test inventreeDjangoVersion and inventreePythonVersion."""
    mod = reload_module(monkeypatch)
    # Django version comes from django.get_version(); patch django module attribute
    class DummyDjango:
        @staticmethod
        def get_version():
            return "5.0.1"
    monkeypatch.setitem(sys.modules, "django", DummyDjango)
    # re-import to bind new django
    if MODULE_PATH in sys.modules:
        del sys.modules[MODULE_PATH]
    mod = importlib.import_module(MODULE_PATH)

    assert mod.inventreeDjangoVersion() == "5.0.1"
    # python version is split off first token
    monkeypatch.setattr(sys, "version", "3.12.2 (main...)")
    assert mod.inventreePythonVersion() == "3.12.2"


def test_commit_hash_branch_date_from_env(monkeypatch):
    """Test inventreeCommitHash, inventreeCommitDate, and inventreeBranch with env and DummyCommit."""
    mod = reload_module(monkeypatch)

    # Env overrides should take precedence
    monkeypatch.setenv("INVENTREE_COMMIT_HASH", "1234abc")
    monkeypatch.setenv("INVENTREE_COMMIT_DATE", "2024-07-04 12:00:00")
    monkeypatch.setenv("INVENTREE_PKG_BRANCH", "feature/x")
    assert mod.inventreeCommitHash() == "1234abc"
    assert mod.inventreeCommitDate() == "2024-07-04"
    assert mod.inventreeBranch() == "feature/x"

    # Clear env and simulate no dulwich (main_commit / main_branch None)
    monkeypatch.delenv("INVENTREE_COMMIT_HASH", raising=False)
    monkeypatch.delenv("INVENTREE_COMMIT_DATE", raising=False)
    monkeypatch.delenv("INVENTREE_PKG_BRANCH", raising=False)
    mod.main_commit = None
    mod.main_branch = None
    assert mod.inventreeCommitHash() is None
    assert mod.inventreeCommitDate() is None
    assert mod.inventreeBranch() is None

    # Provide dummy commit/branch
    mod.main_commit = DummyCommit("deadbeefcafeee", ts=1710000000, tz=0)
    # main_branch is expected bytes
    mod.main_branch = b"main"
    assert mod.inventreeCommitHash() == "deadbee"  # first 7 chars
    # commit_date is derived from timestamp + timezone
    expected_date = str((dt.fromtimestamp(1710000000) + td(seconds=0)).date())
    assert mod.inventreeCommitDate() == expected_date
    assert mod.inventreeBranch() == "main"


def test_inventreeTarget_and_platform(monkeypatch):
    """Test inventreeTarget and inventreePlatform."""
    mod = reload_module(monkeypatch)
    # Target from env or None
    monkeypatch.delenv("INVENTREE_PKG_TARGET", raising=False)
    assert mod.inventreeTarget() is None

    monkeypatch.setenv("INVENTREE_PKG_TARGET", "linux/amd64")
    assert mod.inventreeTarget() == "linux/amd64"

    # Platform delegates to platform.platform(aliased=True) - mock
    class DPlat:
        @staticmethod
        def platform(aliased=False):  # signature compatibility
            assert aliased is True
            return "Linux-6.8.0-x86_64-with-glibc2.39"
    monkeypatch.setitem(sys.modules, "platform", DPlat)
    if MODULE_PATH in sys.modules:
        del sys.modules[MODULE_PATH]
    mod = importlib.import_module(MODULE_PATH)
    assert mod.inventreePlatform() == "Linux-6.8.0-x86_64-with-glibc2.39"


def test_inventreeDatabase_reads_settings(monkeypatch):
    """Test inventreeDatabase reads DB_ENGINE from django settings."""
    # Mock django.conf.settings object to carry DB_ENGINE
    class DummySettings:
        DB_ENGINE = "postgresql"
    class DummyConf:
        settings = DummySettings
    # Inject django.conf.settings before import
    dummy_django = types.SimpleNamespace(conf=DummyConf, get_version=lambda: "5.0.0")
    monkeypatch.setitem(sys.modules, "django", dummy_django)
    if MODULE_PATH in sys.modules:
        del sys.modules[MODULE_PATH]
    mod = importlib.import_module(MODULE_PATH)

    assert mod.inventreeDatabase() == "postgresql"


def test_inventree_identifier_logic(monkeypatch):
    """Test inventree_identifier, inventreeInstanceName, and inventreeInstanceTitle logic."""
    mod = reload_module(monkeypatch)

    # Simulate common.settings.get_global_setting without importing real module
    # We monkeypatch the function the module imports in the function scope by injecting a module
    # named common.settings that provides get_global_setting.
    calls = {"args": []}
    def fake_get_global_setting(key, *args, **kwargs):
        calls["args"].append((key, args, kwargs))
        # Provide behavior depending on key
        if key == "INVENTREE_ANNOUNCE_ID":
            # Only true if env key present
            return kwargs.get("enviroment_key") == "INVENTREE_ANNOUNCE_ID" and os.getenv("INVENTREE_ANNOUNCE_ID") == "1"
        if key == "INVENTREE_INSTANCE_ID":
            return "instance-xyz"
        if key == "INVENTREE_INSTANCE":
            return "MyInstance"
        if key == "INVENTREE_INSTANCE_TITLE":
            return ""
        return None

    common_pkg = types.ModuleType("common")
    settings_mod = types.ModuleType("common.settings")
    settings_mod.get_global_setting = fake_get_global_setting

    monkeypatch.setitem(sys.modules, "common", common_pkg)
    monkeypatch.setitem(sys.modules, "common.settings", settings_mod)

    # No env -> announce flag False -> None
    monkeypatch.delenv("INVENTREE_ANNOUNCE_ID", raising=False)
    assert mod.inventree_identifier() is None

    # With override -> always returns instance id
    assert mod.inventree_identifier(override_announce=True) == "instance-xyz"

    # With env var -> announce true -> returns instance id
    monkeypatch.setenv("INVENTREE_ANNOUNCE_ID", "1")
    assert mod.inventree_identifier() == "instance-xyz"

    # Also validate instance name and title helpers
    assert mod.inventreeInstanceName() == "MyInstance"
    # INVENTREE_INSTANCE_TITLE empty -> default "InvenTree"
    assert mod.inventreeInstanceTitle() == "InvenTree"

    # If a title is present, function returns the instance name
    def fake_get_global_setting_title(key, *args, **kwargs):
        if key == "INVENTREE_INSTANCE_TITLE":
            return "ShownTitle"
        if key == "INVENTREE_INSTANCE":
            return "NameFromInstance"
        if key == "INVENTREE_ANNOUNCE_ID":
            return False
        if key == "INVENTREE_INSTANCE_ID":
            return "instance-xyz"
        return None
    settings_mod.get_global_setting = fake_get_global_setting_title
    assert mod.inventreeInstanceTitle() == "NameFromInstance"


def test_isInvenTreeUpToDate(monkeypatch):
    """Test isInvenTreeUpToDate behavior with global setting."""
    mod = reload_module(monkeypatch)

    # Patch get_global_setting
    def ggs(key, backup_value=None, create=True, **kwargs):
        assert key == "_INVENTREE_LATEST_VERSION"
        return None  # simulate absence -> must return True
    common_pkg = types.ModuleType("common")
    settings_mod = types.ModuleType("common.settings")
    settings_mod.get_global_setting = ggs
    monkeypatch.setitem(sys.modules, "common", common_pkg)
    monkeypatch.setitem(sys.modules, "common.settings", settings_mod)
    # Must assume up-to-date if no record
    assert mod.isInvenTreeUpToDate() is True

    # Provide an older latest version to compare tuples
    def ggs2(key, backup_value=None, create=True, **kwargs):
        return "0.1.0"
    settings_mod.get_global_setting = ggs2
    # With SW version 0.2.0, >= 0.1.0 -> True
    mod.INVENTREE_SW_VERSION = "0.2.0"
    assert mod.isInvenTreeUpToDate() is True

    # Provide higher latest version
    def ggs3(key, backup_value=None, create=True, **kwargs):
        return "9.9.9"
    settings_mod.get_global_setting = ggs3
    mod.INVENTREE_SW_VERSION = "1.0.0"
    # inventree_version (1,0,0) >= latest (9,9,9) -> False
    # The comparison is in a no-cover path originally; still exercise it here.
    assert mod.isInvenTreeUpToDate() is False