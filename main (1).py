import logging
from abc import ABC, abstractmethod
from datetime import datetime

# Define an abstract base Device class.
class Device(ABC):
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.is_on = False

    @abstractmethod
    def status(self):
        pass


# Concrete device classes inheriting from Device.
class Light(Device):
    def __init__(self, device_id):
        super().__init__(device_id, "Light")

    def status(self):
        return f"{self.device_type} {self.device_id} is {'On' if self.is_on else 'Off'}."


class Thermostat(Device):
    def __init__(self, device_id):
        super().__init__(device_id, "Thermostat")
        self.temperature = 0

    def set_temperature(self, temperature):
        self.temperature = temperature

    def status(self):
        return f"{self.device_type} {self.device_id} is {'On' if self.is_on else 'Off'}. Thermostat is set to {self.temperature} degrees."


# Central hub to manage devices.
class SmartHomeSystem:
    def __init__(self):
        self.devices = {}
        self.scheduled_tasks = []
        self.automated_triggers = []

    def add_device(self, device_id, device_type):
        if device_type == "Light":
            self.devices[device_id] = Light(device_id)
        elif device_type == "Thermostat":
            self.devices[device_id] = Thermostat(device_id)

    def remove_device(self, device_id):
        if device_id in self.devices:
            del self.devices[device_id]

    def get_device_status(self, device_id):
        if device_id in self.devices:
            return self.devices[device_id].status()
        else:
            return "Device not found."

    def list_all_devices(self):
        return [self.devices[device_id].status() for device_id in self.devices]

    def add_scheduled_task(self, device_id, time, command):
        self.scheduled_tasks.append({"device": device_id, "time": time, "command": command})

    def add_automated_trigger(self, condition, action):
        self.automated_triggers.append({"condition": condition, "action": action})

    def execute_scheduled_tasks(self):
        current_time = datetime.now().strftime("%H:%M")
        for task in self.scheduled_tasks:
            if task["time"] == current_time:
                self.execute_command(task["device"], task["command"])

    def execute_automated_triggers(self):
        for trigger in self.automated_triggers:
            condition = trigger["condition"]
            action = trigger["action"]
            if eval(condition):
                self.execute_command(action)

    def execute_command(self, device_id, command):
        if device_id in self.devices:
            device = self.devices[device_id]
            if command.lower() == "turn on":
                device.is_on = True
            elif command.lower() == "turn off":
                device.is_on = False
        else:
            logging.error("Device not found for command execution.")


# Usage example and output generation:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Enable logging

    home_system = SmartHomeSystem()

    home_system.add_device(1, "Light")
    home_system.add_device(2, "Thermostat")

    home_system.devices[1].is_on = True
    home_system.devices[2].set_temperature(70)

    home_system.add_scheduled_task(2, "06:00", "Turn On")
    home_system.add_automated_trigger("home_system.devices[2].temperature > 75", "Turn Off(1)")

    home_system.execute_scheduled_tasks()
    home_system.execute_automated_triggers()

    # Output
    print("Status Report:", ", ".join(home_system.list_all_devices()) + ".")
    print("Scheduled Tasks:", home_system.scheduled_tasks)
    print("Automated Triggers:", home_system.automated_triggers)

