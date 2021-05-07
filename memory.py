class Memory:
  def __init__(self, bus):
    self.bus = bus
    self.load('roms/06-ld r,r.gb')
    self.rom += bytearray(0xffff)

  def load(self, file):
    self.rom = bytearray(open(file, "rb").read())

  def read(self, addr):
    return self.rom[addr]

  def write(self, addr, val):
    # self.rom[addr] = val.to_bytes(1, byteorder='little')
    self.rom[addr] = val