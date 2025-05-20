import json

class MQTTPayloads:

    def __init__(self, device):
        self.device = device
        
        self.base_device = {
            "device": {
                "identifiers": [self.device.mac],
                "name": self.device.name_readable,
                "manufacturer": "Petkit",
                "model": self.device.product_name,
                "connections": [["mac", self.device.mac]],
                "serial_number": self.device.serial,
                "sw_version": self.device.firmware
            }
        }
        
        self.entities = {
            "voltage": {
                "name": "Voltage",
                "device_class": "voltage",
                "device_type": "sensor",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "V",
                "state_class": "measurement",
                "value_template": "{{ value_json.voltage }}",
                "entity_category": "diagnostic"
            },
            "battery": {
                "name": "Battery",
                "device_class": "battery",
                "device_type": "binary_sensor",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "value_template": "{{ value_json.battery }}",
                "entity_category": "diagnostic"
            },
            "energy_consumed": {
                "name": "Energy Consumption",
                "device_class": "energy",
                "device_type": "sensor",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "kWh",
                "state_class": "total_increasing",
                "value_template": "{{ value_json.energy_consumed }}",
                "entity_category": "diagnostic"
            },
            "filter_time_left": {
                "name": "Filter time left",
                "device_type": "sensor",
                "icon": "mdi:timelapse",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "days",
                "value_template": "{{ value_json.filter_time_left }}"
            },
            "rssi": {
                "name": "RSSI",
                "device_class": "signal_strength",
                "device_type": "sensor",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "dBm",
                "value_template": "{{ value_json.rssi }}",
                "entity_category": "diagnostic"
            },
            "power_status": {
                "name": "Power",
                "device_class": "power",
                "device_type": "binary_sensor",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "value_template": "{{ value_json.power_status }}",
                "entity_category": "diagnostic"
            },
            "mode": {
                "name": "Mode",
                "device_class": "select",
                "icon": "mdi:auto-mode",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "options": ["Normal", "Smart Mode"],
                "command_template": "{% if value == 'Normal' %} {{ '{ \"mode\": 1 }' }} {% elif value == 'Smart Mode' %} {{ '{ \"mode\": 2 }' }} {% endif %}",
                "value_template": "{% if value_json.mode == 1 %} Normal {% elif value_json.mode == 2 %} Smart Mode {% else %} Unknown {% endif %}"
            },
            "dnd_state": {
                "name": "Do Not Disturb State",
                "device_type": "binary_sensor",
                "icon": "mdi:cancel",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "value_template": "{{ value_json.dnd_state }}",
            },
            "warning_breakdown": {
                "name": "Warning - Breakdown",
                "device_class": "problem",
                "device_type": "binary_sensor",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "value_template": "{{ value_json.warning_breakdown }}"
            },
            "warning_water_missing": {
                "name": "Warning - Water Missing",
                "device_class": "problem",
                "device_type": "binary_sensor",
                "icon": "mdi:water-alert",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "value_template": "{{ value_json.warning_water_missing }}"
            },
            "warning_filter": {
                "name": "Warning - Filter",
                "device_class": "problem",
                "device_type": "binary_sensor",
                "icon": "mdi:alert-circle",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "value_template": "{{ value_json.warning_filter }}"
            },
            "pump_runtime": {
                "name": "Pump Runtime",
                "device_type": "sensor",
                "icon": "mdi:water-sync",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "value_template": "{{ value_json.pump_runtime_readable }}",
                "payload_available": "online",
                "payload_not_available": "offline",
                "entity_category": "diagnostic"
            },
            "pump_runtime_today": {
                "name": "Pump Runtime Today",
                "device_type": "sensor",
                "icon": "mdi:water-sync",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "value_template": "{{ value_json.pump_runtime_today_readable }}",
                "entity_category": "diagnostic"
            },
            "purified_water": {
                "name": "Purified Water",
                "device_type": "sensor",
                "icon": "mdi:air-filter",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "count",
                "value_template": "{{ value_json.purified_water | float | round }}",
                "entity_category": "diagnostic"
            },
            "purified_water_today": {
                "name": "Purified Water Today",
                "device_type": "sensor",
                "icon": "mdi:air-filter",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "count",
                "value_template": "{{ value_json.purified_water_today | float | round }}",
                "entity_category": "diagnostic"
            },
            "filter_percentage": {
                "name": "Filter Percentage",
                "device_type": "sensor",
                "icon": "mdi:percent-circle-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "%",
                "value_template": "{{ value_json.filter_percentage * 100 }}",
                "entity_category": "diagnostic"
            },
            "running_status": {
                "name": "Running status",
                "device_class": "running",
                "device_type": "binary_sensor",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "value_template": "{{ value_json.running_status }}"
            },
            "set_smart_time_on": {
                "name": "Smart Mode Time On",
                "device_type": "number",
                "icon": "mdi:timer-check-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "minutes",
                "min": 1, 
                "max": 10, 
                "step": 1, 
                "command_template": "{\"smart_time_on\": {{ value }} }",
                "value_template": "{{ value_json.smart_time_on }}",
                "entity_category": "config"
            },
            "set_smart_time_off": {
                "name": "Smart Mode Time Off",
                "device_type": "number",
                "icon": "mdi:timer-cancel-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "minutes",
                "min": 1, 
                "max": 10, 
                "step": 1, 
                "command_template": "{\"smart_time_off\": {{ value }} }",
                "value_template": "{{ value_json.smart_time_off }}",
                "entity_category": "config"
            },
            "smart_time_on": {
                "name": "Smart Mode Time On",
                "device_type": "sensor",
                "icon": "mdi:timer-check-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "minutes",
                "value_template": "{{ value_json.smart_time_on }}"
            },
            "smart_time_off": {
                "name": "Smart Mode Time Off",
                "device_type": "sensor",
                "icon": "mdi:timer-cancel-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "minutes",
                "value_template": "{{ value_json.smart_time_off }}"
            },
            "led_switch": {
                "name": "LED Switch",
                "device_class": "switch",
                "icon": "mdi:lightbulb-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "command_template": "{\"led_switch\": {{ value }} }",
                "value_template": "{{ value_json.led_switch }}",
            },
            "led_brightness": {
                "name": "LED Brightness",
                "device_class": "select",
                "icon": "mdi:brightness-5",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "options": ["Low", "Medium", "High"],
                "command_template": "{% if value == 'Low' %} {{ '{ \"led_brightness\": 1 }' }} {% elif value == 'Medium' %} {{ '{ \"led_brightness\": 2 }' }} {% elif value == 'High' %} {{ '{ \"led_brightness\": 3 }' }} {% endif %}",
                "value_template": "{% if value_json.led_brightness == 1 %} Low {% elif value_json.led_brightness == 2 %} Medium {% elif value_json.led_brightness == 3 %} High {% else %} Unknown {% endif %}"
            },
            "led_light_time_on": {
                "name": "LED Light Time On",
                "device_type": "sensor",
                "icon": "mdi:timer-check-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "value_template": "{{ value_json.led_light_time_on_readable }}"
            },
            "set_led_light_time_on": {
                "name": "LED Light Time On",
                "device_type": "number",
                "icon": "mdi:timer-check-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "unit_of_measurement": "minutes",
                "min": 0, 
                "max": 24, 
                "step": 0.25, 
                "command_template": "{\"led_on\": {{ value }} }",
                "value_template": "{% set time = value_json.led_light_time_on_readable %}\n{% set hour, minute = time.split(':') %}\n{% set decimal_minute = (minute | int / 60 * 100) %}\n{{ (hour | int) + (decimal_minute / 100) }}",
                "entity_category": "config"
            },
            "led_light_time_off": {
                "name": "LED Light Time Off",
                "device_type": "sensor",
                "icon": "mdi:timer-cancel-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "value_template": "{{ value_json.led_light_time_off_readable }}"
            },
            "set_led_light_time_off": {
                "name": "LED Light Time Off",
                "device_type": "number",
                "icon": "mdi:timer-cancel-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "min": 0, 
                "max": 24, 
                "step": 0.25, 
                "command_template": "{\"led_off\": {{ value }} }",
                "value_template": "{% set time = value_json.led_light_time_off_readable %}\n{% set hour, minute = time.split(':') %}\n{% set decimal_minute = (minute | int / 60 * 100) %}\n{{ (hour | int) + (decimal_minute / 100) }}",
                "entity_category": "config"
            },
            "do_not_disturb_switch": {
                "name": "Do Not Disturb Switch",
                "device_class": "switch",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "command_template": "{\"do_not_disturb_switch\": {{ value }} }",
                "value_template": "{{ value_json.do_not_disturb_switch }}"
            },
            "do_not_disturb_time_on": {
                "name": "Do Not Disturb Time On",
                "device_type": "sensor",
                "icon": "mdi:timer-check-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "value_template": "{{ value_json.do_not_disturb_time_on_readable }}"
            },
            "set_do_not_disturb_time_on": {
                "name": "Do Not Disturb Time On",
                "device_type": "number",
                "icon": "mdi:timer-check-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "min": 0, 
                "max": 24, 
                "step": 0.25, 
                "command_template": "{\"dnd_on\": {{ value }} }",
                "value_template": "{% set time = value_json.do_not_disturb_time_on_readable %}\n{% set hour, minute = time.split(':') %}\n{% set decimal_minute = (minute | int / 60 * 100) %}\n{{ (hour | int) + (decimal_minute / 100) }}",
                "entity_category": "config"
            },
            "do_not_disturb_time_off": {
                "name": "Do Not Disturb Time Off",
                "device_type": "sensor",
                "icon": "mdi:timer-cancel-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "value_template": "{{ value_json.do_not_disturb_time_off_readable }}"
            },
            "set_do_not_disturb_time_off": {
                "name": "Do Not Disturb Time Off",
                "device_type": "number",
                "icon": "mdi:timer-cancel-outline",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "min": 0, 
                "max": 24, 
                "step": 0.25, 
                "command_template": "{\"dnd_off\": {{ value }} }",
                "value_template": "{% set time = value_json.do_not_disturb_time_off_readable %}\n{% set hour, minute = time.split(':') %}\n{% set decimal_minute = (minute | int / 60 * 100) %}\n{{ (hour | int) + (decimal_minute / 100) }}",
                "entity_category": "config"
            },
            "is_locked": {
                "name": "Locked",
                "device_class": "lock",
                "device_type": "binary_sensor",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 0,
                "payload_off": 1,
                "value_template": "{{ value_json.is_locked }}"
            },
            #"filter_reset": {
            #    "name": "Reset filter",
            #    "device_type": "button",
            #    "icon": "mdi:restart-alert",
            #    "unique_id": f"{self.device.mac_readable}",
            #    "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
            #    "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
            #    "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
            #    "payload_available": "online",
            #    "payload_not_available": "offline",
            #    "payload_on": 1,
            #    "payload_off": 0,
            #    "value_template": "{\"reset_filter\": \"{{ value }}\"}"
            #},
            "filter_reset": {
                "name": "Reset filter",
                "device_type": "button",
                "icon": "mdi:restart-alert",
                "unique_id": f"{self.device.mac_readable}",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_press": "1",
                "command_template": "{\"reset_filter\": {{ value }} }"
            },
            "state_switch": {
                "name": "Run",
                "device_class": "switch",
                "icon": "mdi:play-pause",
                "unique_id": f"{self.device.mac_readable}",
                "state_topic": f"PetkitMQTT/{self.device.mac_readable}/state",
                "command_topic": f"PetkitMQTT/{self.device.mac_readable}/command",
                "availability_topic": f"PetkitMQTT/{self.device.mac_readable}/availability",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_on": 1,
                "payload_off": 0,
                "command_template": "{\"state\": {{ value }} }",
                "value_template": "{{ value_json.running_status }}",
            },
        }

    def discovery(self):  
        
        discovery_entities = []
        
        for entity, data in self.entities.items():
            
            if "device_class" in data:
                device_class = data['device_class']
            
            if "device_type" in data:
                device_class = data['device_type']
                data.pop('device_type')
            
            temp_entity = {}
            temp_entity.update(data)
            temp_entity.update({"unique_id": f"{data['unique_id']}_{entity}"})
            temp_entity.update({"config_topic": f"homeassistant/{device_class}/{data['unique_id']}/{entity}/config"})
            temp_entity.update(self.base_device)
            
            discovery_entities.append(temp_entity)
    
        return discovery_entities
    