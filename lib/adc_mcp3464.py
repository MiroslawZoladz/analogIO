from machine import Pin, SoftSPI
from time import sleep

class ADC:
        # register addreses
    ADCDATA    =0x00   
    CONFIG0    =0x01
    CONFIG1    =0x02
    CONFIG2    =0x03
    CONFIG3    =0x04
    IRQ        =0x05
    MUX        =0x06
    SCAN       =0x07
    TIMER      =0x08
    OFFSETCAL  =0x09
    GAINCAL    =0x0A
    RESERVED_B =0x0B
    RESERVED_C =0x0C
    LOCK       =0x0D
    RESERVED_E =0x0E
    CRCCFG     =0x0F
    
    # MUX channels
    VCM      = 15
    TEMP_M   = 14
    TEMP_P   = 13
    REFIN_M  = 12
    REFIN_P  = 11
    Reserved = 10
    AVDD     =  9
    AGND     =  8
    CH7      =  7
    CH0      =  0
    
        # MCLK
    MCLK_8 = 3
    MCLK_4 = 2
    MCLK_2 = 1
    MCLK_1 = 0 # default

    #OSR
    V98304 = 15
    V81920 = 14
    V49152 = 13
    V40960 = 12
    V24576 = 11
    V20480 = 10
    V16384 = 9
    V8192  = 8
    V4096  = 7
    V2048  = 6
    V1024  = 5
    V512   = 4
    V256   = 3 #(default)
    V128   = 2
    V64    = 1
    V32    = 0
            
    #BOOST
    bx2   =3 
    bx1   =2 #(default)
    bx066 =1
    bx05  =0

    #GAIN
    gx64  = 7
    gx32  = 6
    gx16  = 5
    gx8   = 4
    gx4   = 3
    gx2   = 2
    gx1   = 1 #(default)
    gx1_3 = 0

    #AZ_MUX
    AZ_ON  = 1
    AZ_OFF = 0
        
    def __init__(self, spi_sck_pn, spi_mosi_pn, spi_miso_pn, spi_cs): # spi_miso_pn dumy, must by any input pin
        
                # CALLIB
#         self.volts_per_lsb = nonvolatile_float()  #3.3/32768
        
        #SPI
        sck  = Pin(spi_sck_pn, Pin.OUT)
        mosi = Pin(spi_mosi_pn, Pin.OUT)
        miso = Pin(spi_miso_pn, Pin.IN) 
        self.cs   = Pin(spi_cs, Pin.OUT, value = 1)
        
        self.spi = SoftSPI(baudrate=100000, polarity=0, phase=0, bits=8, firstbit=SoftSPI.MSB, sck=sck, mosi=mosi, miso=miso)
        
        # CONFIG
        self.cfg_AMCLK_OSR(self.MCLK_1,self.V40960)
        self.cfg_BOOST_GAIN_AZ_MUX(self.bx1,self.gx1,self.AZ_OFF)
        self.wr_8bit_reg(self.IRQ,    0x07) # IRQ TOTEM

        # 10 One-shot conversion osets ADC_MODE[1:0] to ‘10’ (Standby) at the end of the conversion
        # 00 16-bit (default ADC coding): 16-bit ADC data; does not allow overrange (ADC code locked to 0xFFFF or 0x8000) (default)
        # 0  CRC-16 only (16-bit format) (default)
        # 0  CRC on communication disabled (default)
        # 0  Enable Digital Offset Calibration Disabled (default)
        # 0  EN_GAINCAL Disabled (default)
        self.wr_8bit_reg(self.CONFIG3,0x80) 

        # 11 Full Shutdown Mode Disabled
        # 11 AMCLK not present on the analog master clock output pin
        # 00 No current source is applied to the ADC inputs (default)
        # 11 = ADC Conversion mode
        self.wr_8bit_reg(self.CONFIG0,0xE3)

    def raw(self,ch_n,ch_p):
        self.cfg_MUX(ch_n,ch_p)
        self.wr_8bit_reg(self.CONFIG0,0xE3) #start convertion
        sleep(0.05)
        _ = self.rd_16bit_reg(self.ADCDATA)
        msb, lsb = _[1], _[2]
        res = (msb<<8)+lsb
        if res & 0x8000:
            res ^= 0xffff
            res *= -1
        return res    
    
    def cfg_MUX(self,ch_n,ch_p):
        ctl = (ch_p<<4) | ch_n
        self.wr_8bit_reg(self.MUX,ctl) # VIN+ = CH0, VIN- = AGND

    def cfg_AMCLK_OSR(self,amclk,osr):
        ctl = (amclk<<6) | (osr<<2) 
        self.wr_8bit_reg(self.CONFIG1,ctl) # AMCLK = MCLK, OSR = 98304 --> (0b00001100). 

    def cfg_BOOST_GAIN_AZ_MUX(self,boost,gain,az_mux):
        
        ctl = (boost<<6)|(gain<<3)|(az_mux<<2)
        self.wr_8bit_reg(self.CONFIG2,ctl)   

    def wr_8bit_reg(self,addr,value):
        WRT_CTRL=0b01000010
        ctl = (WRT_CTRL | (addr<<2)) , value
        write_buf = bytearray(ctl)
        read_buf  = bytearray(write_buf)

        self.cs.off()
        self.spi.write_readinto(write_buf, read_buf)
        self.cs.on()
        
        return read_buf

    def rd_16bit_reg(self,addr):
        RD_CTRL= 0b01000001
        ctl = RD_CTRL|(addr<<2) , 0x55, 0x55
        write_buf = bytearray(ctl)
        read_buf  = bytearray(write_buf)

        self.cs.off()
        self.spi.write_readinto(write_buf, read_buf)
        self.cs.on()
        
        return read_buf


