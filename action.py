import dataclasses


@dataclasses.dataclass
class Action:
    """Action dataclass returned by the input parser after parsing new input. \
    Gets passed to the dispatcher who turns Action into function."""
    command: str = ''
    arguments: list[str] = dataclasses.field(default_factory=list)
    raw_input: str = ''
