# This script assumes the following connections:
# Ch1 : analog signal -> 1+ / GND -> 1-
# Ch2 : analog signal -> 2+ / GND -> 2-

import os, sys
import libm2k
import matplotlib.pyplot as plt
import numpy as np

from utils import *

def parseCmdLine(args):
  # default values
  def_t   = 1e-3 ;
  def_s   = 1e+8 ;
  def_n   = 1    ;
  def_c   = "0,1";
  def_r   = ","  ;
  def_to  = 0.   ;
  def_O   = './output';
  def_o   = 'aho';
  def_v   = 0    ;

  from optparse import OptionParser;
  parser = OptionParser();
  parser.add_option('-t', '--time'      , dest='timelength', type = float, default=def_t , help='Measurement time length for each measurement [sec] (default={:.2e})'.format(def_t));
  parser.add_option('-s', '--samplerate', dest='samplerate', type = float, default=def_s , help='Sampling rate [Hz] (1e+3, 10e+3, 100e+3, 1e+6, 10e+6, 100e+6) (default={:.2e})'.format(def_s));
  parser.add_option('-n', '--nMeasure'  , dest='nMeasure'  , type = int  , default=def_n , help='Number of measurements (default={})'.format(def_n));
  parser.add_option('-c', '--channels'  , dest='channels'  , type = str  , default=def_c , help='String of measured channnel numbers combined with \',\'. There are only 0 ch and 1 ch. (ex, "0", "1", "0,1",..) (default=\"{}\")'.format(def_c));
  parser.add_option('-r', '--rangeTypes', dest='rangeTypes', type = str  , default=def_r , help='String of the voltage range-types combined with \',\' for each channels. \'w\'=-25~25V / otherwise=-2.5~2.5V (ex, "w", "" for one channel, "w,w", ",w", "w,", "," for two channels) (default=\"{}\")'.format(def_r));
  parser.add_option(      '--timeoffset', dest='timeoffset', type = float, default=def_to, help='Start time in plots [sec] (default={:.2e})'.format(def_to));
  parser.add_option(      '--noSave'    , dest='doSave'    , action="store_false" , default=True , help='Not save the data to csv files (default:Save data)');
  parser.add_option(      '--noPlot'    , dest='doPlot'    , action="store_false" , default=True , help='Not save the plots to files (default:Save plots)');
  parser.add_option(      '--overlapPlot'    , dest='overPlot', action="store_true"  , default=False , help='Plots are overlapped in one figure (default:False)');
  parser.add_option('-O', '--outputDir' , dest='outputDir' , type = str  , default=def_O , help='output file directory (default=\"{}\")'.format(def_O));
  parser.add_option('-o', '--outputName', dest='outputName', type = str  , default=def_o , help='output file name without extension (no .png or .txt etc...) (default=\"{}\")'.format(def_o));
  parser.add_option('-v', '--verbose'   , dest='verbose'   , type = int  , default=def_v , help='verbosity (0:Normal, 1:More output, 2:All output, -1:Less output, 2:No output) (default={})'.format(def_v));
  (config, args) = parser.parse_args(args);
  Out("",True,config);
  return config;


def setRange(ain, ch, rangeType) :
  if 'w' in rangeType : ain.setRange(ch,-25 , 25); # wide range of voltage -25~25V
  else                : ain.setRange(ch,-2.5,2.5); # narrow range of voltage -2.5~2.5V (default)
  return;

def closeCtx(ctx) :
  libm2k.contextClose(ctx);
  return;

