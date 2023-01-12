import sys
sys.path.append('../lib')

from dac_dac121S101 import DAC
from pinout import Pinout
from nonvolatile import NonVolatile

class CallibRange:
    def __init__(self):
        self.min = NonVolatile()        
        self.max = NonVolatile()
        
    def save(self):
        self.min.save()
        self.max.save()        

class AnalogOutputs:
    RANGE_MIN_LSB = 0
    RANGE_MAX_LSB = 1500
    
    def __init__(self):        
        bp = Pinout()
        self.dac = [DAC(bp.SPI_SCK, bp.SPI_MOSI, bp.SPI_MISO_ADC_0, cs) for cs in (bp.SPI_CS_DAC_0, bp.SPI_CS_DAC_1,bp.SPI_CS_DAC_2,bp.SPI_CS_DAC_3,bp.SPI_CS_DAC_4,bp.SPI_CS_DAC_5,bp.SPI_CS_DAC_6,bp.SPI_CS_DAC_7)]
        self.disable()
        
#         self.name = 'call_N', 'call_P'
        self.channel = 0
        self.callib_range = [CallibRange() for _ in self.dac]
        self.voltge =       [NonVolatile() for _ in self.dac]
    
    def inc(self):
        v = self.voltge[self.channel].get()
        max_ = self.callib_range[self.channel].max.get()
        if (v + 0.01) < max_: v += 0.01
        self.voltge[self.channel].set(v)
        self._set_voltage(self.channel,v)
           
    def dec(self):
        v = self.voltge[self.channel].get()
        min_ = self.callib_range[self.channel].min.get()                
        if (v - 0.01) > min_: v -= 0.01
        self.voltge[self.channel].set(v)
        self._set_voltage(self.channel,v)
    
    def set_channel(self, channel):
        self.channel = channel
        
    def save(self):
        for v in self.voltge:
            v.save()
    
    def set_voltage(self,v):
        self.voltge[self.channel].set(v)
        self._set_voltage(self.channel,v)
    
#     def get_name(self):
#         return self.name[self.channel]
    
#     def get_voltage(self):
#         return self.voltge[self.channel].get()

    def _set_voltage(self,channel, v):
        dac=self.dac[channel]
        c_range = self.callib_range[channel]
        min_ = c_range.min.get()
        max_ = c_range.max.get()            
        assert  min_ != None and max_ != None , 'err dac_not_calibrated'
        assert  min_ <= v <= max_, 'err voltage_out_of_valid_range'
        lsb = int(((v-min_)*self.RANGE_MAX_LSB)/(max_-min_))+1
        dac.raw(lsb)
            
    def disable(self):
        for dac in self.dac:
            dac.gnd()
    
    def enable(self):
        for ch,(v,cr) in enumerate(zip(self.voltge,self.callib_range)):
            
            if v.get() == None:
                v=cr.min.get()
                assert  v != None , 'err dac_not_calibrated'
            else:
                v=v.get()
                
            self._set_voltage(ch,v)
            
    def min(self):
        for dac in self.dac:
            dac.raw(self.RANGE_MIN_LSB)

    def max(self):
        for dac in self.dac:
            dac.raw(self.RANGE_MAX_LSB)

    # Procedura kalibracji, argumenty w woltach
    # 1. set_min
    # 2. write down
    # 3. set_max
    # 4. write down
    # 5. calib(min,max)   
    def callib(self,v_min, v_max):
        self.callib_range[self.channel].min.set(v_min)
        self.callib_range[self.channel].max.set(v_max)
        self.callib_range[self.channel].save()

        
