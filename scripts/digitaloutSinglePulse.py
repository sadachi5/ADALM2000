# This script uses the following pins:
# digital IO one of 0~15 (asigned by IOpin) / GND

import os, sys
import libm2k
import matplotlib.pyplot as plt
import numpy as np

from utils import *

def parseCmdLine(args):
  # default values
  def_t  = 0.1      ; # time period of one cycle
  def_tON= 1e-2     ; # time period at ON
  def_s  = 1e+3     ; # sample rate
  def_c  = "0"      ;
  def_to = "0.0"    ;
  def_v  = 0        ;
  def_p  = False    ;
  def_np = 10       ;
  def_o  = "aho.png";
  
  from optparse import OptionParser;
  parser = OptionParser();
  parser.add_option('-t', '--timeperiod' , dest='timeperiod' , type = float, default=def_t  , help='Time period for one cycle with a pulse [sec] (default={:.2e})'.format(def_t));
  parser.add_option(      '--timeON'     , dest='timeON'     , type = float, default=def_tr1, help='Time at ON voltage [sec] (default={})'.format(def_tr1));
  parser.add_option('-s', '--samplerate' , dest='samplerate' , type = float, default=def_s  , help='Sampling rate [Hz] (Up to 100e+6) (default={:.2e})'.format(def_s));
  parser.add_option('-c', '--channels'   , dest='channels'   , type = str  , default=def_c  , help='String of output channnel numbers combined with \',\'. There are 0~15 ch. (ex, "0", "1", "0,1",..) (default=\"{}\")'.format(def_c));
  parser.add_option(      '--timeoffsets', dest='timeoffsets', type = str  , default=def_to , help='String of the start-time offset of the square wave [sec] cmbined with \',\' for each channels. (ex, "0.0", "-0.5e-6" for one channel, "0.0,0.5e-6", "0.5e+6,-0.5e+6" for two channels) (default=\"{}\")'.format(def_to));
  parser.add_option('-p', '--doPlot'     , dest='doPlot'     , action = "store_true" , default=def_p  , help='Save a plot of digital output (default=\"{}\")'.format(def_p));
  parser.add_option('-r', '--recordN'     , dest='recordNperiod' , type = float  , default=def_np  , help='Output name of the saved plot (default=\"{}\")'.format(def_o));
  parser.add_option('-o', '--output'     , dest='outputname' , type = str  , default=def_o  , help='Output name of the saved plot (default=\"{}\")'.format(def_o));
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


# convert buffer 2D-array to buffer bit-array
def convert2DtoBitsArray(bit2Darray) :
    nBuffer    = max([ len(array) for array in bit2Darray ]);
    Out('nBuffer = {}'.format(nBuffer),1);
    bitsArray = [];
    # loop over time (buffer)
    for i in range(nBuffer) : 
      #Out('size(bit2Darray[:,{}]) = {}'.format(i, len(bit2Darray[:,i])),1);
      bits = 0;
      for ch in range(g_nDigitalChannels) :
        if len(bit2Darray[ch])>0 : bits += (bit2Darray[ch][i]) * 2**(ch);
        pass;
      bitsArray.append((int)(bits)); #
      pass;
    return bitsArray;


def closeCtx(ctx) :
  libm2k.contextClose(ctx);
  return;

