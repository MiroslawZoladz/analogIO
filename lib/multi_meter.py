from ina219 import INA219_Voltage, INA219_Current

class channel:
    def __init__(self, pot, meters):
        self.pot = pot
        self.meters = meters
        
class MultiMeter:

    def __init__(self, i2c, mode):
        i2c_addr_l = 0x40, 0x41
        
        INA219_m = {'current':INA219_Current,'voltage':INA219_Voltage}[mode]
        self.current_meter_l = [INA219_m(i2c, addr) for addr in i2c_addr_l]
        
        self.channel = 0
        self.current_meter = self.current_meter_l[self.channel] 
    
    def set_channel(self, chan_nr):
        self.channel = int(chan_nr)
        self.current_meter = self.current_meter_l[self.channel] 

    def measure(self):
        return self.current_meter.measure()
    
    def callib(self, value):
        self.current_meter.callib(value)
        
    def config(self, name, value):
        self.current_meter.config(name, value)
        
    def coeff(self):
        return self.current_meter.read_coefficient()
    
    def raw(self):
        return self.current_meter.measure_raw()
        