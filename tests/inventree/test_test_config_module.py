"""Unit tests for InvenTree.test_config helper functions.

Testing framework: pytest (prefer pytest-django if repository provides it).
These tests exercise pure functions, env/config resolution, and filesystem helpers.
Django-dependent helpers are exercised via monkeypatching to avoid requiring a full Django runtime.
"""

import os
import sys
import types
import logging
from pathlib import Path
from contextlib import contextmanager

import pytest

# Import the module under test
# The module path is src/backend/InvenTree/InvenTree/test_config.py
# Ensure import path includes "src/backend" so "InvenTree" package can be resolved in tests.
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_BACKEND = REPO_ROOT / "src" / "backend"
if str(SRC_BACKEND) not in sys.path:
    sys.path.insert(0, str(SRC_BACKEND))

from InvenTree import test_config as tc

@contextmanager
def environ(environ_overrides: dict):
    """Temporarily set environment variables within a 'with' block."""
    old_environ = os.environ.copy()
    try:
        os.environ.update({k: str(v) for k, v in environ_overrides.items()})
        yield
    finally:
        # Restore exact previous state
        os.environ.clear()
        os.environ.update(old_environ)

def test_to_list_basic_and_tuple():
    """Test to_list with basic inputs and tuple handling."""
    assert tc.to_list(["a", "b"]) == ["a", "b"]
    assert tc.to_list(("a", "b")) == ("a", "b")
    assert tc.to_list("a,b") == ["a", "b"]
    assert tc.to_list(" a , b , c ") == ["a", "b", "c"]
    # Custom delimiter
    assert tc.to_list("a|b|c", delimiter="|") == ["a", "b", "c"]
    # Non-string values should be coerced then split
    assert tc.to_list(123) == ["123"]

def test_to_dict_handles_none_and_dict_and_json(caplog):
    """Test to_dict with None, dict, valid and invalid JSON strings."""
    assert tc.to_dict(None) == {}
    src = {"x": 1}
    assert tc.to_dict(src) is src
    assert tc.to_dict('{"a": 5, "b": [1,2]}') == {"a": 5, "b": [1, 2]}
    # Invalid JSON logs exception and returns {}
    caplog.set_level(logging.ERROR, logger="inventree")
    assert tc.to_dict("{not json}") == {}
    # Ensure an exception log record was produced
    assert any("Failed to parse value" in rec.getMessage() for rec in caplog.records)

@pytest.mark.parametrize(
    "value,expect",
    [
        ("1", True),
        ("Y", True),
        ("yes", True),
        ("t", True),
        ("true", True),
        ("on", True),
        ("0", False),
        ("n", False),
        ("false", False),
        ("off", False),
        ("", False),
        (None, False),
    ],
)
def test_is_true_matrix(value, expect):
    """Test is_true function with various truthy and falsy string values."""
    assert tc.is_true(value) is expect

def test_get_base_and_root_dirs_exist():
    """Test that base and root directories exist and base is inside root."""
    base = tc.get_base_dir()
    root = tc.get_root_dir()
    assert base.exists() and base.is_dir()
    assert root.exists() and root.is_dir()
    # base should be inside root (heuristic)
    assert str(base).startswith(str(root))

def test_do_typecast_list_and_dict_and_numeric(caplog):
    """Test do_typecast function for list, dict, and numeric types, and error logging."""
    assert tc.do_typecast("a,b,c", list) == ["a", "b", "c"]
    assert tc.do_typecast('{"a": 1}', dict) == {"a": 1}
    assert tc.do_typecast("5", int) == 5
    assert tc.do_typecast("3.14", float) == pytest.approx(3.14)
    # Failed cast returns original and logs if var_name provided
    caplog.set_level(logging.ERROR, logger="inventree")
    val = tc.do_typecast("abc", int, var_name="TEST_VAR")
    assert val == "abc"
    assert any("Failed to typecast" in rec.getMessage() for rec in caplog.records)

def write_yaml(path: Path, data: dict):
    """Write a dictionary to a YAML file at the given path."""
    import yaml
    text = yaml.safe_dump(data)
    path.write_text(text, encoding="utf-8")

