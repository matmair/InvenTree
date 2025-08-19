"""Test suite for tasks module."""

import builtins
import sys
import types
from pathlib import Path

import pytest

# Import the module under test.
# We attempt common names: tasks.py at repo root or a package path.
# If the module is elsewhere, adjust the import path accordingly.
try:
    import tasks as tasks_mod
except ModuleNotFoundError:
    # Fallback: attempt src/tasks.py or similar structures that are common
    import importlib.util

    candidates = [
        "tasks.py",
        "src/tasks.py",
        "backend/tasks.py",
        "scripts/tasks.py",
        "inv_tasks.py",
    ]
    _loaded = False
    for _c in candidates:
        try:
            p = Path(_c)
            if p.exists():
                spec = importlib.util.spec_from_file_location("tasks_mod", str(p))
                tasks_mod = importlib.util.module_from_spec(spec)
                sys.modules["tasks_mod"] = tasks_mod
                spec.loader.exec_module(tasks_mod)  # type: ignore
                _loaded = True
                break
        except Exception:
            continue
    if not _loaded:
        raise


def test_is_true_truthy_and_falsy_values():
    """Test is_true returns True for truthy inputs and False for falsy ones."""
    # Truthy cases
    for val in ["1", "Y", "y", " yes ", "t", "TRUE", "On", True]:
        assert tasks_mod.is_true(val), f"Expected truthy for {val!r}"

    # Falsy cases
    for val in ["0", "n", "no", "off", "false", "", "random", 0, None, False]:
        assert tasks_mod.is_true(val) is False, f"Expected falsy for {val!r}"


@pytest.mark.parametrize(
    "env_var,value,expected",
    [
        ("INVENTREE_DEVCONTAINER", "True", True),
        ("INVENTREE_DEVCONTAINER", "1", True),
        ("INVENTREE_DEVCONTAINER", "yes", True),
        ("INVENTREE_DEVCONTAINER", "no", False),
        ("INVENTREE_DEVCONTAINER", None, False),
    ],
)
def test_is_devcontainer_environment(monkeypatch, env_var, value, expected):
    """Test is_devcontainer_environment returns expected based on environment variable."""
    if value is None:
        monkeypatch.delenv(env_var, raising=False)
    else:
        monkeypatch.setenv(env_var, value)
    assert tasks_mod.is_devcontainer_environment() is expected


@pytest.mark.parametrize(
    "env_var,value,expected",
    [
        ("INVENTREE_DOCKER", "True", True),
        ("INVENTREE_DOCKER", "0", False),
        ("INVENTREE_DOCKER", None, False),
    ],
)
def test_is_docker_environment(monkeypatch, env_var, value, expected):
    """Test is_docker_environment returns expected based on environment variable."""
    if value is None:
        monkeypatch.delenv(env_var, raising=False)
    else:
        monkeypatch.setenv(env_var, value)
    assert tasks_mod.is_docker_environment() is expected


@pytest.mark.parametrize(
    "env_var,value,expected",
    [
        ("READTHEDOCS", "on", True),
        ("READTHEDOCS", "off", False),
        ("READTHEDOCS", None, False),
    ],
)
def test_is_rtd_environment(monkeypatch, env_var, value, expected):
    """Test is_rtd_environment returns expected based on environment variable."""
    if value is None:
        monkeypatch.delenv(env_var, raising=False)
    else:
        monkeypatch.setenv(env_var, value)
    assert tasks_mod.is_rtd_environment() is expected


def test_is_debug_environment_via_inventree_debug(monkeypatch):
    """Test is_debug_environment returns True when INVENTREE_DEBUG is set."""
    monkeypatch.setenv("INVENTREE_DEBUG", "true")
    monkeypatch.delenv("RUNNER_DEBUG", raising=False)
    assert tasks_mod.is_debug_environment() is True


def test_is_debug_environment_via_runner_debug(monkeypatch):
    """Test is_debug_environment returns True when RUNNER_DEBUG is set."""
    monkeypatch.delenv("INVENTREE_DEBUG", raising=False)
    monkeypatch.setenv("RUNNER_DEBUG", "1")
    assert tasks_mod.is_debug_environment() is True


