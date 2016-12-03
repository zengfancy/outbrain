import math
import feature

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

class SparseVec:
  def __init__(self):
    self.index_val_map = {}
    self.index_delta_map = {}

  def set_val(self, index, val):
    self.index_val_map[index] = val
    self.index_delta_map[index] = []

  def update_val(self, index, delta):
    if index in self.index_val_map:
      self.index_val_map[index] += delta
      self.index_delta_map[index].append(delta)
    else:
      self.index_val_map[index] = delta
      self.index_delta_map[index] = [delta]

  '''
  @return: return 0 if not exist
  '''
  def get_val(self, index):
    if index in self.index_val_map:
      return self.index_val_map[index]
    else:
      return 0

  def get_last_delta(self, index):
    if index in self.index_delta_map and len(self.index_delta_map[index]) > 0:
      return self.index_delta_map[index][-1]
    else:
      return 0

class LrModel:
  def __init__(self, model_file):
    self.weight_vec = SparseVec()
    self.b = 0
    if model_file:
      self.load_from_file(model_file)

  def load_from_file(self, model_file):
    with open(model_file, "r") as f:
      line = f.readline()
      fields = line.split(':')
      self.b = float(fields[1])

      line = f.readline()
      while line:
        if line.startswith('index'):
          fields = line.split(',')
          [name, index] = fields[0].split(':')
          [name, weight] = fields[1].split(':')
          self.weight_vec.set_val(int(index), float(weight))
        line = f.readline()

  def save_to_file(self, file_name, trains):
    with open(file_name, "w") as f:
      f.write("b:" + str(self.b) + "\n")
      for index in self.weight_vec.index_val_map:
        f.write("index:" + str(index) + ", weight:" +
                str(self.weight_vec.index_val_map[index]) + "\n")
        f.write("delta:\n")
        hit_count = len(self.weight_vec.index_delta_map[index]) / trains 
        i = 0
        for delta in self.weight_vec.index_delta_map[index]:
          f.write('%.4f' % (delta / self.weight_vec.index_val_map[index]))
          f.write(" ")
          i += 1
          if i == hit_count:
            f.write("\n")
            i = 0
        f.write("\n")

  def update_params_mini_batch(self, batched_clicked, batched_features,
                               learning_rate, lmbd, momentum):
    if len(batched_clicked) != len(batched_features):
      print("clicked num != features num. quit")
      return
    ys = []

    # learning rate
#    learning_rate = 0.1
    # regularization
#    lmbd = 0.01

    for features in batched_features:
      ys.append(self.infer(features))
    for i in range(len(ys)):
      delta = 0
      if not batched_clicked[i]:
        delta = -learning_rate * ys[i]
      else:
        delta = learning_rate * (1 - ys[i])
      for feat in batched_features[i]:
        for val in feat.vals:
          w_delta = delta - lmbd * self.weight_vec.get_val(val.val)
          # confidence
          w_delta *= val.cfd
          # momentum
          w_delta += momentum * self.weight_vec.get_last_delta(val.val)
          self.weight_vec.update_val(val.val, w_delta)
      self.b += delta - lmbd * self.b


  def update_params(self, clicked, features, learning_rate, lmbd, momentum):
    y = self.infer(features)
    # learning rate
#    learning_rate = 0.1
    delta = 0
    if not clicked:
      delta = -learning_rate * y
    else:
      delta = learning_rate * (1 - y)
    # regularization
#    lmbd = 0.01
    for feat in features:
      for val in feat.vals:
        w_delta = delta - lmbd * self.weight_vec.get_val(val.val)
        # confidence
        w_delta *= val.cfd
        # momentum
        w_delta += momentum * self.weight_vec.get_last_delta(val.val)
        self.weight_vec.update_val(val.val, w_delta)
    self.b += delta - lmbd * self.b

  def infer(self, features):
    weight_sum = 0
    for feat in features:
      for val in feat.vals:
        weight_sum += val.cfd * self.weight_vec.get_val(val.val)
    weight_sum += self.b
    return sigmoid(weight_sum)


