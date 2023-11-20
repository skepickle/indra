from indra import Indra

import sys
import signal
import logging

def main(*args, **kwargs):
  global indra
  #TODO add argument parsing and maybe have logging level be setable.
  logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
  rval = 1
  indra = Indra()
  if (indra):
    rval = indra.main()
  if (indra):
    #print()
    indra.cleanup()
    del indra
  sys.exit(rval)

def ctrl_c_handler(sig, frame):
  global indra
  pass
  return

def signal_handler(sig, frame):
  #print('You pressed CTRL+C: ' + str(sig))
  global indra
  if (indra):
    indra.cleanup()
    del indra
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
