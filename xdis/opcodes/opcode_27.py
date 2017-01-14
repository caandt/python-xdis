"""
CPython 2.7 bytecode opcodes

This is used in bytecode disassembly. This is equivalent to the
opcodes in Python's opcode.py library.
"""

from copy import deepcopy

# These are used from outside this module
from xdis.bytecode import findlinestarts, findlabels

import xdis.opcodes.opcode_2x as opcode_2x
from xdis.opcodes.base import (
    def_op, jabs_op, jrel_op, rm_op, name_op, cmp_op
    )

l = locals()

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

def updateGlobal(version):
    globals().update({'python_version': version})

    # FIXME: Get rid of this (fix uncompyle6)
    # Canonicalize to PJIx: JUMP_IF_y and POP_JUMP_IF_y
    globals().update({'PJIF': opmap['POP_JUMP_IF_FALSE']})
    globals().update({'PJIT': opmap['POP_JUMP_IF_TRUE']})

    globals().update({'JUMP_OPs': map(lambda op: opname[op], hasjrel + hasjabs)})
    globals().update(dict([(k.replace('+', '_'), v) for (k, v) in opmap.items()]))

def compare_op(name, op):
    def_op(l, name, op)
    hascompare.append(op)

# Bytecodes added since 2.3.
# 2.4
def_op(l, 'NOP',           9,  0,  0)
def_op(l, 'YIELD_VALUE',  86,  1,  0)

# 2.5
def_op(l, 'WITH_CLEANUP', 81, -1, -1)

# 2.6
def_op(l, 'STORE_MAP',    54,  3,  2)

# 2.7
rm_op(l, 'BUILD_MAP',     104)
rm_op(l, 'LOAD_ATTR',     105)
rm_op(l, 'COMPARE_OP',    106)
rm_op(l, 'IMPORT_NAME',   107)
rm_op(l, 'IMPORT_FROM',   108)
rm_op(l, 'JUMP_IF_FALSE', 111)
rm_op(l, 'EXTENDED_ARG',  143)
rm_op(l, 'JUMP_IF_TRUE',  112)

def_op(l, 'LIST_APPEND',            94, 2, 1) # Calls list.append(TOS[-i], TOS).
                                              # Used to implement list comprehensions.
def_op(l, 'BUILD_SET',             104)     # Number of set items
def_op(l, 'BUILD_MAP',             105)
name_op(l, 'LOAD_ATTR',            106)
compare_op('COMPARE_OP',           107)

name_op(l, 'IMPORT_NAME',          108,  2,  1)  # Index in name list
name_op(l, 'IMPORT_FROM',          109,  0,  1)

jabs_op(l, 'JUMP_IF_FALSE_OR_POP', 111) # Target byte offset from beginning of code
jabs_op(l, 'JUMP_IF_TRUE_OR_POP',  112)  # ""
jabs_op(l, 'POP_JUMP_IF_FALSE',    114)  # ""
jabs_op(l, 'POP_JUMP_IF_TRUE',     115)  # ""
jrel_op(l, 'SETUP_WITH',           143,  0,  2)

def_op(l, 'EXTENDED_ARG', 145)
def_op(l, 'SET_ADD', 146)
def_op(l, 'MAP_ADD', 147)

updateGlobal(2.7)

from xdis import PYTHON_VERSION, IS_PYPY
if PYTHON_VERSION == 2.7 and not IS_PYPY:
    import dis
    # print(set(dis.opmap.items()) - set(opmap.items()))
    # print(set(opmap.items()) - set(dis.opmap.items()))
    assert all(item in opmap.items() for item in dis.opmap.items())
    assert all(item in dis.opmap.items() for item in opmap.items())
