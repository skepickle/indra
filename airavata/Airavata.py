from mastodon import Mastodon
import time
#from multiprocessing import Pipe

class Airavata:

  def __init__(self):
    self.mastodon = Mastodon(access_token = 'personalgm_usercred.secret')
    print(self.mastodon.__dict__)
    print("Logged in!")
    #self.mastodon.toot('Tooting from Python using #mastodonpy !')

  def __init__(self, credfile):
    self.mastodon = Mastodon(access_token = credfile)
    print(self.mastodon.__dict__)
    try:
      self.mastodon.app_verify_credentials()
      #print("Logged in!")
    except:
      #print("Not logged in!")
      self.mastodon = None
    #self.mastodon.toot('Tooting from Python using #mastodonpy !')

  def main(self, conn):
    i = 0
    while True:
      try:
        time.sleep(1)
        i = (i + 1) % 10
        if conn and conn.poll(0):
          cmd = conn.recv()
          if cmd == "Indra->cleanup()":
            return
        if not i:
          conn.send("ping")
      except KeyboardInterrupt:
        pass
      except Exception as e:
        pass
