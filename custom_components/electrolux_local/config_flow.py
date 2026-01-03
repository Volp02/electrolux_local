import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, DEFAULT_NAME

class ElectroluxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Electrolux Local."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            try:
                # We run this in executor because broadlink discovery is blocking IO
                mac = await self.hass.async_add_executor_job(self._try_connect, host)
                
                await self.async_set_unique_id(mac)
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data={
                        CONF_HOST: host,
                        "mac": mac, # Stored as hex string
                    }
                )
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            }),
            errors=errors
        )

    def _try_connect(self, host):
        """Try to connect and fetch MAC."""
        import broadlink # Import here to avoid top-level dependency issues
        
        # Use simple discovery to verify device and get MAC
        devices = broadlink.discover(discover_ip_address=host, timeout=5)
        if devices:
            dev = devices[0]
            # Device type 0x4f9b check could happen here
            return dev.mac.hex()
        raise Exception("Device not found")
