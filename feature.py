
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

'''
'''
class AdEvent:
  def __init__(self):
    self.ad_id = ad_id
    self.clicked = clicked
    self.display_id = display_id

  def gen_features(self):
    event = self.manager.get_event(self.display_id)
    features = []
    features.append(gen_feature("uuid", event.uuid))
    features.append(gen_feature("geo", event.geo))
    features.append(gen_feature("platform", event.platform))
    features.append(gen_feature("timestamp", event.timestamp))
    
    doc = self.manager.get_doc(self.doc_id)
    features.append(gen_feature("doc_source_id", doc.source_id))
    features.append(gen_feature("doc_publisher", doc.publisher))
    features.append(gen_feature("doc_pub_time", doc.pub_time))
    features.extend(gen_feature("doc_cats", doc.cats))
    features.extend(gen_feature("doc_entities", doc.entities))
    features.extend(gen_feature("doc_topics", doc.topics))

    return features

'''
params features:
'''
class AdFeature:

