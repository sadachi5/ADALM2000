import analogin
import analogoutRampwave
import analogoutSquarewave
import digitaloutSinglePulse
from time import sleep

# 100kHz
#ctx=analogoutSquarewave.analogoutSquarewave(channels=[0,1],voltage1s=[0.,0.],voltage2s=[2.0,2.0],timeoffsets=[0.,2.5e-6],timeRatio1=0.5,timeperiod=1.0e-5,verbose=0); # CH1: signal, CH2:quad

# 10kHz
#ctx=analogoutSquarewave.analogoutSquarewave(channels=[0,1],voltage1s=[0.,0.],voltage2s=[2.0,2.0],timeoffsets=[0.,2.5e-5],timeRatio1=0.5,timeperiod=1.0e-4,verbose=0); # CH1: signal, CH2:quad

# 1kHz
ctx=analogoutSquarewave.analogoutSquarewave(channels=[0,1],voltage1s=[0.,0.],voltage2s=[2.0,2.0],timeoffsets=[0.,2.5e-4],timeRatio1=0.5,timeperiod=1.0e-3,verbose=0); # CH1: signal, CH2:quad

# 1 pulse per 0.1 sec on ch 0  for Z  signal
ctx=digitaloutSinglePulse.digitaloutSinglePulse(ctx=ctx, timeperiod=0.1, timeON=1.0e-5, samplerate = 1e+6, channels=[1], timeoffsets=[0.,0.,0.,0.],doPlot=False, verbose=0);




#ctx=analogoutSquarewave.analogoutSquarewave(channels=[1,0],voltage1s=[0.,2.0],voltage2s=[2.0,0.0],timeoffsets=[0.,2.5e-6],timeRatio1=0.5,timeperiod=1.0e-5,verbose=0);
#ctx=analogoutSquarewave.analogoutSquarewave(channels=[1,0],voltage1s=[0.,2.0],voltage2s=[2.0,0.0],timeoffsets=[0.,-2.5e-6],timeRatio1=0.5,timeperiod=1.0e-5,verbose=0);

#ctx = analogoutRampwave.analogoutRampwave(channels=[0,1],voltage1s=[0.,0.],voltage2s=[1.,1.],timeoffsets=[0.,0.],timeperiod=1e-6,verbose=0);
#ctx = analogin.analogin(ctx=ctx,nMeasure=3,timelength=20e-6,outputName='rampWave');

#ctx=analogoutSquarewave.analogoutSquarewave(channels=[0,],voltage1s=[0.,0.],voltage2s=[0.1,1.],timeoffsets=[0.,1.e-6],timeRatio1=0.5,timeperiod=1.0e-6,verbose=0);
#ctx=analogoutSquarewave.analogoutSquarewave(channels=[0,1],voltage1s=[0.,0.],voltage2s=[1.,1.],timeoffsets=[0.,1.e-6],timeRatio1=0.5,timeperiod=2.0e-6,verbose=0);
#ctx = analogin.analogin(ctx=ctx,nMeasure=3,timelength=100e-6,outputName='squareWave');
#sleep(10);

#ctx = analogin.analogin(ctx=None,channels=[0],nMeasure=1,samplerate=100e+6,timelength=50.0e-6,outputName='squareWave100kHz_0.1V_50us_s100MHz',overlapPlot=False);


#ctx=digitaloutSinglePulse.digitaloutSinglePulse(ctx=ctx, timeperiod=0.1, timeON=0.01, samplerate = 1000, channels=[0,1,2], timeoffsets=[0.,0.005,0.010],doPlot=True, recordNperiod=5, outputname='aho.png', verbose=2); # for test
#ctx=digitaloutSinglePulse.digitaloutSinglePulse(ctx=ctx, timeperiod=0.1, timeON=0.01, samplerate = 1000, channels=[1], timeoffsets=[0.],doPlot=True, recordNperiod=5, outputname='aho.png', verbose=2); # for test
#ctx=digitaloutSinglePulse.digitaloutSinglePulse(ctx=ctx, timeperiod=0.1, timeON=0.01, samplerate = 1000, channels=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], timeoffsets=[0.]*16,doPlot=True, recordNperiod=5, outputname='aho.png', verbose=2); # for test



#analogin.closeCtx(ctx);