def test_get_setting_precedence_env_over_yaml(tmp_path, monkeypatch):
    """Test get_setting prioritizes environment variables over YAML config."""
    # Prepare a temp config directory and file
    conf_dir = tmp_path / "config"
    conf_dir.mkdir(parents=True, exist_ok=True)
    cfg = conf_dir / "config.yaml"
    write_yaml(cfg, {"section": {"value": "from_yaml"}, "plain": "yaml_plain"})

    # Monkeypatch config dir and base dir lookups
    monkeypatch.setenv("INVENTREE_CONFIG_FILE", str(cfg))

    # Ensure cache is cleared
    tc.CONFIG_DATA = None
    tc.CONFIG_LOOKUPS.clear()

    # No env var -> fallback to YAML
    v1 = tc.get_setting(env_var="ENV_ONLY", config_key="section.value", default_value="default")
    assert v1 == "from_yaml"
    assert tc.CONFIG_LOOKUPS["ENV_ONLY"]["source"] == "yaml"

    # With env var -> env takes precedence and is typecasted if requested
    with environ({"ENV_ONLY": "42"}):
        v2 = tc.get_setting(env_var="ENV_ONLY", config_key="section.value", default_value="default", typecast=int)
    assert v2 == 42
    assert tc.CONFIG_LOOKUPS["ENV_ONLY"]["source"] == "env"

    # Missing everywhere -> default with typecast
    v3 = tc.get_setting(env_var="MISSING_ENV", config_key="missing.key", default_value="1,2,3", typecast=list)
    assert v3 == ["1", "2", "3"]
    assert tc.CONFIG_LOOKUPS["MISSING_ENV"]["source"] == "default"

def test_get_boolean_setting_uses_is_true(monkeypatch, tmp_path):
    """Test get_boolean_setting returns boolean values using is_true."""
    cfg = tmp_path / "config.yaml"
    write_yaml(cfg, {"feature": {"enabled": "yes"}})
    monkeypatch.setenv("INVENTREE_CONFIG_FILE", str(cfg))
    # from YAML
    assert tc.get_boolean_setting(config_key="feature.enabled") is True
    # from ENV
    with environ({"FEATURE_FLAG": "0"}):
        assert tc.get_boolean_setting(env_var="FEATURE_FLAG", default_value=True) is False

def test_get_media_static_backup_dirs_create_and_error(tmp_path, monkeypatch):
    """Test get_media_dir, get_static_dir, and get_backup_dir creation and error behavior."""
    # Point settings to temporary paths
    media = tmp_path / "m"
    static = tmp_path / "s"
    backup = tmp_path / "b"
    with environ(
        {
            "INVENTREE_MEDIA_ROOT": str(media),
            "INVENTREE_STATIC_ROOT": str(static),
            "INVENTREE_BACKUP_DIR": str(backup),
        }
    ):
        md = tc.get_media_dir(create=True)
        sd = tc.get_static_dir(create=True)
        bd = tc.get_backup_dir(create=True)

    assert md == media.resolve() and md.exists()
    assert sd == static.resolve() and sd.exists()
    assert bd == backup.resolve() and bd.exists()

    # Missing env with error=False returns None; with error=True raises
    with environ({"INVENTREE_MEDIA_ROOT": ""}):
        assert tc.get_media_dir(create=False, error=False) is None
        with pytest.raises(FileNotFoundError):
            tc.get_media_dir(create=False, error=True)

    with environ({"INVENTREE_STATIC_ROOT": ""}):
        assert tc.get_static_dir(create=False, error=False) is None
        with pytest.raises(FileNotFoundError):
            tc.get_static_dir(create=False, error=True)

    with environ({"INVENTREE_BACKUP_DIR": ""}):
        assert tc.get_backup_dir(create=False, error=False) is None
        with pytest.raises(FileNotFoundError):
            tc.get_backup_dir(create=False, error=True)

