# terminal.py - internal methods for terminal interactions

class Indra():

  def command_prompt(self):
    if (self.account and self.airavata):
      return self.account + ' > '
    return '> '

  def command_input(self, prompt=None):
    import logging
    import readline
    from command_completer import CommandCompleter
    if not prompt:
      prompt = self.command_prompt()
    if not self.commands_completer:
      self.commands_completer = CommandCompleter(self.commands.keys(), self.command_prompt)
    readline.set_completer(self.commands_completer.complete)
    readline.set_completer_delims('')
    readline.parse_and_bind('tab: complete')
    readline.set_completion_display_matches_hook(self.commands_completer.display_matches)
    s = None
    try:
      if prompt:
        s = input(prompt)
      else:
        s = input()
      if not s:
        s = None
    except EOFError:
      logging.debug("Pressed <Ctrl+D>")
      s = None
    except KeyboardInterrupt:
      logging.debug("Pressed <Ctrl+C>")
      s = None
    return s

  def input(self, prompt, options=[]):
    import logging
    import readline
    from command_completer import CommandCompleter
    if options:
      completer = CommandCompleter(options, lambda : prompt)
      readline.set_completer(completer.complete)
      readline.set_completer_delims('')
      readline.parse_and_bind('tab: complete')
      readline.set_completion_display_matches_hook(completer.display_matches)
    else:
      readline.parse_and_bind('tab: redraw-current-line')
    s = None
    try:
      s = input(prompt)
      if not s:
        s = None
    except EOFError:
      logging.debug("Pressed <Ctrl+D>")
      s = None
    except KeyboardInterrupt:
      logging.debug("Pressed <Ctrl+C>")
      s = None
    return s

  def multiline_input(self, prompt, options=[]):
    #TODO
    pass
    return