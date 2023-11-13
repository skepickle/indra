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
    import logging
    logging.debug("->login()")
    try:
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
      if os.path.isfile(cred_file):
        # try to login and return if successful
        airavata = Airavata(cred_file)
        if (airavata.mastodon):
          self.account = account
          self.airavata = airavata
          return
        else:
          del airavata
          logging.error("Failed to login using existing credentials file at "+cred_file)
          logging.error("Prompting further to fix...")
      key    = self.input("Client key: ")
      secret = self.input("Client secret: ")
      token  = self.input("Your access token: ")
      domain = "https://" + account.partition("@")[2]
      try:
        f = open(cred_file, "w")
        f.write(token+"\n")
        f.write(domain+"\n")
        f.write(key+"\n")
        f.write(secret+"\n")
        f.close()
      except:
        logging.error("Could not write to credentials file at "+cred_file)
      if os.path.isfile(cred_file):
        airavata = Airavata(cred_file)
        if (airavata.mastodon):
          self.account = account
          self.airavata = airavata
          return
        else:
          del airavata
          logging.error("Failed to login")
    except KeyboardInterrupt:
      logging.debug("Pressed <Ctrl+C>")
      s = None

  def logout(self):
    import logging
    logging.debug("->logout()")

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
