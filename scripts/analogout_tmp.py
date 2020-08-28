#
# Copyright (c) 2019 Analog Devices Inc.
#
# This file is part of libm2k
# (see http://www.github.com/analogdevicesinc/libm2k).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# This example assumes the following connections:
# W1 -> 1+
# W2 -> 2+
# GND -> 1-
# GND -> 2-
#
# The application will generate a sine and triangular wave on W1 and W2. The signal is fed back into the analog input
# and the voltage values are displayed on the screen

import libm2k
import matplotlib.pyplot as plt
import time
import numpy as np

kHz=1e+3;
MHz=1e+6;
usec=1e-6;

# Number of measurement
nMeasure = 1;

ctx=libm2k.m2kOpen()
if ctx is None:
	print("Connection Error: No ADALM2000 device available/connected to your PC.")
	exit(1)

ctx.calibrateADC()
ctx.calibrateDAC()

ain=ctx.getAnalogIn()
aout=ctx.getAnalogOut()
trig=ain.getTrigger()

# Check device specification

# For analog input
# Check available voltage ranges
#tmp=ain.getAvailableRanges()
#print(tmp); # -2.5~2.5 & -25~25 are available.
# Check available sample rates
#tmp=ain.getAvailableSampleRates()
#print(tmp); # -2.5~2.5 & -25~25 are available.

# For analog output
# Check available sample rates
#tmp=aout.getAvailableSampleRates(0)
#print("available sample rates for Ch 0 analog output :{}".format(tmp));
# 1kHz, 10kHz, 100kHz, 1MHz, 10MHz, 100MHz are available for analog input
#tmp=aout.getAvailableSampleRates(1)
#print("available sample rates for Ch 1 analog output :{}".format(tmp));
# 750Hz, 7.5kHz, 75kHz, 750kHz, 7.5MHz, 75MHz are available for analog output

ain.enableChannel(0,True)
ain.enableChannel(1,True)
#ain.setSampleRate(100000)
#ain.setRange(0,-10,10)
samplerate_in=100.*MHz; # Hz (1*kHz, 10*kHz, 100*kHz, 1*MHz, 10*MHz, 100*MHz)
starttime_in =-10.*usec; # sec
stoptime_in  = 10.*usec; # sec
measuretime_in=stoptime_in - starttime_in;
npoints_in   = (int)(measuretime_in*samplerate_in);
print('npoints @ in = {}'.format(npoints_in));
ain.setSampleRate(samplerate_in) # Hz

ain.setRange(0,-2.5,2.5)

time_in = np.linspace(starttime_in/usec, stoptime_in/usec, npoints_in+1); # time unit is usec

### uncomment the following block to enable triggering
#trig.setAnalogSource(0) # Channel 0 as source
#trig.setAnalogCondition(0,libm2k.RISING_EDGE_ANALOG)
#trig.setAnalogLevel(0,0.5)  # Set trigger level at 0.5
#trig.setAnalogDelay(0) # Trigger is centered
#trig.setAnalogMode(1, libm2k.ANALOG)

samplerate_out = 75*MHz; # Hz (750, 7.5*kHz, 75*kHz, 750*kHz, 7.5*MHz, 75*MHz)
period_out     = 1.*usec; # sec
amp            = 2.0; # V
npoints_period_out = (int)(samplerate_out * period_out)
print('npoints in one period @ out = {}'.format(npoints_period_out));

aout.setSampleRate(0, samplerate_out)
aout.setSampleRate(1, samplerate_out)
aout.enableChannel(0, True)
aout.enableChannel(1, True)

x=np.linspace(-np.pi,np.pi,npoints_period_out+1)
buffer_sin=np.sin(x)
#buffer_saw=np.linspace(-amp,amp,npoints_period_out+1)
buffer_saw1=np.linspace(-amp,amp,npoints_period_out+1)
buffer_saw2=np.linspace(-amp,amp,npoints_period_out*2+1)
#buffer_saw1=np.linspace(-2.,2.,1024)

#buffer = [buffer_sin, buffer_saw]
buffer = [buffer_saw1, buffer_saw2]

aout.setCyclic(True)
aout.push(buffer)

"""
for i in range(nMeasure): # gets 10 triggered samples then quits
    data = ain.getSamples(npoints_in+1)
    #print(data[0]);
    plt.plot(time_in, data[0],linestyle='',marker='o',markersize=1,color='k',label='channel 1')
    plt.plot(time_in, data[1],linestyle='',marker='o',markersize=1,color='r',label='channel 2')
    plt.xlabel('Time [$\mu$s]');
    plt.ylabel('Voltage [V]');
    plt.legend();
    plt.grid(True);
    #plt.plot(data[1])
    #plt.show()
    #time.sleep(0.1)
    plt.savefig("output/aho{}.png".format(i))
    plt.clf()
"""

libm2k.contextClose(ctx)
