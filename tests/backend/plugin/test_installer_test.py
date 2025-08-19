"""Tests for the InvenTree plugin test_installer module."""
import re
import sys
import types
from pathlib import Path

import pytest

# Import the module under test
# The module is named "test_installer" but it is not itself a test; it's a production module.
from InvenTree.plugin import test_installer as installer


try:
    # If pytest-django is present, a 'settings' fixture will be available.
    HAVE_DJANGO_SETTINGS_FIXTURE = True
except Exception:
    HAVE_DJANGO_SETTINGS_FIXTURE = False


class DummyUser:
    """Dummy user with is_staff attribute for testing."""

    def __init__(self, is_staff: bool):
        """Initialize DummyUser with staff flag."""
        self.is_staff = is_staff


class DummyPluginConfig:
    """Dummy plugin configuration to simulate plugin settings."""

    def __init__(
        self,
        key: str = "dummy",
        active: bool = False,
        package_name: str = "dummy-plugin",
        is_package: bool = True,
        installed: bool = True,
        mandatory: bool = False,
        sample: bool = False,
        builtin: bool = False,
    ):
        """Initialize DummyPluginConfig with optional parameters."""
        self.key = key
        self.active = active
        self.package_name = package_name
        self._is_package = is_package
        self._installed = installed
        self._mandatory = mandatory
        self._sample = sample
        self._builtin = builtin

    # These reflect the plugin.models.PluginConfig interface used by uninstall logic

    def is_package(self):
        """Return True if plugin is a package."""
        return self._is_package

    def is_installed(self):
        """Return True if plugin is installed."""
        return self._installed

    def is_mandatory(self):
        """Return True if plugin is mandatory."""
        return self._mandatory

    def is_sample(self):
        """Return True if plugin is a sample."""
        return self._sample

    def is_builtin(self):
        """Return True if plugin is built-in."""
        return self._builtin

    def delete(self):
        """Simulate deletion; mark as deleted."""
        self._deleted = True


@pytest.fixture
def fake_settings(tmp_path, monkeypatch):
    """Provide a minimal settings object/namespace sufficient for the module's usage.

    - BASE_DIR.parent for pip_command cwd
    - PLUGIN_FILE path used by plugins file functions
    - PLUGINS_INSTALL_DISABLED flag gates install/uninstall.
    """
    class _Settings:
        def __init__(self):
            self.BASE_DIR = tmp_path / "src"
            self.BASE_DIR.mkdir(parents=True, exist_ok=True)
            self.PLUGIN_FILE = tmp_path / "plugins.txt"
            self.PLUGINS_INSTALL_DISABLED = False

    s = _Settings()

    # Patch django.conf.settings
    from types import SimpleNamespace

    django_settings = SimpleNamespace(
        BASE_DIR=s.BASE_DIR,
        PLUGIN_FILE=s.PLUGIN_FILE,
        PLUGINS_INSTALL_DISABLED=s.PLUGINS_INSTALL_DISABLED,
    )
    # Inject into module import path for django.conf.settings usage
    # We monkeypatch the settings used inside the module under test
    monkeypatch.setattr(installer, "settings", django_settings, raising=True)
    return django_settings


@pytest.fixture
def mock_log_error(monkeypatch):
    """Provide a list to capture log_error calls."""
    calls = []

    def _log_error(path: str, scope: str = ""):
        calls.append((path, scope))

    monkeypatch.setattr(installer, "log_error", _log_error, raising=True)
    return calls


@pytest.fixture
def mock_staticfiles(monkeypatch):
    """Provide hooks to capture staticfiles plugin collect and clear calls."""
    calls = {"collect": 0, "clear": []}

    class _Static:
        @staticmethod
        def collect_plugins_static_files():
            calls["collect"] += 1

        @staticmethod
        def clear_plugin_static_files(key):
            calls["clear"].append(key)

    monkeypatch.setattr(installer, "plugin", types.SimpleNamespace(staticfiles=_Static), raising=False)
    return calls


