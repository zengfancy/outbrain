import uniform_hash

def hash_string(str, seed):
  return uniform_hash.uniform_hash(str, len(str), seed)

if __name__ == '__main__':
  print("nc:", hash_string("nc", 0))
  print("nm:", hash_string("nm", 0))
  print("uq, 0:", hash_string("uq", 0))
  print("uq, 3:", hash_string("uq", 3))
  print("ab, 0:", hash_string("ab", 0))
  print("ab, 7:", hash_string("ab", 7))
