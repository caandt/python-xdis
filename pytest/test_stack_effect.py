import dis
import sys
import os.path as osp
from xdis.op_imports import get_opcode_module
from xdis.main import get_opcode
from xdis.cross_dis import op_has_argument, xstack_effect
import xdis

if xdis.PYTHON_VERSION > 3.5:
    import importlib.util

    def import_file(path):
        spec = importlib.util.spec_from_file_location("module.name",
                                                      path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return foo

elif 3.3 <= xdis.PYTHON_VERSION <= 3.4:
    from importlib.machinery import SourceFileLoader

    def import_file(path):
        foo = SourceFileLoader("module.name", path).load_module()
        return foo
elif xdis.PYTHON_VERSION <= 3.0:
    import imp

    def import_file(path):
        foo = imp.load_source('module.name', path)
        return foo

def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


srcdir = get_srcdir()
opcode_stack_effect = [-100]*256

def test_stack_effect_fixed():
    for version in ([3, 3], [3, 2]):
        opcode_stack_effect = [-100]*256
        v_str = "%s%s" % (version[0], version[1])
        opc = get_opcode(version, False)
        se_file_py = osp.realpath(osp.join(srcdir, "stackeffect", "effect%s.py" % v_str))
        so = import_file(se_file_py)

        assert opcode_stack_effect

        for opname, opcode, in opc.opmap.items():
            if op_has_argument(opcode, opc):
                continue

            effect = xstack_effect(opcode, opc)
            check_effect = so.opcode_stack_effect[opcode]
            assert check_effect == effect, (
                "in version %s %d (%s) not okay; effect xstack_effect is %d; wrote down %d"
                % (opc.version, opcode, opname, effect, check_effect)
            )
            pass
        pass
    return

def test_stack_effect_vs_dis():

    if xdis.PYTHON_VERSION < 3.4 or xdis.IS_PYPY:
        # TODO figure out some other kind if internal checks to tod.
        print("Skipped for now - need to figure out how to test")
        return

    def test_one(xdis_args, dis_args, has_arg):
        effect = xstack_effect(*xdis_args)
        check_effect = dis.stack_effect(*dis_args)
        assert effect != -100, (
            "%d (%s) needs adjusting; should be: should have effect %d"
            % (opcode, opname, check_effect)
        )
        if has_arg:
            op_val = "with operand %d" % dis_args[1]
        else:
            op_val = ""

        assert check_effect == effect, (
            "%d (%s) %s not okay; effect %d vs %d"
            % (opcode, opname, op_val, effect, check_effect)
        )
        print("%d (%s) is good: effect %d" % (opcode, opname, effect))

    if xdis.IS_PYPY:
        variant = "pypy"
    else:
        variant = ""
    opc = get_opcode_module(None, variant)
    for opname, opcode, in opc.opmap.items():
        if opname in ("EXTENDED_ARG", "NOP"):
            continue
        xdis_args = [opcode, opc]
        dis_args = [opcode]

        # TODO: if opcode takes an argument, we should vary the arg and try
        # values in addition to 0 as done below.
        if op_has_argument(opcode, opc):
            xdis_args.append(0)
            dis_args.append(0)
            has_arg = True
        else:
            has_arg = False

        if (
            xdis.PYTHON_VERSION > 3.7
            and opcode in opc.CONDITION_OPS
            and opname not in ("JUMP_IF_FALSE_OR_POP",
                               "JUMP_IF_TRUE_OR_POP",
                               "POP_JUMP_IF_FALSE",
                               "POP_JUMP_IF_TRUE",
                               "SETUP_FINALLY",)
        ):
            xdis_args.append(0)
            dis_args.append(0)

        if has_arg:
            for i in range(0,3):
                dis_args[1] = xdis_args[2] = i
                test_one(xdis_args, dis_args, has_arg)
                pass
            pass
        else:
            test_one(xdis_args, dis_args, has_arg)
        pass
    return

if __name__ == "__main__":
    test_stack_effect_fixed()
    test_stack_effect_vs_dis()