@pytest.fixture
def mock_registry(monkeypatch):
    """Provide a dummy plugin registry to capture reload calls."""
    calls = {"reload": []}

    class _Registry:
        @staticmethod
        def reload_plugins(full_reload=False, force_reload=False, collect=False):
            calls["reload"].append((full_reload, force_reload, collect))

    # The code performs: from plugin.registry import registry
    # We monkeypatch the import path by creating a dummy module and attribute.
    registry_module = types.SimpleNamespace(registry=_Registry())
    sys.modules["plugin.registry"] = registry_module
    return calls


@pytest.fixture
def mock_subprocess(monkeypatch):
    """Provide hooks for subprocess.check_output to simulate success/failure."""
    class Proc:
        def __init__(self):
            self.calls = []
            self.raise_error = None
            self.next_output = None

        def check_output(self, cmd, cwd=None, stderr=None):
            self.calls.append({"cmd": cmd, "cwd": cwd, "stderr": stderr})
            if self.raise_error is not None:
                e = subprocess.CalledProcessError(
                    returncode=self.raise_error.get("returncode", 1),
                    cmd=cmd,
                    output=self.raise_error.get("output", b"pip failed\nreason"),
                )
                raise e
            return self.next_output if self.next_output is not None else b"OK"

    import subprocess

    proc = Proc()
    monkeypatch.setattr(installer.subprocess, "check_output", proc.check_output, raising=True)
    return proc


@pytest.fixture
def mock_get_constraint_file(monkeypatch, tmp_path):
    """Provide a temporary constraint file and monkeypatch get_constraint_file."""
    cf = tmp_path / "constraints.txt"
    cf.write_text("# constraints\n")
    monkeypatch.setattr(installer, "get_constraint_file", lambda: cf, raising=True)
    return cf


def test_pip_command_builds_correct_invocation(fake_settings, mock_subprocess, monkeypatch):
    """Test that pip_command builds the correct invocation."""
    out = installer.pip_command("show", "somepkg")
    assert out == b"OK"
    assert len(mock_subprocess.calls) == 1
    call = mock_subprocess.calls[0]
    assert call["cmd"][0] == "/usr/bin/pythonX"
    assert call["cmd"][1:3] == ["-m", "pip"]
    assert call["cmd"][-2:] == ["show", "somepkg"]
    assert Path(call["cwd"]) == fake_settings.BASE_DIR.parent


def test_handle_pip_error_single_line_raises_validationerror(mock_log_error, monkeypatch):
    """Test that handle_pip_error raises ValidationError for single-line output."""
    import subprocess

    class E(subprocess.CalledProcessError):
        pass

    err = subprocess.CalledProcessError(1, ["pip"], output=b"Only one error line")
    with pytest.raises(installer.ValidationError) as ex:
        installer.handle_pip_error(err, "plugin_install")
    assert ("plugin_install", "pip") in mock_log_error
    assert "Only one error line" in str(ex.value)


def test_handle_pip_error_multiple_lines_list_raises_validationerror(mock_log_error):
    """Test that handle_pip_error raises ValidationError for multiple-line output."""
    import subprocess

    err = subprocess.CalledProcessError(1, ["pip"], output=b"line1\nline2\n\n")
    with pytest.raises(installer.ValidationError) as ex:
        installer.handle_pip_error(err, "plugin_install")
    assert ("plugin_install", "pip") in mock_log_error
    assert "line1" in str(ex.value) and "line2" in str(ex.value)


def test_get_install_info_success_parses_output(fake_settings, mock_subprocess):
    """Test that get_install_info parses pip show output successfully."""
    mock_subprocess.next_output = b"Name: testpkg\nVersion: 1.2.3\nLocation: /some/path\n"
    info = installer.get_install_info("testpkg==1.0")
    assert info["name"] == "testpkg"
    assert info["version"] == "1.2.3"
    assert info["location"] == "/some/path"


