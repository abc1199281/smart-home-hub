import os

from smart_home_hub.__main__ import _resolve_env_vars


def test_resolve_env_vars_substitutes(monkeypatch):
    monkeypatch.setenv("MY_SECRET", "hunter2")
    assert _resolve_env_vars("${MY_SECRET}") == "hunter2"


def test_resolve_env_vars_preserves_unset():
    key = "UNLIKELY_VAR_XYZ_999"
    os.environ.pop(key, None)
    assert _resolve_env_vars(f"${{{key}}}") == f"${{{key}}}"


def test_resolve_env_vars_nested(monkeypatch):
    monkeypatch.setenv("USER_EMAIL", "a@b.com")
    monkeypatch.setenv("USER_PASS", "pw123")
    data = {
        "devices": [
            {"name": "plug", "email": "${USER_EMAIL}", "password": "${USER_PASS}"},
            {"name": "other", "host": "192.168.1.1"},
        ]
    }
    result = _resolve_env_vars(data)
    assert result["devices"][0]["email"] == "a@b.com"
    assert result["devices"][0]["password"] == "pw123"
    assert result["devices"][1]["host"] == "192.168.1.1"
