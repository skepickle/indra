from indra import Indra

import sys
#import os
import signal

def main(*args, **kwargs):
  global pgm
  rval = 0
  pgm = Indra()
  if (pgm):
    rval = pgm.main()
  if (pgm):
    pgm.cleanup()
    del pgm
  sys.exit(rval)

def signal_handler(sig, frame):
  #print('You pressed CTRL+C: ' + str(sig))
  global pgm
  if (pgm):
    pgm.cleanup()
    del pgm
  sys.exit(130)

if __name__ == '__main__':
  # print(os.name)
  # print(sys.platform)
  signal.signal(signal.SIGINT,  signal_handler)
  signal.signal(signal.SIGQUIT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)
  if hasattr(signal, "SIGBREAK"):
    signal.signal(signal.SIGBREAK, signal_handler)
  main()
