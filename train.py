import lr_model
import feature
import auc

class Trainer:
  def __init__(self):
    self.model = lr_model.LrModel()
    self.learning_rate = 0.1
    self.lmbd = 0.01

  def train(self, label_feature_list):
    for label_feature in label_feature_list:
      self._train_ad_event(label_feature.clicked, label_feature.features)

  def train_ad_event(self, clicked, features):
    self.model.update_params(clicked, features, self.learning_rate, self.lmbd)

  def infer_ad_event(self, features):
    return self.model.infer(features)

MAX_ITER = 21
if __name__ == '__main__':
  trainer = Trainer()
  trains = 0
  for i in range(MAX_ITER):
    with open('features.txt', 'r') as f:
      if i % 5 == 0 and i > 0:
        print("assissing the " + str(i) + "th iteration...")
        result = []
        line = f.readline()
        while line:
          line = line.rstrip()
          [clicked, features_str] = line.split(':')
          features = feature.parse_features(features_str)
          ctr = trainer.infer_ad_event(features)
          result.append([ctr, int(clicked)])
          line = f.readline()
        print("auc:" + str(auc.assess(result)))
      else:
        print("training the " + str(i) + "th iteration...")
        trains += 1
        line = f.readline()
        while line:
          line = line.rstrip()
          [clicked, features_str] = line.split(':')
          features = feature.parse_features(features_str)
          trainer.train_ad_event(int(clicked), features)
          line = f.readline()

      
  trainer.model.save_to_file("model", trains)
