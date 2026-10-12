import pytest

from app.configs.demo_config import DemoConfig


def test_demo_disabled_by_default():
    config = DemoConfig()

    assert config.enabled is False


def test_demo_configuration():
    config = DemoConfig(
        enabled=True,
        physics_step_seconds=10,
        simulated_seconds_per_tick=3600,
        degradation_rate=0.5,
    )

    assert config.enabled is True
    assert config.physics_step_seconds == 10
    assert config.simulated_seconds_per_tick == 3600
    assert config.degradation_rate == 0.5


@pytest.mark.parametrize(
    "field",
    [
        "physics_step_seconds",
        "simulated_seconds_per_tick",
        "degradation_rate",
    ],
)
def test_invalid_configuration(field):
    values = {field: 0}

    with pytest.raises(ValueError):
        DemoConfig(**values)