def test_is_debug_environment_false(monkeypatch):
    """Test is_debug_environment returns False when debug vars indicate false."""
    monkeypatch.setenv("INVENTREE_DEBUG", "0")
    monkeypatch.delenv("RUNNER_DEBUG", raising=False)
    assert tasks_mod.is_debug_environment() is False


def test_get_version_vals_success_with_dotenv(monkeypatch, tmp_path):
    """Test get_version_vals successfully reads VERSION file using dotenv."""
    # Skip if dotenv is not installed and we don't want to manipulate import machinery
    pytest.importorskip("dotenv")
    # Prepare a VERSION file as dotenv format
    version_dir = tmp_path
    (version_dir / "VERSION").write_text("INVENTREE_PKG_INSTALLER=PKG\nFOO=bar\n", encoding="utf-8")

    # Patch local_dir to point to our temp directory
    monkeypatch.setattr(tasks_mod, "local_dir", lambda: version_dir)

    vals = tasks_mod.get_version_vals()
    assert vals.get("INVENTREE_PKG_INSTALLER") == "PKG"
    assert vals.get("FOO") == "bar"


def test_get_version_vals_importerror(monkeypatch, tmp_path, capsys):
    """Test get_version_vals handles ImportError when dotenv is missing."""
    # Create VERSION file; import of dotenv will be forced to fail
    version_dir = tmp_path
    (version_dir / "VERSION").write_text("INVENTREE_PKG_INSTALLER=PKG\n", encoding="utf-8")
    monkeypatch.setattr(tasks_mod, "local_dir", lambda: version_dir)

    orig_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "dotenv" or (name == "dotenv" and "dotenv_values" in fromlist):
            raise ImportError("No module named 'dotenv'")
        return orig_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    vals = tasks_mod.get_version_vals()
    captured = capsys.readouterr().out
    assert vals == {}
    assert "dotenv package not installed" in captured


def test_is_pkg_installer_with_content():
    """Test is_pkg_installer returns correct boolean based on provided dict."""
    assert tasks_mod.is_pkg_installer({"INVENTREE_PKG_INSTALLER": "PKG"}) is True
    assert tasks_mod.is_pkg_installer({"INVENTREE_PKG_INSTALLER": "OTHER"}) is False
    assert tasks_mod.is_pkg_installer({}) is False


def test_is_pkg_installer_load_content(monkeypatch):
    """Test is_pkg_installer with load_content flag fetches version values."""
    monkeypatch.setattr(tasks_mod, "get_version_vals", lambda: {"INVENTREE_PKG_INSTALLER": "PKG"})
    assert tasks_mod.is_pkg_installer(load_content=True) is True
    monkeypatch.setattr(tasks_mod, "get_version_vals", lambda: {"INVENTREE_PKG_INSTALLER": "OTHER"})
    assert tasks_mod.is_pkg_installer(load_content=True) is False


def test_is_pkg_installer_by_path(monkeypatch):
    """Test is_pkg_installer_by_path detects pkg installer based on sys.argv."""
    monkeypatch.setattr(sys, "argv", ["/opt/inventree/env/bin/invoke", "whatever"])
    assert tasks_mod.is_pkg_installer_by_path() is True
    monkeypatch.setattr(sys, "argv", ["/usr/local/bin/invoke"])
    assert tasks_mod.is_pkg_installer_by_path() is False


def test_get_installer_with_env(monkeypatch):
    """Test get_installer reads INVENTREE_PKG_INSTALLER from environment."""
    monkeypatch.setenv("INVENTREE_PKG_INSTALLER", "PKG")
    assert tasks_mod.get_installer() == "PKG"
    monkeypatch.delenv("INVENTREE_PKG_INSTALLER", raising=False)
    assert tasks_mod.get_installer() is None


