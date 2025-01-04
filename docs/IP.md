<a id="ksenia_lares.ip_api"></a>

# ksenia\_lares.ip\_api

<a id="ksenia_lares.ip_api.IpAPI"></a>

## IpAPI Objects

```python
class IpAPI(BaseApi)
```

Implementation for the IP range of Kseni Lares (Lare 16 IP, 48 IP & 128 IP).

<a id="ksenia_lares.ip_api.IpAPI.__init__"></a>

#### \_\_init\_\_

```python
def __init__(data: dict) -> None
```

Initialize the API with the necessary connection details.

**Arguments**:

- `data` _dict_ - A dictionary containing the following keys:
  - username (str): The username for authentication.
  - password (str): The password for authentication.
  - host (str): The hostname or IP address of the API.
  - port (int): The port number of the API.
  

**Raises**:

- `ValueError` - If any required parameter is missing or invalid.

<a id="ksenia_lares.ip_api.IpAPI.info"></a>

#### info

```python
async def info() -> AlarmInfo
```

Get info about the alarm system, like name and version.

**Returns**:

- `AlarmInfo` - General information about the alarm system.

<a id="ksenia_lares.ip_api.IpAPI.get_zones"></a>

#### get\_zones

```python
async def get_zones() -> List[Zone]
```

Get status of all zones.

**Returns**:

- `List[Zone]` - List of the zones in the alarm system.

<a id="ksenia_lares.ip_api.IpAPI.get_partitions"></a>

#### get\_partitions

```python
async def get_partitions() -> List[Partition]
```

Get status of partitions.

**Returns**:

- `List[Partition]` - List of the partitions in the alarm system.

<a id="ksenia_lares.ip_api.IpAPI.get_scenarios"></a>

#### get\_scenarios

```python
async def get_scenarios() -> List[Scenario]
```

Get status of scenarios

**Returns**:

- `List[Scenario]` - List of the scenarios in the alarm system.

<a id="ksenia_lares.ip_api.IpAPI.activate_scenario"></a>

#### activate\_scenario

```python
async def activate_scenario(scenario: int | Scenario,
                            pin: Optional[str]) -> bool
```

Active the given scenario on the alarm. Can be used to arm or disarm the alarm.

**Arguments**:

- `scenario` _int | Scenario_ - Thescenario to activate, by ID or from a retrieved scenario
- `pin` _Optional[str]_ - The pin code for the alarm, if the scenario doesn't have `NoPin` set, this is required.
  

**Returns**:

- `bool` - `True` when the scenario is actived, `False` if any issue occured.

<a id="ksenia_lares.ip_api.IpAPI.bypass_zone"></a>

#### bypass\_zone

```python
async def bypass_zone(zone: int | Zone, pin: str, bypass: bool) -> bool
```

Activates or deactivates the bypass on the given zone.

**Arguments**:

- `zone` _int | Zone_ - The zone or id of the zone to (un)bypass
- `pin` _str_ - PIN code, required for bypass
- `bypass` _bool_ - True to bypass zone, False to unbypass.
  

**Returns**:

- `bool` - True if the (un)bypass was executed successfully.

<a id="ksenia_lares.ip_api.IpAPI.get_model"></a>

#### get\_model

```python
async def get_model() -> str
```

Get model of the alarm system

**Returns**:

- `str` - The model of the alarm system (128IP, 48IP or 16IP)

