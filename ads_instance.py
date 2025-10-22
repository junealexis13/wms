import board
from adafruit_ads1x15.ads1115 import ADS1115

def get_ads():
    """Initialize ADS1115 once and reuse across sensors."""
    i2c = board.I2C()
    ads = ADS1115(i2c)
    ads.gain = 1  # ±4.096V
    return ads
