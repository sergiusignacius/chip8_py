from emulator import Emulator
import pygame
import time
import sys

def load_rom(path, chip8):
    with open(path, "rb") as f:
        bytes = f.read()
        chip8.load_rom(bytes)

if __name__ == '__main__':
    args = len(sys.argv)
    if args < 2:
        print("Usage: chip8_py <rom>")
        sys.exit(1)

    rom_path = sys.argv[1]
    emulator = Emulator()
    load_rom(rom_path, emulator)
    
    pygame.init()
    pygame.display.set_caption("Chip8")
    clock = pygame.time.Clock()
    start = time.time()
    while True:
        start_time = time.process_time()
        pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                emulator.key_down(event.key)
            if event.type == pygame.KEYUP:
                emulator.key_up(event.key)

        if not emulator.wait_for_key_press:
            for i in range(10):
                emulator.run()
        else:
            print("waiting for key press")

        emulator.decrease_timers()

        end = time.time()
        delta = end - start
        start = end

        emulator.draw_display()
        clock.tick(60)