def test_task_exception_handler_module_not_found(monkeypatch, capsys):
    """Test task_exception_handler handles ModuleNotFoundError specially."""
    # Prevent actual default excepthook output
    called = {}

    def fake_excepthook(t, v, tb):
        called["ok"] = (t, v, tb)

    monkeypatch.setattr(sys, "__excepthook__", fake_excepthook)

    v = ModuleNotFoundError("No module named 'foo'")
    tasks_mod.task_exception_handler(ModuleNotFoundError, v, None)
    out = capsys.readouterr().out
    assert "Error importing required module: foo" in out
    assert "Ensure the correct Python virtual environment is active" in out


def test_task_exception_handler_other_exception(monkeypatch, capsys):
    """Test task_exception_handler delegates to default hook for other exceptions."""
    # Prevent actual default excepthook output
    called = {}

    def fake_excepthook(t, v, tb):
        called["ok"] = True

    monkeypatch.setattr(sys, "__excepthook__", fake_excepthook)

    v = ValueError("bad")
    tasks_mod.task_exception_handler(ValueError, v, None)
    out = capsys.readouterr().out
    # Should not print module-not-found guidance
    assert "Error importing required module:" not in out
    assert called.get("ok") is True


def test_wrap_color_and_print_helpers(capsys):
    """Test wrap_color and print helper functions produce colored output."""
    txt = tasks_mod.wrap_color("hello", "92")
    assert txt == "\033[92mhello\033[0m"

    tasks_mod.success("ok")
    tasks_mod.error("err")
    tasks_mod.warning("warn")
    tasks_mod.info("inf")

    out = capsys.readouterr().out
    assert "\033[92mok\033[0m" in out
    assert "\033[91merr\033[0m" in out
    assert "\033[93mwarn\033[0m" in out
    assert "\033[94minf\033[0m" in out


def test_state_logger_default_name(monkeypatch, capsys):
    """Test state_logger decorator logs start and done with default function name."""
    # Force debug env to enable logging
    monkeypatch.setenv("INVENTREE_DEBUG", "1")
    monkeypatch.delenv("RUNNER_DEBUG", raising=False)

    calls = []

    @tasks_mod.state_logger
    def sample_task(_c):
        calls.append("ran")

    sample_task(None)
    out = capsys.readouterr().out
    assert "# invoke task named `sample_task`| start" in out
    assert "# invoke task named `sample_task`| done" in out
    assert calls == ["ran"]


def test_state_logger_custom_name(monkeypatch, capsys):
    """Test state_logger decorator logs start and done with custom name."""
    monkeypatch.setenv("INVENTREE_DEBUG", "1")

    @tasks_mod.state_logger("custom task")
    def custom(_c):
        pass

    custom(None)
    out = capsys.readouterr().out
    assert "# custom task| start" in out
    assert "# custom task| done" in out


def _dummy_invoke_module(tmp_path: Path, version: str) -> types.SimpleNamespace:
    # Create a dummy invoke module replacement
    m = types.SimpleNamespace()
    m.__version__ = version
    # place __file__ somewhere we can control
    m.__file__ = str(tmp_path / "invoke" / "__init__.py")
    (tmp_path / "invoke").mkdir(parents=True, exist_ok=True)
    (tmp_path / "invoke" / "__init__.py").write_text("# dummy", encoding="utf-8")
    return m


def test_envcheck_invoke_version_ok(monkeypatch, tmp_path):
    """Test envcheck_invoke_version does not exit for supported invoke versions."""
    dummy = _dummy_invoke_module(tmp_path, "2.1.0")
    monkeypatch.setattr(tasks_mod, "invoke", dummy, raising=True)
    # Should not raise SystemExit
    tasks_mod.envcheck_invoke_version()


def test_envcheck_invoke_version_fail(monkeypatch, tmp_path, capsys):
    """Test envcheck_invoke_version exits for unsupported invoke versions."""
    dummy = _dummy_invoke_module(tmp_path, "1.9.9")
    monkeypatch.setattr(tasks_mod, "invoke", dummy, raising=True)
    with pytest.raises(SystemExit):
        tasks_mod.envcheck_invoke_version()
    out = capsys.readouterr().out
    assert "The installed invoke version (1.9.9) is not supported!" in out


