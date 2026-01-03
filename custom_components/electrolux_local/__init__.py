\"\"\"The Electrolux Local integration.\"\"\"
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[str] = ["climate"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    \"\"\"Set up Electrolux Local from a config entry.\"\"\"
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    \"\"\"Unload a config entry.\"\"\"
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        pass
    return unload_ok
