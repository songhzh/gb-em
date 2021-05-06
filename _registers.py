class Registers:
  def __init__(self):
    self._a = 0
    self._f = 0
    self._b = 0
    self._c = 0
    self._d = 0
    self._e = 0
    self._h = 0
    self._l = 0
    self._sp = 0
    self._pc = 0

  @property
  def a(self):
    return self._a

  @a.setter
  def a(self, nn):
    self._a = nn & 0xff

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