def test_envcheck_invoke_path_ok_env_prefix(monkeypatch, tmp_path):
    """Test envcheck_invoke_path passes when invoke is under virtualenv prefix."""
    dummy = _dummy_invoke_module(tmp_path, "2.2.0")
    # Make invoke path under env path
    env_prefix = tmp_path / "venv"
    (env_prefix / "lib").mkdir(parents=True, exist_ok=True)
    dummy.__file__ = str(env_prefix / "lib" / "invoke" / "__init__.py")
    (env_prefix / "lib" / "invoke").mkdir(parents=True, exist_ok=True)
    (env_prefix / "lib" / "invoke" / "__init__.py").write_text("# dummy", encoding="utf-8")

    monkeypatch.setattr(tasks_mod, "invoke", dummy, raising=True)
    monkeypatch.setattr(sys, "prefix", str(env_prefix))
    # Not docker or RTD, to enforce check
    monkeypatch.setenv("INVENTREE_DOCKER", "0")
    monkeypatch.setenv("READTHEDOCS", "0")
    tasks_mod.envcheck_invoke_path()  # should pass without exit


def test_envcheck_invoke_path_fail(monkeypatch, tmp_path, capsys):
    """Test envcheck_invoke_path exits when invoke is not under virtualenv prefix."""
    dummy = _dummy_invoke_module(tmp_path, "2.2.0")
    monkeypatch.setattr(tasks_mod, "invoke", dummy, raising=True)
    monkeypatch.setattr(sys, "prefix", str(tmp_path / "another_prefix"))

    # ensure not in docker or RTD
    monkeypatch.delenv("INVENTREE_DOCKER", raising=False)
    monkeypatch.delenv("READTHEDOCS", raising=False)

    with pytest.raises(SystemExit):
        tasks_mod.envcheck_invoke_path()
    out = capsys.readouterr().out
    assert "INVE-E2 - Wrong Invoke Path" in out


def test_envcheck_python_version_pass(monkeypatch):
    """Test envcheck_python_version does not exit for supported Python versions."""
    class VInfo:
        major = 3
        minor = 10

    monkeypatch.setattr(sys, "version_info", VInfo())
    monkeypatch.setattr(sys, "version", "3.10.1 (main, Jan 1 2024, 00:00:00)")

    tasks_mod.envcheck_python_version()  # no exit


def test_envcheck_python_version_fail(monkeypatch, capsys):
    """Test envcheck_python_version exits for unsupported Python versions."""
    class VInfo:
        major = 3
        minor = 8

    monkeypatch.setattr(sys, "version_info", VInfo())
    monkeypatch.setattr(sys, "version", "3.8.18 (main, Jan 1 2024, 00:00:00)")
    with pytest.raises(SystemExit):
        tasks_mod.envcheck_python_version()
    out = capsys.readouterr().out
    assert "InvenTree requires Python 3.9 or above" in out


def test_envcheck_invoke_cmd_skip_in_docker(monkeypatch, capsys):
    """Test envcheck_invoke_cmd skips checks in Docker environment."""
    monkeypatch.setenv("INVENTTREE_DOCKER", "1")
    monkeypatch.setattr(sys, "argv", ["/anything"])
    tasks_mod.envcheck_invoke_cmd()
    out = capsys.readouterr().out
    # Should produce no error outputs
    assert "Wrong Invoke Environment" not in out


