import outbrain_manager
import feat_hash

'''
param feat_type: string
param feat_val : string
'''
def hash_feature(feat_ns, feat_val):
  ns_hash = feat_hash.hash_string(feat_ns, 0)
  return feat_hash.hash_string(feat_val, ns_hash)

'''
param val:
param cfd: confidence, may be None
'''
class FeatVal:
  def __init__(self, val, cfd = None):
    self.val = val
    if cfd:
      self.cfd = cfd
    else:
      self.cfd = 1

'''
param name:
param vals: list of @FeatVal
'''
class Feature:
  def __init__(self, name, vals):
    self.name = name
    self.vals = vals

  def dump(self):
    print("name:" + self.name)
    for val in self.vals:
      print("val:" + str(val.val) + ", cfd:" + str(val.cfd))


def dump_feature(feature):
  vals_str = ""
  for val in feature.vals:
    if val.cfd:
      vals_str += str(val.val) + '#' + str(val.cfd) + '@'
    else:
      vals_str += str(val.val) + '#@'
  # remove the last '@'
  if len(vals_str) != 0:
    vals_str = vals_str[:-1]
  line = feature.name + '$' + vals_str
  return line

def dump_features(features):
  line = ""
  if len(features) == 0:
    return ""
  for feature in features:
    line += dump_feature(feature) + '^'
  # remove the last '^'
  return line[:-1]

def parse_feature(line):
  [name, vals_str] = line.split('$')
  val_strs = vals_str.split('@')
  vals = []
  for val_str in val_strs:
    [val, cfd] = val_str.split('#')
    if cfd and len(cfd) != 0:
      vals.append(FeatVal(int(val), float(cfd)))
    else:
      vals.append(FeatVal(int(val)))
  return Feature(name, vals)

def parse_features(line):
  feature_strs = line.split('^')
  features = []
  for feature_str in feature_strs:
    features.append(parse_feature(feature_str))
  return features


g_ns = {}
g_ns["uuid"] = "uu"
g_ns["geo"] = "ge"
g_ns["platform"] = "pt"
g_ns["timestamp"] = "ts"
g_ns["doc_source_id"] = "sc"
g_ns["doc_publisher"] = "pb"
g_ns["doc_pub_time"] = "pt"
g_ns["doc_cats"] = "ct"
g_ns["doc_entities"] = "en"
g_ns["doc_topics"] = "tp"
g_ns["ad_camp"] = "ca"
g_ns["ad_adv"] = "ad"
g_ns["ad_doc_source_id"] = "asc"
g_ns["ad_doc_publisher"] = "apb"
g_ns["ad_doc_pub_time"] = "apt"
g_ns["ad_doc_cats"] = "act"
g_ns["ad_doc_entities"] = "aen"
g_ns["ad_doc_topics"] = "atp"

def get_feat_ns(f_type):
  return g_ns[f_type]

