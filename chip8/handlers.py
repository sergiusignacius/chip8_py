from random import randint
import pygame
from .utils import KEY_MAPPINGS, REVERSE_MAPPINGS

PC_NEXT = ["next", ""]
PC_SKIP = ["skip", ""]
PC_NONE = ["none", ""]
def PC_JUMP(addr): return ["jump", addr]

def PC_SKIP_IF(cond):
    if cond:
        return PC_SKIP
    else:
        return PC_NEXT

def handle_00e0(cpu, x, y, n, kk, nnn):
    cpu.display = [0] * 64 * 32
    return PC_NEXT

def handle_00ee(cpu, x, y, n, kk, nnn):
    previous_pc = cpu.stack[cpu.sp]
    cpu.sp -= 1
    return PC_JUMP(previous_pc + 2)

def handle_1nnn(cpu, x, y, n, kk, nnn):
    return PC_JUMP(nnn)

def handle_2nnn(cpu, x, y, n, kk, nnn):
    cpu.sp += 1
    cpu.stack[cpu.sp] = cpu.pc
    return PC_JUMP(nnn)

def handle_3xkk(cpu, x, y, n, kk, nnn):
    return PC_SKIP_IF(cpu.V[x] == kk)

def handle_4xkk(cpu, x, y, n, kk, nnn):
    return PC_SKIP_IF(cpu.V[x] != kk)

def handle_5xy0(cpu, x, y, n, kk, nnn):
    return PC_SKIP_IF(cpu.V[x] == cpu.V[y])

def handle_6xkk(cpu, x, y, n, kk, nnn):
    cpu.V[x] = kk
    return PC_NEXT

def handle_7xkk(cpu, x, y, n, kk, nnn):
    value = cpu.V[x] + kk
    cpu.V[x] = value if value < 256 else value - 256
    return PC_NEXT

def handle_8xy0(cpu, x, y, n, kk, nnn):
    cpu.V[x] = cpu.V[y]
    return PC_NEXT

def handle_8xy1(cpu, x, y, n, kk, nnn):
    cpu.V[x] = cpu.V[x] | cpu.V[y]
    cpu.V[x] &= 0xFF
    return PC_NEXT

def handle_8xy2(cpu, x, y, n, kk, nnn):
    cpu.V[x] = cpu.V[x] & cpu.V[y]
    cpu.V[x] &= 0xFF
    return PC_NEXT

def handle_8xy3(cpu, x, y, n, kk, nnn):
    cpu.V[x] = cpu.V[x] ^ cpu.V[y]
    cpu.V[x] &= 0xFF
    return PC_NEXT

def handle_8xy4(cpu, x, y, n, kk, nnn):
    value = cpu.V[x] + cpu.V[y]
    if value > 255:
        cpu.V[0xF] = 1
        cpu.V[x] = (value - 256) & 0xFF
    else:
        cpu.V[0xF] = 0
        cpu.V[x] = value & 0xFF

    return PC_NEXT

def handle_8xy5(cpu, x, y, n, kk, nnn):
    value = cpu.V[x] - cpu.V[y]
    if value < 0:
        cpu.V[0xF] = 0
        cpu.V[x] = value & 0xFF
        # cpu.V[x] = 0
    else:
        cpu.V[0xF] = 1
        cpu.V[x] = value & 0xFF

    return PC_NEXT

def handle_8xy6(cpu, x, y, n, kk, nnn):
    cpu.V[0xF] = (cpu.V[x] & 0x0001)
    cpu.V[x] >>= 1

    return PC_NEXT

def handle_8xy7(cpu, x, y, n, kk, nnn):
    cpu.V[0xF] = 1 if cpu.V[y] > cpu.V[x] else 0
    cpu.V[x] = cpu.V[y] - cpu.V[x]
    cpu.V[x] &= 0xFF

    return PC_NEXT

def handle_8xye(cpu, x, y, n, kk, nnn):
    cpu.V[0xF] = cpu.V[x] >> 7  
    cpu.V[x] <<= 1
    cpu.V[x] &= 0xFF

    return PC_NEXT

def handle_9xy0(cpu, x, y, n, kk, nnn):
    return PC_SKIP_IF(cpu.V[x] != cpu.V[y])

def handle_annn(cpu, x, y, n, kk, nnn):
    cpu.i = nnn

    return PC_NEXT

def handle_bnnn(cpu, x, y, n, kk, nnn):
    return PC_JUMP(nnn + cpu.V[0])

def handle_cxkk(cpu, x, y, n, kk, nnn):
    rnum = randint(0, 255)
    cpu.V[x] = rnum & kk

    return PC_NEXT

def handle_dxyn(cpu, x, y, n, kk, nnn):
    xpos = cpu.V[x]
    ypos = cpu.V[y]
    cpu.V[0xF] = 0
    for i in range(n):
        sprite = cpu.get_ram()[cpu.i + i]
        row = (ypos + i) % 32
        for j in range(8):
            b = (sprite & 0x80) >> 7
            col = (xpos + j) % 64
            index = row * 64 + col
            pixel = b
            if b == 1 and cpu.get_pixel(row, col) == 1:
                cpu.V[0xF] = 1
                pixel = 0
            elif b == 0 and cpu.get_pixel(row, col) == 1:
                pixel = 1

            cpu.set_pixel(row, col, pixel)
            sprite <<= 1
    cpu.update_display()

    return PC_NEXT

def handle_ex9e(cpu, x, y, n, kk, nnn):
    if cpu.keypad[cpu.V[x]] == 1:
        return PC_SKIP
    
    return PC_NEXT

def handle_exa1(cpu, x, y, n, kk, nnn):
    if cpu.keypad[cpu.V[x]] == 0:
        return PC_SKIP
    
    return PC_NEXT

def handle_fx07(cpu, x, y, n, kk, nnn):
    cpu.V[x] = cpu.delay

    return PC_NEXT

def handle_fx0a(cpu, x, y, n, kk, nnn):
    cpu.set_wait_for_key_press(x)
    return PC_NONE

def handle_fx15(cpu, x, y, n, kk, nnn):
    cpu.delay = cpu.V[x]

    return PC_NEXT

def handle_fx18(cpu, x, y, n, kk, nnn):
    cpu.sound = cpu.V[x]

    return PC_NEXT

def handle_fx1e(cpu, x, y, n, kk, nnn):
    cpu.i += cpu.V[x]

    return PC_NEXT

def handle_fx29(cpu, x, y, n, kk, nnn):
    cpu.i = cpu.V[x] * 5
    return PC_NEXT

def handle_fx33(cpu, x, y, n, kk, nnn):
    value = cpu.V[x]
    ram = cpu.get_ram()
    ram[cpu.i] = int(value / 100)
    ram[cpu.i + 1] = int((value % 100) / 10)
    ram[cpu.i + 2] = int((value % 100) % 10)

    return PC_NEXT

def handle_fx55(cpu, x, y, n, kk, nnn):
    loc = cpu.i
    for i in range(x + 1):
        cpu.get_ram()[loc + i] = cpu.V[i]

    return PC_NEXT

def handle_fx65(cpu, x, y, n, kk, nnn):
    for i in range(x + 1):
        cpu.V[i] = cpu.get_ram()[cpu.i + i]

    return PC_NEXT