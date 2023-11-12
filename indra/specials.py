# specials.py - special methods for Indra class

class Indra():

  def __init__(self):
    self.airavata = None
    self.account  = None
    self.running  = True
    self.commands = {
      'help'     : self.help,
      'login'    : self.login,
      'logout'   : self.logout,
      'quit'     : self.quit,
      'exit'     : self.quit,
    }

  def __enter__(self):
    print("Indra __enter__()")

  def __exit__(self, ex_type, ex_value, ex_traceback):
    print("Indra __exit__()")

  def __del__(self):
    print("\nIndra __del__()")
    self.cleanup()
