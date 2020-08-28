# This script uses the following pins:
# Ch1 : W1(analog signal) / GND
# Ch2 : W2(analog signal) / GND

import os, sys
import libm2k
import matplotlib.pyplot as plt
import numpy as np

from utils import *

def parseCmdLine(args):
  # default values
  def_t  = 1e-6     ;
  def_tr1= 0.5      ; # ratio of time at voltage1 to time period
  def_T  = 0        ;
  def_s  = 75e+6    ;
  def_c  = "0,1"    ;
  def_v1s= "0.0,0.0";
  def_v2s= "1.0,1.0";
  def_to = "0.0,0.0";
  def_v  = 0        ;
  
  from optparse import OptionParser;
  parser = OptionParser();
  parser.add_option('-t', '--timeperiod' , dest='timeperiod' , type = float, default=def_t  , help='Time period of the square wave [sec] (default={:.2e})'.format(def_t));
  parser.add_option(      '--timeRatio1' , dest='timeRatio1' , type = float, default=def_tr1, help='Ratio of time at VOLTAGE1S to TIMEPERIOD [ratio] (default={})'.format(def_tr1));
  parser.add_option('-T', '--runtime'    , dest='runtime'    , type = float, default=def_T  , help='Analog output runtime [sec]. If RUNTIME <= 0., the analog output is kept after this job is finished. (defalut={:.2e})'.format(def_T));
  parser.add_option('-s', '--samplerate' , dest='samplerate' , type = float, default=def_s  , help='Sampling rate [Hz] (750, 7.5e+3, 75e+3, 750e+3, 7.5e+6, 75e+6) (default={:.2e})'.format(def_s));
  parser.add_option('-c', '--channels'   , dest='channels'   , type = str  , default=def_c  , help='String of output channnel numbers combined with \',\'. There are only 0 ch and 1 ch. (ex, "0", "1", "0,1",..) (default=\"{}\")'.format(def_c));
  parser.add_option(      '--voltage1s'  , dest='voltage1s'  , type = str  , default=def_v1s, help='String of the voltage1(start voltage of the one square wave) [V] combined with \',\' for each channels. (ex, "0.0", "-1.0" for one channel, "0.0,0.0", "-1.0,0.0" for two channels) (default=\"{}\")'.format(def_v1s));
  parser.add_option(      '--voltage2s'  , dest='voltage2s'  , type = str  , default=def_v2s, help='String of the voltage2(end voltage of the one square wave) [V] combined with \',\' for each channels. (ex, "1.0", "2.0" for one channel, "1.0,1.0", "1.0,2.0" for two channels) (default=\"{}\")'.format(def_v2s));
  parser.add_option(      '--voltage1'   , dest='voltage1'   , type = float, default=None   , help='The voltage1(start voltage of the one square wave) [V] for all the channels. Usually this is None and VOLTAGE1S is used. (default=None)');
  parser.add_option(      '--voltage2'   , dest='voltage2'   , type = float, default=None   , help='The voltage2(end voltage of the one square wave) [V] for all the channels. Usually this is None and VOLTAGE2S is used. (default=None)');
  parser.add_option(      '--timeoffsets', dest='timeoffsets', type = str  , default=def_to , help='String of the start-time offset of the square wave [sec] cmbined with \',\' for each channels. (ex, "0.0", "-0.5e-6" for one channel, "0.0,0.5e-6", "0.5e+6,-0.5e+6" for two channels) (default=\"{}\")'.format(def_to));
  parser.add_option('-v', '--verbose'    , dest='verbose'    , type = int  , default=def_v  , help='verbosity (0:Normal, 1:More output, 2:All output, -1:Less output, 2:No output) (default={})'.format(def_v));
  (config, args) = parser.parse_args(args);                                                   
  Out("",True,config);
  return config;


# shift the waveform by timeoffset
# |timeoffset| should be less than timeperiod. Otherwise, this function does not work correctly.
def shiftWave(waveform, timeoffset, samplerate) :
  if timeoffset!=0.0 :
    pointoffset = (int)(timeoffset*samplerate);
    waveform    = np.roll(waveform, pointoffset);
    pass;
  return waveform;

