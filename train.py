


class Trainer:
  def do_training(self, ad_events):
    for event in ad_events:
      features = event.gen_features()
      self.train_ad_event(event.clicked, features)

  def train_ad_event(self, clicked, features):
    self.model.update_params(clicked, features)

  def infer_ad_event(self, features):
    return self.model.infer(features)
