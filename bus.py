from cpu import Cpu
from memory import Memory

class Bus:
  def __init__(self):
    self.cpu = Cpu(self)
    self.mem = Memory(self)

  def read_mem(self, addr):
    return self.mem.read(addr)

  def write_mem(self, addr, val):
    self.mem.write(addr, val)

b = Bus()
for i in range(1000):
  b.cpu.step()