def test_get_config_file_prefers_env_and_creates_from_template(tmp_path, monkeypatch, capsys):
    """Test get_config_file respects env var and creates config file from template."""
    # Create a fake base dir and template
    # We monkeypatch get_base_dir and get_config_dir to our tmp paths
    fake_base = tmp_path / "base"
    fake_conf = tmp_path / "conf"
    (fake_base / "InvenTree").mkdir(parents=True, exist_ok=True)
    fake_conf.mkdir(parents=True, exist_ok=True)

    # Provide a template file
    template = fake_base / "config_template.yaml"
    template.write_text("key: default", encoding="utf-8")

    monkeypatch.setattr(tc, "get_base_dir", lambda: fake_base)
    monkeypatch.setattr(tc, "get_config_dir", lambda: fake_conf)

    # Case 1: Explicit env path used; since it doesn't exist and create=True, it should be created from template
    env_cfg = fake_conf / "custom.yaml"
    with environ({"INVENTREE_CONFIG_FILE": str(env_cfg)}):
        path = tc.get_config_file(create=True)
    assert path == env_cfg.resolve()
    # Should have been created from template
    assert path.exists()
    assert "key: default" in path.read_text()

    # Case 2: No env provided; default under config dir
    os.environ.pop("INVENTREE_CONFIG_FILE", None)
    # Remove existing config.yaml to force creation
    default_cfg = fake_conf / "config.yaml"
    if default_cfg.exists():
        default_cfg.unlink()
    path2 = tc.get_config_file(create=True)
    assert path2 == default_cfg.resolve()
    assert default_cfg.exists()

    # Standard output printed creation notices
    out = capsys.readouterr().out
    assert "InvenTree configuration file 'config.yaml' not found - creating default file" in out
    assert "Created config file" in out

def test_load_config_data_caching(tmp_path, monkeypatch):
    """Test load_config_data caching behavior with set_cache flag."""
    cfg = tmp_path / "config.yaml"
    write_yaml(cfg, {"x": {"y": 7}})

    # Point get_config_file to our path
    monkeypatch.setenv("INVENTREE_CONFIG_FILE", str(cfg))

    # No cache initially
    tc.CONFIG_DATA = None
    d1 = tc.load_config_data(set_cache=False)
    assert d1 == {"x": {"y": 7}}
    # Set cache
    d2 = tc.load_config_data(set_cache=True)
    assert d2 == {"x": {"y": 7}}
    # Ensure subsequent call without set_cache picks up cached instance (by identity or equality)
    d3 = tc.load_config_data(set_cache=False)
    assert d3 == {"x": {"y": 7}}
    # Changing file should not impact cached data unless set_cache=True
    write_yaml(cfg, {"x": {"y": 9}})
    d4 = tc.load_config_data(set_cache=False)
    assert d4 == {"x": {"y": 7}}  # still old since cached
    d5 = tc.load_config_data(set_cache=True)
    assert d5 == {"x": {"y": 9}}

def test_get_constraint_file_creates_when_missing(tmp_path, monkeypatch, caplog):
    """Test get_constraint_file creates constraints file when missing and respects force_write."""
    # Prepare a fake base dir with InvenTree subdir for constraint file location
    fake_base = tmp_path / "base"
    target_dir = fake_base / "InvenTree"
    target_dir.mkdir(parents=True, exist_ok=True)

    # Monkeypatch get_base_dir and version constants
    monkeypatch.setattr(tc, "get_base_dir", lambda: fake_base)

    # Provide a fake version module attributes via monkeypatching import in tc.get_constraint_file
    class FakeVersionModule(types.SimpleNamespace):
        INVENTREE_SW_VERSION = "1.2.3"
        INVENTREE_SW_NXT_MAJOR = "2.0"

    # Inject into sys.modules so from .version import ... resolves
    pkg_mod = sys.modules.get("InvenTree")
    if pkg_mod is None:
        sys.modules["InvenTree"] = types.ModuleType("InvenTree")
    sys.modules["InvenTree.version"] = types.ModuleType("InvenTree.version")
    sys.modules["InvenTree.version"].INVENTREE_SW_VERSION = "1.2.3"
    sys.modules["InvenTree.version"].INVENTREE_SW_NXT_MAJOR = "2.0"

    caplog.set_level(logging.WARNING, logger="inventree")

    const_path = tc.get_constraint_file(force_write=False)
    assert Path(const_path).exists()
    text = Path(const_path).read_text()
    assert "# InvenTree constraints file" in text
    # Ensure it formatted the package constraint line with the version range
    assert "inventree-server~=1.2.3,<2.0" in text.replace(" ", "")

    # It should have warned because the file did not exist and force_write=False
    assert any("Constraint file does not exist" in rec.getMessage() for rec in caplog.records)

    # Calling again should return existing path without re-writing content
    caplog.clear()
    const_path2 = tc.get_constraint_file(force_write=False)
    assert const_path2 == const_path
    assert len(caplog.records) == 0

    # Force write should re-create/overwrite
    Path(const_path).unlink()
    const_path3 = tc.get_constraint_file(force_write=True)
    assert Path(const_path3).exists()

