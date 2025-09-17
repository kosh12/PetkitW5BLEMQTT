import json
import asyncio
from .utils import Utils

class Commands:
    def __init__(self, ble_manager, device, logger):
        self.ble_manager = ble_manager
        self.device = device
        self.logger = logger
        if hasattr(ble_manager, 'mac') and ble_manager.mac is not None:
            self.mac = ble_manager.mac
        else:
            self.mac = None
            self.logger.warning("ble_manager.mac is not available")
        self.sequence = 0
        
    def increment_sequence(self):
        self.sequence += 1
        if self.sequence > 255:
            self.sequence = 0
    
    async def update_device_state(self):
        """Обновляем состояние устройства после изменений"""
        await asyncio.sleep(1)  # Ждем выполнение команды
        await self.device.update_if_needed(self, force=True)
        self.logger.info("Device state updated after command")
    
    def init_device_data(self):
        connectiondata = self.ble_manager.connectiondata[self.device.mac].details
        self.device.status = {"rssi": connectiondata['props']['RSSI']}
        
        discovered_bytes = Utils.bytes_to_unsigned_integers(Utils.combine_byte_arrays(connectiondata['props']['ServiceData']))
        device_integer_identifier = discovered_bytes[5]

        self.logger.debug(f"Received ServiceData {discovered_bytes}")
        
        device_properties = Utils.get_device_properties(device_integer_identifier)
        
        self.device.name = device_properties['name']
        self.device.name_readable = device_properties['name'].replace("_", " ")
        self.device.product_name = device_properties['product_name']
        self.device.device_type = device_properties['device_type']
        self.device.type_code = device_properties['type_code']
    
    async def init_device_connection(self):
        await self.get_device_details()
        await asyncio.sleep(1.5)
        
        await self.init_device()
        
        await self.get_device_sync()
        await asyncio.sleep(0.75)
        await self.set_datetime()
        await asyncio.sleep(0.75)
        
        while self.device.serial in "Uninitialized" or self.device.serial == 0:
            await self.get_device_details()
            await asyncio.sleep(1.5)
        
        if not self.device.device_initialized:
            await self.init_device()
            await asyncio.sleep(3.0)
            
            await self.ble_manager.disconnect_device(self.mac)
            await asyncio.sleep(1.0)
            await self.ble_manager.connect_device(self.mac)
            await asyncio.sleep(1.0)
            await self.init_device_connection()

        await self.get_device_info()
        await asyncio.sleep(0.75)
        await self.get_device_type()
        await asyncio.sleep(0.75)
        await self.get_battery()
        await asyncio.sleep(0.75)
        await self.get_device_state()
        await asyncio.sleep(0.75)
        await self.get_device_config()

    async def get_battery(self):
        cmd = 66
        type = 1
        seq = self.sequence
        data = [0, 0]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return

    async def init_device(self):
        cmd = 73
        type = 1
        seq = self.sequence

        self.secret = Utils.pad_array(Utils.replace_last_two_if_zero(Utils.reverse_unsigned_array(self.device.device_id_bytes)), 8)
        device_id = Utils.pad_array(self.device.device_id_bytes, 8)
        
        data = [0, 0] + device_id + self.secret
        self.logger.debug(f"Device ID: {device_id}")
        self.logger.debug(f"Secret: {self.secret}")
        self.logger.debug(f"Data: {data}")
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return

    async def set_datetime(self):
        cmd = 84
        type = 1
        seq = self.sequence
        data = Utils.time_in_bytes()
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return

    async def get_device_sync(self):
        cmd = 86
        type = 1
        seq = self.sequence
        data = [0, 0] + self.secret
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return

    async def get_device_info(self):
        cmd = 200
        type = 1
        seq = self.sequence
        data = []
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return
        
    async def get_device_type(self):
        cmd = 201
        type = 1
        seq = self.sequence
        data = []
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return
        
    async def get_device_state(self):
        cmd = 210
        type = 1
        seq = self.sequence
        data = [0, 0]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return
        
    async def get_device_config(self):
        cmd = 211
        type = 1
        seq = self.sequence
        data = [0, 0]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return

    async def get_device_details(self):
        if self.device.device_id:
            return
        
        cmd = 213
        type = 1
        seq = self.sequence
        data = [0, 0]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return

    async def set_light_setting(self, state):
        cmd = 215
        type = 1
        seq = self.sequence
        data = [state]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        self.device.on_led_changed()  # ← ПОМЕЧАЕМ ДЛЯ ОБНОВЛЕНИЯ
        return

    async def set_dnd_setting(self, state):
        cmd = 216
        type = 1
        seq = self.sequence
        data = [state]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        self.device.on_dnd_changed()  # ← ПОМЕЧАЕМ ДЛЯ ОБНОВЛЕНИЯ
        return

    async def set_device_mode(self, state, mode):
        cmd = 220
        type = 1
        seq = self.sequence
        data = [state, mode]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        self.device.on_mode_changed()  # ← ПОМЕЧАЕМ ДЛЯ ОБНОВЛЕНИЯ
        return

    async def set_device_config(self, data):
        cmd = 221
        type = 1
        seq = self.sequence
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        self.device.mark_all_for_update()  # ← ПОМЕЧАЕМ ДЛЯ ОБНОВЛЕНИЯ
        return

    async def set_reset_filter(self):
        cmd = 222
        type = 1
        seq = self.sequence
        data = [0]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        self.device.on_filter_reset()  # ← ПОМЕЧАЕМ ДЛЯ ОБНОВЛЕНИЯ
        return

    async def set_updated_light(self, state):
        cmd = 225
        type = 1
        seq = self.sequence
        data = [state]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        self.device.on_led_changed()  # ← ПОМЕЧАЕМ ДЛЯ ОБНОВЛЕНИЯ
        return

    async def set_updated_dnd(self, state):
        cmd = 226
        type = 1
        seq = self.sequence
        data = [state]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        self.device.on_dnd_changed()  # ← ПОМЕЧАЕМ ДЛЯ ОБНОВЛЕНИЯ
        return
        
    async def get_device_update(self):
        cmd = 230
        type = 2
        seq = self.sequence
        data = [1]
        
        bytes = Utils.build_command(seq, cmd, type, data)
        await self.ble_manager.message_producer(bytes)
        
        self.increment_sequence()
        self.logger.info(f"Queued command: {cmd}")
        return
