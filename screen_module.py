import time
import board
import busio
import os
import subprocess
import datetime
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from temp_module import TemperatureModule 
from ph_module import voltage_to_ph
from nh3_module import calculate_nh3_from_analog, fetch_ammonia_from_analog

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

    time.sleep(0.5)
    ph_value = voltage_to_ph()
    time.sleep(0.5) # added delay
    nh3_value, rs, ratio = calculate_nh3_from_analog(fetch_ammonia_from_analog())

    # Display sections
    draw.text((0, 16), f"NH3: {nh3_value:.2f} | Rs{rs:.2f}", font=font, fill=255)
    draw.text((0, 30), f"Temp: {temperature:.2f} °C", font=font, fill=255)
    draw.text((0, 44), f"pH:   {ph_value:.2f}", font=font, fill=255)


    # Show updated image
    oled.image(image)
    oled.show()

    print(f"[{datetime.datetime.now()}] pH {ph_value:.2f} | NH3 {nh3_value:.2f} ppm | Temp {temperature:.2f} °C")

    with open('logging.log', 'a') as rd:
        rd.write(f"[{datetime.datetime.now()}] pH {ph_value:.2f} | NH3 {nh3_value:.2f} ppm | Temp {temperature:.2f} °C")
        rd.close()
    time.sleep(LOOPTIME)
