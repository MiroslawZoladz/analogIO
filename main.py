HELP =""" 
Analog Outputs (unit: V)
oe  : enable all channels
od  : disable all channels
och : set curent channel
ov  : set voltage
omin: set max value on all dac-s
omax: set min value on all dac-s
oc  : callibrate curent channel, arguments: voltage at omin, voltage at omax 

Analog Inputs (unit: mV)   
ich : set curent channel
iv  : get voltage from current channel
iva : get voltage from all channels
ivapp:get voltage from all channels, nice formated
ic  :  callibrate curent channel, arguments: current applied voltage 

Current Meter  (unit: mA)
cmch: set curent channel
cmm : measure
cmc : config
cmf : get coeff
cmr : get raw (adc)

Voltage Meter  (unit: mV)    
vmch: set curent channel
vmm : measure
vmc : config
vmf : get coeff
vmr : get raw (adc)
"""

from machine import Pin, SoftI2C
from analog_outputs import AnalogOutputs
from analog_inputs   import AnalogInputs
from multi_meter import MultiMeter

ao = AnalogOutputs()
ai = AnalogInputs()

sda=Pin(16)
scl=Pin(17)
i2c=SoftI2C(sda=sda, scl=scl, freq=100000)
cm = MultiMeter(i2c,'current')
vm = MultiMeter(i2c,'voltage')

while True:    
    command = input("")    
    try:
        # command parsing and validating
        tokens = command.split()
        if not tokens:
            print(HELP)
            continue
        cmd, arg  = tokens[0], [float(s) for s in tokens[1:]]
                
        # analog outputs
        if   cmd == 'oe'  : ao.enable()
        elif cmd == 'od'  : ao.disable()
        elif cmd == 'och' : ao.set_channel(int(arg[0]))
        elif cmd == 'ov'   : ao.set_voltage(float(arg[0]))
        elif cmd == 'omin': ao.min()
        elif cmd == 'omax': ao.max()
        elif cmd == 'oc'  : ao.callib(*arg)        
        
        # analog inputs
        elif cmd == 'ich'  : ai.set_channel(int(arg[0]))
        elif cmd == 'iv'   : print(f'{ai.get_voltage(*arg):0.3f}')
        elif cmd == 'iva'  : print(' '.join([f'{v:0.3f}' for v in ai.get_voltage_all()]))
        elif cmd == 'ivapp': [print(f'ch_{ch_i:02d}: {v:0.3f}') for ch_i,v in enumerate(ai.get_voltage_all())] #[print(f'ch_{ch_i:02d}: {v:0.3f}') for ch_i,v in enumerate(ai.get_voltage_all())]
        elif cmd == 'ic'   : ai.callib(*arg)

        # current meter
        elif cmd == 'cmch': cm.set_channel(*arg)    
        elif cmd == 'cmm' :            
            val = cm.measure()
            if val>10000:
                val  = 0
            print(val)
        elif cmd == 'cmc': cm.callib(int(*arg))
        elif cmd == 'cmf': print(cm.coeff())
        elif cmd == 'cmr': print(cm.raw())

        # voltage meter
        elif cmd == 'vmch': vm.set_channel(*arg)    
        elif cmd == 'vmm' :            
            val = vm.measure()
            if val>10000:
                val  = 0
            print(val)
        elif cmd == 'vmc': vm.callib(int(*arg))
        elif cmd == 'vmf': print(vm.coeff())
        elif cmd == 'vmr': print(vm.raw())

        else: print(HELP)
        
        print('ok')

    except Exception as e:
        print('Error',e)

