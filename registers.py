class Registers:
  def __init__(self):
    self.a = 0
    self.f = 0
    self.b = 0
    self.c = 0
    self.d = 0
    self.e = 0
    self.h = 0
    self.l = 0
    self.sp = 0
    self.pc = 0

  @property
  def bc(self):
    return (self.b << 8) | self.c

  @bc.setter
  def bc(self, nn):
    self.b = nn >> 8
    self.c = nn & 0xff

  @property
  def de(self):
    return (self.d << 8) | self.e

  @de.setter
  def de(self, nn):
    self.d = nn >> 8
    self.e = nn & 0xff

  @property
  def hl(self):
    return (self.h << 8) | self.l

  @hl.setter
  def hl(self, nn):
    self.h = nn >> 8
    self.l = nn & 0xff

  @property
  def f_z(self):
    return (self.f >> 7) & 1

  @f_z.setter
  def f_z(self, bit):
    self.f = Registers.set_bit(self.f, 7) if bit else Registers.clr_bit(self.f, 7)

  @property
  def f_n(self):
    return (self.f >> 6) & 1

  @f_n.setter
  def f_n(self, bit):
    self.f = Registers.set_bit(self.f, 6) if bit else Registers.clr_bit(self.f, 6)

  @property
  def f_h(self):
    return (self.f >> 5) & 1

  @f_h.setter
  def f_h(self, bit):
    self.f = Registers.set_bit(self.f, 5) if bit else Registers.clr_bit(self.f, 5)

  @property
  def f_c(self):
    return (self.f >> 4) & 1

  @f_c.setter
  def f_c(self, bit):
    self.f = Registers.set_bit(self.f, 4) if bit else Registers.clr_bit(self.f, 4)

  def set_bit(val, pos):
    return val | (1 << pos)

  def clr_bit(val, pos):
    return val & ~(1 << pos)