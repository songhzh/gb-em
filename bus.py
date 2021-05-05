from cpu import Cpu
from memory import Memory

class Bus:
  def __init__(self):
    self.cpu = Cpu(self)
    self.memory = Memory(self)

  def read(self, addr):
    return self.memory.fetch(addr)