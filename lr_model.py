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

class LrModel:
  def __init__(self):
    self.weight_vec = SparseVec()
    self.b = 0

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

  def update_params_mini_batch(self, batched_clicked, batched_features, learning_rate, lmbd):
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
          self.weight_vec.update_val(val.val, w_delta)
      self.b += delta - lmbd * self.b


  def update_params(self, clicked, features, learning_rate, lmbd):
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
        self.weight_vec.update_val(val.val, w_delta)
    self.b += delta - lmbd * self.b

  def infer(self, features):
    weight_sum = 0
    for feat in features:
      for val in feat.vals:
        weight_sum += val.cfd * self.weight_vec.get_val(val.val)
    weight_sum += self.b
    return sigmoid(weight_sum)


