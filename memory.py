class Memory:
  def __init__(self, bus):
    self.bus = bus

  def fetch(self, addr):
    return 0x00