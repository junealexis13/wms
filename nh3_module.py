import time
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ads1x15.ads1115 as ADS


def fetch_ammonio_from_analog():
    # I2C setup
    i2c = busio.I2C(board.SCL, board.SDA)

    # ADS1115 setup
    ads = ADS.ADS1115(i2c)
    ads.gain = 1  # Gain = 1 for 0-4.096V range

    # MQ135 connected to A0
    chan = AnalogIn(ads, ADS.P0)
    return chan.value, chan.voltage