def test_envcheck_invoke_cmd_pkg_installer(monkeypatch, capsys):
    """Test envcheck_invoke_cmd warns for pkg installer environment."""
    monkeypatch.delenv("INVENTREE_DOCKER", raising=False)
    monkeypatch.delenv("READTHEDOCS", raising=False)
    monkeypatch.delenv("INVENTREE_DEVCONTAINER", raising=False)

    # Force pkg installer environment but not the path
    monkeypatch.setattr(tasks_mod, "is_pkg_installer", lambda load_content=False: True)
    monkeypatch.setattr(tasks_mod, "is_pkg_installer_by_path", lambda: False)
    monkeypatch.setattr(sys, "argv", ["/usr/bin/python"])
    monkeypatch.setattr(sys, "prefix", "/venv")
    tasks_mod.envcheck_invoke_cmd()
    out = capsys.readouterr().out
    assert "INVE-W9 - Wrong Invoke Environment" in out
    assert "inventree run invoke" in out


def test_envcheck_invoke_cmd_unknown_environment(monkeypatch, capsys):
    """Test envcheck_invoke_cmd warns for unknown environment."""
    monkeypatch.delenv("INVENTREE_DOCKER", raising=False)
    monkeypatch.delenv("READTHEDOCS", raising=False)
    monkeypatch.delenv("INVENTREE_DEVCONTAINER", raising=False)
    monkeypatch.setattr(tasks_mod, "is_pkg_installer", lambda load_content=False: False)
    monkeypatch.setattr(sys, "argv", ["/usr/bin/python"])
    tasks_mod.envcheck_invoke_cmd()
    out = capsys.readouterr().out
    assert "Unknown environment, not checking used invoke command" in out
    assert "INVE-W9 - Wrong Invoke Environment" in out


def test_main_invokes_all_checks(monkeypatch):
    """Test main invokes all environment checks in order."""
    called = {"v": False, "p": False, "path": False, "cmd": False}
    monkeypatch.setattr(tasks_mod, "envcheck_invoke_version", lambda: called.__setitem__("v", True))
    monkeypatch.setattr(tasks_mod, "envcheck_python_version", lambda: called.__setitem__("p", True))
    monkeypatch.setattr(tasks_mod, "envcheck_invoke_path", lambda: called.__setitem__("path", True))
    monkeypatch.setattr(tasks_mod, "envcheck_invoke_cmd", lambda: called.__setitem__("cmd", True))

    tasks_mod.main()
    assert called == {"v": True, "p": True, "path": True, "cmd": True}


def test_apps_contains_expected_items():
    """Test apps function returns expected app names."""
    result = tasks_mod.apps()
    # Ensure core apps listed
    for name in ["build", "common", "company", "order", "part", "stock", "users", "plugin", "InvenTree"]:
        assert name in result
    # Sanity: non-empty list
    assert len(result) >= 5


def test_content_excludes_defaults():
    """Test content_excludes returns default excluded content types."""
    out = tasks_mod.content_excludes()
    # Always-excluded content types
    for key in [
        "contenttypes",
        "auth.permission",
        "admin.logentry",
        "django_q.schedule",
        "django_q.task",
        "django_q.ormq",
        "exchange.rate",
        "exchange.exchangebackend",
        "common.dataoutput",
        "common.newsfeedentry",
        "common.notificationentry",
        "common.notificationmessage",
        "importer.dataimportsession",
        "importer.dataimportcolumnmap",
        "importer.dataimportrow",
    ]:
        assert f"--exclude {key}" in out

    # Defaults allow auth/tokens/plugins/sso/session,
    # hence these should NOT be present by default
    for key in [
        "auth.group",
        "auth.user",
        "users.apitoken",
        "plugin.pluginconfig",
        "plugin.pluginsetting",
        "socialaccount.socialapp",
        "socialaccount.socialtoken",
        "sessions.session",
        "usersessions.usersession",
    ]:
        assert f"--exclude {key}" not in out


def test_content_excludes_all_blocked():
    """Test content_excludes blocks all content types when flags are false."""
    out = tasks_mod.content_excludes(
        allow_auth=False,
        allow_tokens=False,
        allow_plugins=False,
        allow_sso=False,
        allow_session=False,
    )
    for key in [
        "auth.group",
        "auth.user",
        "users.apitoken",
        "plugin.pluginconfig",
        "plugin.pluginsetting",
        "socialaccount.socialapp",
        "socialaccount.socialtoken",
        "sessions.session",
        "usersessions.usersession",
    ]:
        assert f"--exclude {key}" in out


