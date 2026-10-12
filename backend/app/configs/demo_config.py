from dataclasses import dataclass


@dataclass(frozen=True)
class DemoConfig:
    """
    Configuration for accelerated simulation mode.
    """

    enabled: bool = False

    # Maximum simulated seconds per internal physics update
    physics_step_seconds: float = 10.0

    # Total simulated seconds advanced per simulation tick
    simulated_seconds_per_tick: float = 3600.0

    # Base degradation rate used only in demo mode
    degradation_rate: float = 0.5

    def __post_init__(self):
        if self.physics_step_seconds <= 0:
            raise ValueError(
                "physics_step_seconds must be greater than zero"
            )

        if self.simulated_seconds_per_tick <= 0:
            raise ValueError(
                "simulated_seconds_per_tick must be greater than zero"
            )

        if self.degradation_rate <= 0:
            raise ValueError(
                "degradation_rate must be greater than zero"
            )