import time
import board
import math
from ads_instance import get_ads
from adafruit_ads1x15 import ADS1115, ads1x15, AnalogIn

def fetch_ammonia_from_analog(ads_instance):
    """Reads analog voltage from MQ137 via ADS1115."""
    chan = AnalogIn(ads_instance, ads1x15.Pin.A1)
    return chan.voltage

def calculate_nh3_from_analog(ads_instance, vcc=5.0, rl=10000, ro=20000):
    """
    Convert analog voltage to NH3 PPM.
    ro must be determined from calibration in clean air or known 100ppm NH3.
    """
    vout = fetch_ammonia_from_analog(ads_instance)
    if vout <= 0:
        return 0, 0, 0
    
    if vout >= vcc * 0.99:  # Allow 1% tolerance
        print(f"Warning: Vout ({vout:.3f}V) near Vcc ({vcc}V) - sensor may be saturated")
        return 0.0, float('inf'), float('inf')


    rs = rl * (vcc - vout) / vout
    ratio = rs / ro

    # MQ137 ammonia calibration curve constants
    a = -1.67
    b = 1.3
    ppm = 10 ** (a * math.log10(ratio) + b)

    return ppm, rs, ratio

if __name__ == "__main__":
    # 🔧 Adjust this after calibration
    RO = 20000  # replace with your calibrated value

    while True:
        ads = get_ads()
        voltage = fetch_ammonia_from_analog()
        ppm, rs, ratio = calculate_nh3_from_analog(voltage,ads, ro=RO)

        print(f"Voltage: {voltage:.3f} V | Rs: {rs:.1f} Ω | Rs/Ro: {ratio:.3f} | NH3: {ppm:.2f} ppm")
        time.sleep(1.5)
