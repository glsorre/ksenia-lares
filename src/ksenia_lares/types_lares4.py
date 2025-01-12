from dataclasses import dataclass
from enum import Enum
from signal import alarm
from typing import Optional, TypedDict

class ZoneStatus(Enum):
    """Bypass of alarm zone."""

    READY = "R"
    ARMED = "A"

class ZoneBypass(Enum):
    """Bypass of alarm zone."""

    OFF = "NO"
    ON = "YES"

class Model(Enum):
    """Bypass of alarm zone."""

    LARES_4 = "lares4"
    BTICINO_4200 = "bticino4200"

@dataclass
class Zone:
    """Alarm zone."""

    id: int
    status: ZoneStatus
    bypass: ZoneBypass
    tamper: str
    alarm: str
    ohm: str
    vas: str
    label: str 

    @property
    def enabled(self):
        return self.status == ZoneStatus.READY
