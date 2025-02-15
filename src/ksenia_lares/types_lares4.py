from argparse import ArgumentDefaultsHelpFormatter
from ast import Str
from ctypes import Array
from dataclasses import dataclass
from enum import Enum
from sqlite3 import Time
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

class BusPeripheralType(Enum):
    DOMUS = "DOMUS"

class ThermostatSeason(Enum):
    """Thermostat season."""
    WINTER = "WIN"
    SUMMER = "SUM"

class ThermostatMode(Enum):
    """Thermostat mode."""
    OFF = "OFF"
    MANUAL = "MAN"
    MANUAL_TIMER = "MAN_TMR"
    WEEKLY = "WEEKLY"
    SPECIAL_1 = "SD1"
    SPECIAL_2 = "SD2"

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

@dataclass
class Output:
    """Output."""
    id: int
    description: str
    cnv: str
    category: str
    mode: str

@dataclass
class BusPeripheral:
    """Bus peripheral."""
    id: int
    description: str
    type: BusPeripheralType

@dataclass
class OutputStatus:
    """Output status."""
    id: int
    status: str
    position: Optional[int] = None
    target_position: Optional[int] = None

@dataclass
class SystemArmStatus:
    """System status."""
    mode: str
    status: str

@dataclass
class SystemTemperatureStatus:
    """System status."""
    inside: Optional[float] = None
    outside: Optional[float] = None

@dataclass
class SystemTimeStatus:
    """System status."""
    gmt: int
    timezone: int
    timezone_minutes: int
    dawn: Time
    dusk: Time

@dataclass
class SystemStatus:
    """System status."""
    id: int
    informations: Array
    tamper: Array
    tamper_memory: Array
    alarm: Array
    alarm_memory: Array
    fault: Array
    fault_memory: Array
    arm: SystemArmStatus
    temperature: SystemTemperatureStatus
    time: SystemTimeStatus

@dataclass
class LinkStatus:
    type: str
    serial_number: str
    bus: int

@dataclass
class DomusStatus:
    temperature: float
    humidity: float
    light: float

@dataclass
class BusPeripheralStatus:
    """Bus peripheral status."""
    id: int
    type: BusPeripheralType
    status: str
    bus: int
    link: LinkStatus
    domus: Optional[DomusStatus] = None

@dataclass
class ThermostatStatus:
    """Thermostat status."""
    season: ThermostatSeason
    mode: ThermostatMode
    output: str
    timer: Optional[Time] = None

@dataclass
class TemperatureStatus:
    """Temperature status."""
    id: int
    temperature: float
    thermostat: ThermostatStatus