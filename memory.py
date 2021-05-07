class Memory:
  def __init__(self, board):
    self.board = board

    # 0x0000 - 0x7fff
    self.rom = self.load_rom('roms/tetris.gb')
    assert len(self.rom) == 0x8000

    # 0x8000 - 0x9fff
    self.vram = None

    # 0xa000 - 0xbfff
    self.sram = None

    # 0xc000 - 0xdfff
    self.wram = None

    # 0xe000 - 0xfdff
    # echo ram

    # 0xfe00 - 0xfe9f
    self.oam = None
    
    # 0xfea0 - 0xfeff
    # prohibited

    # 0xff00 - 0xff7f
    self.ioregs = None

    # 0xff80 - 0xfffe
    self.hram = None

    # 0xffff
    self.ie = None

  def load_rom(self, file):
    return bytearray(open(file, "rb").read())

  def read(self, addr):
    return self.rom[addr]

  def write(self, addr, val):
    self.rom[addr] = val
    # if 0x8000 <= addr < 0x9fff:
    #   print(self.board.cpu.regs.pc)