def test_get_secret_key_env_and_file_generation(tmp_path, monkeypatch, caplog):
    """Test get_secret_key returns env value, reads from file, or generates new key."""
    caplog.set_level(logging.INFO, logger="inventree")
    # Env var present -> returns the value directly
    with environ({"INVENTREE_SECRET_KEY": "supersecret"}):
        assert tc.get_secret_key() == "supersecret"

    # Env var for file path takes precedence over default locations
    key_file = tmp_path / "key.txt"
    key_file.write_text("fromfile", encoding="utf-8")
    with environ({"INVENTREE_SECRET_KEY_FILE": str(key_file)}):
        assert tc.get_secret_key() == "fromfile"
        # return_path returns a Path
        assert tc.get_secret_key(return_path=True) == key_file.resolve()

    # No envs -> create in default config dir
    fake_base = tmp_path / "base"
    fake_conf = tmp_path / "conf"
    (fake_base / "InvenTree").mkdir(parents=True, exist_ok=True)
    fake_conf.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(tc, "get_base_dir", lambda: fake_base)
    monkeypatch.setattr(tc, "get_config_dir", lambda: fake_conf)

    # Remove envs
    os.environ.pop("INVENTREE_SECRET_KEY", None)
    os.environ.pop("INVENTREE_SECRET_KEY_FILE", None)

    # Trigger generation
    path = tc.get_secret_key(return_path=True)
    assert isinstance(path, Path)
    assert path.exists()
    content = tc.get_secret_key()
    assert isinstance(content, str)
    assert content.strip() != ""

def test_get_oidc_private_key_env_and_generate(tmp_path, monkeypatch):
    """Test get_oidc_private_key returns env raw key, reads from file, or generates new key."""
    # Raw key in env
    with environ({"INVENTREE_OIDC_PRIVATE_KEY": "RAW_RSA"}):
        assert tc.get_oidc_private_key() == "RAW_RSA"

    # Use provided path via env
    pem = tmp_path / "oidc.pem"
    pem.write_text("PEM_CONTENT", encoding="utf-8")
    with environ({"INVENTREE_OIDC_PRIVATE_KEY_FILE": str(pem)}):
        assert tc.get_oidc_private_key(return_path=False) == "PEM_CONTENT"
        assert tc.get_oidc_private_key(return_path=True) == pem.resolve()

    # No env; generate at default config dir if missing
    fake_conf = tmp_path / "conf"
    fake_conf.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(tc, "get_config_dir", lambda: fake_conf)
    # Ensure no old default file exists in base dir
    fake_base = tmp_path / "base"
    (fake_base / "InvenTree").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(tc, "get_base_dir", lambda: fake_base)

    # Remove envs
    os.environ.pop("INVENTREE_OIDC_PRIVATE_KEY", None)
    os.environ.pop("INVENTREE_OIDC_PRIVATE_KEY_FILE", None)

    key_text = tc.get_oidc_private_key(return_path=False)
    assert "BEGIN RSA PRIVATE KEY" in key_text
    key_path = tc.get_oidc_private_key(return_path=True)
    assert isinstance(key_path, Path)
    assert key_path.exists()