def test_get_install_info_called_process_error_sets_error(fake_settings, mock_subprocess, mock_log_error):
    """Test that get_install_info handles CalledProcessError and logs an error."""
    mock_subprocess.raise_error = {"returncode": 1, "output": b"not found"}
    info = installer.get_install_info("missing")
    assert "error" in info
    assert "not found" in info["error"]
    assert any(path == "get_install_info" and scope == "pip" for (path, scope) in mock_log_error)


def test_plugins_file_hash_none_when_absent(fake_settings, mock_log_error):
    """Test that plugins_file_hash returns None when the plugin file is absent."""
    assert installer.plugins_file_hash() is None


def test_plugins_file_hash_computed(fake_settings, mock_log_error):
    """Test that plugins_file_hash computes the correct hash of the plugin file."""
    content = b"pkgA==1.0\n# comment\n"
    fake_settings.PLUGIN_FILE.write_bytes(content)
    h = installer.plugins_file_hash()
    import hashlib
    assert h == hashlib.sha256(content).hexdigest()


def test_install_plugins_file_success(fake_settings, mock_subprocess, mock_staticfiles):
    """Test that install_plugins_file installs plugins and collects static files successfully."""
    fake_settings.PLUGIN_FILE.write_text("pkgA==1.0\n")
    result = installer.install_plugins_file()
    assert result is True
    call = mock_subprocess.calls[0]
    cmd = call["cmd"]
    assert cmd[3:] == ["install", "--disable-pip-version-check", "-U", "-r", str(fake_settings.PLUGIN_FILE)]
    assert mock_staticfiles["collect"] == 1


def test_install_plugins_file_missing_file_returns_none(fake_settings, mock_subprocess, mock_staticfiles, monkeypatch):
    """Test that install_plugins_file returns None when the plugin file is missing."""
    fake_settings.PLUGIN_FILE = None
    monkeypatch.setattr(installer, "settings", fake_settings, raising=True)
    result = installer.install_plugins_file()
    assert result is None
    assert mock_staticfiles["collect"] == 0


def test_install_plugins_file_pip_error_returns_false(fake_settings, mock_subprocess):
    """Test that install_plugins_file returns False on pip error."""
    fake_settings.PLUGIN_FILE.write_text("pkgA==1.0\n")
    mock_subprocess.raise_error = {"returncode": 1, "output": b"pip failed"}
    assert installer.install_plugins_file() is False


def test_update_plugins_file_add_new(fake_settings):
    """Test that update_plugins_file adds a new plugin entry."""
    fake_settings.PLUGIN_FILE.write_text("")
    installer.update_plugins_file("myplugin")
    txt = fake_settings.PLUGIN_FILE.read_text()
    assert re.search(r"(?m)^myplugin\s*$", txt)


def test_update_plugins_file_replace_existing_and_preserve_comments(fake_settings):
    """Test that update_plugins_file replaces existing plugin and preserves comments."""
    fake_settings.PLUGIN_FILE.write_text("# header\nmyplugin==0.1\nother\n")
    installer.update_plugins_file("myplugin", version="2.0.0")
    txt = fake_settings.PLUGIN_FILE.read_text().splitlines()
    assert txt[0].startswith("# header")
    assert "myplugin==2.0.0" in txt
    assert "other" in txt


def test_update_plugins_file_remove_matching(fake_settings):
    """Test that update_plugins_file removes matching plugin entries when remove is True."""
    fake_settings.PLUGIN_FILE.write_text("myplugin==1.0\nother\n")
    installer.update_plugins_file("myplugin", remove=True)
    assert "myplugin" not in fake_settings.PLUGIN_FILE.read_text()
    assert "other" in fake_settings.PLUGIN_FILE.read_text()


def test_install_plugin_disallowed_for_non_staff(monkeypatch):
    """Test that install_plugin raises ValidationError for non-staff users."""
    user = DummyUser(is_staff=False)
    with pytest.raises(installer.ValidationError):
        installer.install_plugin(packagename="pkg", user=user)


