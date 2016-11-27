


class Trainer:
  def __init__(self):
    self.manager = OutBrainManager()
    self.manager.read_data_file()

  def train(self):
    clicks = self.manager.clicks
    ad_events = []
    for i in range(100000):
      ad_event = AdEvent(clicks[i])
      ad_events.append(ad_event)
    self.do_train(ad_events)

  def _do_train(self, ad_events):
    for event in ad_events:
      features = event.gen_features()
      self._train_ad_event(event.clicked, features)

  def _train_ad_event(self, clicked, features):
    self.model.update_params(clicked, features)

  def infer_ad_event(self, features):
    return self.model.infer(features)
