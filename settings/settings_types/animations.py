from dataclasses import dataclass, field


@dataclass
class AnimationSettigs:
    frames_nr: int = field(default=None)
    speed: float = field(default=None)
