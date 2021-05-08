from instructions import instructions
from registers import Registers

class Cpu:
  def __init__(self, board):
    self.regs = Registers()
    self.board = board

    self.halted = False
    self.pending_ei = False
    self.ime = False

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

  def handle_interrupt(self, flag, vec):
    self.ime = False
    self.bus.clr_if(flag)
    self.cpu.regs.sp -= 2
    self.cpu.write_word(self.cpu.regs.sp, self.cpu.regs.pc)
    self.cpu.regs.pc = vec

  def check_interrupts(self):
    int_enable = self.read(0xffff)
    int_flag = self.read(0xff0f)
    interrupts = int_enable & int_flag
    if interrupts:
      self.halted = False
    if interrupts and self.ime:
      if interrupts & (1 << 0): # vblank
        self.handle_interrupt(0, 0x40)
      elif interrupts & (1 << 1): # lcd stat
        self.handle_interrupt(1, 0x48)
      elif interrupts & (1 << 2): # timer
        self.handle_interrupt(2, 0x50)
      elif interrupts & (1 << 3): # serial
        self.handle_interrupt(3, 0x58)
      elif interrupts & (1 << 4): # joypad
        self.handle_interrupt(4, 0x60)
      else:
        raise RuntimeError('Unknown interrupt flag')
      return True
    if self.pending_ei:
      self.ime = True
      self.pending_ei = False
    return False

  def step(self):
    # if self.regs.pc == 0xc000:
    #   print()
    interrupted = self.check_interrupts()
    if interrupted:
      return 5
    if self.halted:
      return 4
    opcode = self.fetch_byte()
    cycles = instructions[opcode](self)
    # if opcode != 0:
    #   print(instructions[opcode].__name__)
    #   self.regs.print()
    #   print()
    return cycles