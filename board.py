from cpu import Cpu
from memory import Memory

from time import sleep

class Board:
  def __init__(self):
    self.cpu = Cpu(self)
    self.mem = Memory(self)

  def read_mem(self, addr):
    return self.mem.read(addr)

  def write_mem(self, addr, val):
    self.mem.write(addr, val)

  def set_if(self, flag):
    flags = self.read_mem(0xff0f)
    if flags & (1 << flag):
      raise ValueError('Flag already set')
    val = flags ^ (1 << flag)
    self.write_mem(0xff0f, val)

  def clr_if(self, flag):
    flags = self.read_mem(0xff0f)
    if not flags & (1 << flag):
      raise ValueError('Flag already cleared')
    val = flags ^ (1 << flag)
    self.write_mem(0xff0f, val)

b = Board()
while True:
  b.cpu.step()
  # input('')