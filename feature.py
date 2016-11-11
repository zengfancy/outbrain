'''
param val:
param cfd: confidence, may be None
'''
class FeatVal:
  def __init__(self, val, cfd = None):
    self.val = val
    self.cfd = cfd

'''
param name:
param vals: list of @FeatVal
'''
class Feature:
  def __init__(self, name, vals):
    self.name = name
    self.vals = vals

def hash_string(feat_type, feat_val):

'''
'''
class AdEvent:
  def __init__(self):
    self.ad_id = ad_id
    self.clicked = clicked
    self.display_id = display_id

  def gen_features(self):
    # generate display features, like uuid, geo, platform, etc
    event = self.manager.get_event(self.display_id)
    features = []
    features.append(gen_feature("uuid", event.uuid))
    features.append(gen_feature("geo", event.geo))
    features.append(gen_feature("platform", event.platform))
    features.append(gen_feature("timestamp", event.timestamp))
    
    # generate display document features
    doc = self.manager.get_doc(event.doc_id)
    features.append(gen_feature("doc_source_id", doc.source_id))
    features.append(gen_feature("doc_publisher", doc.publisher))
    features.append(gen_feature("doc_pub_time", doc.pub_time))
    features.extend(gen_feature("doc_cats", doc.cats))
    features.extend(gen_feature("doc_entities", doc.entities))
    features.extend(gen_feature("doc_topics", doc.topics))

    # generate ad features
    ad = self.manager.get_ad(self.ad_id)
    features.append(gen_feature("ad_camp", ad.camp))
    features.append(gen_feature("ad_adv", ad.advertiser))
    # generate ad doc features
    doc = self.manager.get_doc(ad.doc_id)
    features.append(gen_feature("ad_doc_source_id", doc.source_id))
    features.append(gen_feature("ad_doc_publisher", doc.publisher))
    features.append(gen_feature("ad_doc_pub_time", doc.pub_time))
    features.extend(gen_feature("ad_doc_cats", doc.cats))
    features.extend(gen_feature("ad_doc_entities", doc.entities))
    features.extend(gen_feature("ad_doc_topics", doc.topics))

    return features

  def gen_feature(self, f_type, f_val):
    feat_ns = feat_ns[f_type]
    if f_val is list:
      feat_vals = []
      for val in f_val:
        feat_hash = hash_string(f_type, val)
        feat_vals.append(FeatVal(feat_ns, feat_hash))
      return feat_vals
    else:
      feat_hash = hash_string(f_type, f_val)
      return FeatVal(feat_ns, feat_hash)
       

'''
params features:
'''
class AdFeature:

