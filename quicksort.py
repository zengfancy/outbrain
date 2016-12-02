

def partition(l, start, end):
  pivot = l[end]                      
  bottom = start-1                        
  top = end                                

  done = 0
  while not done:                        
    while not done:                   
      bottom = bottom + 1              
      if bottom == top:                
        done = 1                    
        break

      if l[bottom][0] > pivot[0]:
        l[top] = l[bottom]
        break
    while not done:
      top = top - 1
      if top == bottom:
        done = 1
        break

      if l[top][0] < pivot[0]:
        l[bottom] = l[top]
        break
  l[top] = pivot
  return top


def quicksort(l, start, end):
  if start < end:
    split = partition(l, start, end)
    quicksort(l, start, split - 1)
    quicksort(l, split + 1, end)
  else:
    return

'''
@param result: [[ctr, clicked]....]
'''
def quick_sort(result):
  quicksort(result, 0, len(result) - 1)

if __name__ == '__main__':
  l = [[0.4, 0], [0.3, 1], [0.8, 0], [0.1, 1], [0.9, 1], [0.6, 0], [0.4, 1], [0.2, 1], [0.7, 0]]
  print(l)
  quick_sort(l)
  print(l)