def analogin(
  timelength  = 10.*usec,  # Measurement time length for each measurement [sec]
  samplerate  = 100.*MHz,  # Sampling rate [Hz] (1*kHz, 10*kHz, 100*kHz, 1*MHz, 10*MHz, 100*MHz)
  nMeasure    = 1,         # Number of measurements
  channels    = [0,1],     # Channel numbers to be recorded ([0] or [1] or [0,1])
  rangeTypes = ['',''],    # String array of the voltage range type for each channels; 'w'=-25~25V, otherwise=-2.5~2.5V
  timeoffset  =  0.*usec , # Start time in plots [sec]
  ctx=None,            # Instance of ADALM2000
  doSave  = True,      # Save the data to csv files or not
  doPlot  = True,      # Save the plots to files or not
  overlapPlot=False,   # Plots are overlapped in one figure
  outputDir  = './output',  # Directory for the saved files 
  outputName = 'aho', # File name of the saved files
  verbose    = 0    , # Verbosity
    ):
  setVerbose(verbose);

  # argument check
  if len(rangeTypes) < len(channels) :
    Error('The number of rangeTypes is less than that of channels. Their numbers should be same.');
    Error('   channels   = ',channels  );
    Error('   rangeTypes = ',rangeTypes);
    exit(1);
 
  # initialize
  if ctx is None:
    ctx=libm2k.m2kOpen();
    if ctx is None:
      Error("Connection Error: No ADALM2000 device available/connected to your PC.");
      exit(1);
      pass;
    ctx.calibrateADC();
    ctx.calibrateDAC();
    pass;
  ain=ctx.getAnalogIn();
  for ch in range(g_nAnalogInChannels) : ain.enableChannel(ch,False);
  
  # define numbers
  npoints     = (int)(timelength*samplerate)+1;
  Out('measurement time length = {} [usec]'.format(timelength/usec),0);
  Out('# of measurement = {}'.format(nMeasure),0);
  Out('# of sampling points in each measurement = {}'.format(npoints),0);
  
  # Setting
  for ch in channels :
    Out('channel {} : ON'.format(ch),0);
    ain.enableChannel(ch,True);
    setRange(ain, ch, rangeTypes[channels.index(ch)]);
    pass;
  ain.setSampleRate(samplerate); # Hz
  
  # Measure
  outputAllFullpath = '{}/{}'.format(outputDir, outputName);
  time = np.linspace(timeoffset, timeoffset+timelength, npoints); # time unit is sec
  time_usec = time/usec;
  datas=[];
  for i in range(nMeasure):
    data = ain.getSamples(npoints);
    datas.append(data);
    Out('{}th data ='.format(i), 2, data);
    pass;

  # Make output directory
  if (doSave or doPlot) and (not os.path.isdir(outputDir)):
    Out('Making directory: {}'.format(outputDir), 0);
    os.makedirs(outputDir);
    pass;

  for i in range(nMeasure):
    # Output name
    if nMeasure==1 : outputFullpath = outputAllFullpath;
    else           : outputFullpath = '{}_{}'.format(outputAllFullpath, i);

    # Save data
    if doSave :
      Out('save data for {}th measurement...'.format(i), 2);
      header    = 'time[sec] '+' '.join([ 'output_ch{}'.format(ch) for ch in channels ]);
      savearray = np.concatenate([[time],datas[i]]);
      Out('    header = {}'.format(header), 2);
      Out('    save data array = ', 2, savearray);
      np.savetxt(outputFullpath+'.csv', savearray.transpose(), fmt='%.18e', delimiter=' ', header=header,comments='#');
      pass;

    # Plot
    if doPlot :
      for k, ch in enumerate(channels) : 
        if overlapPlot :
          color = g=getcolor(k);
          linestyle = getlinestyle(i);
          marker='';
          markersize=1;
          label ='channel {}: {}th'.format(ch, i);
        else :
          color = g=getcolor(k);
          linestyle = '';
          marker='o';
          markersize=1;
          label ='channel {}'.format(ch);
          pass;
        plt.plot(time_usec, datas[i][k],linestyle=linestyle,marker=marker,markersize=markersize,color=color,label=label);
        pass; # End of loop over channels
      plt.xlabel('Time [$\mu$s]');
      plt.ylabel('Voltage [V]');
      plt.legend();
      plt.grid(True);
      if not overlapPlot :
        plt.savefig(outputFullpath+'.png');
        plt.clf();
        pass;
      pass;

    pass; # End of loop over nMeasure
  if doPlot and overlapPlot : 
    plt.savefig(outputAllFullpath+'.png');
    plt.clf();
    pass;


  return ctx; # End of analogin()
  

if __name__ == '__main__':
  config  = parseCmdLine(sys.argv);

  ctx = analogin(
      timelength  = config.timelength,  # [sec] Measurement time length for each measurement
      samplerate  = config.samplerate,  # [Hz] Sampling rate (1*kHz, 10*kHz, 100*kHz, 1*MHz, 10*MHz, 100*MHz)
      nMeasure    = config.nMeasure  ,  # Number of measurements
      channels    = [ (int)(ch) for ch in (config.channels).split(',') ], # Channel numbers to be recorded ([0] or [1] or [0,1])
      rangeTypes  = (config.rangeTypes).split(','),                       # String array of the voldate range type for each channels; 'w'=-25~25V, otherwise=-2.5~2.5V
      timeoffset  = config.timeoffset , # [sec] Start time in plots
      ctx     = None,               # Instance of ADALM2000
      doSave  = config.doSave,      # Save the data to csv files or not
      doPlot  = config.doSave,      # Save the plots to files or not
      overlapPlot = overlapPlot,    # Plots are overlapped in one figure
      outputDir  = config.outputDir,  # Directory for the saved files 
      outputName = config.outputName, # File name of the saved files
      verbose    = config.verbose,    # Verbosity
      );

  # Close ctx
  closeCtx(ctx);

  pass; # End of __main__
