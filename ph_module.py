import time
import board
import math
from adafruit_ads1x15 import ADS1115, ads1x15, AnalogIn

def fetch_ph_from_analog():
    """Reads analog voltage from PH-4502C via ADS1115."""
	i2c = board.I2C()
	ads = ADS1115(i2c)
	ads.gain = 1  # Gain = 1 => ±4.096V range
	chan = AnalogIn(ads, ads1x15.Pin.A0)
	return chan.voltage


def voltage_to_ph():
	vout = fetch_ph_from_analog()
	V_neutral = 2.5   # should still be validated for pH 7
	V_acid = 3.0      # should be pH 4 
	return 7 - ((vout - V_neutral) * (7 - 4) / (V_neutral - V_acid))

if __name__ == "__main__":
	while True:
		pH = voltage_to_ph()
		time.sleep(1.5)
 		print(f"pH: {pH}")
