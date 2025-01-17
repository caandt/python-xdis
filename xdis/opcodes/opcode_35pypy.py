# (C) Copyright 2017, 2020, 2023 by Rocky Bernstein
"""
PYPY 3.5 opcodes

This is a like Python 3.5's opcode.py with some classification
of stack usage.
"""

import xdis.opcodes.opcode_35 as opcode_35
from xdis.opcodes.base import (
    def_op,
    finalize_opcodes,
    init_opdata,
    jrel_op,
    name_op,
    nargs_op,
    update_pj3,
    varargs_op,
)
from xdis.opcodes.format.extended import (
    extended_format_ATTR,
    extended_format_RETURN_VALUE,
)

version_tuple = (3, 5)
python_implementation = "PyPy"

loc = locals()
init_opdata(loc, opcode_35, version_tuple, is_pypy=True)

## FIXME: DRY common PYPY opcode additions

# PyPy only
# ----------
def_op(loc, "FORMAT_VALUE", 155)
def_op(loc, "BUILD_STRING", 157)
name_op(loc, "LOOKUP_METHOD", 201, 1, 2)
nargs_op(loc, "CALL_METHOD", 202, -1, 1)
loc["hasvargs"].append(202)

# Used only in single-mode compilation list-comprehension generators
varargs_op(loc, "BUILD_LIST_FROM_ARG", 203)

# Used only in assert statements
jrel_op(loc, "JUMP_IF_NOT_DEBUG", 204, conditional=True)

# There are no opcodes to remove or change.
# If there were, they'd be listed below.

opcode_extended_fmt = {
    "LOAD_ATTR": extended_format_ATTR,
    "RETURN_VALUE": extended_format_RETURN_VALUE,
    "STORE_ATTR": extended_format_ATTR,
}

# FIXME remove (fix uncompyle6)
update_pj3(globals(), loc)
finalize_opcodes(loc)