def test_local_and_manage_paths():
    """Test local_dir, manage_py_dir, and manage_py_path return correct paths."""
    loc = tasks_mod.local_dir()
    assert isinstance(loc, Path)
    mp_dir = tasks_mod.manage_py_dir()
    assert mp_dir == loc.joinpath("src", "backend", "InvenTree")
    mp_path = tasks_mod.manage_py_path()
    assert mp_path == mp_dir.joinpath("manage.py")


def test_run_success_builds_correct_command(monkeypatch, tmp_path):
    """Test run builds and runs correct command on success."""
    recorded = {}

    class Ctx:
        def run(self, cmd, pty=False, env=None):
            recorded["cmd"] = cmd
            recorded["pty"] = pty
            recorded["env"] = env

    # Force local_dir() to our temp path to make command deterministic
    monkeypatch.setattr(tasks_mod, "local_dir", lambda: tmp_path)
    c = Ctx()
    tasks_mod.run(c, "echo hello", env={"A": "B"})
    assert recorded["cmd"] == f'cd "{tmp_path}" && echo hello'
    assert recorded["pty"] is False
    assert recorded["env"] == {"A": "B"}


def test_run_failure_raises_and_logs(monkeypatch, capsys, tmp_path):
    """Test run logs error and re-raises UnexpectedExit on failure."""
    # Create a fake UnexpectedExit class and attach to module under test
    class FakeUnexpectedExitError(Exception):
        pass

    monkeypatch.setattr(tasks_mod, "UnexpectedExit", FakeUnexpectedExitError, raising=True)

    class Ctx:
        def run(self, cmd, pty=False, env=None):
            raise FakeUnexpectedExitError("boom")

    monkeypatch.setattr(tasks_mod, "local_dir", lambda: tmp_path)

    with pytest.raises(FakeUnexpectedExitError):
        tasks_mod.run(Ctx(), "failing command")
    out = capsys.readouterr().out
    assert "ERROR: InvenTree command failed: 'failing command'" in out
    assert "Refer to the error messages in the log above for more information" in out


def test_manage_invokes_run_with_manage_py(monkeypatch, tmp_path):
    """Test manage delegates to run with manage.py command."""
    calls = {}

    def fake_run(c, cmd, path, pty, env):
        calls["args"] = (c, cmd, path, pty, env)

    monkeypatch.setattr(tasks_mod, "run", fake_run)
    # Control manage_py_dir to a deterministic path
    monkeypatch.setattr(tasks_mod, "manage_py_dir", lambda: tmp_path / "src" / "backend" / "InvenTree")
    tasks_mod.manage(object(), "migrate", pty=True, env={"X": "Y"})
    assert calls["args"][1] == "python3 manage.py migrate"
    assert calls["args"][2] == tmp_path / "src" / "backend" / "InvenTree"
    assert calls["args"][3] is True
    assert calls["args"][4] == {"X": "Y"}


def test_yarn_invokes_run_in_frontend_dir(monkeypatch, tmp_path):
    """Test yarn delegates to run in frontend directory."""
    calls = {}

    def fake_run(c, cmd, path, pty):
        calls["args"] = (c, cmd, path, pty)

    monkeypatch.setattr(tasks_mod, "run", fake_run)
    # Control local_dir
    monkeypatch.setattr(tasks_mod, "local_dir", lambda: tmp_path)
    tasks_mod.yarn(object(), "yarn build")
    assert calls["args"][1] == "yarn build"
    assert calls["args"][2] == tmp_path / "src" / "frontend"
    assert calls["args"][3] is False


def test_node_available_all_present(monkeypatch, capsys):
    """Test node_available returns True when both node and yarn are available."""
    def fake_check_output(args, stderr=None, shell=False):
        cmd = args[0] if isinstance(args, list) else args
        if "yarn --version" in cmd:
            return b"1.22.19\n"
        if "node --version" in cmd:
            return b"v20.12.1\n"
        raise FileNotFoundError()

    monkeypatch.setattr(tasks_mod.subprocess, "check_output", fake_check_output)
    assert tasks_mod.node_available() is True
    # No warning expected
    out = capsys.readouterr().out
    assert "Node is available but yarn is not" not in out


