import time
import board
import statistics
import math
from adafruit_ads1x15 import ADS1115, ads1x15, AnalogIn
from tqdm import tqdm

def fetch_ph_from_analog():
    """Reads analog voltage from PH-4502C via ADS1115."""
    i2c = board.I2C()
    ads = ADS1115(i2c)
    ads.gain = 1  # Gain = 1 => ±4.096V range
    chan = AnalogIn(ads, ads1x15.Pin.A0)
    return chan.voltage

def voltage_to_ph():
    vout = fetch_ph_from_analog()

    # Calibrated voltages at known pH values
    V_acid = 3.8872  # pH 4
    V_neutral = 3.67 # pH 7
    V_base = 3.147   # pH 10

    x_vals = [V_acid, V_neutral, V_base]
    y_vals = [4.0, 7.0, 10.0]

    # Compute slope (m) and intercept (b) using linear regression
    n = len(x_vals)
    sum_x = sum(x_vals)
    sum_y = sum(y_vals)
    sum_xy = sum(x*y for x, y in zip(x_vals, y_vals))
    sum_x2 = sum(x*x for x in x_vals)

    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    b = (sum_y - m * sum_x) / n

    ph_value = m * vout + b
    return max(min(ph_value, 14), 0)


def calibrate():
    # start
    ph4  = []
    ph7  = []
    ph10 = []

    # ask to start
    start = input('PREPARE pH10 and start calibrating pH 4. Enter "y/Y" to continue. "n/N" to stop: ')
    if any([start == 'y', start == 'Y' ]):
        for i in tqdm(range(100)):
            time.sleep(0.1)
            ph10.append(fetch_ph_from_analog())
        print('Done!')
        print(statistics.mean(ph10))
    elif any([start == 'n', start == 'N' ]):
        return

    start = input('PREPARE pH4 and start calibrating pH 4. Enter "y/Y" to continue. "n/N" to stop: ')
    if any([start == 'y', start == 'Y' ]):
        for i in tqdm(range(100)):
            time.sleep(0.1)
            ph4.append(fetch_ph_from_analog())
        print('Done!')
        print(statistics.mean(ph4))
    elif any([start == 'n', start == 'N' ]):
        return
    
    start = input('PREPARE pH7 and start calibrating pH 4. Enter "y/Y" to continue. "n/N" to stop: ')
    if any([start == 'y', start == 'Y' ]):
        for i in tqdm(range(100)):
            time.sleep(0.1)
            ph7.append(fetch_ph_from_analog())
        print('Done!')
        print(statistics.mean(ph7))
    elif any([start == 'n', start == 'N' ]):
        return
    

    print(f'FINAL Voltage Averages: pH7 = {statistics.mean(ph7)}, pH4 = {statistics.mean(ph4)}, pH10 = {statistics.mean(ph10)}')


    with open('ph_calibration_report.log', 'a') as rd:
        rd.write('Calibration Report\n')
        rd.write('Using Analytical Grade pH calibration stds.\n')
        rd.write('--------------------------------\n')
        rd.write(f'pH4 - Avg Voltage Readings: {statistics.mean(ph4)}\n')
        rd.write(f'pH7 - Avg Voltage Readings: {statistics.mean(ph7)}\n')
        rd.write(f'pH10 - Avg Voltage Readings: {statistics.mean(ph10)}\n')
        rd.write('--------------------------------\n')
        rd.write('Raw Readings\n')
        rd.write(f'pH4 {"\n".join(ph4)}\n')
        rd.write(f'pH7 {"\n".join(ph7)}\n')
        rd.write(f'pH10 {"\n".join(ph10)}\n')

if __name__ == "__main__":
    while True:
        pH = voltage_to_ph()
        time.sleep(1.5)
        print(f"pH: {pH}")
