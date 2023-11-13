# special.py - special methods for Indra class

class Indra():

  def __enter__(self):
    import logging
    logging.debug("->Indra.__enter__()")

  def __exit__(self, ex_type, ex_value, ex_traceback):
    import logging
    logging.debug("->Indra.__exit__()")

  def __del__(self):
    import logging
    logging.debug("->Indra.__del__()")
    self.cleanup()
