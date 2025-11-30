import asyncio
from bleak import BleakClient

class AuraLEDController:
    """
    Principal class
    """
    COMMAND_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"  
    def __init__(self, address: str):
        self.address = address
        self.client = BleakClient(address)

    async def connect(self):
        """
        Connect to the Aura LED
        """
        try:
            await self.client.connect()
            print("Connected")
        except Exception as e:
            print(f"Error: {e}")
    
    async def disconnect(self):
        """
        Disconnect from the Aura LED
        """
        try:
            await self.client.disconnect()
            print("Disconnected")
        except Exception as e:
            print(f"Error: {e}")
    
    async def send_command(self, cmd_bytes: list):
        """
        Send a command to the Aura LED
        """
        if len(cmd_bytes) != 9:
            return
        try:
            command = bytearray(cmd_bytes)
            await self.client.write_gatt_char(self.COMMAND_UUID, command)
        except Exception as e:
            print(f"Error: {e}")
    
    async def set_power(self, is_on: bool):
        """
        Turn ON / OFF the LED
        """
        cmd = [
            0x7e,
            0x00,
            0x04,
            0x01 if is_on else 0x00,
            0x00, 0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"LED {'ON' if is_on else 'OFF'}.")
    
    async def set_brightness(self, brightness: int):
        """
        Set brightness
        """
        if not (0 <= brightness <= 100):
            print("Error: Brightness out of range (0-100).")
            return
        cmd = [
            0x7e,
            0x00,
            0x01,
            brightness,
            0x00, 0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"🔆 Brillo ajustado a {brightness}%.")
    
    async def set_color_rgb(self, r: int, g: int, b: int):
        """
        Set color in RGB mode
        """
        for color, name in zip((r, g, b), ("R", "G", "B")):
            if not (0 <= color <= 255):
                print(f"Error: {name} out of range (0-255).")
                return
        cmd = [
            0x7e,
            0x00,
            0x05,
            0x03,
            r, g, b,
            0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f" Color changed to (R:{r}, G:{g}, B:{b}).")
    
    async def set_effect_speed(self, speed: int):
        """
        Set effect speed
        """
        if not (0 <= speed <= 100):
            print("Error: Speed out of range (0-100).")
            return
        cmd = [
            0x7e,
            0x00,
            0x02,
            speed,
            0x00, 0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Effect speed set to {speed}.")
        
    async def set_mode_grayscale(self):
        """
        Set grayscale mode
        """
        cmd = [
            0x7e,
            0x00,
            0x03,
            0x00,
            0x01,
            0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print("Grayscale mode enabled.")
    
    async def set_mode_temperature(self, temperature: int):
        """
            Set temperature mode
        """
        if not (128 <= temperature <= 138):
            print("Error: Temperature out of range (128-138).")
            return
        cmd = [
            0x7e,
            0x00,
            0x03,
            temperature,
            0x02,
            0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Temperature mode enabled with value {temperature}.")
    
    async def set_mode_effect(self, effect: int):
        """
        Set effect mode
        """
        cmd = [
            0x7e,
            0x00,
            0x03,
            effect,
            0x03,
            0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Effect mode enabled with code 0x{effect:02x}.")
    
    async def set_mode_dynamic(self, val: int):
        """
        Set dynamic mode
        """
        cmd = [
            0x7e,
            0x00,
            0x03,
            val,
            0x04,
            0x00, 0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Dynamic mode enabled with value {val}.")
    
    async def set_color_for_grayscale_mode(self, grayscale: int):
        """
        Set color for grayscale mode
        """
        if not (0 <= grayscale <= 100):
            print("Error: Grayscale out of range (0-100).")
            return
        cmd = [
            0x7e,
            0x00,
            0x05,
            0x01,
            grayscale,
            0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Grayscale mode enabled with value {grayscale}.")
    
    async def set_color_for_temperature_mode(self, temperature: int):
        """
        Set color for temperature mode
        """
        if not (0 <= temperature <= 100):
            print("Error: Temperature out of range (0-100).")
            return
        cmd = [
            0x7e,
            0x00,
            0x05,
            0x02,
            temperature,
            0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Temperature mode enabled with value {temperature}.")
    
    async def set_val_for_dynamic_mode(self, val: int):
        """
        Set value for dynamic mode
        """
        cmd = [
            0x7e,
            0x00,
            0x06,
            val,
            0x00, 0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Dynamic mode enabled with value {val}.")
    
    async def set_sensitivity_for_dynamic_mode(self, sensitivity: int):
        """
        Set sensitivity for dynamic mode
        
        Protocolo:
          7e 00 07 sensitivity 00 00 00 00 ef
        """
        cmd = [
            0x7e,
            0x00,
            0x07,
            sensitivity,
            0x00, 0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Sensitivity for dynamic mode set to {sensitivity}.")
    
    async def set_rgb_order(self, rgb_order: int):
        """
        Set RGB order
        """
        cmd = [
            0x7e,
            0x00,
            0x08,
            rgb_order,
            0x00, 0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"RGB order set to {rgb_order}.")
        
        cmd = [
            0x7e,
            0x00,
            0x08,
            rgb_order,
            0x00, 0x00, 0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"RGB order set to {rgb_order}.")
    
    async def set_rgb_order_custom(self, c1: int, c2: int, c3: int):
        """
        Set custom RGB order
        """
        cmd = [
            0x7e,
            0x00,
            0x81,
            c1, c2, c3,
            0x00, 0x00,
            0xef
        ]
        await self.send_command(cmd)
        print(f"Custom RGB order set to {c1}, {c2}, {c3}.")
    
    async def set_macro(self, macro_id: int):
        """
        Activate a macro sending an effect command.
        This method is an alias of set_mode_effect to use macros.
        """
        await self.set_mode_effect(macro_id)
        print(f"Macro activated with ID: {macro_id}.")