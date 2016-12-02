import quicksort

'''
@param result: [[ctr, clicked]....]
@return: auc
'''
def assess(result):
  quicksort.quick_sort(result)
  num_sum = 0
  # [[ctr, recall_rate]...]
  tmp_result = []
  for elem in result:
    if elem[1] == 1:
      num_sum += 1
    tmp_result.append([elem[0], num_sum])
  for elem in tmp_result:
    elem[1] = float(elem[1]) / float(num_sum)

  last_ctr = 0
  pos_area = 0
  neg_area = 0
  for elem in tmp_result:
    l = elem[0] - last_ctr
    neg_area += elem[1] * l
    pos_area += (1 - elem[1]) * l
    last_ctr = elem[0]
  print("pos_area:" + str(pos_area))
  print("neg_area:" + str(neg_area))
  return pos_area / (pos_area + neg_area)

if __name__ == '__main__':
  l = [[0.4, 0], [0.3, 1], [0.8, 0], [0.1, 1], [0.9, 1], [0.6, 0], [0.4, 1], [0.2, 1], [0.7, 0]]
  print(l)
  print("auc:" + str(assess(l)))
  l = [[0.4, 0], [0.3, 0], [0.8, 1], [0.1, 0], [0.9, 1], [0.6, 1], [0.4, 0], [0.2, 0], [0.7, 1]]
  print(l)
  print("auc:" + str(assess(l)))  
