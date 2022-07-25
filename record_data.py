import pyvisa as visa
from oscilloscope import *
import sys
import time

csv_filename = "Run_"+str(int(time.time()))

channels = []
for c in sys.argv[1:]:
    channels.append(int(c))

scope = Oscilloscope("USB0::0xF4EC::0xEE38::SDSMMGKD5R3898::INSTR")

for c in channels:
    scope.add_channel(c, ChannelType.DC)

scope.timeout(2000)
scope.chunk_size(20*1024*1024)
scope.initialize()


while 1:
    while not scope.trigger_status().triggered:
        pass
    for c in channels:
        with open("%s_C%d.csv"%(csv_filename, c), "a") as csv_file:
            csv_file.write(str(scope.waveform(c)))
    
    






