import subprocess

class TemperatureModule:
    '''Reads DS18B20 Temperature Sensor in °C'''
    def __init__(self):
        pass

    def fetch_temp(self):
        try:
            result = subprocess.run(
                ["cat", "/sys/bus/w1/devices/28-*/temperature"],
                capture_output=True,
                text=True,
                shell=True,
                check=True
            )
            return float(result.stdout.strip())/1000.0
        
        except subprocess.CalledProcessError as e:
            print("Error reading sensor:", e)
            return None
        
        except ValueError:
            print("Invalid temperature format")
            return None
