#import sys
#sys.path.append('../lib')

from adc_mcp3464 import ADC
from pinout import Pinout
from nonvolatile import NonVolatile

class AnalogInputs:
    def __init__(self):
        bp = Pinout()
        
        _ = list()
        for miso, cs in zip([bp.SPI_MISO_ADC_0], [bp.SPI_CS_ADC_0]):
            _.append(ADC(bp.SPI_SCK, bp.SPI_MOSI, miso, cs))
        self.adc = _
        
        self.volts_per_lsb = [NonVolatile() for _ in self.adc]
        self.channel = 0
        
    def set_channel(self, ch):
        adc_ix = ch//7
        assert adc_ix < len(self.adc), 'ERR channel ix invalid'  
        self.channel = ch
        
    def get_voltage(self):
        ch = self.channel
        adc_ix = ch//7
        adc_ch_ix = ch-(adc_ix*7)+1                  
        coeff = self.volts_per_lsb[adc_ix].get()
        assert  coeff != None, 'ERR adc_not_calibrated'       
        return self.adc[adc_ix].raw(0,adc_ch_ix)*coeff
    
    def get_voltage_all(self):
        ch_bac = self.channel
        voltages_l = list()
        for ch in range(7*len(self.adc)):
            self.channel = ch
            voltages_l.append(self.get_voltage())
        self.channel = ch_bac 
        return voltages_l            
        
    def callib(self, adc_i, voltage):
        adc_i = int(adc_i)
        lsb = self.adc[adc_i].raw(0,1)
        self.volts_per_lsb[adc_i].set(voltage/lsb)
        self.volts_per_lsb[adc_i].save()



