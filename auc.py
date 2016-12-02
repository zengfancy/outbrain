import quicksort

'''
@param result: [[ctr, clicked]....]
@return: auc
'''
def assess(result):
  quicksort.quick_sort(result)
  tpr = 0
  fpr = 0
  for elem in result:
    if elem[1] == 1:
      tpr += 1
    else:
      fpr += 1

  pos_area = 0
  neg_area = 0
  i = len(result) - 1
  x = 0
  y = 0
  while i >= 0:
    if result[i][1] == 1:
      y += 1
    else:
      x += 1
      pos_area += y/tpr
      neg_area += 1 - y/tpr
    i -= 1

  print("pos_area:" + str(pos_area))
  print("neg_area:" + str(neg_area))
  return pos_area / (pos_area + neg_area)

if __name__ == '__main__':
  l = [[0.4, 0], [0.3, 1], [0.8, 0], [0.1, 1], [0.9, 1], [0.6, 0], [0.4, 1], [0.2, 1], [0.7, 0]]
  print(l)
  print("auc:" + str(assess(l)))
  l = [[0.4, 0], [0.3, 1], [0.8, 0], [0.1, 0], [0.9, 1], [0.6, 1], [0.4, 0], [0.2, 0], [0.7, 1]]
  print(l)
  print("auc:" + str(assess(l)))  
