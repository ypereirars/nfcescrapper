from dataclasses import dataclass

__all__ = ["TeleBotUser"]


@dataclass
class TeleBotUser:
    id: int = 0
    username: str = ""
    first_name: str = ""
    last_name: str = ""

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})".strip()
