
import broadlink
import sys

HOST = "192.168.178.170"

print(f"Attempting to discover device at {HOST}...")

try:
    devices = broadlink.discover(discover_ip_address=HOST, timeout=5)
    if devices:
        dev = devices[0]
        print(f"Success! Found device: {dev}")
        print(f"Type: {hex(dev.devtype)}")
        print(f"MAC: {dev.mac.hex()}")
        print(f"Host: {dev.host}")
        
        print("Attempting authentication...")
        if dev.auth():
            print("Authentication SUCCESS!")
        else:
            print("Authentication FAILED.")
            
        print("Attempting to get status...")
        try:
            # Try to read status
            # For 0x4f9b ACs, usually we send a specific packet, but let's try generic check_sensors if available or just auth
             pass
        except Exception as e:
            print(f"Get status error: {e}")

    else:
        print("Discovery returned no devices.")

except Exception as e:
    print(f"Error during discovery: {e}")
