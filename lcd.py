MODE_OAM = 2
MODE_VRAM = 3
MODE_HBLANK = 0
MODE_VBLANK = 1

class Lcd:
  def __init__(self, board):
    self.board = board
    self.mode = MODE_OAM
    self.clock = 0
    self.line = 0

  def read_oam(self):
    if self.clock >= 80:
      self.clock -= 80
      self.mode = MODE_VRAM

  def read_vram(self):
    if self.clock >= 172:
      self.clock -= 172
      self.mode = MODE_HBLANK
      self.write_scan()

  def hblank(self):
    if self.clock >= 204:
      self.clock -= 204
      self.line += 1

      if self.line > 143:
        self.mode = MODE_VBLANK
      else:
        self.mode = MODE_OAM

  def vblank(self):
    if self.clock >= 456:
      self.clock -= 456

      if self.line == 144:
        self.board.set_if(0)
      if self.line > 153:
        self.mode = MODE_OAM
        self.line = 0

      self.line += 1
      
  def step(self, cycles):
    self.clock += cycles

    if self.mode == MODE_OAM:
      self.read_oam()
    elif self.mode == MODE_VRAM:
      self.read_vram()
    elif self.mode == MODE_HBLANK:
      self.hblank()
    elif self.mode == MODE_VBLANK:
      self.vblank()
    else:
      raise ValueError('Invalid LCD mode')

  def write_scan(self):
    pass