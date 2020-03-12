import time
import asyncio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw import neopixel
import board
import busio


class Neo:
    def __init__(self):
        self.num_pixels = 8
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.ss = Seesaw(self.i2c_bus)
        self.pin = 25
        self.pixels = None
        self.colors = {
            'WHITE': (255, 255, 255),
            'RED': (255, 0, 0),
            'YELLOW': (255, 255, 0),
            'ORANGE': (255, 165, 0),
            'LIME': (0, 255, 0),
            'GREEN': (0, 128, 0),
            'CYAN': (0, 255, 255),
            'BLUE': (0, 0, 255),
            'PURPLE': (180, 0, 255)
        }

    async def set_pixel(self, pixel, color):
        self.pixels = neopixel.NeoPixel(self.ss, self.pin, self.num_pixels,
                                        brightness=0.2, auto_write=False)
        self.pixels[pixel] = self.colors[color]
        self.pixels.show()
        return (True)

    def clear(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        return (True)

    def wheel(self, pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b)

    async def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    async def test_display(self):
        ORDER = neopixel.RGB
        self.pixels = neopixel.NeoPixel(self.ss, self.pin, self.num_pixels,
                                        brightness=0.2, auto_write=False,
                                        pixel_order=ORDER)
        self.pixels.fill((255, 0, 0))
        self.pixels.show()
        time.sleep(1)
        self.pixels.fill((0, 255, 0))
        self.pixels.show()
        time.sleep(1)
        self.pixels.fill((0, 0, 255))
        self.pixels.show()
        time.sleep(1)
        await self.rainbow_cycle(0.001)
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        return (True)
