class Event:
  def __init__(self):
    self.display_id = display_id
    self.uuid = uuid
    self.doc_id = doc_id
    self.geo = geo
    self.platform = platform
    self.timestamp = timestamp


class Doc:
  def __init__(self):
    self.source_id = source_id
    self.publisher = publisher
    self.pub_time = pub_time
    self.cats = cats
    self.entities = entities
    self.topics = topics

class Ad:
  def __init__():
    self.ad_id = ad_id
    self.camp = camp
    self.doc_id = doc_id
    self.advertiser = advertiser

'''
param events: map<display_id, Event>
param docs: map<doc_id, Doc>
'''
class OutBrainManager:
  def init(self):
    self.events = []
    self.docs = []
    self.ads = []

  def get_event(self, display_id):
    if self.events.has_key(display_id):
      return self.events[display_id]
    else:
      return None

  def get_doc(self, doc_id):
    if self.docs.has_key(doc_id):
      return self.docs[doc_id]
    else:
      return None

  def get_ad(self, ad_id)
    if self.ads.has_key(ad_id):
      return self.ads[ad_id]
    else:
      return None