def test_get_frontend_settings_defaults_and_overrides(monkeypatch, tmp_path):
    """Test get_frontend_settings default values and config overrides."""
    # Minimal: no env/config -> defaults + debug true
    tc.CONFIG_DATA = None
    tc.CONFIG_LOOKUPS.clear()
    # Point to a simple config with no frontend_settings
    cfg = tmp_path / "config.yaml"
    write_yaml(cfg, {})
    monkeypatch.setenv("INVENTREE_CONFIG_FILE", str(cfg))

    s = tc.get_frontend_settings(debug=True)
    # Ensure required defaults
    assert s["debug"] is True
    assert s["environment"] == "development"
    assert s["show_server_selector"] is True
    assert "server_list" in s
    assert isinstance(s["server_list"], list)
    # base_url default
    assert s["base_url"] in ("web", "/web/", "web/")

    # Provide overrides via dict in config
    cfg2 = tmp_path / "config2.yaml"
    write_yaml(
        cfg2,
        {
            "frontend_settings": {
                "debug": False,  # should be overwritten by argument
                "api_host": "http://api.example",
                "server_list": [{"id": 1}],
                "url_compatibility": "not_a_bool",  # coerced to True via exception handling
            }
        },
    )
    monkeypatch.setenv("INVENTREE_CONFIG_FILE", str(cfg2))
    s2 = tc.get_frontend_settings(debug=False)
    assert s2["debug"] is False
    assert s2["environment"] == "production"
    assert s2["api_host"] == "http://api.example"
    assert s2["server_list"] == [{"id": 1}]
    assert s2["url_compatibility"] is True

def test_check_config_dir_warns_and_sets_global_warning(tmp_path, caplog, monkeypatch):
    """Test check_config_dir warns and sets global warning for uncommon config directory."""
    # Put config in a tmp dir different from the recommended directory
    recommended = tmp_path / "recommended"
    elsewhere = tmp_path / "elsewhere"
    recommended.mkdir(parents=True, exist_ok=True)
    elsewhere.mkdir(parents=True, exist_ok=True)
    file_path = elsewhere / "config.yaml"
    file_path.write_text("x: 1", encoding="utf-8")

    # Simulate get_config_dir to be recommended
    monkeypatch.setattr(tc, "get_config_dir", lambda: recommended)

    # Provide a dummy common.settings.set_global_warning
    fake_common = types.ModuleType("common")
    fake_settings = types.ModuleType("common.settings")

    class GlobalWarningCode:
        UNCOMMON_CONFIG = "UNCOMMON_CONFIG"

    calls = {}

    def set_global_warning(code, payload):
        calls["code"] = code
        calls["payload"] = payload

    fake_settings.GlobalWarningCode = GlobalWarningCode
    fake_settings.set_global_warning = set_global_warning
    fake_common.settings = fake_settings
    sys.modules["common"] = fake_common
    sys.modules["common.settings"] = fake_settings

    caplog.set_level(logging.WARNING, logger="inventree")

    tc.check_config_dir("INVENTREE_CONFIG_FILE", file_path, config_dir=None)

    # Should warn
    assert any("INVE-W10" in rec.getMessage() for rec in caplog.records)
    # Should invoke set_global_warning with recommended path
    assert calls.get("code") == "UNCOMMON_CONFIG"
    assert calls.get("payload", {}).get("path") == str(recommended)

def test_ensure_dir_with_default_filesystem(tmp_path):
    """Test ensure_dir creates directories idempotently."""
    # New directory created
    target = tmp_path / "nested" / "dir"
    assert not target.exists()
    tc.ensure_dir(target)
    assert target.exists() and target.is_dir()
    # Calling again should be idempotent
    tc.ensure_dir(target)
    assert target.exists()

def test_get_config_dir_by_installer_env(monkeypatch):
    """Test get_config_dir returns correct paths for different installer environments."""
    # inventreeInstaller returns indicators based on env variables
    with environ({"INVENTREE_DOCKER": "true"}):
        assert str(tc.get_config_dir()) == "/home/inventree/data"
    with environ({"INVENTREE_DEVCONTAINER": "true"}):
        assert str(tc.get_config_dir()) == "/home/inventree/dev"
    with environ({"INVENTREE_PKG_INSTALLER": "PKG"}):
        assert str(tc.get_config_dir()) == "/etc/inventree"

    # Fallback to project config directory under root if none matched
    os.environ.pop("INVENTREE_DOCKER", None)
    os.environ.pop("INVENTREE_DEVCONTAINER", None)
    os.environ.pop("INVENTREE_PKG_INSTALLER", None)
    # get_root_dir may vary; just assert it ends with /config
    p = tc.get_config_dir()
    assert p.name == "config"

