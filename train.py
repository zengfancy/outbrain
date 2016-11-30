import lr_model
import feature

class Trainer:
  def __init__(self):

  def train(self, label_feature_list):
    for label_feature in label_feature_list:
      self._train_ad_event(label_feature.clicked, label_feature.features)

  def train_ad_event(self, clicked, features):
    self.model.update_params(clicked, features)

  def infer_ad_event(self, features):
    return self.model.infer(features)

if __name__ == '__main__':
  trainer = Trainer()
  with open('', 'r') as f:
    line = f.readline()
    while line:
      line = line.rstrip()
      [clicked, features_str] = line.split(':')
      features = feature.parse_features(features_str)
      trainer.train_ad_event(clicked, features)
      line = f.readline()
