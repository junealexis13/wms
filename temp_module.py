import subprocess
import time

class TemperatureModule:
    """Reads DS18B20 Temperature Sensor in °C"""
    def __init__(self):
        pass

    def fetch_temp(self):
        try:
            # Use shell=True with a string command so wildcard expands
            result = subprocess.run(
                "cat /sys/bus/w1/devices/28-*/temperature",
                capture_output=True,
                text=True,
                shell=True,
                check=True
            )

            # Check if there's output
            if result.stdout.strip():
                temp_c = float(result.stdout.strip()) / 1000.0
                print(f"Temperature: {temp_c:.2f} °C")
                return temp_c
            else:
                print("No temperature data received.")
                return None

        except subprocess.CalledProcessError as e:
            print("Error reading sensor:", e)
            return None

        except ValueError:
            print("Invalid temperature format")
            return None



if __name__ == "__main__":
    mod = TemperatureModule()
    while True:
        time.sleep(1)
        mod.fetch_temp()