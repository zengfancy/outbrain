swig -python uniform_hash.i
gcc -std=c99 -fPIC -c uniform_hash.c uniform_hash_wrap.c -I/export/App/training_platform/anaconda3/include/python3.5m
gcc -shared uniform_hash.o uniform_hash_wrap.o -o _uniform_hash.so
