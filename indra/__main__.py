from indra import Indra

import sys
import signal

def main(*args, **kwargs):
  global pgm
  import logging
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
  rval = 0
  pgm = Indra()
  if (pgm):
    rval = pgm.main()
  if (pgm):
    #print()
    pgm.cleanup()
    del pgm
  sys.exit(rval)

def ctrl_c_handler(sig, frame):
  global pgm

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
  #signal.signal(signal.SIGINT,  ctrl_c_handler)
  signal.signal(signal.SIGQUIT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)
  if hasattr(signal, "SIGBREAK"):
    signal.signal(signal.SIGBREAK, signal_handler)
  main()
