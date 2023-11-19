# internal.py - internal methods for Indra class

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
    self.commands_completer = None
    self.parent_conn = None
    self.child_conn = None
    self.child_proc = None

  def config_dir(self):
    import logging
    import os
    dir = os.path.expanduser("~") + "/.vritrasura"
    if os.path.exists(dir) and os.path.isfile(dir):
      logging.error('~/.vritrasura exists but is not a directory')
      raise NotADirectoryError
    if not os.path.exists(dir):
      os.mkdir(dir, 0o750)
      return dir
    if not (os.access(dir, os.R_OK) and
            os.access(dir, os.X_OK)):
      logging.error('~/.vritrasura directory exists but is not accessible')
      raise PermissionError
    return dir

  def config_dir_accounts(self):
    import logging
    import os
    import os.path
    dir = self.config_dir()
    return [f.removesuffix('.cred') for f in os.listdir(dir)
      if os.path.isfile(os.path.join(dir, f)) and f.endswith('.cred')]

  def cleanup(self):
    import logging
    logging.debug('Indra clean up.')
    if (self.airavata):
      # if (logged in): send pipe info to airavata process and wait for ack.
      if self.parent_conn:
        self.parent_conn.send("Indra->cleanup()")
      del self.airavata
      self.account = None

  def null_sig_handler(signum, frame):
    return