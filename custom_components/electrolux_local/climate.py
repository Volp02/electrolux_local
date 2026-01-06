from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature, HVACMode
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_HOST
from .electrolux import ElectroluxClimate, HVACMode as EleMode, FanMode as EleFan
import binascii
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    host = entry.data[CONF_HOST]
    mac_hex = entry.data["mac"]
    name = entry.title
    
    # Init device
    mac_bytes = binascii.unhexlify(mac_hex)
    async_add_entities([ElectroluxEntity(host, mac_bytes, name, entry.entry_id)], True)

class ElectroluxEntity(ClimateEntity):
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.TURN_OFF
        | ClimateEntityFeature.TURN_ON
    )
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL, HVACMode.AUTO, HVACMode.DRY, HVACMode.FAN_ONLY]
    _attr_fan_modes = ["auto", "low", "mid", "high"]
    _attr_target_temperature_step = 1
    
    # Map HA <-> Elec
    _HVAC_MAP = {
        HVACMode.AUTO: EleMode.AUTO,
        HVACMode.COOL: EleMode.COOL,
        HVACMode.HEAT: EleMode.HEAT,
        HVACMode.DRY: EleMode.DRY,
        HVACMode.FAN_ONLY: EleMode.FAN,
    }
    _HVAC_MAP_INV = {v: k for k, v in _HVAC_MAP.items()}

    _FAN_MAP = {
        "auto": EleFan.AUTO,
        "low": EleFan.LOW,
        "mid": EleFan.MID,
        "high": EleFan.HIGH,
    }
    _FAN_MAP_INV = {v: k for k, v in _FAN_MAP.items()}

    def __init__(self, host, mac, name, unique_id):
        self._host = host
        self._mac = mac
        self._name = name
        self._attr_unique_id = unique_id
        
        self._device = None
        self._create_device()

    def _create_device(self):
        """Create or recreate the device instance."""
        try:
             _LOGGER.debug("Creating device instance for %s", self._host)
             self._device = ElectroluxClimate((self._host, 80), self._mac)
        except Exception as e:
             _LOGGER.error("Failed to create device instance: %s", e)

    def update(self):
        # Blocking call in executor
        if self._device is None:
            self._create_device()
            
        try:
            status = self._device.get_status()
            
            # Power
            is_on = status.get('ac_pwr', 0) == 1
            if not is_on:
                self._attr_hvac_mode = HVACMode.OFF
            else:
                mode_val = status.get('ac_mode')
                try:
                    ele_mode = EleMode(mode_val)
                    self._attr_hvac_mode = self._HVAC_MAP_INV.get(ele_mode, HVACMode.AUTO)
                except ValueError:
                    self._attr_hvac_mode = HVACMode.AUTO

            self._attr_current_temperature = status.get('envtemp')
            self._attr_target_temperature = status.get('temp')
            
            fan_val = status.get('ac_mark')
            try:
                ele_fan = EleFan(fan_val)
                self._attr_fan_mode = self._FAN_MAP_INV.get(ele_fan, "auto")
            except ValueError:
                self._attr_fan_mode = "auto"

            # Swing - Removed
                
        except Exception as e:
            if self._attr_available:
                _LOGGER.warning("Device connection lost: %s. Recreating device instance.", e)
            
            self._attr_available = False
            
            # Recreate device to force fresh socket/session next time
            self._create_device()
            return
            
        self._attr_available = True

    def set_hvac_mode(self, hvac_mode):
        if hvac_mode == HVACMode.OFF:
            self._device.set_power(False)
        else:
            # check if we need to turn on
            if self._attr_hvac_mode == HVACMode.OFF:
                self._device.set_power(True)
            
            ele_mode = self._HVAC_MAP.get(hvac_mode)
            if ele_mode:
                self._device.set_mode(ele_mode)
        
    def set_temperature(self, **kwargs):
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp:
            self._device.set_temp(int(temp))

    def set_fan_mode(self, fan_mode):
        ele_fan = self._FAN_MAP.get(fan_mode)
        if ele_fan:
             self._device.set_fan(ele_fan)
