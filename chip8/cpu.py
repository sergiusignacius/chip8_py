import sys
from .instruction import Instruction, make_instruction

PC_NEXT = ["next", ""]
PC_SKIP = ["skip", ""]

def PC_JUMP(addr): return ["jump", addr]

class Cpu:

    def __init__(self, emulator):
        self.emulator = emulator
        self.pc = 0x200
        self.i = 0
        self.V = [0]*16
        self.sp = 0
        self.stack = [0]*16
        self.sound = 0
        self.delay = 0
        self.keypad = [0]*16

    def fetch(self):
        ram = self.emulator.ram
        b1, b0 = ram[self.pc], ram[self.pc + 1]
        opcode = (b1 << 8) | b0
        return opcode
    
    def execute(self, opcode):
        inst = make_instruction(opcode)
        
        if inst is None:
            print(f"Couldn't decode instruction: {hex(opcode)}")
            sys.exit(1)
        else:
            nibbles = [
                (opcode & 0xF000) >> 12,
                (opcode & 0x0F00) >> 8,
                (opcode & 0x00F0) >> 4,
                (opcode & 0x000F)
            ]
            nnn = opcode & 0x0FFF
            kk = opcode & 0x00FF
            x = nibbles[1]
            y = nibbles[2]
            n = nibbles[3]
            # print(inst.to_string(x, y, n, kk, nnn))
            pc_update = inst.handle(self, x, y, n, kk, nnn)

            match pc_update:
                case ["next", _]:
                    self.pc += 2
                case ["jump", addr]:
                    self.pc = addr
                case ["skip", _]:
                    self.pc += 4
                case ["none", _]:
                    pass

    def show_display(self):
        self.emulator.show_display()
    
    def get_pixel(self, x, y):
        return self.emulator.get_pixel(x, y)

    def set_pixel(self, x, y, v):
        self.emulator.set_pixel(x, y, v)

    def clear_display(self):
        self.emulator.clear_display()

    def get_ram(self):
        return self.emulator.ram

    def set_wait_for_key_press(self, b):
        self.emulator.set_wait_for_key_press(b)