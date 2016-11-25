import uniform_hash

def hash_string(str, seed):
  return uniform_hash.uniform_hash(str, len(str), seed)

