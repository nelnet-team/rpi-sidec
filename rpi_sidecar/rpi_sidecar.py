"""Main module."""
import asyncio
from display import display
from neo import neo
import time
import RPi.GPIO as GPIO
import functools


class RpiSidecar:
    def __init__(self):
        self.neo = neo.Neo()
        self.display = display.DisplayInfo()

    def gpio_interrupt(self):
        print("Entering gpio_interrupt")
        time.sleep(0.2)
        pin = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.wait_for_edge(pin, GPIO.FALLING)
        return (True)

    def run_in_executor(f):
        # Decorator to run a function in an executor
        @functools.wraps(f)
        def inner(*args, **kwargs):
            loop = asyncio.get_running_loop()
            return loop.run_in_executor(None, lambda: f(*args, **kwargs))
        return inner

    # Create an executor to make the interrupt awaitable
    @run_in_executor
    def wait_for_interrupt(self):
        print("Entering wait_for_interrupt")
        resp = self.gpio_interrupt()
        return (resp)

    async def process_interrupt(self):
        print("Entering process_interrupt")
        res = await self.wait_for_interrupt()
        print("Interupt triggered")

    async def display_info(self):
        while True:
            try:
                task = asyncio.create_task(self.display.display_sys_info())
                await self.process_interrupt()
                task.cancel()
                task = asyncio.create_task(self.display.display_interface())
                await self.process_interrupt()
                task.cancel()
            except asyncio.CancelledError:
                return ()

    async def start_neo(self):
        task = asyncio.create_task(self.neo.test_display())
        asyncio.create_task(self.neo.set_pixel(0, 'RED'))

    def shutdown(self):
        self.neo.clear()

    async def main(self):
        await asyncio.gather(self.display_info(), self.start_neo())


if __name__ == '__main__':
    try:
        obj = RpiSidecar()
        asyncio.run(obj.main())
    except KeyboardInterrupt:
        obj.shutdown()
        print('Terminated\n')
