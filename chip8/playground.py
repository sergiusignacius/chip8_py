# from tracemalloc import start
# import pygame
# from random import randint
# import sys
# import time

# KEY_MAPPINGS = {
#     0x0: pygame.K_1,
#     0x1: pygame.K_2,
#     0x2: pygame.K_3,
#     0x3: pygame.K_4,
#     0x4: pygame.K_5,
#     0x5: pygame.K_q,
#     0x6: pygame.K_w,
#     0x7: pygame.K_e,
#     0x8: pygame.K_r,
#     0x9: pygame.K_t,
#     0xA: pygame.K_a,
#     0xB: pygame.K_s,
#     0xC: pygame.K_d,
#     0xD: pygame.K_f,
#     0xE: pygame.K_g,
#     0xF: pygame.K_z,
# }
# SPRITES = [
#     0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
#     0x20, 0x60, 0x20, 0x20, 0x70, # 1
#     0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2 
#     0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3 
#     0x90, 0xF0, 0x90, 0x10, 0x10, # 4 
#     0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5 
#     0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6 
#     0xF0, 0x10, 0x20, 0x40, 0x40, # 7 
#     0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8 
#     0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9 
#     0xF0, 0x90, 0xF0, 0x90, 0x90, # A 
#     0xE0, 0x90, 0x30, 0x90, 0xE0, # B 
#     0xF0, 0x80, 0x80, 0x80, 0xF0, # C 
#     0xE0, 0x90, 0x90, 0x90, 0xE0, # D 
#     0xF0, 0x80, 0xF0, 0x80, 0xF0, # E 
#     0xF0, 0x80, 0xF0, 0x80, 0x80  # F
# ]

# PC_NEXT = ["next", ""]
# PC_SKIP = ["skip", ""]
# def PC_JUMP(addr): return ["jump", addr]

# DRAW_GRID = False
# PIXEL_SCALING = 10

# class Chip8:
    
#     def __init__(self):
#         self.ram = [0] * 4096
#         self.display = [0] * 64 * 32
#         self.program_size = 0
#         self.screen = pygame.display.set_mode((64 * PIXEL_SCALING, 32 * PIXEL_SCALING))
#         self.cpu = Cpu(self)
    
#     def load_rom(self, bytes):
#         i = 0
#         for b in SPRITES:
#             self.ram[i] = b
#             i += 1

#         i = 0
#         for b in bytes:
#             self.ram[0x200 + i] = b
#             i += 1

#         self.program_size = len(bytes)

#     def tick(self):
#         more = self.cpu.fetch()
#         self.cpu.decode()
#         self.cpu.execute()
#         return more

#     def show_display(self):
#         black = (0, 0, 0)
#         white = (255, 255, 255)
#         self.screen.fill(black)

#         for i in range(len(self.display)):
#             if self.display[i] == 1:
#                 color = white
#             else:
#                 color = black
#             pygame.draw.rect(self.screen, color, pygame.Rect((i % 64) * PIXEL_SCALING, int(i / 64) * PIXEL_SCALING, PIXEL_SCALING, PIXEL_SCALING))
        
#         if DRAW_GRID:
#             for i in range(1, 64):
#                 pygame.draw.line(self.screen, white, (i * PIXEL_SCALING, 0), (i * PIXEL_SCALING, 32 * PIXEL_SCALING))

#             for i in range(1, 32):
#                 pygame.draw.line(self.screen, white, (0, i * PIXEL_SCALING), (64 * PIXEL_SCALING, i * PIXEL_SCALING))
    
#     def set_pixel(self, x, y, v):
#         self.display[x * 64 + y] = v

# class Cpu:
    
#     def __init__(self, chip8):
#         self.ram = chip8.ram
#         self.display = chip8.display
#         self.screen = chip8.screen
#         self.chip8 = chip8
#         self.pc = 0x200
#         self.opcode = 0
#         self.nibbles = []
#         self.i = 0
#         self.V = [0]*16
#         self.sp = 0
#         self.stack = [0]*16
#         self.sound = 0
#         self.delay = 0

#     def fetch(self):
#         b1, b0 = self.ram[self.pc], self.ram[self.pc + 1]
#         self.opcode = (b1 << 8) | b0
#         return self.pc < len(self.ram) and self.pc - 0x200 < self.chip8.program_size

#     def decode(self):
#         self.nibbles = [
#             (self.opcode & 0xF000) >> 12,
#             (self.opcode & 0x0F00) >> 8,
#             (self.opcode & 0x00F0) >> 4,
#             (self.opcode & 0x000F)
#         ]

#     def execute(self, disassemble=False):
#         nnn = self.opcode & 0x0FFF
#         kk = self.opcode & 0x00FF
#         x = self.nibbles[1]
#         y = self.nibbles[2]
#         n = self.nibbles[3]

#         pc_update = PC_NEXT
#         match self.nibbles:
#             case [0x0, 0x0, 0xE, 0x0]: 
#                 if disassemble:
#                     print("CLS")
#                 self.display = [0] * 64 * 32

