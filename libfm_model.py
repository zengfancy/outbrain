import math
import feature

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

'''
param weight_map: map<int, float>
'''
class SparseWeight:
  def __init__(self):
    self.weight_map = {}

  def set_weight(self, index, weight):
    self.weight_map[index] = weight

  def get_weight(self, index):
    if index in self.weight_map:
      return self.weight_map[index]
    else:
      return 0

  def apply_gradient(self, index, grad):
    if index in self.weight_map:
      self.weight_map[index] += grad
    else:
      self.weight_map[index] = grad

VEIGH_LEN = 7
class Veigh:
  def __init__(self):
    self.v = []
    for i in range(VEIGH_LEN):
      self.v[i] = 0.000001
    return

  def add_veigh(self, veigh):
    for i in range(VEIGH_LEN):
      self.v[i] += veigh.v[i]
    return

def add_veigh(v1, v2):
def sub_veigh(v1, v2):
def dot(v1, v2):
'''
@param veigh_map: map<int, list<float>>
'''
class SparseVeigh:
  def __init__(self):
    self.veigh_map = {}

  def set_veigh(self, index, veigh):
    self.veigh_map[index] = veigh

  def get_veigh(self, index):
    if index in self.veigh_map:
      return self.veigh_map[index]
    else:
      return None

  def apply_gradient(self, index, grad):
    if index in self.veigh_map:
      self.veigh_map[index].add_veigh(grad)
    else:
      self.veigh_map[index] = grad


class LibfmModel:
  def __init__(self, model_file):
    self.b = 0;
    self.weight_vec = SparseWeight()
    self.veigh_mat = SparseVeigh()
    if model_file:
      self.load_from_file(model_file)

  def load_from_file(self, model_file):
    return

  def update_params(self, clicked, features, learning_rate, lmbd, momentum):
    y = self.infer(features)
    grad = 0
    if not clicked:
      grad = -learning_rate * y
    else:
      grad = learning_rate * (1 - y)

    sigma_v_grad = Veigh()
    v_grads = []
    indices = []
    # update weight
    for feat in features:
      for val in feat.vals:
        w_grad = grad - lmbd * self.weight_vec.get_weight(val.val)
        w_grad *= val.cfd
        self.weight_vec.apply_gradient(val.val, w_grad)

        v_grad = val.cfd * self.veigh_mat.get_veigh(val.val)
        indices.append(val.val)
        v_grads.append(v_grad)
        sigma_v_grad.add_veigh(v_grad)

    # update veigh
    for i in len(indices):
      self.veigh_mat.apply_gradient(indices[i], sub_veigh(sigma_v_grad,
                                                          v_grads[i]))
 
    # update b
    self.b += grad - lmbd * self.b
    return

  '''
  sum = b + w*x + dot(vi, vj)*xi*xj
  '''
  def infer(self, features):
    weight_sum = 0
    weights = []
    veighs = []
    cfds = []
    for feat in features:
      for val in feat.vals:
        cfds.append(val.cfd)
        weights.append(self.weight_vec.get_weight(val.val))
        veighs.append(self.veigh_mat.get_veigh(val.val))
    weight_sum += self.b
    for i in range(len(weights)):
      weight_sum += weights[i] * cfds[i]
      for j in range(i + 1, len(weights)):
        weight_sum += cfd[i] * cfd[j] * dot(veighs[i], veighs[j])

    return sigmoid(weight_sum)

