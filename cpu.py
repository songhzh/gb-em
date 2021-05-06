from instructions import instructions
from registers import Registers

class Cpu:
  def __init__(self, bus):
    self.regs = Registers()
    self.cycles = 0
    self.bus = bus

  def bus_read(self, addr):
    return self.bus.read_mem(addr)

  def bus_write(self, addr, val):
    self.bus.write_mem(addr, val)

  def fetch_byte(self):
    byte = self.bus_read(self.regs.pc)
    self.regs.pc += 1
    return byte

  def fetch_word(self):
    lo = self.fetch_byte()
    hi = self.fetch_byte()
    return (hi << 8) | lo

  def step(self):
    opcode = self.fetch_byte()
    if opcode != 0:
      print(instructions[opcode].__name__)
    cycles = instructions[opcode](self)