#             case [0x0, 0x0, 0xE, 0xE]: 
#                 if disassemble:
#                     print("RET")
#                 previous_pc = self.stack[self.sp]
#                 self.sp -= 1
#                 pc_update = ["jump", previous_pc + 2]

#             case [0x1, _, _, _]:
#                 if disassemble:
#                     print(f"JP {hex(nnn)}")
#                 pc_update = PC_JUMP(nnn)

#             case [0x2, _, _, _]:
#                 if disassemble:
#                     print(f"CALL {hex(nnn)}")
#                 self.sp += 1
#                 self.stack[self.sp] = self.pc
#                 pc_update = PC_JUMP(nnn)
    
#             case [0x3, _, _, _]:
#                 if disassemble:
#                     print(f"SE V{x} ")
#                 if self.V[x] == kk:
#                     pc_update = PC_SKIP

#             case [0x4, _, _, _]:
#                 if disassemble:
#                     print(f"SNE V{x}")
#                 if self.V[x] != kk:
#                     pc_update = PC_SKIP

#             case [0x5, _, _, _]:
#                 if disassemble:
#                     print(f"SE V{x} V{y}")
#                 if self.V[x] == self.V[y]:
#                     pc_update = PC_SKIP

#             case [0x6, _, _, _]:
#                 if disassemble:
#                     print(f"LD V{x} {hex(kk)}")
#                 self.V[x] = kk

#             case [0x7, _, _, _]:
#                 if disassemble:
#                     print(f"ADD V{x} {hex(kk)}")
#                 value = self.V[x] + kk
#                 self.V[x] = value if value < 256 else value - 256

#             case [0x8, _, _, 0x0]:
#                 if disassemble:
#                     print(f"LD V{x} V{y}")
#                 self.V[x] = self.V[y]

#             case [0x8, _, _, 0x1]:
#                 if disassemble:
#                     print(f"OR V{x}, V{y}")
#                 self.V[x] = self.V[x] | self.V[y]
#                 self.V[x] &= 0xFF

#             case [0x8, _, _, 0x2]:
#                 if disassemble:
#                     print(f"AND V{x}, V{y}")
#                 self.V[x] = self.V[x] & self.V[y]
#                 self.V[x] &= 0xFF

#             case [0x8, _, _, 0x3]:
#                 if disassemble:
#                     print(f"XOR V{x}, V{y}")
#                 self.V[x] = self.V[x] ^ self.V[y]
#                 self.V[x] &= 0xFF

#             case [0x8, _, _, 0x4]:
#                 if disassemble:
#                     print(f"ADDC V{x}, V{y}")
#                 value = self.V[x] + self.V[y]
#                 if value > 255:
#                     self.V[0xF] = 1
#                     self.V[x] = (value - 256) & 0xFF
#                 else:
#                     self.V[0xF] = 0
#                     self.V[x] = value & 0xFF

#             case [0x8, _, _, 0x5]:
#                 if disassemble:
#                     print(f"SUB V{x}, V{y}")
#                 self.V[0xF] = 1 if self.V[x] > self.V[y] else 0
#                 self.V[x] -= self.V[y]
#                 self.V[x] &= 0xFF

#             case [0x8, _, _, 0x6]:
#                 if disassemble:
#                     print(f"SHR V{x}")
#                 self.V[0xF] = (self.V[x] & 0x0001)
#                 self.V[x] >>= 1
#                 # self.V[x] &= 0xFF

#             case [0x8, _, _, 0x7]:
#                 if disassemble:
#                     print(f"SUBN V{x}, V{y}")
#                 self.V[x] = self.V[y] - self.V[x]
#                 self.V[0xF] = 1 if self.V[y] > self.V[x] else 0
#                 self.V[x] &= 0xFF

#             case [0x8, _, _, 0xE]:
#                 if disassemble:
#                     print(f"SHL V{x}")
#                 self.V[0xF] = self.V[x] >> 7
#                 self.V[x] <<= 1
#                 self.V[x] &= 0xFF

#             case [0x9, _, _, 0x0]:
#                 if disassemble:
#                     print(f"SNE V{x}, V{y}")
#                 if self.V[x] != self.V[y]:
#                     pc_update = PC_SKIP

#             case [0xA, _, _, _]:
#                 if disassemble:
#                     print(f"LD I, {nnn}")
#                 self.i = nnn

#             case [0xB, _, _, _]:
#                 if disassemble:
#                     print(f"JP V0, {nnn}")
#                 pc_update = PC_JUMP(nnn + self.V[0])

#             case [0xC, _, _, _]:
#                 if disassemble:
#                     print(f"RND V{x}, {kk}")
#                 rnum = randint(0, 255)
#                 self.V[x] = rnum & kk

