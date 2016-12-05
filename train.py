import lr_model
import libfm_model
import feature
import auc

class Trainer:
  def __init__(self, model_file = None):
    self.model = lr_model.LrModel(model_file)
    self.learning_rate = 0.0002
    self.lmbd = 0 #0.000005
    self.momentum = 0

  def train_ad_event(self, clicked, features):
    self.model.update_params(clicked, features, self.learning_rate, self.lmbd,
                             self.momentum)

  def infer_ad_event(self, features):
    return self.model.infer(features)

def train(trainer, file_name):
  with open(file_name, 'r') as f:
    line = f.readline()
    while line:
      line = line.rstrip()
      [clicked, features_str] = line.split(':')
      features = feature.parse_features(features_str)
      trainer.train_ad_event(int(clicked), features)
      line = f.readline()

def assess(trainer, file_name):
  with open(file_name, 'r') as f:
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

MAX_ITER = 6
if __name__ == '__main__':
  trainer = Trainer("model")
  trains = 0
  for i in range(MAX_ITER):
    if i & 1:
      print("assessing the " + str(i) + "th iteration...")
      assess(trainer, 'features_test.txt')
    else:
      print("training the " + str(i) + "th iteration...")
      trains += 1
      train(trainer, 'features.txt')

  trainer.model.save_to_file("model", trains)

