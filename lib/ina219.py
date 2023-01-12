# from nonvolatile_float import nonvolatile_float
from nonvolatile import NonVolatile
from config import Config

class INA219:
       
    __REG_ADDR_CONFIGURATION = 0
    
    Config_reg_buffer = Config(['md','sadc','badc','pg','brng'], [0,3,7,11,13], [0x7,0xf,0xf,0x0,0x0])
        
    def __init__(self, i2c, addr):
        self._i2c = i2c
        self._addr = addr
        self._callib_coef = NonVolatile()
        
    def config(self, name, val):
        self.Config_reg_buffer.set(name, val)
        
    def measure(self):
        coeff = self._callib_coef.get()
        assert coeff != None, 'ERR channel no calibrated'
        return self.measure_raw()*coeff
    
    def measure_raw(self):
        self._i2c.writeto_mem(self._addr, self.__REG_ADDR_CONFIGURATION, self.Config_reg_buffer.get_bytes())
        reg_val = self._i2c.readfrom_mem(self._addr, self._voltage_reg, 2)
        return int.from_bytes(reg_val, 'big')>>self._voltage_val_bp
        
    def callib(self, measured_mili):
        self._callib_coef.set(measured_mili/self.measure_raw())
        self._callib_coef.save()
    
    def read_coefficient(self):
        return self._callib_coef.get()
    

class INA219_Current (INA219):
    
    __REG_ADDR_SHUNT_VOLTAGE = 1
    
    def __init__(self, i2c, addr):
        #self._i2c = i2c
        INA219.__init__(self, i2c, addr)
        self._voltage_reg = self.__REG_ADDR_SHUNT_VOLTAGE
        self._voltage_val_bp = 0
        
class INA219_Voltage (INA219):
    
    __REG_ADDR_BUS_VOLTAGE = 2
    
    def __init__(self, i2c, addr):
        #self._i2c = i2c
        INA219.__init__(self, i2c, addr)
        self._voltage_reg = self.__REG_ADDR_BUS_VOLTAGE
        self._voltage_val_bp = 3