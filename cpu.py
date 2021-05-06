from instructions import instructions
from registers import Registers

class Cpu:
  def __init__(self, bus):
    self.regs = Registers()
    self.cycles = 0
    self.bus = bus

  def fetch(self, addr):
    return self.bus.read(addr)

  def fetch_pc(self):
    byte = self.fetch(self.regs.pc)
    self.regs.pc += 1
    return byte

  def step(self):
    opcode = self.fetch_pc()
    cycles = instructions[opcode](self)