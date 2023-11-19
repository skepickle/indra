#import multiprocessing as mp
import time
import logging

from indra.internal   import Indra as IndraInternal
from indra.special    import Indra as IndraSpecial
from indra.terminal   import Indra as IndraTerminal
from indra.connection import Indra as IndraConnection

class Indra(IndraInternal, IndraSpecial, IndraTerminal, IndraConnection):

  def help(self):
    logging.debug("->help()")

  def quit(self):
    logging.debug("->quit()")
    #TODO ask for confirmation
    self.running = False

  def main(self):
    logging.debug("->main()")
    self.running = True
    while self.running:
      try:
        cmd = self.command_input()
        if cmd in self.commands.keys():
          self.commands[cmd]()
        #TODO HERE check pipe from Airavata
        #TODO HERE update state
        #TODO HERE
        #TODO HERE
        while self.parent_conn and self.parent_conn.poll(0):
          logging.info("~>main(): " + str(self.parent_conn.recv()))
        time.sleep(0.10)
      except KeyboardInterrupt:
        logging.debug("Pressed <Ctrl+C>")
        s = None
      except Exception as e:
        logging.debug('Exception occurred: ' + str(type(e)))
    return 0
