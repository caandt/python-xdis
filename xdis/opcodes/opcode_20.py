"""
CPython 2.0 bytecode opcodes

This is used in bytecode disassembly. This is equivalent to the
opcodes in Python's dis.py library.
"""

from copy import deepcopy

from xdis.opcodes.base import def_op, rm_op, cmp_op

l = locals()

# These are used from outside this module
from xdis.bytecode import findlinestarts, findlabels
import xdis.opcodes.opcode_2x as opcode_2x

# FIXME: can we DRY this even more?

# Make a *copy* of opcode_2x values so we don't pollute 2x
HAVE_ARGUMENT = opcode_2x.HAVE_ARGUMENT
cmp_op = list(cmp_op)
hasconst = list(opcode_2x.hasconst)
hascompare = list(opcode_2x.hascompare)
hasfree = list(opcode_2x.hasfree)
hasjabs = list(opcode_2x.hasjabs)
hasjrel = list(opcode_2x.hasjrel)
haslocal = list(opcode_2x.haslocal)
hasname = list(opcode_2x.hasname)
hasnargs = list(opcode_2x.hasnargs)
hasvargs = list(opcode_2x.hasvargs)
opmap = deepcopy(opcode_2x.opmap)
opname = deepcopy(opcode_2x.opname)
oppush = list(opcode_2x.oppush)
oppop  = list(opcode_2x.oppop)

EXTENDED_ARG = opcode_2x.EXTENDED_ARG

# 2.3 Bytecodes not in 2.0
rm_op(l, 'BINARY_FLOOR_DIVIDE', 26)
rm_op(l, 'BINARY_TRUE_DIVIDE', 27)
rm_op(l, 'BINARY_INPLACE_DIVIDE', 28)
rm_op(l, 'INPLACE_TURE_DIVIDE', 29)
rm_op(l, 'GET_ITER', 68)
rm_op(l, 'YIELD_VALUE', 86)
rm_op(l, 'FOR_ITER', 93)

# 2.1 Bytecodes not in 2.0
rm_op(l, 'CONTINUE_LOOP', 119)
rm_op(l, 'MAKE_CLOSURE', 134)
rm_op(l, 'LOAD_CLOSURE', 135)
rm_op(l, 'LOAD_DEREF', 136)
rm_op(l, 'STORE_DEREF', 137)


# 2.0 Bytecodes not in 2.3
def_op(l, opname, opmap, 'FOR_LOOP', 114)
def_op(l, opname, opmap, 'SET_LINENO', 127)

for object in opcode_2x.fields2copy:
    globals()[object] =  deepcopy(getattr(opcode_2x, object))

def updateGlobal():
    globals().update({'python_version': 2.1})
    # Canonicalize to PJIx: JUMP_IF_y and POP_JUMP_IF_y
    globals().update({'PJIF': opmap['JUMP_IF_FALSE']})
    globals().update({'PJIT': opmap['JUMP_IF_TRUE']})

    globals().update({'JUMP_OPs': map(lambda op: opcode_2x.opname[op],
                                          opcode_2x.hasjrel + opcode_2x.hasjabs)})
    globals().update(dict([(k.replace('+', '_'), v) for (k, v) in opcode_2x.opmap.items()]))
    return

updateGlobal()

import sys
if sys.version_info[0:2] == (2, 0):
    import dis
    assert len(opname) == len(dis.opname)
    for i in range(len(dis.opname)):
        assert dis.opname[i] == opname[i], [i, dis.opname[i], opname[i]]
