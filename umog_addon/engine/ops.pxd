cdef enum:
    MAX_INS = 2
    MAX_OUTS = 2

cpdef enum Operation:
    ADD
    SUBTRACT
    MULTIPLY
    DIVIDE
    DISPLACE
    LOOP
    NOP

cdef struct Instruction:
    Operation op
    unsigned int ins[MAX_INS]
    unsigned int outs[MAX_OUTS]
