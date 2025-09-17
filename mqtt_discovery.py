# PetkitW5BLEMQTT/mqtt_discovery.py
import json

class MQTTDiscovery:
    def __init__(self, mqtt_client, logger):
        self.mqtt_client = mqtt_client
        self.logger = logger
    
    async def setup_ha_discovery(self, device):
        """Setup Home Assistant MQTT Auto-Discovery"""
        try:
            # Сенсор уровня воды
            water_config = {
                "name": f"Petkit {device.name_readable} Water Level",
                "device_class": "water",
                "state_topic": f"petkit/{device.mac}/state",
                "value_template": "{{ value_json.water_level }}",
                "unit_of_measurement": "%",
                "device": {
                    "identifiers": [f"petkit_{device.mac}"],
                    "name": device.name_readable,
                    "manufacturer": "Petkit",
                    "model": device.product_name
                }
            }
            
            # Сенсор батареи
            battery_config = {
                "name": f"Petkit {device.name_readable} Battery",
                "device_class": "battery",
                "state_topic": f"petkit/{device.mac}/state",
                "value_template": "{{ value_json.battery }}",
                "unit_of_measurement": "%",
                "device": {
                    "identifiers": [f"petkit_{device.mac}"]
                }
            }
            
            # Публикуем конфигурации
            await self.mqtt_client.publish(
                f"homeassistant/sensor/petkit_{device.mac}_water/config",
                json.dumps(water_config)
            )
            
            await self.mqtt_client.publish(
                f"homeassistant/sensor/petkit_{device.mac}_battery/config", 
                json.dumps(battery_config)
            )
            
            self.logger.info("Home Assistant MQTT Auto-Discovery setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up HA discovery: {e}")
