import Domoticz
from devices.device import Device


class SelectorSwitch(Device):
    SELECTOR_TYPE_BUTTONS = '0'
    SELECTOR_TYPE_MENU = '1'

    def __init__(self, devices, alias, value_key):
        super().__init__(devices, alias, value_key)

        self.level_names = []
        self.level_values = []
        self.selector_style = SelectorSwitch.SELECTOR_TYPE_MENU

    def add_level(self, name, value):
        self.level_names.append(name)
        self.level_values.append(value)

    def set_selector_style(self, selector_style):
        self.selector_style = selector_style

    def create_device(self, unit, device_id, device_name, message):
        options = {}
        options['LevelActions'] = ''
        options['LevelNames'] = '|'.join(self.level_names)
        options['LevelOffHiddden'] = 'false'
        options['SelectorStyle'] = self.selector_style

        return Domoticz.Device(Unit=unit, DeviceID=device_id, Name=device_name, TypeName="Selector Switch", Options=options, Image=9).Create()

    def get_numeric_value(self, value, device):
        return 1 if self.get_string_value(value, device) > 0 else 0

    def get_string_value(self, value, device):
        try:
            index = self.level_values.index(value)
        except:
            Domoticz.Debug('Unable to find selector switch level for value "' + value + '", device: ' + device.Name)
            index = 0

        return index * 10