def sigmoid(x):
  return 1 / (1 + exp(-x))

class SparseVec:
  def __init__(self):
    self.index_val_map = {}

  def set_val(self, index, val):
    self.index_val_map[index] = val

  def update_val(self, index, delta):
    self.index_val_map[index] += delta

  def get_val(self, index):
    if self.index_val_map.has_key(index):
      return self.index_val_map[index]
    else:
      return None

class LrModel:
  def __init__(self):
    self.weight_vec = SparseVec
    self.b = 0

  def update_params(self, clicked, features):
    y = self.infer(features)
    # learning rate
    alpha = 0.001
    if not clicked:
      delta = -alpha * y
    else:
      delta = alpha * (1 - y)
    # regularization
    lamb = 0.00001
    for feat in features:
      delta -= lamb * self.weight_vec.get_val(feat.val)
      self.weight_vec.update_val(feat.val, delta)

  def infer(self, features):
    weight_sum = 0
    for feat in features:
      weight_sum += self.weight_vec.get_val(feat.val)
    weight_sum += self.b
    return sigmoid(weight_sum)
