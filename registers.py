FLAG_Z = 7
FLAG_N = 6
FLAG_H = 5
FLAG_C = 4

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
  def f(self):
    return self._f

  @f.setter
  def f(self, nn):
    self._f = nn & 0xff

  @property
  def b(self):
    return self._b

  @b.setter
  def b(self, nn):
    self._b = nn & 0xff

  @property
  def c(self):
    return self._c

  @c.setter
  def c(self, nn):
    self._c = nn & 0xff

  @property
  def d(self):
    return self._d

  @d.setter
  def d(self, nn):
    self._d = nn & 0xff

  @property
  def e(self):
    return self._e

  @e.setter
  def e(self, nn):
    self._e = nn & 0xff

  @property
  def h(self):
    return self._h

  @h.setter
  def h(self, nn):
    self._h = nn & 0xff

  @property
  def l(self):
    return self._l

  @l.setter
  def l(self, nn):
    self._l = nn & 0xff

  @property
  def bc(self):
    return (self._b << 8) | self._c

  @bc.setter
  def bc(self, nn):
    self._b = nn >> 8
    self._c = nn & 0xff

  @property
  def de(self):
    return (self._d << 8) | self._e

  @de.setter
  def de(self, nn):
    self._d = nn >> 8
    self._e = nn & 0xff

  @property
  def hl(self):
    return (self._h << 8) | self._l

  @hl.setter
  def hl(self, nn):
    self._h = nn >> 8
    self._l = nn & 0xff

  @property
  def sp(self):
    return self._sp

  @sp.setter
  def sp(self, nn):
    self._sp = nn & 0xffff

  @property
  def pc(self):
    return self._pc

  @pc.setter
  def pc(self, nn):
    self._pc = nn & 0xffff

  def flags(self, z, n, h, c):
    f = 0
    if z is not None:
      f |= z << FLAG_Z
    if n is not None:
      f |= n << FLAG_N
    if h is not None:
      f |= h << FLAG_H
    if c is not None:
      f |= c << FLAG_C
    self.f = f