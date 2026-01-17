import os
from dataclasses import dataclass


def _to_bool(v: str, default: bool = False) -> bool:
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "t", "yes", "y", "on")


@dataclass(frozen=True)
class Settings:
    DEV_MODE: bool
    LOG_LEVEL: str

    USE_GROUNDING: bool
    GROUNDING_TIMEOUT_SEC: float
    GROUNDING_MAX_ATTEMPTS: int

    CB_FAIL_THRESHOLD: int
    CB_RESET_TIMEOUT_SEC: float

    HIDE_EXISTENCE_ON_UNAUTHORIZED: bool

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            DEV_MODE=_to_bool(os.getenv("DEV_MODE"), default=True),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO").upper(),

            USE_GROUNDING=_to_bool(os.getenv("USE_GROUNDING"), default=True),
            GROUNDING_TIMEOUT_SEC=float(os.getenv("GROUNDING_TIMEOUT_SEC", "2.0")),
            GROUNDING_MAX_ATTEMPTS=int(os.getenv("GROUNDING_MAX_ATTEMPTS", "2")),

            CB_FAIL_THRESHOLD=int(os.getenv("CB_FAIL_THRESHOLD", "5")),
            CB_RESET_TIMEOUT_SEC=float(os.getenv("CB_RESET_TIMEOUT_SEC", "30.0")),

            HIDE_EXISTENCE_ON_UNAUTHORIZED=_to_bool(
                os.getenv("HIDE_EXISTENCE_ON_UNAUTHORIZED"), default=False
            ),
        )