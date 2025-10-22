import time
import board
<<<<<<< HEAD
import busio
from adafruit_ads1x15 import ADS1015, AnalogIn, ads1x15, ADS1115
=======
import math
from adafruit_ads1x15 import ADS1115, ads1x15, AnalogIn
>>>>>>> acb866dc1aa6b3c9bd1d77cff5662d59154acce6

def fetch_ammonia_from_analog():
    """Reads analog voltage from MQ137 via ADS1115."""
    i2c = board.I2C()
    ads = ADS1115(i2c)
    ads.gain = 1  # Gain = 1 => ±4.096V range
    chan = AnalogIn(ads, ads1x15.Pin.A0)
    return chan.voltage

<<<<<<< HEAD
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
=======
def calculate_nh3_from_analog(vout, vcc=5.0, rl=10000, ro=20000):
    """
    Convert analog voltage to NH3 PPM.
    ro must be determined from calibration in clean air or known 100ppm NH3.
    """
    if vout <= 0:
        return 0, 0, 0

    rs = rl * (vcc - vout) / vout
    ratio = rs / ro

    # MQ137 ammonia calibration curve constants
    a = -1.67
    b = 1.47
    ppm = 10 ** (a * math.log10(ratio) + b)

    return ppm, rs, ratio

if __name__ == "__main__":
    # 🔧 Adjust this after calibration
    RO = 20000  # replace with your calibrated value

    while True:
        voltage = fetch_ammonia_from_analog()
        ppm, rs, ratio = calculate_nh3_from_analog(voltage, ro=RO)

        print(f"Voltage: {voltage:.3f} V | Rs: {rs:.1f} Ω | Rs/Ro: {ratio:.3f} | NH3: {ppm:.2f} ppm")
        time.sleep(1.5)
>>>>>>> acb866dc1aa6b3c9bd1d77cff5662d59154acce6