def digitaloutSinglePulse(
  timeperiod = 0.1    , # Time period for one cycle with a pulse [sec]
  timeON     = 1e-2   , # Time at ON voltage [sec]
  samplerate = 1.*kHz , # Sampling rate [Hz] (Up to 100MHz)
  channels   = [0]    , # String of output channnel numbers combined with \',\'. There are 0~15 ch.
  timeoffsets= [0.0]  , # String of the start-time offset of the square wave [sec] cmbined with \',\' for each channels. (ex, "0.0", "-0.5e-6" for one channel, "0.0,0.5e-6", "0.5e+6,-0.5e+6" for two channels)
  ctx        = None   , # Instance of ADALM2000
  verbose    = 0      , # Verbosity
  doPlot     = False  , # Make & Save digital output plot
  recordNperiod = 10       , # Number of periods to record
  outputname    = "aho.png", # Output filename of the digital output plot
    ):
  setVerbose(verbose);

  # Argument check
  if len(timeoffsets) < len(channels) :
    Error('The number of timeoffsets is less than that of channels. Their numbers should be same.');
    Error('    channels    = ',channels );
    Error('    timeoffsets = ',timeoffsets);
    exit(1);
  for i,ch in enumerate(channels) :
    if abs(timeoffsets[i]) >= timeperiod :
      Error('|timeoffset| for ch {} is more than timeperiod. |timeoffset| should be < timeperiod.'.format(ch));
      Error('    timeoffset = {}'.format(timeoffsets[i]));
      Error('    timeperiod = {}'.format(timeperiod    ));
      exit(1);
    pass;

 
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
  dig=ctx.getDigital();
  for ch in range(g_nDigitalChannels) : 
    dig.enableChannel(ch,False);
    dig.setValueRaw(ch,0);
    pass;
  
  # Define run condition
  npointsPeriod = (int)(timeperiod*samplerate);
  dig.setCyclic(True);
  npoints  = npointsPeriod;
  Out('# of sampling points in a period = {}'.format(npoints),0);

  # Define outputs
  npointsON  = (int)(timeON*samplerate      );
  npointsOFF = (int)(npointsPeriod-npointsON);
  Out('time period / # of points in one period = {} usec / {} points'.format(timeperiod/usec, npointsPeriod),0);
  Out('time / # of points at ON  in one period = {} usec / {} points'.format(timeON/usec    , npointsON ),0);
  Out('time / # of points at OFF in one period = {} usec / {} points'.format((timeperiod-timeON)/usec, npointsOFF),0);
  buffer_array = [];
  for ch in range(g_nDigitalChannels) :
    if not ch in channels : 
      buffer_array.append([]);
      continue;
    chIndex = channels.index(ch);
    Out('Definning output for ch {}...'.format(ch),0);

    # Define waveform for one period
    waveformON = [0b1]*npointsON ; # array size = npointsON
    waveformOFF= [0b0]*npointsOFF; # array size = npointsOFF
    waveform = np.concatenate([ waveformON, waveformOFF ]);
    waveform = shiftWave(waveform, timeoffsets[chIndex], samplerate);
    Out('    time offset = {} [usec]'.format(timeoffsets[chIndex]/usec),0);
    Out('    waveform of one period ',2,waveform);

    buffer_array.append(waveform);
    pass;
  Out('buffer array of digital output ',2,buffer_array);

  # convert buffer 2D-array to buffer bit-array
  buffer_bits = convert2DtoBitsArray(buffer_array);
  
  # Setting
  for ch in channels :
    Out('channel {} : ON'.format(ch),0);
    dig.setDirection(ch,libm2k.DIO_OUTPUT)
    dig.enableChannel(ch,True);
    pass;
  dig.setSampleRateIn(samplerate); # Hz
  dig.setSampleRateOut(samplerate); # Hz
  
  # Run
  if verbose > 1 :
    for val in buffer_bits : Out('push value : {}'.format(bin(val)),2);
    pass;
  dig.push(buffer_bits);

  # Make & Save a plot of digital output
  if doPlot :
      # Get digital output
      npointsRecord = (int)(npointsPeriod*recordNperiod);
      data  = dig.getSamples(npointsRecord);
      utime = [ t/samplerate *1.e+6 for t in range(npointsRecord) ]; # Time [usec]
      if verbose>1 :
        for val in data : Out(bin(val),2);
        pass;
      # Make a plot
      for ch in range(g_nDigitalChannels) :
        y = [ 0b1 & (val>>ch) for val in data ];
        Out('y (ch={}) = {}'.format(ch, y),1);
        plt.plot(utime,y,label='ch {}'.format(ch), color=getcolor(ch));
        pass;
      plt.grid(True);
      plt.legend();
      plt.xlabel('Time [$\mu$sec]');
      plt.ylabel('Digital Output');
      plt.savefig(outputname);
      pass;
 
  return ctx; # End of digitalSinglePulse()
  

if __name__ == '__main__':
  config  = parseCmdLine(sys.argv);

  channels    = [ (int)(ch) for ch in (config.channels).split(',') ];
  timeoffsets = [ (float)(t) for t in (config.timeoffsets).split(',') ];

  ctx = digitaloutSinglePulse(
      timeperiod = config.timeperiod, # Time period of the square wave [sec]
      timeON     = config.timeON    , # Time at ON voltage [sec]
      samplerate = config.samplerate, # Sampling rate [Hz] (Up to 100MHz)
      channels   = channels,          # Array of output channnel numbers combined with \',\'. There are only 0 ch and 1 ch. (ex, "0", "1", "0,1",..)
      timeoffsets= timeoffsets,       # Start time offset of the square wave [sec] for each channels
      verbose    = config.verbose,    # Verbosity
      doPlot     = config.doPlot,     #
      recordNperiod = config.recordNperiod,# Number of periods to record
      outputname    = config.outputname,   # Output filename of the digital output plot
      ); 

  # Close ctx
  closeCtx(ctx);

  pass; # End of __main__