# repeat waveform until the total number of points is npoints
def repeatWave(waveform, npoints): 
  waveform_1period = waveform;
  nperiods_int     = (int)(npoints/(len(waveform_1period)));
  waveform       = np.tile(waveform_1period,nperiods_int); # repeat one period in nperiods_int times
  npoints_remain = npoints - len(waveform_1period)*nperiods_int; # remaining points to make npoints
  waveform = np.concatenate([waveform, waveform_1period[:npoints_remain]]);
  Out('Required # of points        = {}'.format(npoints),0);
  Out('# of points of the waveform = {}'.format(len(waveform)),0);
  return waveform;

def closeCtx(ctx) :
  libm2k.contextClose(ctx);
  return;

def analogoutSquarewave(
  timeperiod = 1.*usec,   # Time period of the square wave [sec]
  timeRatio1 = 0.5    ,   # Ratio of time at VOLTAGE1S to TIMEPERIOD [ratio]
  runtime    = 0.     ,   # Analog output runtime [sec]. If runtime <= 0., the analog output is kept after this job is finished.
  samplerate = 75.*MHz,   # Sampling rate [Hz] (750, 7.5*kHz, 75*kHz, 750*kHz, 7.5*MHz, 75*MHz)
  channels   = [0,1],     # Array of output channnel numbers combined with \',\'. There are only 0 ch and 1 ch. (ex, "0", "1", "0,1",..)
  voltage1s  = [0.0,0.0], # Array of the voltage1(start voltage of the one square wave) [V] for each channels
  voltage2s  = [1.0,1.0], # Array of the voltage2(end   voltage of the one square wave) [V] for each channels
  timeoffsets= [0.0,0.0], # Start time offset of the square wave [sec] for each channels
  ctx    =None,           # Instance of ADALM2000
  verbose    = 0    , # Verbosity
    ):
  setVerbose(verbose);

  # Argument check
  if len(voltage1s) < len(channels) or len(voltage2s) < len(channels) or len(timeoffsets) < len(channels) :
    Error('The number of voltage1s or voltage2s or timeoffsets is less than that of channels. Their numbers should be same.');
    Error('    channels    = ',channels );
    Error('    voltage1s   = ',voltage1s);
    Error('    voltage2s   = ',voltage2s);
    Error('    timeoffsets = ',timeoffsets);
    exit(1);
  for i,ch in enumerate(channels) :
    if abs(timeoffsets[i]) >= timeperiod :
      Error('|timeoffset| for ch {} is more than timeperiod. |timeoffset| should be < timeperiod.'.format(ch));
      Error('    timeoffset = {}'.format(timeoffsets[i]));
      Error('    timeperiod = {}'.format(timeperiod    ));
      exit(1);
    pass;
  voltage1s = checkIsFloat(voltage1s,'voltage1s');
  voltage2s = checkIsFloat(voltage2s,'voltage2s');

 
  # Initialize
  if ctx is None:
    ctx=libm2k.m2kOpen();
    if ctx is None:
      Error("Connection Error: No ADALM2000 device available/connected to your PC.");
      exit(1);
      pass;
    ctx.calibrateDAC();
    ctx.calibrateADC();
    pass;
  aout=ctx.getAnalogOut();
  for ch in range(g_nAnalogOutChannels) : aout.enableChannel(ch,False);
  
  # Define run condition
  npointsPeriod = (int)(timeperiod*samplerate);
  if runtime>0.0:
    aout.setCyclic(False);
    npoints  = (int)(runtime*samplerate)+1;
  else :
    aout.setCyclic(True);
    runtime  = 0.0;
    npoints  = npointsPeriod;
    pass;
  Out('runtime              = {} [usec] (0 means to keep running)'.format(runtime/usec),0);
  Out('# of sampling points = {} (0 means to keep running)'.format(npoints),0);

  # Define outputs
  npointsPeriod1= (int)(timeperiod*samplerate*timeRatio1);
  npointsPeriod2= (int)(npointsPeriod-npointsPeriod1);
  Out('time period / # of points in one period = {} usec / {} points'.format(timeperiod/usec, npointsPeriod),0);
  Out('time / # of points at voltage1 in one period = {} usec / {} points'.format(timeperiod/usec*timeRatio1     , npointsPeriod1),0);
  Out('time / # of points at voltage2 in one period = {} usec / {} points'.format(timeperiod/usec*(1.-timeRatio1), npointsPeriod1),0);
  buffer = [];
  for ch in range(g_nAnalogOutChannels) :
    if not ch in channels : 
      buffer.append([]);
      continue;
    chIndex = channels.index(ch);
    Out('Definning output for ch {}...'.format(ch),0);
    Out('    start voltage (voltage1) of square wave = {} V'.format(voltage1s[chIndex]),0);
    Out('    end   voltage (voltage2) of square wave = {} V'.format(voltage2s[chIndex]),0);

    # Define waveform for one period
    waveform1 = [voltage1s[chIndex]]*npointsPeriod1; # array size = npointsPeriod1
    waveform2 = [voltage2s[chIndex]]*npointsPeriod2; # array size = npointsPeriod2
    waveform = np.concatenate([ waveform1, waveform2 ]);
    waveform = shiftWave(waveform, timeoffsets[chIndex], samplerate);
    Out('    time offset = {} [usec]'.format(timeoffsets[chIndex]/usec),0);
    Out('    waveform of one period = ',2,waveform);

    # Only for runtime>0
    if runtime > 0:
      waveform = repeatWave(waveform, npoints);
      Out('    waveform for the runtime = ',2,waveform);
      pass;


    buffer.append(waveform);
    pass;
  Out('buffer of analog output = ',2,buffer);
  
  # Setting
  for ch in channels :
    Out('channel {} : ON'.format(ch),0);
    aout.enableChannel(ch,True);
    aout.setSampleRate(ch, samplerate); # Hz
    pass;
  
  # Run
  isAllChannel = True;
  for ch in range(g_nAnalogOutChannels) :
    if len(buffer[ch])==0 :
      isAllChannel = False;
      break;
    pass;
  if isAllChannel : 
    Out('push buffer for all channels',0);
    aout.push(buffer);
  else            :
    for ch in channels :
      Out('push buffer for ch {}'.format(ch),0);
      aout.push(ch, buffer[ch]);
      pass;
    pass;

 
  return ctx; # End of analogoutSquarewave()
  

