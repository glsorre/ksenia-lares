from argparse import ArgumentDefaultsHelpFormatter
from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypedDict
from unicodedata import category

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
        return self.status == ZoneStatus.ARMED

@dataclass
class Partition:
    """Alarm partition."""

    id: int
    armed: str
    tamper: str
    alarm: str
    test: str

    @property
    def enabled(self):
        return self.armed != "D"
    
@dataclass
class Scenario:
    """Alarm scenario."""

    id: int
    description: str
    pin: str
    category: str