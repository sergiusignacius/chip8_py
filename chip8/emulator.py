import pygame
from cpu import Cpu
from utils import KEY_MAPPINGS, REVERSE_MAPPINGS

PIXEL_SCALING = 10
SPRITES = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
    0x20, 0x60, 0x20, 0x20, 0x70, # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2 
    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3 
    0x90, 0x90, 0xF0, 0x10, 0x10, # 4 
    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5 
    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6 
    0xF0, 0x10, 0x20, 0x40, 0x40, # 7 
    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8 
    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9 
    0xF0, 0x90, 0xF0, 0x90, 0x90, # A 
    0xE0, 0x90, 0x30, 0x90, 0xE0, # B 
    0xF0, 0x80, 0x80, 0x80, 0xF0, # C 
    0xE0, 0x90, 0x90, 0x90, 0xE0, # D 
    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E 
    0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]
DRAW_GRID = False

class Emulator:

    def __init__(self):
        self.ram = [0] * 4096
        self.display = [0] * 64 * 32
        self.program_size = 0
        self.screen = pygame.display.set_mode((64 * PIXEL_SCALING, 32 * PIXEL_SCALING))
        self.cpu = Cpu(self)
        self.wait_for_key_press = False
        self.screen_is_dirty = True

    def load_rom(self, bytes):
        i = 0
        for b in SPRITES:
            self.ram[i] = b
            i += 1

        i = 0
        for b in bytes:
            self.ram[0x200 + i] = b
            i += 1

        self.program_size = len(bytes)

    def update_display(self):
        black = (0, 0, 0)
        white = (255, 255, 255)
        self.screen.fill(black)

        for i in range(len(self.display)):
            if self.display[i] == 1:
                color = white
            else:
                color = black
            pygame.draw.rect(self.screen, color, pygame.Rect((i % 64) * PIXEL_SCALING, int(i / 64) * PIXEL_SCALING, PIXEL_SCALING, PIXEL_SCALING))
        
        if DRAW_GRID:
            for i in range(1, 64):
                pygame.draw.line(self.screen, white, (i * PIXEL_SCALING, 0), (i * PIXEL_SCALING, 32 * PIXEL_SCALING))

            for i in range(1, 32):
                pygame.draw.line(self.screen, white, (0, i * PIXEL_SCALING), (64 * PIXEL_SCALING, i * PIXEL_SCALING))
        self.screen_is_dirty = True

    def get_pixel(self, x, y):
        return self.display[x * 64 + y]

    def set_pixel(self, x, y, v):
        self.display[x * 64 + y] = v

    def run(self):
        opcode = self.cpu.fetch()
        self.cpu.execute(opcode)
    
    def clear_display(self):
        self.display = [0] * 4096
        self.update_display()
    
    def draw_display(self):
        if self.screen_is_dirty:
            pygame.display.flip()
            self.screen_is_dirty = False

    def decrease_timers(self):
        if self.cpu.delay > 0:
            self.cpu.delay -= 1
        if self.cpu.sound > 0:
            self.cpu.sound -= 1

    def key_down(self, key):
        if key in REVERSE_MAPPINGS:
            self.cpu.keypad[REVERSE_MAPPINGS[key]] = 1
            print(self.cpu.keypad)  
            if self.wait_for_key_press:
                self.cpu.pc += 2
                self.cpu.V[self.wait_for_key_press] = REVERSE_MAPPINGS[key]
                self.wait_for_key_press = None
    
    def key_up(self, key):
        if key in REVERSE_MAPPINGS and self.cpu.keypad[REVERSE_MAPPINGS[key]] == 1:
            self.cpu.keypad[REVERSE_MAPPINGS[key]] = 0
            print(self.cpu.keypad)
            
    
    def set_wait_for_key_press(self, b):
        self.wait_for_key_press = b