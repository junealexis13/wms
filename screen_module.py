import time
import board
import busio
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from temp_module import TemperatureModule  # import your DS18B20 reader class

# ──────────────────────────────────────────────
# Display Parameters
WIDTH = 128
HEIGHT = 64
LOOPTIME = 1.0  # seconds
# ──────────────────────────────────────────────

# I2C setup
i2c = board.I2C()

# OLED object
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display
oled.fill(0)
oled.show()

# Create drawing canvas
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load custom font
font = ImageFont.truetype(os.path.join("resources", "fonts", "PixelOperator.ttf"), 14)

# Temperature module (DS18B20)
temp_sensor = TemperatureModule()

# ──────────────────────────────────────────────
# Example functions for pH and NH3 placeholders
# Replace these later with your Arduino serial reads
# ──────────────────────────────────────────────
def read_ph():
    # Placeholder — replace with actual pH sensor read
    return 7.25

def read_nh3():
    # Placeholder — replace with actual NH3 sensor read
    return 0.15  # e.g., ppm
# ──────────────────────────────────────────────

while True:
    # Clear screen
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Header
    draw.text((0, 0), "ARDUINO-WMS v0.2", font=font, fill=255)

    # System stats (optional)
    try:
        cmd_ip = "hostname -I | cut -d' ' -f1"
        IP = subprocess.check_output(cmd_ip, shell=True).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        IP = "No IP"

    # Sensor readings
    temperature = temp_sensor.fetch_temp()
    if temperature is None:
        temperature = 0.0

    ph_value = read_ph()
    nh3_value = read_nh3()

    # Display section
    draw.text((0, 16), f"IP: {IP}", font=font, fill=255)
    draw.text((0, 30), f"Temp: {temperature:.2f} °C", font=font, fill=255)
    draw.text((0, 44), f"pH:   {ph_value:.2f}", font=font, fill=255)
    draw.text((70, 44), f"NH₃: {nh3_value:.2f}", font=font, fill=255)

    # Show updated image
    oled.image(image)
    oled.show()

    time.sleep(LOOPTIME)
