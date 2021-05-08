from cpu import Cpu
from lcd import Lcd
from memory import Memory

class Board:
  def __init__(self, rom):
    self.cpu = Cpu(self)
    self.lcd = Lcd(self)
    self.mem = Memory(self)
    self.reset_regs()
    self.mem.load_rom(rom)

  def reset_regs(self):
    # self.cpu.regs.af = 0x1180
    # self.cpu.regs.bc = 0x0000
    # self.cpu.regs.de = 0xff56
    # self.cpu.regs.hl = 0x000d
    # self.cpu.regs.sp = 0xfffe
    # self.cpu.regs.pc = 0x0100

    self.cpu.regs.af = 0x01b0
    self.cpu.regs.bc = 0x0013
    self.cpu.regs.de = 0x00d8
    self.cpu.regs.hl = 0x014d
    self.cpu.regs.sp = 0xfffe
    self.cpu.regs.pc = 0x0100
    self.write_mem(0xff05, 0x00) # tima
    self.write_mem(0xff06, 0x00) # tma
    self.write_mem(0xff07, 0x00) # tac
    self.write_mem(0xff10, 0x80) # nr10
    self.write_mem(0xff11, 0xbf) # nr11
    self.write_mem(0xff12, 0xf3) # nr12
    self.write_mem(0xff14, 0xbf) # nr14
    self.write_mem(0xff16, 0x3f) # nr21
    self.write_mem(0xff17, 0x00) # nr22
    self.write_mem(0xff19, 0xbf) # nr24
    self.write_mem(0xff1a, 0x7f) # nr30
    self.write_mem(0xff1b, 0xff) # nr31
    self.write_mem(0xff1c, 0x9f) # nr32
    self.write_mem(0xff1e, 0xbf) # nr34
    self.write_mem(0xff20, 0xff) # nr41
    self.write_mem(0xff21, 0x00) # nr42
    self.write_mem(0xff22, 0x00) # nr43
    self.write_mem(0xff23, 0xbf) # nr44
    self.write_mem(0xff24, 0x77) # nr50
    self.write_mem(0xff25, 0xf3) # nr51
    self.write_mem(0xff26, 0xf1) # nr52
    self.write_mem(0xff40, 0x91) # lcdc
    self.write_mem(0xff42, 0x00) # scy
    self.write_mem(0xff43, 0x00) # scx
    self.write_mem(0xff45, 0x00) # lyc
    self.write_mem(0xff47, 0xfc) # bgp
    self.write_mem(0xff48, 0xff) # obp0
    self.write_mem(0xff49, 0xff) # obp1
    self.write_mem(0xff4a, 0x00) # wv
    self.write_mem(0xff4b, 0x00) # wx
    self.write_mem(0xffff, 0x00) # ie

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