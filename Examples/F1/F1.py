from livef1.adapters.realtime_client import RealF1Client
import time
from LedBLELib import AuraLEDController
import asyncio

LED_MAC_ADDRESS = "78:9C:E7:0F:E3:79"
DELAY_TV_SECONDS = 34

led = AuraLEDController(LED_MAC_ADDRESS)

latest_timing_data_list = []
driver_list = []

flagsColors = {
    "AllClear": (0, 255, 0),
    "Yellow": (255, 255, 0),
    "Red": (255, 0, 0),
    "SafetyCar": (255, 165, 0),
    "VirtualSafetyCar": (0, 0, 255),
    "DoubleYellow": (255, 255, 0),
}

race = RealF1Client(["SessionStatus", "TimingDataF1", "TrackStatus", "DriverList"])

def hex_a_rgb(codigo_hex):
    if not codigo_hex or not isinstance(codigo_hex, str):
        return (255, 255, 255)
    codigo_hex = codigo_hex.lstrip('#')
    if len(codigo_hex) != 6:
        return (255, 255, 255)
    try:
        return (int(codigo_hex[0:2], 16), int(codigo_hex[2:4], 16), int(codigo_hex[4:6], 16))
    except ValueError:
        return (255, 255, 255)

async def ejecutar_con_delay(corutina, *args):
    """Espera X segundos y luego ejecuta la función de luces"""
    await asyncio.sleep(DELAY_TV_SEGUNDOS)
    await corutina(*args)

async def inicializar_luces():
    try:
        await led.connect()
        await led.set_power(True)
        await led.set_brightness(100)
        await led.set_color_rgb(255, 0, 0)
    except Exception as e:
        print(f"Warning: Could not connect to the lights: {e}")

async def LucesFlag(bandera):
    print(f"Executing lights (TV Sync): {bandera}")
    r, g, b = flagsColors.get(bandera, (255, 255, 255))
    try:
        await led.set_color_rgb(r, g, b)
    except:
        pass

async def LucesCorredor(NumeroCorredor, lista):
    for piloto in lista:  
        if piloto.get('RacingNumber') == NumeroCorredor:
            nombre = piloto.get("FullName")
            color_hex = piloto.get("TeamColour")
            print(f"Winner (TV Sync): {nombre}")
            r, g, b = hex_a_rgb(color_hex)
            try:
                await led.set_color_rgb(r, g, b)
            except:
                pass
            return 
    print(f"No information found for driver {NumeroCorredor}")


@race.callback("driver_list")
async def handle_driver_list(records):
    global driver_list
    lista_temporal = records.get("DriverList")
    if lista_temporal is None and isinstance(records, list):
        driver_list = records
    elif lista_temporal:
        driver_list = lista_temporal

@race.callback("timing_data_f1")
async def handle_timing_data(records):
    global latest_timing_data_list
    timing_data = records.get("TimingDataF1")
    if timing_data is None and isinstance(records, list):
        latest_timing_data_list = records
    elif timing_data:
        latest_timing_data_list = timing_data

@race.callback("track_status")
async def handle_new_flag(records):
    bandera_data = records.get("TrackStatus")
    if bandera_data is None and isinstance(records, list):
         bandera_data = records

    if bandera_data and isinstance(bandera_data, list):
        mensaje = bandera_data[0].get('Message') 
        if mensaje:
            asyncio.create_task(ejecutar_con_delay(LucesFlag, mensaje))


@race.callback("session_status")
async def handle_session_status(records):
    estado = records.get("status")
    session_info = records.get("SessionStatus")

    if not estado and session_info and isinstance(session_info, list) and session_info:
        estado = session_info[0].get("status")

    if estado in ("Finished", "Ends"):
        print(f"🏁 Race finished in data. Waiting {DELAY_TV_SEGUNDOS}s to show winner...")
        
        datos_tiempo_actuales = list(latest_timing_data_list) 
        lista_pilotos_actual = list(driver_list)

        async def procesar_ganador_diferido():
            if datos_tiempo_actuales:
                ganador = next(
                    (driver for driver in datos_tiempo_actuales if driver.get('Position') == '1'),
                    None
                )
                if ganador:
                    driver_no = ganador.get('DriverNo', 'N/A')
                    await LucesCorredor(driver_no, lista_pilotos_actual)
                else:
                    print("No P1 found in saved data.")

        asyncio.create_task(ejecutar_con_delay(procesar_ganador_diferido))

async def main():
    print(f"Starting F1 client with {DELAY_TV_SEGUNDOS}s delay...")
    await inicializar_luces()
    await race._async_run()

if __name__ == "__main__":
    asyncio.run(main())