#             case [0xD, _, _, _]:
#                 if disassemble:
#                     print(f"DISPLAY {x} {y} {n}")
#                 xpos = self.V[x]
#                 ypos = self.V[y]
#                 self.V[0xF] = 0
#                 for i in range(n):
#                     sprite = self.ram[self.i + i]
#                     row = (ypos + i) % 32
#                     for j in range(8):
#                         b = (sprite & 0x80) >> 7
#                         col = (xpos + j) % 64
#                         index = row * 64 + col
#                         pixel = b
#                         if b == 1 and self.display[index] == 1:
#                             self.V[0xF] = 1
#                             pixel = 0
#                         elif b == 0 and self.display[index] == 1:
#                             pixel = 1

#                         self.chip8.set_pixel(row, col, pixel)

#                         sprite <<= 1
#                 chip8.show_display()
#                 pygame.display.update() 

#             case [0xE, _, 0x9, 0xE]:
#                 if disassemble:
#                     print(f"SKP V{x}")
#                 key_to_check = x
#                 pressed = pygame.key.get_pressed()
#                 if pressed[KEY_MAPPINGS[key_to_check]]:
#                     pc_update = PC_SKIP

#             case [0xE, _, 0xA, 0x1]:
#                 if disassemble:
#                     print(f"SKNP V{x}")
#                 key_to_check = x
#                 pressed = pygame.key.get_pressed()
#                 if not pressed[KEY_MAPPINGS[key_to_check]]:
#                     pc_update = PC_SKIP

#             case [0xF, _, 0x0, 0x7]:
#                 if disassemble:
#                     print(f"LD V{x}, DT")
#                 self.V[x] = self.delay

#             case [0xF, _, 0x0, 0xA]:
#                 if disassemble:
#                     print(f"LD V{x}, K")
                
#                 pc_update = ["stop", ""]
#                 keys_pressed = pygame.key.get_pressed()
#                 if any(keys_pressed):
#                     for k, v in KEY_MAPPINGS.items():
#                         if keys_pressed[v]:
#                             self.V[x] = k
#                             pc_update = PC_NEXT
#             case [0xF, _, 0x1, 0x5]:
#                 if disassemble:
#                     print(f"LD DT, V{x}")
#                 self.delay = self.V[x]
            
#             case [0xF, _, 0x1, 0x8]:
#                 self.sound = self.V[x]

#             case [0xF, _, 0x1, 0xE]:
#                 if disassemble:
#                     print(f"ADD I, V{x}")
#                 self.i += self.V[x]

#             case [0xF, _, 0x2, 0x9]:
#                 if disassemble:
#                     print(f"LD F, V{x}")
#                 self.i = self.V[x] * 5

#             case [0xF, _, 0x3, 0x3]:
#                 # The interpreter takes the decimal value of Vx, and places the hundreds digit in memory at location in I, 
#                 # the tens digit at location I+1, and the ones digit at location I+2.
#                 if disassemble:
#                     print(f"LD B, V{x}")
#                 val = self.V[x]
#                 self.ram[self.i] = int(val / 100)
#                 self.ram[self.i + 1] = int((val % 100) / 10)
#                 self.ram[self.i + 2] = int((val % 100) % 10)

#             case [0xF, _, 0x5, 0x5]:
#                 if disassemble:
#                     print(f"LD [I], V{x}")
#                 loc = self.i
#                 for i in range(x + 1):
#                     self.ram[loc + i] = self.V[i]

#             case [0xF, _, 0x6, 0x5]:
#                 if disassemble:
#                     print(f"LD V{x}, [I]")
#                 for i in range(x + 1):
#                     self.V[i] = self.ram[self.i + i]

#             case _: 
#                 if disassemble:
#                     print(f"Not implemented: {[hex(n) for n in self.nibbles]}")
#                 pass
        
#         if disassemble:
#             self.pc += 2
#         else:
#             match pc_update:
#                 case ["jump", n]: 
#                     self.pc = n
#                 case ["skip", _]: 
#                     self.pc += 4
#                 case ["next", _]: 
#                     self.pc += 2
#                 # case _: print("???")

def load_rom(path, chip8):
    with open(path, "rb") as f:
        bytes = f.read()
        chip8.load_rom(bytes)

pygame.init()
chip8 = Chip8()
# load_rom("./maze.ch8", chip8)
load_rom("./bc_test.ch8", chip8)

i = 0
start_time = time.process_time()
ops = 0
cpu_freq = 500
timer_freq = 60
while True:
    more = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if more:
        more = chip8.tick()
        ops += 1
    
    if ops % cpu_freq == 0:
        elapsed = time.process_time() - start_time
        time_to_next_sec = 1.0 - elapsed
        # print(f"Sleeping. Elapsed: {elapsed}. Time to next sec: {time_to_next_sec}")
        if time_to_next_sec > 0:
            time.sleep(min(0, 1 - (time.process_time() - start_time)))

    if ops % timer_freq == 0:
        elapsed = time.process_time() - start_time
        time_to_next_sec = 1.0 - elapsed
        print(f"Sleeping Sound/Delay. Elapsed: {elapsed}. Time to next sec: {time_to_next_sec}")
        if time_to_next_sec > 0:
            time.sleep(min(0, 1 - (time.process_time() - start_time)))