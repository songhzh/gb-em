class Memory:
  def __init__(self, board, rom):
    self.board = board

    # 0x0000 - 0x7fff
    self.rom = bytearray(0x8000)
    # 0x8000 - 0x9fff
    self.vram = bytearray(0x2000)
    # 0xa000 - 0xbfff
    self.sram = bytearray(0x2000)
    # 0xc000 - 0xdfff
    self.wram = bytearray(0x2000)
    # 0xe000 - 0xfdff
    # (echo ram)
    # 0xfe00 - 0xfe9f
    self.oam = bytearray(0xa0)
    # 0xfea0 - 0xfeff
    # (prohibited)
    # 0xff00 - 0xff7f
    self.ioregs = bytearray(0x80)
    # 0xff80 - 0xfffe
    self.hram = bytearray(0x7f)
    # 0xffff
    self.ie = bytearray(1)

    self.load_rom(rom)

  def load_rom(self, file):
    with open(file, 'rb') as f:
      i = 0
      byte = f.read(1)
      while byte != b'':
        val = int.from_bytes(byte, byteorder='little', signed=False)
        self.write(i, val)
        i += 1
        byte = f.read(1)

  def read(self, addr):
    if 0x0000 <= addr < 0x8000:
      return self.rom[addr]
    if 0x8000 <= addr < 0xa000:
      return self.vram[addr-0x8000]
    if 0xa000 <= addr < 0xc000:
      return self.sram[addr-0xa000]
    if 0xc000 <= addr < 0xe000:
      return self.wram[addr-0xc000]
    if 0xe000 <= addr < 0xfe00:
      return self.wram[addr-0xe000]
    if 0xfe00 <= addr < 0xfea0:
      return self.oam[addr-0xfe00]
    if 0xfea0 <= addr < 0xff00:
      return
    if 0xff00 <= addr < 0xff80:
      return self.ioregs[addr-0xff00]
    if 0xff80 <= addr < 0xffff:
      return self.hram[addr-0xff80]
    if addr == 0xffff:
      return self.ie[0]
    raise IndexError('Reading memory out of bounds')

  def write(self, addr, val):
    if 0x0000 <= addr < 0x8000:
      self.rom[addr] = val
      return
    if 0x8000 <= addr < 0xa000:
      self.vram[addr-0x8000] = val
      return
    if 0xa000 <= addr < 0xc000:
      self.sram[addr-0xa000] = val
      return
    if 0xc000 <= addr < 0xe000:
      self.wram[addr-0xc000] = val
      return
    if 0xe000 <= addr < 0xfe00:
      self.wram[addr-0xe000] = val
      return
    if 0xfe00 <= addr < 0xfea0:
      self.oam[addr-0xfe00] = val
      return
    if 0xfea0 <= addr < 0xff00:
      return
    if 0xff00 <= addr < 0xff80:
      self.ioregs[addr-0xff00] = val
      return
    if 0xff80 <= addr < 0xffff:
      self.hram[addr-0xff80] = val
      return
    if addr == 0xffff:
      self.ie[0] = val
      return
    raise IndexError('Writing memory out of bounds', hex(addr))