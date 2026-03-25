#!/usr/bin/env python

from gfxhat import lcd, backlight, fonts
from gfxhat.st7567 import ST7567_SETCONTRAST
from PIL import Image, ImageFont, ImageDraw
import time


def set_contrast(c):
    lcd.st7567.setup()
    lcd.st7567._command([ST7567_SETCONTRAST, c])

print("""

GFX HAT - Contrast Scanner

This example scans through the available contrast values, from 20 to 63,
and displays this on the LCD. This is then repeated with the backlight
set to white.

Contrast values below around 20 are not visible and are skipped.

Press Ctrl+C to exit.

""")

font = ImageFont.truetype(fonts.Bitocra13Full, 13)

width, height = lcd.dimensions()

image = Image.new("1", (128, 64), "black")
draw = ImageDraw.Draw(image)


def scan_contrast():
    for c in range(25, 64):
        draw.rectangle((0, 0, width, height), "black")

        message = "Contrast: {:02d}".format(c)

        bbox = font.getbbox(message)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        left, top = (width - w) / 2, (height - h) / 2

        draw.text((left, top), message, 1, font=font)

        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x, y))
                lcd.set_pixel(x, y, pixel)

        set_contrast(c)
        lcd.show()
        time.sleep(0.4)

    lcd.clear()
    lcd.show()


lcd.show()

backlight.set_all(0, 0, 0)
backlight.show()


try:
    set_contrast(0)
    scan_contrast()

    set_contrast(0)
    backlight.set_all(255, 255, 255)
    backlight.show()

    scan_contrast()
    set_contrast(0)

    backlight.set_all(0, 0, 0)
    backlight.show()
    print("Done!")

except KeyboardInterrupt:
    set_contrast(0)
    backlight.set_all(0, 0, 0)
    backlight.show()
    print("Quit via keyboard.")