def test_install_plugin_disabled_by_setting(fake_settings, monkeypatch):
    """Test that install_plugin raises ValidationError when installation is disabled by settings."""
    fake_settings.PLUGINS_INSTALL_DISABLED = True
    monkeypatch.setattr(installer, "settings", fake_settings, raising=True)
    with pytest.raises(installer.ValidationError):
        installer.install_plugin(packagename="pkg", user=DummyUser(True))


@pytest.mark.parametrize(
    "url,packagename,version,expected_full,extra_flags",
    [
        (None, "pkg", None, "pkg", []),
        (None, "pkg", "1.2.3", "pkg==1.2.3", []),
        ("https://index.example/simple", None, None, "https://index.example/simple", ["-i"]),
        ("git+https://github.com/x/y.git", "pkg", None, "pkg@git+https://github.com/x/y.git", []),
        ("git+https://github.com/x/y.git", None, None, "git+https://github.com/x/y.git", []),
    ],
)
def test_install_plugin_command_building(
    fake_settings, mock_subprocess, mock_get_constraint_file, url, packagename, version, expected_full, extra_flags, mock_registry, mock_staticfiles
):
    """Test that install_plugin builds the correct pip install command for various inputs."""
    def fake_get_install_info(name):
        return {"location": "/venv/site-packages", "version": "9.9.9"}

    orig_get_install_info = installer.get_install_info
    installer.get_install_info = fake_get_install_info

    try:
        ret = installer.install_plugin(url=url, packagename=packagename, user=DummyUser(True), version=version)
        assert "success" in ret
        call = mock_subprocess.calls[0]
        cmd = call["cmd"]
        assert cmd[:3] == [sys.executable, "-m", "pip"]
        assert cmd[3:9] == [
            "install",
            "-U",
            "--disable-pip-version-check",
            "-c",
            str(mock_get_constraint_file),
        ]
        if extra_flags:
            assert extra_flags[0] in cmd
        assert cmd[-1] == expected_full
        assert mock_registry["reload"]
    finally:
        installer.get_install_info = orig_get_install_info


def test_install_plugin_pip_error_raises_validationerror(fake_settings, mock_subprocess, mock_get_constraint_file):
    """Test that install_plugin raises ValidationError on pip error."""
    mock_subprocess.raise_error = {"returncode": 1, "output": b"pip exploded"}
    with pytest.raises(installer.ValidationError):
        installer.install_plugin(packagename="pkg", user=DummyUser(True))


def test_validate_package_plugin_checks(monkeypatch):
    """Test that validate_package_plugin enforces package plugin configuration rules."""
    cfg = DummyPluginConfig()
    cfg.plugin = None
    with pytest.raises(installer.ValidationError):
        installer.validate_package_plugin(cfg)
    cfg.plugin = object()
    cfg._is_package = False
    with pytest.raises(installer.ValidationError):
        installer.validate_package_plugin(cfg)
    cfg._is_package = True
    cfg.package_name = ""
    with pytest.raises(installer.ValidationError):
        installer.validate_package_plugin(cfg)
    cfg.package_name = "abc"
    with pytest.raises(installer.ValidationError):
        installer.validate_package_plugin(cfg, user=DummyUser(False))
    installer.validate_package_plugin(cfg, user=DummyUser(True))


def test_uninstall_plugin_happy_path(fake_settings, mock_subprocess, mock_registry, mock_staticfiles, mock_log_error, monkeypatch):
    """Test that uninstall_plugin successfully uninstalls plugins and clears config/static files."""
    cfg = DummyPluginConfig(active=False, package_name="pkgA")
    cfg.plugin = object()
    monkeypatch.setattr(installer, "get_install_info", lambda name: {"location": "/venv", "version": "1.0"}, raising=True)
    result = installer.uninstall_plugin(cfg, user=DummyUser(True), delete_config=True)
    assert result["success"] is True
    call = mock_subprocess.calls[0]
    assert call["cmd"][3:6] == ["uninstall", "-y", "pkgA"]
    assert mock_staticfiles["clear"] == [cfg.key]
    assert mock_registry["reload"]


