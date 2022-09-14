import unittest
from chip8.cpu import Cpu

MOCK_PROGRAM = [
    0x00,
    0xEE,
    0x11,
    0x12
]

class MockEmulator:

    def __init__(self):
        self.ram = [0] * 1024
        for i in range(len(MOCK_PROGRAM)):
            self.ram[0x200 + i] = MOCK_PROGRAM[i]

class TestCpuFetch(unittest.TestCase):
    def setUp(self):
        self.emulator = MockEmulator()

    def test_initialization(self):
        cpu = Cpu(self.emulator)
        self.assertEqual(cpu.pc, 0x200)
        self.assertEqual(cpu.sp, 0x0)

    def test_fetch(self):
        cpu = Cpu(self.emulator)
        opcode = cpu.fetch()
        self.assertEqual(opcode, 0x00EE)
        cpu.pc += 2
        opcode = cpu.fetch()
        self.assertEqual(opcode, 0x1112)