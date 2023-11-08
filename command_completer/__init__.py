class CommandCompleter(object):  # Custom completer

  def __init__(self, options, prompter):
    self.options = sorted(options)
    self.prompter = prompter

  def complete(self, text, state):
    if state == 0:  # on first trigger, build possible matches
      if not text:
        self.matches = self.options[:]
      else:
        text = text.strip()
        self.matches = [s for s in self.options
                        if s and s.startswith(text)]
    # return match indexed by state
    try:
      return self.matches[state]
    except IndexError:
      return None

  def display_matches(self, substitution, matches, longest_match_length):
    import readline
    from os import get_terminal_size
    line_buffer = readline.get_line_buffer()
    columns = get_terminal_size().columns
    print()
    tpl = "{:<" + str(int(max(map(len, matches)) * 1.2)) + "}"
    buffer = ""
    for match in matches:
      match = tpl.format(match[len(substitution):])
      if len(buffer + line_buffer + match) > columns:
        print(buffer)
        buffer = ""
      buffer += line_buffer + match
    if buffer:
        print(buffer)
    print(self.prompter(), end="")
    print(line_buffer, end="", flush=True)
