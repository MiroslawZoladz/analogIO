class bit_file:
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val
        
class Config:
    
    def __init__(self, names, positions, values):

        self.cfg_bitfiles = {n:bit_file(p,v) for n,p,v in zip(names, positions, values)}
    
    def set(self, name, val):
        try:
            self.cfg_bitfiles[name].val=val
        except:
            print('Wrong name')
        
    def get_bytes(self):
        self.config_reg = sum([self.cfg_bitfiles[name].val <<  self.cfg_bitfiles[name].pos for name in self.cfg_bitfiles])
        return bytearray([(self.config_reg >> 8) & 0xFF, self.config_reg & 0xFF])