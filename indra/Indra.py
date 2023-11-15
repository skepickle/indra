#import multiprocessing as mp

from airavata import Airavata

from indra.internal import Indra as IndraInternal
from indra.special import Indra as IndraSpecial
from indra.cli import Indra as IndraCLI

class Indra(IndraInternal, IndraSpecial, IndraCLI):

  def help(self):
    import logging
    logging.debug("->help()")

  def login(self):
    try:
      import logging
      logging.debug("->login()")
      import os.path
      try:
        config_dir = self.config_dir()
      except:
        return
      if self.account:
        logging.info("Already logged into "+str(self.account))
        logging.info("Logout first if you want to log into another account")
        return
      while True:
        account = self.input("Account: ", self.config_dir_accounts())
        if account and account.count('@') != 1:
          logging.error("Account names must fit <username@example.com> pattern")
        else:
          break
      if not account:
        logging.error("Cancelling login")
        return
      cred_file = config_dir+"/"+account+".cred"
      while True:
        if os.path.isfile(cred_file):
          import signal
          # try to login and return if successful
          original_sigint_handler = signal.getsignal(signal.SIGINT)
          signal.signal(signal.SIGINT, self.null_sig_handler)
          airavata = Airavata(cred_file)
          if (airavata.mastodon):
            self.account = account
            self.airavata = airavata
            signal.signal(signal.SIGINT, original_sigint_handler)
            return
          else:
            del airavata
            logging.error("Failed to login using existing credentials file at "+cred_file)
            logging.error("Prompting further to overwrite file...")
            signal.signal(signal.SIGINT, original_sigint_handler)
        domain = "https://" + account.partition("@")[2]
        while True:
          key = self.input("Client key: ")
          if not key:
            logging.error("Cancelling login")
            return
          if key.len() != 43:
            logging.error("Invalid client key")
          else:
            break
        while True:
          secret = self.input("Client secret: ")
          if not secret:
            logging.error("Cancelling login")
            return
          if secret.len() != 43:
            logging.error("Invalid client secret")
          else:
            break
        while True:
          token = self.input("Your access token: ")
          if not token:
            logging.error("Cancelling login")
            return
          if token.len() != 43:
            logging.error("Invalid access token")
          else:
            break
        try:
          f = open(cred_file, "w")
          f.write(token+"\n"+domain+"\n"+key+"\n"+secret+"\n")
          f.close()
        except:
          logging.error("Could not write to credentials file at "+cred_file)
          return
    except KeyboardInterrupt:
      logging.debug("Pressed <Ctrl+C>")

  def logout(self):
    try:
      import logging
      logging.debug("->logout()")
    except KeyboardInterrupt:
      logging.debug("Pressed <Ctrl+C>")

  def quit(self):
    import logging
    logging.debug("->quit()")
    #TODO ask for confirmation
    self.running = False

  def main(self):
    import logging
    import time
    logging.debug("->main()")
    while self.running:
      try:
        cmd = self.command_input()
        if cmd in self.commands.keys():
          self.commands[cmd]()
        #TODO HERE check pipe from Airavata
        #TODO HERE update state
        #TODO HERE
        #TODO HERE
        time.sleep(0.10)
      except KeyboardInterrupt:
        logging.debug("Pressed <Ctrl+C>")
        s = None
      except Exception as e:
        logging.debug('Exception occurred: ' + str(type(e)))

    return 0
