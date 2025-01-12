
import aiohttp
import json
import ssl
import time
import asyncio

from typing import List

from .types_lares4 import (
    Model,
    Zone,
    ZoneBypass,
    ZoneStatus
)
from .base_api import BaseApi
from ksenia_lares import base_api

def u(e):
    t = [];
    for n in range(0, len(e)):
        r = ord(e[n]);
        if (r < 128):
            t.append(r)
        else:
            if (r < 2048):
                t.append(192 | r >> 6)
                t.append(128 | 63 & r)
            else:
                if (r < 55296 or r >= 57344):
                    t.append(224 | r >> 12)
                    t.append(128 | r >> 6 & 63)
                    t.append(128 | 63 & r)
                else:
                    n = n + 1; 
                    r = 65536 + ((1023 & r) << 10 | 1023 & ord(e[n]));
                    t.append(240 | r >> 18)
                    t.append(128 | r >> 12 & 63)
                    t.append(128 | r >> 6 & 63)
                    t.append(128 | 63 & r)
        n = n+1

    return t

def crc16(e):
    i = u(e);
    l = e.rfind('"CRC_16"') + len('"CRC_16"') + (len(i) - len(e));
    r = 65535;
    s = 0;
    while s < l:
        t = 128;
        o = i[s];
        while t:	
            if(32768& r):
                n = 1;
            else:
                n = 0;
            r <<= 1;
            r &= 65535;
            if(o & t):
                r = r + 1;
            if(n):
                r = r^4129;
            t >>= 1;
        s=s+1;
    return ("0x"+format(r,'04x'));

def get_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT
    return ctx


class CommandFactory:
    def __init__(self, sender: str, pin: str) -> None:
        self._command_id = 0
        self._sender = sender
        self._pin = pin

    def get_sender(self) -> str:
        return self._sender
    
    def get_login_id(self) -> str:
        return self._login_id
    
    def set_login_id(self, login_id: str) -> None:
        self._login_id = login_id
    
    def get_pin(self) -> str:
        return self._pin
    
    def get_current_command_id(self) -> int:
        return self._command_id
    
    def get_next_command_id(self) -> int:
        self._command_id += 1
        return self._command_id
    
    def build_payload(self, payload: dict) -> dict:
        print(getattr(payload, "PIN", False))
        return {
            **payload,
            **({"ID_LOGIN": self.get_login_id()} if "ID_LOGIN" in payload else {}),
            **({"PIN": self.get_pin()} if "PIN" in payload else {})
        }
    
    def build_command(self, cmd: str, payload_type: str, payload: dict) -> dict:
        timestamp = str(int(time.time()))
        
        command = {
            "SENDER": self.get_sender(),
            "RECEIVER": "",
            "CMD": cmd,
            "ID": f"{self.get_next_command_id()}",
            "PAYLOAD_TYPE": payload_type,
            "PAYLOAD": self.build_payload(payload),
            "TIMESTAMP": f"{timestamp}",
            "CRC_16": '0x0000',
        }

        command['CRC_16'] = crc16(json.dumps(command))

        return command

class Lares4API():
    def __init__(self, data, model: Model = Model.LARES_4):
        if not all(key in data for key in ("url", "pin", "sender")):
            raise ValueError(
                "Missing one or more of the following keys: host, pin, sender"
            )                                                                                                                                                                                                                                     
        self.url = data["url"]
        self.host = f"wss://{data['url']}/KseniaWsock"
        self.model = model
        self.command_factory = CommandFactory(
            data["sender"], data["pin"]
        )
        self.is_running = False

    async def connect(self):
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect(
            self.host,
            protocols=['KS_WSOCK'],
            ssl_context=get_ssl_context()
        )
        print(f"Connected to {self.url}")
        self.is_running = True

    async def send_message(self, message):
        if self.ws:
            await self.ws.send_json(message)
            print(f"Sent: {message}")
        else:
            print("WebSocket is not connected.")

    async def close(self):
        self.is_running = False
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
        print("Connection closed")

    async def run(self):
        await self.connect()
        
        receive_login = asyncio.create_task(self.receive_login())
        login = asyncio.create_task(self.send_login())
        await asyncio.gather(receive_login, login)

    async def send_login(self):
        login_command = self.command_factory.build_command(
            cmd="LOGIN",
            payload_type="UNKNOWN" if self.model == Model.LARES_4 else "USER",
            payload={
                "PIN": True
            }
        )
        await self.send_message(login_command)

    async def receive_login(self):
        if self.ws:
            msg = await asyncio.wait_for(self.ws.receive(), timeout=1.0)
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                print(data)
                if data["CMD"] == "LOGIN_RES":
                    self.command_factory.set_login_id(data["PAYLOAD"]["ID_LOGIN"])
                else:
                    print("Login failed")
        else:
            print("WebSocket is not connected.")

    async def get(self, cmd: str, payload_type: str, payload: dict) -> dict | None:
        command = self.command_factory.build_command(cmd, payload_type, payload)
        await self.send_message(command)
        response = await self.receive()
        return response
    
    async def receive(self) -> dict | None:
        if self.ws:
            msg = await self.ws.receive()
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                return data
        else:
            print("WebSocket is not connected.")

    async def info(self):
        info = await self.get(
            'REALTIME',
            'REGISTER',
            {
                'ID_LOGIN': True,
                'TYPES': [
                    'STATUS_SYSTEM'
                ],
            }
        )
        return info
    
    async def get_zones(self) -> List[Zone]:
        zones = await self.get(
            "READ",
            "MULTI_TYPES",
            {
                "ID_LOGIN": True,
                "ID_READ": "1",
                "TYPES": [
                    "STATUS_ZONES"
                ]
            }
        )

        if zones:
            status_zones = zones['PAYLOAD']['STATUS_ZONES']
            return [
                Zone(
                    id=zone['ID'],
                    status=ZoneStatus(zone['STA']),
                    bypass=ZoneBypass(zone['BYP']),
                    tamper=zone['T'],
                    alarm=zone['A'],
                    ohm=zone['OHM'],
                    vas=zone['VAS'],
                    label=zone['LBL'],
                )
                for zone in status_zones
            ]
        return []
    
    async def get_partitions(self):
        partitions = await self.get(
            "READ",
            "MULTI_TYPES",
            {
                "ID_LOGIN": True,
                "ID_READ": "1",
                "TYPES": [
                    "STATUS_PARTITIONS"
                ]
            }
        )

        return partitions

    async def get_scenarios(self):
        scenarios = await self.get(
            "READ",
            "MULTI_TYPES",
            {
                "ID_LOGIN": True,
                "ID_READ": "1",
                "TYPES": [
                    "STATUS_SCENARIOS"
                ]
            }
        )

        return scenarios
    
    async def activate_scenario(self, scenario_id):
        scenario = await self.get(
            "CMD_USR",
            "CMD_EXE_SCENARIO",
            {
                "ID_LOGIN": True,
                "PIN": True,
                "SCENARION": {
                    "ID": scenario_id,
                }
            }
        )

        return scenario
    
    async def bypass_zone(self, zone: int | Zone, zone_bypass: ZoneBypass) -> bool:
        bypass_zone = await self.get(
            "CMD_USR",
            "CMD_BYP_ZONE",
            {
                "ID_LOGIN": True,
                "PIN": True,
                "ZONE": {
                    "ID": zone.id if isinstance(zone, Zone) else zone,
                    "BYP": zone_bypass
                }
            }
        )
        if bypass_zone:
            return bypass_zone['PAYLOAD']['RESULT'] == 'OK'
        return False
