import multiprocessing as mp
import time

from airavata import Airavata

from indra.specials import Indra as IndraSpecials
from indra.cli import Indra as IndraCLI

class Indra(IndraSpecials, IndraCLI):

  def cleanup(self):
    print('\nIndra clean up.')
    if (self.airavata):
      # if (logged in): send pipe info to airavata process and wait for ack.
      del self.airavata
      self.account = None

  def help(self):
    print("help")
    #TODO print help info

  def login(self):
    try:
      print("login()")
      import os.path
      config_dir = os.path.expanduser("~") + "/.pgm"
      if os.path.exists(config_dir) and os.path.isfile(config_dir):
        print("ERROR: ~/.pgm is is not a directory.")
        return
      if not os.path.exists(config_dir):
        os.mkdir(config_dir, 0o750)
      if self.account:
        print("Already logged into "+str(self.account))
        print("Logout first if you want to log into another account")
        return
      else:
        del airavata
        print("Failed to login")
      #TODO prompt for cred/auth
      account = self.input("Account: ")
      if not account:
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
          print("Failed to login using existing credentials file at "+cred_file)
          print("Prompting further to fix...")
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
        print("Error: Could not write to credentials file at "+cred_file)
      if os.path.isfile(cred_file):
        # try to login and return if successful
        airavata = Airavata(cred_file)
        if (airavata.mastodon):
          self.account = account
          self.airavata = airavata
          return
        else:
          del airavata
          print("Failed to login")
    except KeyboardInterrupt:
      print(" <Ctrl+C>")
      s = None

  def logout(self):
    print("logout")
    #TODO ask for confirmation

  def quit(self):
    print("quit")
    #TODO ask for confirmation
    self.running = False

  def main(self):
    try:
      while self.running:
        try:
          cmd = self.command_input(self.command_prompt())
          if cmd in self.commands.keys():
            self.commands[cmd]()
          #TODO HERE check pipe from Airavata
          #TODO HERE update state
          #TODO HERE
          #TODO HERE
          time.sleep(0.10)
        except KeyboardInterrupt:
          print(" <Ctrl+C>")
          s = None

    except Exception as e:
      print('Interrupted something else')
      print(e)
      return 1

    return 0
