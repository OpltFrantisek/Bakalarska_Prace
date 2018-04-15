import logging
from pymodbus.client.sync import ModbusTcpClient
from homeassistant.helpers.event import track_state_change
from homeassistant.components.switch import SwitchDevice
from homeassistant.const import DEVICE_DEFAULT_NAME

import custom_components.plc_modbus as plcModbus

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'modbus_sw'

def setup_platform(hass, config, add_devices, discovery_info=None):
    registers = plcModbus.registers
    switches = []
    #simatic s7-1200 - prvni patro
   
    for i in range(0,2):
        r = plcModbus.RegisterHandler(i,"192.168.0.11", 502+i)
        registers.append(r)
        for a in range(0,16):
           # _LOGGER.info(a)
            switches.append(ModbusSwitch(str(i)+"_"+str(a),r,a))

    def handle_Write(call):
        for r in registers:
            r.write_reg()

    def handle_Read(call):
        for r in registers:
            r.read_reg()

    def handle_Update(call):
        if Com.com:
            return
        Com.com = True
        for r in registers:
            r.write_reg()
            r.read_reg()
        Com.com = False
    add_devices(switches)


class ModbusSwitch(SwitchDevice):

    def __init__(self, name, register,index):
        self._name = name
        self.register = register
        self.index = index
        self._state = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        self._state = self.register.status(self.index)
        #self._state = Nevim.switchOnOff(self.ip, self.port, self.register)
        return self._state

    def turn_on(self):
        self.register.set_bit(self.index,1)
        self.is_on
        #Nevim.writeRegister(self.ip, self.port, self.register, 1)
        #self._state = Nevim.switchOnOff(self.ip, self.port, self.register)

    def turn_off(self):
        self.register.set_bit(self.index, 0)
        self.is_on
        #Nevim.writeRegister(self.ip, self.port, self.register, 0)
        #self._state = Nevim.switchOnOff(self.ip, self.port, self.register)
class ModbusStatus(SwitchDevice):

    def __init__(self, name):
        self._name = name
        self._state = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    def turn_on(self):
        self._state = True
        self.is_on


    def turn_off(self):
        self._state = False
        self.is_on






