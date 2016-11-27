import math

def sigmoid(x):
  return 1 / (1 + exp(-x))

class SparseVec:
  def __init__(self):
    self.index_val_map = {}

  def set_val(self, index, val):
    self.index_val_map[index] = val

  def update_val(self, index, delta):
    if self.index_val_map.has_key(index):
      self.index_val_map[index] += delta
    else:
      self.index_val_map[index] = delta

  def get_val(self, index):
    if self.index_val_map.has_key(index):
      return self.index_val_map[index]
    else:
      return None

class LrModel:
  def __init__(self):
    self.weight_vec = SparseVec()
    self.b = 0

  def update_params_mini_batch(self, batched_clicked, batched_features):
    if len(batched_clicked) != len(batched_features):
      print("clicked num != features num. quit")
      return
    ys = []

    # learning rate
    alpha = 0.001
    # regularization
    lamb = 0.00001

    for features in batched_features:
      ys.append(self.infer(features))
    for i in range(len(ys)):
      delta = 0
      if not batched_clicked[i]:
        delta = -alpha * ys[i]
      else:
        delta = alpha * (1 - ys[i])
      for feat in batched_features[i]:
        for val in feat.vals:
          w_delta = delta - lamb * self.weight_vec.get_val(val.val)
          # confidence
          w_delta *= val.cfd
          self.weight_vec.update_val(val.val, w_delta)
      self.b += delta - lamb * self.b


  def update_params(self, clicked, features):
    y = self.infer(features)
    # learning rate
    alpha = 0.001
    delta = 0
    if not clicked:
      delta = -alpha * y
    else:
      delta = alpha * (1 - y)
    # regularization
    lamb = 0.00001
    for feat in features:
      for val in feat.vals:
        w_delta = delta - lamb * self.weight_vec.get_val(val.val)
        # confidence
        w_delta *= val.cfd
        self.weight_vec.update_val(val.val, w_delta)
    self.b += delta - lamb * self.b

  def infer(self, features):
    weight_sum = 0
    for feat in features:
      for val in feat.vals:
        weight_sum += val.cfd * self.weight_vec.get_val(val.val)
    weight_sum += self.b
    return sigmoid(weight_sum)



