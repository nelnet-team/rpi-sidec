"""Main module."""
import asyncio
from display import display
import time
import RPi.GPIO as GPIO
import functools


def gpio_interrupt():
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
def wait_for_interrupt():
    print("Entering wait_for_interrupt")
    resp = gpio_interrupt()
    return (resp)


async def process_interrupt(obj):
    print("Entering process_interrupt")
    res = await wait_for_interrupt()
    print("Interupt triggered")


async def display_info(obj):
    while True:
        try:
            task = asyncio.create_task(obj.display_sys_info())
            await process_interrupt(obj)
            task.cancel()
            task = asyncio.create_task(obj.display_interface())
            await process_interrupt(obj)
            task.cancel()
        except asyncio.CancelledError:
            return ()


async def main():
    obj = display.DisplayInfo()
    await asyncio.create_task(display_info(obj))

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # loop.stop
        print('Terminated\n')
