from datetime import datetime
from sets import Set

class Event:
  def __init__(self, display_id, uuid, doc_id, geo, platform, timestamp):
    self.display_id = display_id
    self.uuid = uuid
    self.doc_id = doc_id
    self.geo = geo
    self.platform = platform
    self.timestamp = timestamp

class Entity:
  def __init__(self, ent_id, cfd):
    self.id = ent_id
    self.cfd = cfd

class Topic:
  def __init__(self, topic_id, cfd):
    self.id = topic_id 
    self.cfd = cfd

class Cat:
  def __init__(self, cat_id, cfd):
    self.id = cat_id
    self.cfd = cfd

class Doc:
  def __init__(self, doc_id, source_id, publisher, pub_time):
    self.doc_id = doc_id
    self.source_id = source_id
    self.publisher = publisher
    self.pub_time = pub_time
    self.cats = []
    self.entities = []
    self.topics = []

class Ad:
  def __init__(self, ad_id, camp, doc_id, advertiser):
    self.ad_id = ad_id
    self.camp = camp
    self.doc_id = doc_id
    self.advertiser = advertiser
    
class Click:
  def __init__(self, display_id, ad_id, clicked):
    self.display_id = display_id
    self.ad_id = ad_id
    self.clicked = clicked

'''
param events: map<display_id, Event>
param docs: map<doc_id, Doc>
'''
class OutBrainManager:
  def __init__(self):
    self.events = {}
    self.docs = {}
    self.ads = {}
    self.clicks = []
    self.doc_id_set = Set()
    self.read_data_file()

  def _read_file(self, file_name, on_read_line):
    f = open(file_name, "r")
    print("start reading " + file_name)
    start = datetime.utcnow()

    # abandon the first line
    line = f.readline()

    line_num = 0
    line = f.readline()
    while line:
      line = line.rstrip()
      on_read_line(line)
      line = f.readline()
      line_num = line_num + 1

    end = datetime.utcnow()
    print("time elapsed seconds:" + str((end-start).seconds))
    print("line num:" + str(line_num))
    print("read " + file_name + " end")
    f.close()

  def _read_ads(self, file_name):
    def on_read_line(line):
      # ad_id,document_id,campaign_id,advertiser_id
      # 1,6614,1,7
      [ad_id, doc_id, camp_id, adv_id] = line.split(',')
      self.ads[ad_id] = Ad(ad_id, camp_id, doc_id, adv_id)
      self.doc_id_set.add(doc_id)
    self._read_file(file_name, on_read_line)

  def _read_events(self, file_name):
    def on_read_line(line):
      # display_id,uuid,document_id,timestamp,platform,geo_location
      # 1,cb8c55702adb93,379743,61,3,US>SC>519
      [display_id, uuid, doc_id, ts , pt, geo] = line.split(',')
      self.events[display_id] = Event(display_id, uuid, doc_id, geo, pt, ts)
      self.doc_id_set.add(doc_id)
    self._read_file(file_name, on_read_line)

  def _read_clicks(self, file_name):
    def on_read_line(line):
      # display_id,ad_id,clicked
      # 1,42337,0
      [display_id, ad_id, clicked] = line.split(',')
      self.clicks.append(Click(display_id, ad_id, clicked))
    self._read_file(file_name, on_read_line)

  def _read_docs(self, doc_meta, doc_ent, doc_cat, doc_topic):
    def on_read_doc_meta_line(line):
      # document_id,source_id,publisher_id,publish_time
      # 1595802,1,603,2016-06-05 00:00:00
      [doc_id, src_id, pub_id, pub_time] = line.split(',')
      if doc_id in self.doc_id_set:
        self.docs[doc_id] = Doc(doc_id, src_id, pub_id, pub_time)

    def on_read_doc_ent_line(line):
      # document_id,entity_id,confidence_level
      # 1524246,f9eec25663db4cd83183f5c805186f16,0.672865314504701
      [doc_id, ent_id, cfd] = line.split(',')
      if self.docs.has_key(doc_id):
        self.docs[doc_id].entities.append(Entity(ent_id, cfd))

    def on_read_doc_topic_line(line):
      # document_id,topic_id,confidence_level
      # 1595802,140,0.0731131601068925
      [doc_id, topic_id, cfd] = line.split(',')
      if self.docs.has_key(doc_id):
        self.docs[doc_id].topics.append(Topic(topic_id, cfd))

    def on_read_doc_cat_line(line):
      # document_id,category_id,confidence_level
      # 1595802,1611,0.92
      [doc_id, cat_id, cfd] = line.split(',')
      if self.docs.has_key(doc_id):
        self.docs[doc_id].cats.append(Cat(cat_id, cfd))

    self._read_file(doc_meta, on_read_doc_meta_line)
    self._read_file(doc_ent, on_read_doc_ent_line)
    self._read_file(doc_cat, on_read_doc_cat_line)
    self._read_file(doc_topic, on_read_doc_topic_line)

  def read_data_file(self):
    self._read_events("data/mini_events.csv")
    self._read_clicks("data/mini_clicks_train.csv")
    self._read_ads("data/promoted_content.csv")
    self._read_docs("data/documents_meta.csv", 
            "data/documents_entities.csv",
            "data/documents_categories.csv",
            "data/documents_topics.csv")

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

  def get_ad(self, ad_id):
    if self.ads.has_key(ad_id):
      return self.ads[ad_id]
    else:
      return None

if __name__ == '__main__':
  manager = OutBrainManager()