'''
'''
class AdEvent:
  '''
  param click: Click type
  '''
  def __init__(self, click):
    self.ad_id = click.ad_id
    self.clicked = click.clicked
    self.display_id = click.display_id

  '''
  @return: a list of class Feature
  '''
  def gen_features(self, manager):
    # generate display features, like uuid, geo, platform, etc
    event = manager.get_event(self.display_id)
    features = []
    features.append(self.gen_feature("uuid", event.uuid))
    features.append(self.gen_feature("geo", event.geo))
    features.append(self.gen_feature("platform", event.platform))
    features.append(self.gen_feature("timestamp", event.timestamp))
    
    # generate display document features
    doc = manager.get_doc(event.doc_id)
    features.append(self.gen_feature("doc_source_id", doc.source_id))
    features.append(self.gen_feature("doc_publisher", doc.publisher))
    features.append(self.gen_feature("doc_pub_time", doc.pub_time))
    features.append(self.gen_feature("doc_cats", doc.cats))
    features.append(self.gen_feature("doc_entities", doc.entities))
    features.append(self.gen_feature("doc_topics", doc.topics))

    # generate ad features
    ad = manager.get_ad(self.ad_id)
    features.append(self.gen_feature("ad_camp", ad.camp))
    features.append(self.gen_feature("ad_adv", ad.advertiser))

    # generate ad doc features
    doc = manager.get_doc(ad.doc_id)
    features.append(self.gen_feature("ad_doc_source_id", doc.source_id))
    features.append(self.gen_feature("ad_doc_publisher", doc.publisher))
    features.append(self.gen_feature("ad_doc_pub_time", doc.pub_time))
    features.append(self.gen_ent_topic_cat_feature("ad_doc_cats", doc.cats))
    features.append(self.gen_ent_topic_cat_feature("ad_doc_entities", doc.entities))
    features.append(self.gen_ent_topic_cat_feature("ad_doc_topics", doc.topics))

    return features

  '''
  @return: class Feature
  '''
  def gen_feature(self, f_type, f_val):
    feat_ns = get_feat_ns(f_type)
    feat_hash = hash_feature(feat_ns, str(f_val))
    return Feature(feat_ns, [FeatVal(feat_hash)])

  def gen_ent_topic_cat_feature(self, f_type, f_vals):
    feat_ns = get_feat_ns(f_type)
    feat_vals = []
    for val in f_vals:
      feat_hash = hash_feature(feat_ns, val.id)
      feat_vals.append(FeatVal(feat_hash, val.cfd))
    return Feature(feat_ns, feat_vals)

if __name__ == '__main__':
  manager = outbrain_manager.OutBrainManager()
  if False:
    manager.events[123] = outbrain_manager.Event(123, "45garerertet646", 345, "geo", 2, 34)
    manager.docs[345] = outbrain_manager.Doc(345, 12, 4, "2014-12-12")
    manager.docs[346] = outbrain_manager.Doc(346, 13, 8, "2014-12-12")
    manager.ads[321] = outbrain_manager.Ad(321, 3, 346, 5)
    ad = AdEvent(outbrain_manager.Click(123, 321, True))
    features = ad.gen_features(manager)
    for feat in features:
      feat.dump()
  elif False:
    manager.read_data_file("data/mini_events.csv", 
                         "data/mini_clicks_train.csv",
                         "data/promoted_content.csv",
                         "data/documents_meta.csv",
                         "data/documents_entities.csv",
                         "data/documents_categories.csv",
                         "data/documents_topics.csv")

    print("read data file ended!!!")
    num = 0
    feat_map = {}
    for click in manager.clicks:
      num += 1
      if num % 100000 == 0:
        print("finish " + str(num) + " clicks' feature generation...")
      ad_event = AdEvent(click)
      features = ad_event.gen_features(manager)
      for feature in features:
        feat_info = str(click.ad_id) + "_" + str(click.display_id) + "_" + feature.name
        for val in feature.vals:
          if val.val in feat_map.keys():
            feat_map[val.val].append(feat_info)
          else:
            feat_map[val.val] = [feat_info]

    print("generating features ended!!!")
    with open("abc.txt", "w") as f:
      for val in feat_map.keys():
        feat_str = "val:" + str(val) + ", slots:" + str(len(feat_map[val])) + "-"
        for feat_info in feat_map[val]:
          feat_str += feat_info + "   "
        f.write(feat_str + "\n")
  else:
    manager.read_data_file("data/mini_events.csv", 
                         "data/mini_clicks_train.csv",
                         "data/promoted_content.csv",
                         "data/documents_meta.csv",
                         "data/documents_entities.csv",
                         "data/documents_categories.csv",
                         "data/documents_topics.csv")
    with open("features.txt", "w") as f:
      num = 0
      for click in manager.clicks:
        num += 1
        if num % 100000 == 0:
          print("finish " + str(num) + " clicks' feature generation...")
        ad_event = AdEvent(click)
        features = ad_event.gen_features(manager)
        line = str(ad_event.clicked) + ":" + dump_features(features) + "\n"
        f.write(line)

