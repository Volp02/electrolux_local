import struct
import typing as t
from enum import IntEnum
import json
import binascii
import time
from broadlink.device import Device
from broadlink.exceptions import DataValidationError
import logging

_LOGGER = logging.getLogger(__name__)

# Constants
MAX_TEMP = 32 # Usually max for ACs is around 30-32
MIN_TEMP = 16 # Usually min is 16
DEVICE_TYPE = 0x4f9b

class HVACMode(IntEnum):
    AUTO = 4
    COOL = 0
    HEAT = 1
    DRY = 2
    FAN = 3
    HEAT_8 = 6

class FanMode(IntEnum):
    AUTO = 0
    LOW = 1
    MID = 2
    HIGH = 3
    TURBO = 4
    QUIET = 5

class ElectroluxClimate(Device):
    """
    Controls an Electrolux air conditioner locally using the Broadlink protocol (0x4f9b).
    Based on community reverse engineering.
    """

    TYPE = "ELECTROLUX_OEM"

    def __init__(self, host: t.Tuple[str, int], mac: t.Union[bytes, str], devtype: int = DEVICE_TYPE, timeout: int = 10, name: str = "", model: str = "", manufacturer: str = "", is_locked: bool = False) -> None:
        super().__init__(host, mac, devtype, timeout, name, model, manufacturer, is_locked)
        if not self.auth():
             _LOGGER.warning("Initial authentication failed")

    def _send(self, command: int, data: bytes = b"") -> dict:
        """Send a packet to the device and return the decrypted JSON payload."""
        packet = bytearray(0xD)
        packet[0x00:0x02] = command.to_bytes(2, "little")
        packet[0x02:0x06] = bytes.fromhex("a5a55a5a")

        packet[0x08] = 0x01 if len(data) <= 2 else 0x02
        packet[0x09] = 0x0b
        packet[0xA:0xB] = len(data).to_bytes(2, "little")

        packet.extend(data)

        d_checksum = sum(packet[0x08:], 0xC0AD) & 0xFFFF
        packet[0x06:0x08] = d_checksum.to_bytes(2, "little")

        try:
            resp = self.send_packet(0x6A, packet)
        except Exception as e:
            _LOGGER.warning("Send failed (%s), attempting re-auth", e)
            try:
                if self.auth():
                    _LOGGER.warning("Re-authenticated with device")
                    time.sleep(0.5) # Give it a moment
                    resp = self.send_packet(0x6A, packet)
                else:
                    _LOGGER.warning("Re-authentication failed (auth() returned False)")
                    raise e
            except Exception as auth_e:
                _LOGGER.warning("Re-authentication failed with error: %s", auth_e)
                # If auth failed, raise original error so we know it was a send failure originally
                raise e
        
        # Check broadlink error code
        err = resp[0x22:0x24]
        if err != b'\x00\x00':
             raise Exception(f"Broadlink Error Code: {err.hex()}")

        dcry = self.decrypt(resp[0x38:])
        
        # We could verify checksum of response here but trusting device for now
        r_length = struct.unpack("h", dcry[0xA:0xC])[0]
        payload = dcry[0xE:0xE + r_length]
        
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"raw_payload": payload.hex()}

    def get_status(self) -> dict:
        return self._send(0x0e, bytearray('{}', "ascii"))

    def set_temp(self, temp: int) -> dict:
        temp = max(MIN_TEMP, min(temp, MAX_TEMP))
        return self._send(0x17, bytearray('{"temp":%s}'%(temp), "ascii"))

    def set_power(self, power_on: bool) -> dict:
        # ac_pwr: 1 = ON, 0 = OFF
        return self._send(0x18, bytearray('{"ac_pwr":%s}'%(1 if power_on else 0), "ascii"))
    
    def set_mode(self, mode: HVACMode) -> dict:
        return self._send(0x19, bytearray('{"ac_mode":%s}'%(mode.value), "ascii"))
    
    def set_fan(self, fan: FanMode) -> dict:
        return self._send(0x19, bytearray('{"ac_mark":%s}'%(fan.value), "ascii"))

    def set_swing_vertical(self, swing_on: bool) -> dict:
        return self._send(0x19, bytearray('{"ac_vdir":%s}'%(1 if swing_on else 0), "ascii"))

    def set_led_display(self, led_on: bool) -> dict:
        return self._send(0x19, bytearray('{"scrdisp":%s}'%(1 if led_on else 0), "ascii"))

    def set_sleep_mode(self, sleep_on: bool) -> dict:
        return self._send(0x18, bytearray('{"ac_slp":%s}'%(1 if sleep_on else 0), "ascii"))

    def set_silent_mode(self, silent_on: bool) -> dict:
        # Some devices use qtmode or similar
        return self._send(0x19, bytearray('{"qtmode":%s}'%(1 if silent_on else 0), "ascii"))
