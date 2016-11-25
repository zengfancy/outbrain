%module uniform_hash
%include "stdint.i"
%{
/* Put header files here or function declarations like below */
extern uint32_t uniform_hash (const char * key, size_t len, uint32_t seed);
%}

extern uint32_t uniform_hash (const char * key, size_t len, uint32_t seed);
