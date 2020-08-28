
kHz=1e+3;
MHz=1e+6;
usec=1e-6;

g_nAnalogInChannels  = 2; # Number of all the analog in channels for ADALM2000
g_nAnalogOutChannels = 2; # Number of all the analog out channels for ADALM2000
g_nDigitalChannels   =16; # Number of all the digital channels for ADALM2000
g_colors     = [
        'k','r','b','g','c',
        'm','y','tab:blue','tab:orange','tab:green',
        'tab:red','tab:purple','tab:brown','tab:pink','tab:gray',
        ];
g_linestyles = ['solid','dotted','dashed','dashdot', (0,(1,10)), (0,(5,10)), (0,(5,5)), (0,(5,1))];

def getcolor(i):
  I=i;
  if I>=len(g_colors) : I = I % len(g_colors);
  return g_colors[I];
def getlinestyle(i):
  I=i;
  if I>=len(g_linestyles) : I = I % len(g_linestyles);
  return g_linestyles[I];

# for Out() & Error()
import inspect, resource;
g_verbose=0; # 0: default, 1:More cout, 2:All cout, -1:Less cout, -2:No cout

def setVerbose(verbose):
  global g_verbose;
  g_verbose = verbose;
  return;

def Out(comment,verbosityLevel=1,*args) :
  if verbosityLevel<=g_verbose :
    mem      = resource.getrusage(resource.RUSAGE_SELF)[2];
    funcname = inspect.currentframe().f_back.f_code.co_name;
    if len(args)>0 : print( '{}() ({}KB): {} / {}'.format(funcname, (int)(mem/1024), comment, args));
    else           : print( '{}() ({}KB): {}'     .format(funcname, (int)(mem/1024), comment));
    pass;
  return; # End of Out()

def Error(comment,*args) :
  mem      = resource.getrusage(resource.RUSAGE_SELF)[2];
  funcname = inspect.currentframe().f_back.f_code.co_name;
  if len(args)>0 : print( '{}() ({}KB): Error!! {} / {}'.format(funcname, (int)(mem/1024), comment, args));
  else           : print( '{}() ({}KB): Error!! {}'     .format(funcname, (int)(mem/1024), comment));
  return; # End of Error()


def checkIsFloat(varray, arrayname='array') :
  for i, v in enumerate(varray) :
    if isinstance(v,int) :
      Out('Warning!! The {} is int type. This should be float.'.format(arrayname),1);
      v = float(v);
      varray[i] = v;
      pass;
    if not isinstance(v,float) :
      Error('The {} is not float type. This should be float.'.format(arrayname));
      Error('    {}           = {}'.format(arrayname,varray)          );
      Error('    {}[{}])      = {}'.format(arrayname,i,varray[i])     );
      Error('    type({}[{}]) = {}'.format(arrayname,i,type(varray[i])) );
      exit(1);
      pass;
    pass;
  return varray;
 

def closeCtx():
    pass;
