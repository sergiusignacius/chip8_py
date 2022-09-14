import unittest
from chip8.instruction import hash_opcode, make_instruction

class InstructionTests(unittest.TestCase):

    def test_hash_opcode(self):
        self.assertEqual(hash_opcode(0xE0), 0xE0)
        self.assertEqual(hash_opcode(0xEE), 0xEE)
        self.assertEqual(hash_opcode(0x1), 0x1)
        self.assertEqual(hash_opcode(0x00E0), 0xE0)
        self.assertEqual(hash_opcode(0x00EE), 0xEE)
        self.assertEqual(hash_opcode(0x1000), 0x1)
        self.assertEqual(hash_opcode(0x1FFF), 0x1)
        self.assertEqual(hash_opcode(0x2FFF), 0x2)
        self.assertEqual(hash_opcode(0x3FFF), 0x3)
        self.assertEqual(hash_opcode(0x4FFF), 0x4)
        self.assertEqual(hash_opcode(0x5FFF), 0x5)
        self.assertEqual(hash_opcode(0x6FFF), 0x6)
        self.assertEqual(hash_opcode(0x7FFF), 0x7)
        self.assertEqual(hash_opcode(0x8FFF), 0x8F)
        self.assertEqual(hash_opcode(0x9FFF), 0x9)
        self.assertEqual(hash_opcode(0xAFFF), 0xA)
        self.assertEqual(hash_opcode(0xBFFF), 0xB)
        self.assertEqual(hash_opcode(0xCFFF), 0xC)
        self.assertEqual(hash_opcode(0xDFFF), 0xD)
        self.assertEqual(hash_opcode(0xEFFF), 0xEFF)
        self.assertEqual(hash_opcode(0xFFFF), 0xFFF)

    def test_get_instruction_nnn(self):
        insn = make_instruction(0x00E0)
        self.assertIsNotNone(insn)
        self.assertEqual(insn.mnemonic, "CLS")

    def test_get_instruction_xkk(self):
        insn = make_instruction(0xC123)
        self.assertIsNotNone(insn)
        self.assertEqual(insn.mnemonic, "RND")

    def test_all_instructions_defined(self):
        instruction_samples = [
            0x00E0, 0x00EE, 0x1333, 0x2333, 
            0x3422, 0x4422, 0x5120, 0x6325, 
            0x7531, 0x8120, 0x8121, 0x8122,
            0x8123, 0x8124, 0x8125, 0x8126, 
            0x8127, 0x812E, 0x9230, 0xA333, 
            0xB333, 0xC356, 0xD124, 0xE39E,
            0xE3A1, 0xF107, 0xF10A, 0xF115, 
            0xF118, 0xF11E, 0xF129, 0xF133, 
            0xF155, 0xF165 
        ]

        for instr in instruction_samples:
            print(instr)
            self.assertIsNotNone(make_instruction(instr))