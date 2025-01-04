<a id="ksenia_lares.base_api"></a>

# ksenia\_lares.base\_api

<a id="ksenia_lares.base_api.BaseApi"></a>

## BaseApi Objects

```python
class BaseApi(ABC)
```

Base API for the Ksenia Lares

<a id="ksenia_lares.base_api.BaseApi.info"></a>

#### info

```python
@abstractmethod
async def info() -> AlarmInfo
```

Get info about the alarm system, like name and version.

**Returns**:

- `AlarmInfo` - General information about the alarm system.

<a id="ksenia_lares.base_api.BaseApi.get_zones"></a>

#### get\_zones

```python
@abstractmethod
async def get_zones() -> List[Zone]
```

Get status of all zones.

**Returns**:

- `List[Zone]` - List of the zones in the alarm system.

<a id="ksenia_lares.base_api.BaseApi.get_partitions"></a>

#### get\_partitions

```python
@abstractmethod
async def get_partitions() -> List[Partition]
```

Get status of partitions.

**Returns**:

- `List[Partition]` - List of the partitions in the alarm system.

<a id="ksenia_lares.base_api.BaseApi.get_scenarios"></a>

#### get\_scenarios

```python
@abstractmethod
async def get_scenarios() -> List[Scenario]
```

Get status of scenarios

**Returns**:

- `List[Scenario]` - List of the scenarios in the alarm system.

<a id="ksenia_lares.base_api.BaseApi.activate_scenario"></a>

#### activate\_scenario

```python
@abstractmethod
async def activate_scenario(scenario: int | Scenario,
                            pin: Optional[str]) -> bool
```

Active the given scenario on the alarm. Can be used to arm or disarm the alarm.

**Arguments**:

- `scenario` _int | Scenario_ - Thescenario to activate, by ID or from a retrieved scenario
- `pin` _Optional[str]_ - The pin code for the alarm, if the scenario doesn't have `NoPin` set, this is required.
  

**Returns**:

- `bool` - `True` when the scenario is actived, `False` if any issue occured.

<a id="ksenia_lares.base_api.BaseApi.bypass_zone"></a>

#### bypass\_zone

```python
@abstractmethod
async def bypass_zone(zone: int | Zone, pin: str, bypass: ZoneBypass) -> bool
```

Activates or deactivates the bypass on the given zone.

**Arguments**:

- `zone` _int | Zone_ - The zone or id of the zone to (un)bypass.
- `pin` _str_ - PIN code, required for bypass.
- `bypass` _ZoneBypass_ - Set to bypass or unbypass zone.
  

**Returns**:

- `bool` - True if the (un)bypass was executed successfully.

