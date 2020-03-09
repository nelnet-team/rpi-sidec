"""Main module."""
import asyncio
from display import display


async def main(obj):
    await obj.display_interface()

if __name__ == '__main__':
    displayinfo = display.DisplayInfo()
    try:
        asyncio.run(main(displayinfo))
    except KeyboardInterrupt:
        print('Terminated\n')
