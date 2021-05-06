from cpu import Cpu
from memory import Memory

class Bus:
  def __init__(self):
    self.cpu = Cpu(self)
    self.mem = Memory(self)

  def read_mem(self, addr):
    return self.mem.fetch(addr)