def test_node_available_node_only_warns(monkeypatch, capsys):
    """Test node_available returns False and warns when only node is available."""
    def fake_check_output(args, stderr=None, shell=False):
        cmd = args[0] if isinstance(args, list) else args
        if "yarn --version" in cmd:
            raise FileNotFoundError()
        if "node --version" in cmd:
            return b"v18.19.0\n"
        raise FileNotFoundError()

    monkeypatch.setattr(tasks_mod.subprocess, "check_output", fake_check_output)
    assert tasks_mod.node_available() is False
    out = capsys.readouterr().out
    assert "Node is available but yarn is not." in out


def test_node_available_bypass_yarn(monkeypatch, capsys):
    """Test node_available bypasses yarn check when bypass_yarn is True."""
    def fake_check_output(args, stderr=None, shell=False):
        cmd = args[0] if isinstance(args, list) else args
        if "yarn --version" in cmd:
            raise FileNotFoundError()
        if "node --version" in cmd:
            return b"v16.20.2\n"
        raise FileNotFoundError()

    monkeypatch.setattr(tasks_mod.subprocess, "check_output", fake_check_output)
    assert tasks_mod.node_available(bypass_yarn=True) is True
    out = capsys.readouterr().out
    # No warning because bypass_yarn=True
    assert "Node is available but yarn is not." not in out


def test_node_available_versions_tuple(monkeypatch):
    """Test node_available returns version tuple when requested."""
    def fake_check_output(args, stderr=None, shell=False):
        cmd = args[0] if isinstance(args, list) else args
        if "yarn --version" in cmd:
            return b"1.22.22\n"
        if "node --version" in cmd:
            return b"v20.0.0\n"
        raise FileNotFoundError()

    monkeypatch.setattr(tasks_mod.subprocess, "check_output", fake_check_output)
    ok, node_v, yarn_v = tasks_mod.node_available(versions=True)
    assert ok is True
    assert node_v == "v20.0.0"
    assert yarn_v == "1.22.22"


def test_check_file_existence_prompts_and_exits(monkeypatch, tmp_path, capsys):
    """Test check_file_existence prompts and exits when file exists and overwrite is False."""
    # Ensure decorator does not print debug logs
    monkeypatch.delenv("INVENTREE_DEBUG", raising=False)
    monkeypatch.delenv("RUNNER_DEBUG", raising=False)

    f = tmp_path / "export.csv"
    f.write_text("data", encoding="utf-8")

    # Simulate user input 'n'
    inputs = iter(["n"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        tasks_mod.check_file_existence(f, overwrite=False)

    out = capsys.readouterr().out
    assert "file already exists" in out.lower()
    assert "Cancelled export operation" in out


def test_check_file_existence_overwrite_skips_prompt(monkeypatch, tmp_path, capsys):
    """Test check_file_existence skips prompt when overwrite is True."""
    f = tmp_path / "export.csv"
    f.write_text("data", encoding="utf-8")

    calls = {"asked": False}

    def fake_input(prompt):
        calls["asked"] = True
        return "y"

    monkeypatch.setattr(builtins, "input", fake_input)
    tasks_mod.check_file_existence(f, overwrite=True)
    out = capsys.readouterr().out
    assert calls["asked"] is False  # No prompt when overwrite=True
    assert "Cancelled export operation" not in out


def test_check_file_existence_no_file(monkeypatch, tmp_path, capsys):
    """Test check_file_existence does nothing when file does not exist."""
    f = tmp_path / "nope.csv"
    if f.exists():
        f.unlink()
    # Should silently pass
    tasks_mod.check_file_existence(f, overwrite=False)
    out = capsys.readouterr().out
    assert out == "" or "# " in out  # could have state_logger logs if debug is enabled