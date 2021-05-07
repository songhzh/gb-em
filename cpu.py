from instructions import instructions
from registers import Registers

class Cpu:
  def __init__(self, board):
    self.regs = Registers()
    self.board = board

    self.halted = False
    self.int_master_enable = False
    self.int_enable = True
    self.int_flag = False

  def read(self, addr):
    return self.board.read_mem(addr)

  def read_word(self, addr):
    hi = self.read(addr+1)
    lo = self.read(addr)
    return (hi << 8) | lo

  def write(self, addr, val):
    self.board.write_mem(addr, val)

  def write_word(self, addr, val):
    self.write(addr, val & 0xff)
    self.write(addr+1, val >> 8)

  def fetch_byte(self):
    byte = self.read(self.regs.pc)
    self.regs.pc += 1
    return byte

  def fetch_word(self):
    lo = self.fetch_byte()
    hi = self.fetch_byte()
    return (hi << 8) | lo

  def step(self):
    opcode = self.fetch_byte()
    cycles = instructions[opcode](self)
    if opcode != 0:
      print(instructions[opcode].__name__)
      self.regs.print()
    return cycles