import multiprocessing as mp
import readline
import time

from airavata import Airavata
from command_completer import CommandCompleter

class Indra:

  def __init__(self):
    self.airavata = None
    self.account  = None
    self.running  = True

  def __enter__(self):
    print("Indra __enter__()")

  def __exit__(self, ex_type, ex_value, ex_traceback):
    print("Indra __exit__()")

  def __del__(self):
    print("\nIndra __del__()")
    self.cleanup()

  def cleanup(self):
    print('\nIndra clean up.')
    if (self.airavata):
      # if (logged in): send pipe info to airavata process and wait for ack.
      del self.airavata
      self.account = None

  def prompt(self):
    if (self.account and self.airavata):
      return self.account + ' > '
    return '> '

  def help(self):
    print("help")
    #TODO print help info

  def login(self):
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
    #TODO prompt for cred/auth
    account = input("Account: ")
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
    key    = input("Client key: ")
    secret = input("Client secret: ")
    token  = input("Your access token: ")
    try:
      domain = "https://" + account.partition("@")[2]
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

  def logout(self):
    print("logout")
    #TODO ask for confirmation

  def quit(self):
    print("quit")
    #TODO ask for confirmation
    self.running = False

  def main(self):
    commands = {
      'help'     : self.help,
      'login'    : self.login,
      'logout'   : self.logout,
      'quit'     : self.quit,
      'exit'     : self.quit,
    }
    completer = CommandCompleter(commands.keys(), self.prompt)
    readline.set_completer(completer.complete)
    readline.set_completer_delims('')
    readline.parse_and_bind('tab: complete')
    readline.set_completion_display_matches_hook(completer.display_matches)
    try:
      while self.running:
        cmd = None
        try:
          cmd = input(self.prompt())
        except EOFError:
          print("EOFError")
        if cmd in commands.keys():
          commands[cmd]()
        #TODO HERE check pipe from Airavata
        #TODO HERE update state
        #TODO HERE
        #TODO HERE
        time.sleep(0.1)

    except Exception as e:
      print('Interrupted something else')
      print(e)
      return 1

    return 0