@pytest.mark.parametrize(
    "attr,expected_msg",
    [
        ("PLUGINS_INSTALL_DISABLED", "disabled"),
    ],
)
def test_uninstall_plugin_disabled_by_setting(fake_settings, attr, expected_msg, monkeypatch):
    """Test that uninstall_plugin raises ValidationError when uninstallation is disabled by settings."""
    setattr(fake_settings, attr, True)
    monkeypatch.setattr(installer, "settings", fake_settings, raising=True)
    with pytest.raises(installer.ValidationError) as ex:
        installer.uninstall_plugin(DummyPluginConfig(), user=DummyUser(True))
    assert expected_msg in str(ex.value)


@pytest.mark.parametrize(
    "cfg_kwargs, expected_error_fragment",
    [
        ({"active": True}, "currently active"),
        ({"installed": False}, "not installed"),
        ({"is_package": False}, "not a packaged plugin"),
        ({"package_name": ""}, "package name not found"),
        ({"mandatory": True}, "mandatory"),
        ({"sample": True}, "sample"),
        ({"builtin": True}, "built-in"),
    ],
)
def test_uninstall_plugin_validation_errors(fake_settings, cfg_kwargs, expected_error_fragment, monkeypatch):
    """Test that uninstall_plugin raises ValidationError for various invalid plugin configurations."""
    # Build DummyPluginConfig kwargs
    init_kwargs = {
        "active": cfg_kwargs.get("active", False),
        "package_name": cfg_kwargs.get("package_name", "pkgA"),
        "is_package": cfg_kwargs.get("is_package", True),
        "installed": cfg_kwargs.get("installed", True),
        "mandatory": cfg_kwargs.get("mandatory", False),
        "sample": cfg_kwargs.get("sample", False),
        "builtin": cfg_kwargs.get("builtin", False),
    }
    cfg = DummyPluginConfig(**init_kwargs)
    cfg.plugin = object()

    if cfg.active:
        with pytest.raises(installer.ValidationError) as ex:
            installer.uninstall_plugin(cfg, user=DummyUser(True))
        assert "currently active" in str(ex.value)
        return

    if not cfg.is_installed():
        with pytest.raises(installer.ValidationError) as ex:
            installer.uninstall_plugin(cfg, user=DummyUser(True))
        assert "not installed" in str(ex.value)
        return

    if not cfg.is_package():
        with pytest.raises(installer.ValidationError) as ex:
            installer.uninstall_plugin(cfg, user=DummyUser(True))
        assert "not a packaged plugin" in str(ex.value)
        return

    if not cfg.package_name:
        with pytest.raises(installer.ValidationError) as ex:
            installer.uninstall_plugin(cfg, user=DummyUser(True))
        assert "package name not found" in str(ex.value)
        return

    if cfg.is_mandatory():
        with pytest.raises(installer.ValidationError) as ex:
            installer.uninstall_plugin(cfg, user=DummyUser(True))
        assert "mandatory" in str(ex.value)
        return

    if cfg.is_sample():
        with pytest.raises(installer.ValidationError) as ex:
            installer.uninstall_plugin(cfg, user=DummyUser(True))
        assert "sample" in str(ex.value)
        return

    if cfg.is_builtin():
        with pytest.raises(installer.ValidationError) as ex:
            installer.uninstall_plugin(cfg, user=DummyUser(True))
        assert "built-in" in str(ex.value)
        return


def test_uninstall_plugin_installation_not_found_raises(fake_settings, monkeypatch):
    """Test that uninstall_plugin raises ValidationError when installation information is not found."""
    cfg = DummyPluginConfig(active=False, package_name="pkgA")
    cfg.plugin = object()
    monkeypatch.setattr(installer, "get_install_info", lambda name: {}, raising=True)
    with pytest.raises(installer.ValidationError) as ex:
        installer.uninstall_plugin(cfg, user=DummyUser(True))
    assert "installation not found" in str(ex.value)