if __name__ == '__main__':
  config  = parseCmdLine(sys.argv);

  channels  = [ (int)(ch) for ch in (config.channels).split(',') ];
  voltage1s = [ (float)(v) for v in (config.voltage1s).split(',') ];
  voltage2s = [ (float)(v) for v in (config.voltage2s).split(',') ];
  if config.voltage1!=None : voltage1s = [config.voltage1]*len(channels);
  if config.voltage2!=None : voltage2s = [config.voltage2]*len(channels);
  timeoffsets = [ (float)(t) for t in (config.timeoffsets).split(',') ];

  ctx = analogoutSquarewave(
      timeperiod = config.timeperiod, # Time period of the square wave [sec]
      timeRatio1 = config.timeRatio1, # Ratio of time at VOLTAGE1S to TIMEPERIOD [ratio]
      runtime    = config.runtime,    # Analog output runtime [sec]. If runtime <= 0., the analog output is kept after this job is finished.
      samplerate = config.samplerate, # Sampling rate [Hz] (750, 7.5*kHz, 75*kHz, 750*kHz, 7.5*MHz, 75*MHz)
      channels   = channels,          # Array of output channnel numbers combined with \',\'. There are only 0 ch and 1 ch. (ex, "0", "1", "0,1",..)
      voltage1s  = voltage1s,         # Array of the voltage1(start voltage of the one square wave) [V] for each channels
      voltage2s  = voltage2s,         # Array of the voltage2(end   voltage of the one square wave) [V] for each channels
      timeoffsets= timeoffsets,       # Start time offset of the square wave [sec] for each channels
      verbose    = config.verbose,    # Verbosity
      ); 

  # Close ctx
  closeCtx(ctx);

  pass; # End of __main__
