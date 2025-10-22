import time
import board
import busio
from adafruit_ads1x15 import ADS1015, AnalogIn, ads1x15, ADS1115


def fetch_ammonia_from_analog():
    # I2C setup
 
    i2c = board.I2C()
    ads = ADS1115(i2c)
    ads.gain = 1  # Gain = 1 for 0-4.096V range

    # MQ135 connected to A0
    chan = AnalogIn(ads, ads1x15.Pin.A0)
    return chan.voltage

def calculate_nh3_from_analog(vout, vcc=5.0, rl=10000, ro=20000):
	#calculate sensor resistance (Rs)
	rs = rl*(vcc-vout)/vout

	#calc ratio
	ratio = rs/ro

	#nh3 approximations
	a = -1.67
	b = 1.47

	ppm = 10 ** (a * math.log10(ratio) + b)
	return max(ppm, 0), rs

if __name__ == "__main__":
	voltage = fetch_ammonia_from_analog()
	ppm, rs = calculate_nh3_ppm(voltage)

	print(f"{ppm} ppm")
