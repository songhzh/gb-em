class Memory:
  def __init__(self, bus):
    self.bus = bus
    self.load('roms/tetris.gb')
    self.rom += bytearray(0xffff)

  def load(self, file):
    self.rom = bytearray(open(file, "rb").read())

  def read(self, addr):
    return self.rom[addr]

  def write(self, addr, val):
    self.rom[addr] = val
    # if 0x8000 <= addr < 0x9fff:
    #   print(self.bus.cpu.regs.pc)