import asyncio
import time
import re
from LedBLELib import * 

LOG_PATH = "/home/agus/.minecraft/logs/latest.log"

LED_MAC_ADDRESS = "78:9C:E7:0F:E3:79"
led = AuraLEDController(LED_MAC_ADDRESS)

i = 1
last_line_checked = None  

async def flash_red():
    global i
    if i == 1:
        await led.connect()
    
    await led.set_power(True)
    
    await led.set_color_rgb(255, 0, 0)
    await led.set_brightness(100)
    await asyncio.sleep(0.5)  
    
    await led.set_color_rgb(255, 255, 255)
    await led.set_brightness(128)
    i += 1

def check_damage():
    global last_line_checked
    with open(LOG_PATH, "r", encoding="utf-8") as log:
        lines = log.readlines()
        if not lines:
            return False

        current_line = lines[-1].strip()  

        if current_line == last_line_checked:
            return False
        else:
            last_line_checked = current_line  
        if re.search(
            r"\[CHAT\].*?(se cayó de un lugar muy alto|fue asesinado|sufrió daño|hit the ground too hard|fue disparado por|fue abatido por|murió|se quem[oó] hasta morir|se ahog[oó]|fue quemado|was shot by|was slain by|was killed by|burned to death|blew up|was blown up by|fell out of the world|fell from a high place)",
            current_line,
            re.IGNORECASE,
        ):
            return True

    return False

async def main():
    while True:
        if check_damage():
            await flash_red()
        time.sleep(1)  


asyncio.run(main())
