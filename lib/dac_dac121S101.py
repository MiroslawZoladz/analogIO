import sys
sys.path.append('../lib')

from machine import Pin, SoftSPI

class DAC:
    
    def __init__(self, spi_sck_pn, spi_mosi_pn, spi_miso_pn, spi_cs): # spi_miso_pn dumy, must by any input pin 
        
        #spi
        sck  = Pin(spi_sck_pn, Pin.OUT)
        mosi = Pin(spi_mosi_pn, Pin.OUT)
        miso = Pin(spi_miso_pn, Pin.IN) 
        self.cs   = Pin(spi_cs, Pin.OUT, value = 1)
        
        self.spi = SoftSPI(baudrate=100000, polarity=0, phase=0, bits=8, firstbit=SoftSPI.MSB, sck=sck, mosi=mosi, miso=miso)

    def gnd(self): #Power-Down with 1kΩ to GND        
        msb = 0b0010000
        lsb = 0x00 
        self.cs.off()
        self.spi.write(bytearray([msb,lsb]))
        self.cs.on()
                
    def raw(self,value):
        msb = (value>>8) & 0x0F
        lsb = value & 0xFF 
        self.cs.off()
        self.spi.write(bytearray([msb,lsb]))
        self.cs.on()        

