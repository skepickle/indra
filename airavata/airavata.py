from mastodon import Mastodon

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
