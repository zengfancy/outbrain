from datetime import datetime

'''
param display_id: int
param uuid: str
param doc_id: int
param geo: str
param platform: int
param timestamp: int
'''
class Event:
  def __init__(self, display_id, uuid, doc_id, geo, platform, timestamp):
    self.display_id = display_id
    self.uuid = uuid
    self.doc_id = doc_id
    self.geo = geo
    self.platform = platform
    self.timestamp = timestamp

'''
param ent_id: str
param cfd: float
'''
class Entity:
  def __init__(self, ent_id, cfd):
    self.id = ent_id
    self.cfd = cfd

'''
param topic_id: int
param cfd: float
'''
class Topic:
  def __init__(self, topic_id, cfd):
    self.id = topic_id 
    self.cfd = cfd

'''
param cat_id: int
param cfd: float
'''
class Cat:
  def __init__(self, cat_id, cfd):
    self.id = cat_id
    self.cfd = cfd

'''
param doc_id: int
param src_id: int
param publisher: int
param pub_time: str
'''
class Doc:
  def __init__(self, doc_id, source_id, publisher, pub_time):
    self.doc_id = doc_id
    self.source_id = source_id
    self.publisher = publisher
    self.pub_time = pub_time
    self.cats = []
    self.entities = []
    self.topics = []

'''
param ad_id: int
param camp: int
param doc_id: int
param adv:  int
'''
class Ad:
  def __init__(self, ad_id, camp, doc_id, advertiser):
    self.ad_id = ad_id
    self.camp = camp
    self.doc_id = doc_id
    self.advertiser = advertiser
   
'''
param display_id: int
param ad_id: int
param clicked: bool
'''
class Click:
  def __init__(self, display_id, ad_id, clicked):
    self.display_id = display_id
    self.ad_id = ad_id
    self.clicked = clicked

#US>ZA>345
def extract_geo(geo):
  new_geo = ''
  l = geo.split('>')
  for elem in l:
    if len(elem) > 0 and elem[0] >= 'A' and elem[0] <= 'Z':
      new_geo += elem
  return new_geo

#2016-06-05 00:00:00
def extract_pub_time(pub_time):
  l = pub_time.split(' ')
  lst = l[0].split('-')
  if len(lst) >= 2:
    return lst[0] + lst[1]
  elif len(lst) == 1:
    return lst[0]
  else:
    return ''

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
    self.doc_id_set = {}

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
      self.doc_id_set[doc_id] = 1
    self._read_file(file_name, on_read_line)

  def _read_events(self, file_name):
    def on_read_line(line):
      # display_id,uuid,document_id,timestamp,platform,geo_location
      # 1,cb8c55702adb93,379743,61,3,US>SC>519
      [display_id, uuid, doc_id, ts , pt, geo] = line.split(',')
      geo = extract_geo(geo)
      self.events[display_id] = Event(display_id, uuid, doc_id, geo, pt, ts)
      self.doc_id_set[doc_id] = 1
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
      pub_time = extract_pub_time(pub_time)
      if doc_id in self.doc_id_set.keys():
        self.docs[doc_id] = Doc(doc_id, src_id, pub_id, pub_time)

    def on_read_doc_ent_line(line):
      # document_id,entity_id,confidence_level
      # 1524246,f9eec25663db4cd83183f5c805186f16,0.672865314504701
      [doc_id, ent_id, cfd] = line.split(',')
      if doc_id in self.docs:
        self.docs[doc_id].entities.append(Entity(ent_id, cfd))

    def on_read_doc_topic_line(line):
      # document_id,topic_id,confidence_level
      # 1595802,140,0.0731131601068925
      [doc_id, topic_id, cfd] = line.split(',')
      if doc_id in self.docs:
        self.docs[doc_id].topics.append(Topic(topic_id, cfd))

    def on_read_doc_cat_line(line):
      # document_id,category_id,confidence_level
      # 1595802,1611,0.92
      [doc_id, cat_id, cfd] = line.split(',')
      if doc_id in self.docs:
        self.docs[doc_id].cats.append(Cat(cat_id, cfd))

    self._read_file(doc_meta, on_read_doc_meta_line)
    self._read_file(doc_ent, on_read_doc_ent_line)
    self._read_file(doc_cat, on_read_doc_cat_line)
    self._read_file(doc_topic, on_read_doc_topic_line)

  def read_data_file(self, event_file, click_file, ad_file, doc_meta_file,
                     doc_ent_file, doc_cat_file, doc_topic_file):
    self._read_events(event_file)
    self._read_clicks(click_file)
    self._read_ads(ad_file)
    self._read_docs(doc_meta_file, doc_ent_file, doc_cat_file, doc_topic_file)

  def get_event(self, display_id):
    if display_id in self.events:
      return self.events[display_id]
    else:
      return None

  def get_doc(self, doc_id):
    if doc_id in self.docs:
      return self.docs[doc_id]
    else:
      return None

  def get_ad(self, ad_id):
    if ad_id in self.ads:
      return self.ads[ad_id]
    else:
      return None

if __name__ == '__main__':
  manager = OutBrainManager()
  manager.read_data_file("data/mini_events.csv", 
                         "data/mini_clicks_train.csv",
                         "data/promoted_content.csv",
                         "data/documents_meta.csv",
                         "data/documents_entities.csv",
                         "data/documents_categories.csv",
                         "data/documents_topics.csv")
