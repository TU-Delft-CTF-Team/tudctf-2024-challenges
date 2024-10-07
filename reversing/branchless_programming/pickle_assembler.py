import ast
from enum import Enum
from pickletools import opcodes
import struct

instructions = {o.name: o for o in opcodes}


class ArgumentType(Enum):
    UINT1 = 0
    UINT2 = 1
    UINT4 = 2
    UINT8 = 3
    UNICODE = 4
    BYTES = 5
    INT4 = 6


def compile(program):
    assembled = assemble(program)
    assembled += assemble_instruction('STOP')
    program_size = len(assembled)
    return assemble_instruction('PROTO', '4') + assemble_instruction('FRAME', str(program_size)) + assembled


def assemble(program):
    lines = program.split('\n')
    return b''.join(assemble_line(line) for line in lines if not is_blank(line))


def is_blank(line):
    code = line.split('#')[0]
    return len(code) == 0 or code.isspace()


def assemble_line(line):
    opcode, args = parse_line(line)
    return assemble_instruction(opcode, *args)


def parse_line(line):
    line = line.strip().split('#')[0]
    [opcode, *args] = line.split()
    return (opcode, args)


def assemble_instruction(opcode, *args):
    instruction = instructions.get(opcode)
    if instruction is None:
        raise ValueError(f'Instruction with opcode {opcode!r} doesn\'t exist')
    argument_types = convert_argument_types(instruction.arg)
    result = bytes([ord(instruction.code)])
    if len(argument_types) != len(args):
        raise ValueError(f'In instruction {opcode}: expected {len(argument_types)} arguments, but got {len(args)}')
    for (v, t) in zip(args, argument_types):
        result += assemble_argument(v, t)
    return result


def convert_argument_types(argument_descriptor):
    if argument_descriptor is None:
        return []
    return {
        'uint1': [ArgumentType.UINT1],
        'uint2': [ArgumentType.UINT2],
        'uint4': [ArgumentType.UINT4],
        'uint8': [ArgumentType.UINT8],
        'unicodestring1': [ArgumentType.UINT1, ArgumentType.UNICODE],
        'bytes1': [ArgumentType.UINT1, ArgumentType.BYTES],
        'int4': [ArgumentType.INT4]
    }[argument_descriptor.name]


def assemble_argument(value, type):
    match type:
        case ArgumentType.UINT1:
            return struct.pack('<B', int(value))
        case ArgumentType.UINT2:
            return struct.pack('<H', int(value))
        case ArgumentType.UINT4:
            return struct.pack('<I', int(value))
        case ArgumentType.UINT8:
            return struct.pack('<Q', int(value))
        case ArgumentType.UNICODE:
            return ast.literal_eval(value).encode('utf-8')
        case ArgumentType.BYTES:
            return ast.literal_eval(value)
        case ArgumentType.INT4:
            return struct.pack('<i', int(value))


if __name__ == '__main__':
    import pickle

    with open('program.pas', 'rt') as f:
        program = f.read()

    flag = 'TUDCTF{br4nch1355_r3v3r53_3ng1n33r1ng_ch4113ng3_1_h0p3_y0u_d0nt_h4t3_m3_t00_much_f0r_th15_:D}'
    # flag = 'a'
    p = compile(program)
    print(p)
    print(pickle.loads(p))

    with open('challenge.pickle', 'wb') as f:
        f.write(p)
