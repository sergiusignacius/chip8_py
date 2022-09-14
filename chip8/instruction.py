from enum import Enum
from .handlers import *

class OpType(Enum):
    NNN = 0,
    XKK = 1,
    X = 2,
    XY = 3,
    XYN = 4,
    FULL = 5

class Instruction:
    def __init__(self, mnemonic, handler, optype):
        self.handler = handler
        self.optype = optype
        self.mnemonic = mnemonic
    
    def to_string(self, x, y, n, kk, nnn):
        match self.optype:
            case OpType.FULL:
                return self.mnemonic
            case OpType.NNN:
                return "{} {}".format(self.mnemonic, nnn)
            case OpType.XKK:
                return "{} V{}, {}".format(self.mnemonic, x, kk)
            case OpType.X:
                return "{}, V{}".format(self.mnemonic, x)
            case OpType.XY:
                return "{} V{}, V{}".format(self.mnemonic, x, y)
            case OpType.XYN:
                return "{} V{}, V{}, {}".format(self.mnemonic, x, y, n)

    def handle(self, cpu, x, y, n, kk, nnn):
        return self.handler(cpu, x, y, n, kk, nnn)    
    

INSTRUCTION_SET = {}

def hash_opcode(instr):
    kk = instr & 0x00FF
    y = (instr & 0x0F00) >> 8
    msb = (instr & 0xF000) >> 12
    n = instr & 0x000F
    
    hash_code = 0
    if msb == 0x00:
        hash_code = kk
    elif msb == 0xF or msb == 0xE:
        hash_code = (msb << 8) | kk
    elif msb == 0x8:
        hash_code = (msb << 4) | n
    else:
        hash_code = msb
    
    return hash_code

def build_instruction_table():
    INSTRUCTION_SET[hash_opcode(0xE0)]      = Instruction('CLS',        handle_00e0, OpType.FULL)
    INSTRUCTION_SET[hash_opcode(0xEE)]      = Instruction('RET',        handle_00ee, OpType.FULL)
    INSTRUCTION_SET[hash_opcode(0x1)]       = Instruction('JP',         handle_1nnn, OpType.NNN)
    INSTRUCTION_SET[hash_opcode(0x2)]       = Instruction('CALL',       handle_2nnn, OpType.NNN)
    INSTRUCTION_SET[hash_opcode(0x3)]       = Instruction('SE',         handle_3xkk, OpType.XKK)
    INSTRUCTION_SET[hash_opcode(0x4)]       = Instruction('SNE',        handle_4xkk, OpType.XKK)
    INSTRUCTION_SET[hash_opcode(0x5)]       = Instruction('SE',         handle_5xy0, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x6)]       = Instruction('LD',         handle_6xkk, OpType.XKK)
    INSTRUCTION_SET[hash_opcode(0x7)]       = Instruction('ADD',        handle_7xkk, OpType.XKK)
    INSTRUCTION_SET[hash_opcode(0x80)]      = Instruction('LD',         handle_8xy0, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x81)]      = Instruction('OR',         handle_8xy1, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x82)]      = Instruction('AND',        handle_8xy2, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x83)]      = Instruction('XOR',        handle_8xy3, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x84)]      = Instruction('ADD',        handle_8xy4, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x85)]      = Instruction('SUB',        handle_8xy5, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x86)]      = Instruction('SHR',        handle_8xy6, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x87)]      = Instruction('SUBN',       handle_8xy7, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x8E)]      = Instruction('SHL',        handle_8xye, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0x9)]       = Instruction('SNE',        handle_9xy0, OpType.XY)
    INSTRUCTION_SET[hash_opcode(0xA)]       = Instruction('LD I',       handle_annn, OpType.NNN)
    INSTRUCTION_SET[hash_opcode(0xB)]       = Instruction('JP V0',      handle_bnnn, OpType.NNN)
    INSTRUCTION_SET[hash_opcode(0xC)]       = Instruction('RND',        handle_cxkk, OpType.XKK)
    INSTRUCTION_SET[hash_opcode(0xD)]       = Instruction('DRW',        handle_dxyn, OpType.XYN)
    INSTRUCTION_SET[hash_opcode(0xE09E)]     = Instruction('SKP',        handle_ex9e, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xE0A1)]     = Instruction('SKNP',       handle_exa1, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF007)]     = Instruction('LD DT I',    handle_fx07, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF00A)]     = Instruction('LD K I',     handle_fx0a, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF015)]     = Instruction('LD DT',      handle_fx15, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF018)]     = Instruction('LD ST',      handle_fx18, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF01E)]     = Instruction('ADD I',      handle_fx1e, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF029)]     = Instruction('LD F',       handle_fx29, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF033)]     = Instruction('LD B',       handle_fx33, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF055)]     = Instruction('LD [I]',     handle_fx55, OpType.X)
    INSTRUCTION_SET[hash_opcode(0xF065)]     = Instruction('LD [I] I',   handle_fx65, OpType.X)


def make_instruction(instr) -> Instruction | None:
    if len(INSTRUCTION_SET) == 0:
        build_instruction_table()
    return INSTRUCTION_SET.get(hash_opcode(instr), None)