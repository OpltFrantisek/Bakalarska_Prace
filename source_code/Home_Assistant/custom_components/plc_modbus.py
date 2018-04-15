import logging
from pymodbus.client.sync import ModbusTcpClient
import homeassistant.helpers.config_validation as cv


registers = []
stat = []


DOMAIN = 'plc_modbus'
ATTR_NAME = 'name'
DEFAULT_NAME = 'World'


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_hello(call):
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set('hello_service.hello', name)

    def handle_Write(call):
       for r in registers:
           r.write_reg()

    def handle_Read(call):
        for r in registers:
            r.read_reg()

    hass.services.register(DOMAIN, 'hello', handle_hello)
    hass.services.register(DOMAIN, 'plc_Write', handle_Write)
    hass.services.register(DOMAIN, 'plc_Read', handle_Read)

    # Return boolean to indicate that initialization was successfully.
    return True
class RegisterHandler:
    REGISTER_SIZE = 16
    register_number = 0
    ip = "192.168.1.5"
    port = 502
    reg = 15
    count = 0
    change = False
    def __init__(self,register,ip,port):
        self.register_number = register
        self.ip = ip
        self.port = port
        self.reg = Comunication.readRegister(self.ip,self.port,self.register_number)

    def write_reg(self):
        #_LOGGER.info(self.reg)
       # _LOGGER.error("Mozna budu zapisovat")
        if self.change:
           # _LOGGER.error("Zapisuji")
            Comunication.writeRegister(self.ip,self.port,self.register_number,self.reg)
            self.change = False


    def status(self,index):
        #_LOGGER.info("#################")
        #_LOGGER.info(self.reg)
       # _LOGGER.info(index)
        mask = 1<<index
        value = mask & self.reg
        #_LOGGER.info(value)
        if value == 0:
            return False
        else:
            return True

    def read_reg(self):
        if not self.change:
            self.reg = Comunication.readRegister(self.ip, self.port, self.register_number)


    def set_bit(self,index,x):
        mask = 1 << index  # Compute mask, an integer with just bit 'index' set.
        self.reg &= ~mask  # Clear the bit indicated by the mask (if x is False)

        if x:
            self.reg |= mask  # If x was True, set the bit indicated by the mask.
        self.change = True

class Comunication:
    def writeRegister(ip, port,register, value):
        client = ModbusTcpClient(ip,port)
        client.write_register(register, value)
        client.close()
        return True

    def writeRegisters(ip, port,register, values):
        client = ModbusTcpClient(ip,port)
        client.write_registers(register, values)
        client.close()
        return True

    def readRegisters(ip, port):
        client = ModbusTcpClient(ip, port)
        result = client.read_holding_registers(0, 2)
        client.close()
        return [result.getRegister(0),result.getRegister(1)]
    def readRegister(ip, port,register):
        client = ModbusTcpClient(ip, port)
        result = client.read_holding_registers(register, 1)
        client.close()
        return result.getRegister(0)

    def switchOnOff(ip, port,register):
        temp = Comunication.readRegister(ip, port,register)
        #_LOGGER.error('response from modbus slave: %s', temp, )
        if temp == 1:
            return True
        else:
            return False