from cpu import Cpu
from lcd import Lcd
from memory import Memory

class Board:
  def __init__(self, rom):
    self.cpu = Cpu(self)
    self.lcd = Lcd(self)
    self.mem = Memory(self, rom)

  def read_mem(self, addr):
    return self.mem.read(addr)

  def write_mem(self, addr, val):
    self.mem.write(addr, val)

  def set_if(self, flag):
    flags = self.read_mem(0xff0f)
    if flags & (1 << flag):
      return
    val = flags ^ (1 << flag)
    self.write_mem(0xff0f, val)

  def clr_if(self, flag):
    flags = self.read_mem(0xff0f)
    if not flags & (1 << flag):
      return
    val = flags ^ (1 << flag)
    self.write_mem(0xff0f, val)

  def step(self):
    cycles = self.cpu.step()
    self.lcd.step(cycles)