def test_get_custom_file_static_and_media_resolution(monkeypatch, caplog):
    """Test get_custom_file resolves files from static and media storage."""
    # Avoid importing Django by providing fake modules in sys.modules
    # Fake StaticFilesStorage with exists method
    class FakeStatic:
        def __init__(self, existing):
            self._existing = set(existing)

        def exists(self, path):
            return path in self._existing

    # Fake default_storage with exists method
    class FakeDefaultStorage:
        def __init__(self, existing):
            self._existing = set(existing)

        def exists(self, path):
            return path in self._existing

    # Inject fake modules and names
    fake_django_contrib_staticfiles_storage = types.ModuleType(
        "django.contrib.staticfiles.storage"
    )
    fake_django_contrib_staticfiles_storage.StaticFilesStorage = lambda: FakeStatic(
        {"static/file.css"}
    )

    fake_django_core_files_storage = types.ModuleType("django.core.files.storage")
    fake_django_core_files_storage.default_storage = FakeDefaultStorage(
        {"media/file.css"}
    )

    sys.modules["django.contrib"] = types.ModuleType("django.contrib")
    sys.modules["django.contrib.staticfiles"] = types.ModuleType(
        "django.contrib.staticfiles"
    )
    sys.modules["django.contrib.staticfiles.storage"] = (
        fake_django_contrib_staticfiles_storage
    )
    sys.modules["django.core"] = types.ModuleType("django.core")
    sys.modules["django.core.files"] = types.ModuleType("django.core.files")
    sys.modules["django.core.files.storage"] = fake_django_core_files_storage

    caplog.set_level(logging.INFO, logger="inventree")

    # Case 1: found in static
    v1 = tc.get_custom_file("ENV", "CONF", "asset", lookup_media=True)
    # By default get_setting returns None when not provided, so provide value via env
    with environ({"ENV": "static/file.css"}):
        v1 = tc.get_custom_file("ENV", "CONF", "asset", lookup_media=True)
    assert v1 == "static/file.css"
    assert any("Loading asset from static directory" in rec.getMessage() for rec in caplog.records)

    caplog.clear()
    # Case 2: found in media when lookup_media=True
    with environ({"ENV": "media/file.css"}):
        v2 = tc.get_custom_file("ENV", "CONF", "asset", lookup_media=True)
    assert v2 == "media/file.css"
    assert any("Loading asset from media directory" in rec.getMessage() for rec in caplog.records)

    caplog.clear()
    # Case 3: missing -> warning and returns Falsey value
    with environ({"ENV": "not/found.css"}):
        v3 = tc.get_custom_file("ENV", "CONF", "asset", lookup_media=False)
    assert v3 is False
    assert any("could not be found" in rec.getMessage() for rec in caplog.records)

def test_get_plugin_file_creates_when_missing(tmp_path, monkeypatch, caplog):
    """Test get_plugin_file creates plugin file when missing or uses env path."""
    caplog.set_level(logging.WARNING, logger="inventree")
    # Point config file to a tmp dir; plugin file should be created next to it
    cfg = tmp_path / "config.yaml"
    cfg.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("INVENTREE_CONFIG_FILE", str(cfg))

    # No env for plugin file -> default to config dir/plugins.txt
    plugin_path = tc.get_plugin_file()
    assert isinstance(plugin_path, Path)
    assert plugin_path.exists()
    text = plugin_path.read_text()
    assert "InvenTree Plugins" in text

    # Provide explicit path via env
    caplog.clear()
    explicit = tmp_path / "custom_plugins.txt"
    with environ({"INVENTREE_PLUGIN_FILE": str(explicit)}):
        p2 = tc.get_plugin_file()
        assert p2 == explicit
        assert p2.exists()
    # Verify warnings were issued in first path (creation)
    assert any("Plugin configuration file does not exist" in rec.getMessage() for rec in caplog.records)

def test_get_plugin_dir_returns_setting_from_env_or_config(tmp_path, monkeypatch):
    """Test get_plugin_dir returns plugin directory from environment or config."""
    # Via env
    with environ({"INVENTREE_PLUGIN_DIR": "/tmp/plugins"}):
        assert tc.get_plugin_dir() == "/tmp/plugins"
    # Via config file
    cfg = tmp_path / "config.yaml"
    write_yaml(cfg, {"plugin_dir": "/var/plugins"})
    monkeypatch.setenv("INVENTREE_CONFIG_FILE", str(cfg))
    os.environ.pop("INVENTREE_PLUGIN_DIR", None)
    assert tc.get_plugin_dir() == "/var/plugins"