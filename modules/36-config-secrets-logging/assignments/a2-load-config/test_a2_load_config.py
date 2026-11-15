import dataclasses

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize("text", ["1", "true", "TRUE", " Yes ", "on"])
def test_parse_bool_true(text):
    assert m.parse_bool(text) is True


@pytest.mark.parametrize("text", ["0", "false", "False", " NO ", "off"])
def test_parse_bool_false(text):
    assert m.parse_bool(text) is False


@pytest.mark.parametrize("text", ["", "maybe", "2", "tru"])
def test_parse_bool_invalid(text):
    with pytest.raises(ValueError):
        m.parse_bool(text)


def test_defaults_when_only_required_is_set():
    cfg = m.load_config({"API_KEY": "k123"})
    assert cfg == m.Config(api_key="k123", app_name="app", port=8000, debug=False, timeout=5.0)


def test_all_values_are_converted():
    env = {
        "API_KEY": "  k123  ",
        "APP_NAME": "robot",
        "PORT": "9000",
        "DEBUG": "yes",
        "TIMEOUT": "2.5",
        "UNRELATED": "ignored",
    }
    cfg = m.load_config(env)
    assert cfg.api_key == "k123"
    assert cfg.app_name == "robot"
    assert cfg.port == 9000
    assert cfg.debug is True
    assert cfg.timeout == 2.5


def test_config_is_frozen():
    cfg = m.load_config({"API_KEY": "k"})
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.port = 1


def test_repr_hides_the_secret():
    cfg = m.load_config({"API_KEY": "super-secret-value"})
    assert "super-secret-value" not in repr(cfg)
    assert "port=8000" in repr(cfg)


@pytest.mark.parametrize("env", [{}, {"API_KEY": ""}, {"API_KEY": "   "}])
def test_api_key_is_required(env):
    with pytest.raises(m.ConfigError) as info:
        m.load_config(env)
    assert any("API_KEY" in p for p in info.value.problems)


@pytest.mark.parametrize("port", ["abc", "0", "65536", "-1", "80.5", ""])
def test_invalid_port(port):
    with pytest.raises(m.ConfigError) as info:
        m.load_config({"API_KEY": "k", "PORT": port})
    assert [p for p in info.value.problems if "PORT" in p]


@pytest.mark.parametrize("timeout", ["0", "-2", "fast", "nan"])
def test_invalid_timeout(timeout):
    with pytest.raises(m.ConfigError) as info:
        m.load_config({"API_KEY": "k", "TIMEOUT": timeout})
    assert [p for p in info.value.problems if "TIMEOUT" in p]


def test_boundary_ports_are_valid():
    assert m.load_config({"API_KEY": "k", "PORT": "1"}).port == 1
    assert m.load_config({"API_KEY": "k", "PORT": "65535"}).port == 65535


def test_all_problems_are_reported_together():
    env = {"PORT": "x", "DEBUG": "maybe", "TIMEOUT": "-1"}
    with pytest.raises(m.ConfigError) as info:
        m.load_config(env)
    problems = info.value.problems
    assert len(problems) == 4
    for name in ("API_KEY", "PORT", "DEBUG", "TIMEOUT"):
        assert any(name in p for p in problems)
    assert "PORT" in str(info.value)
