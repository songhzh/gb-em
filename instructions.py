import logging, sys

logging.basicConfig(level=logging.DEBUG)

def signed(val):
  sign = -1 if val & 0x80 else 1
  val = (val ^ 0xff) + 1
  return sign * (val & 0xff) 

def inc_byte(cpu, val):
  res = (val + 1) & 0xff
  z = 1 if res else 0
  h = 1 if val & 0xf == 0xf else 0
  cpu.regs.flags(z, 0, h, None)
  return res

def dec_byte(cpu, val):
  res = (val - 1) & 0xff
  z = 1 if res == 0 else 0
  h = 0 if val & 0xf else 1
  cpu.regs.flags(z, 1, h, None)
  return res

def add_word(cpu, val0, val1):
  res = val0 + val1
  h = 1 if (val0 & 0xfff) + (val1 & 0xfff) > 0xfff else 0
  c = 1 if res > 0xffff else 0
  cpu.regs.flags(None, 0, h, c)
  return res & 0xffff

def rlc(cpu, val):
  c = 1 if val & 0x80 else 0
  res = (val << 1) | c
  z = res == 0
  cpu.regs.flags(z, 0, 0, c)
  return res & 0xff

def rl(cpu, val):
  c = 1 if val & 0x80 else 0
  res = (val << 1) | (cpu.regs.f_c)
  z = res == 0
  cpu.regs.flags(z, 0, 0, c)
  return res & 0xff

def rrc(cpu, val):
  c = val & 1
  res = (val >> 1) | (c << 7)
  z = res == 0
  cpu.regs.flags(z, 0, 0, c)
  return res & 0xff

def rr(cpu, val):
  c = val & 1
  res = (val >> 1) | (cpu.regs.f_c << 7)
  z = res == 0
  cpu.regs.flags(z, 0, 0, c)
  return res & 0xff

def sla(cpu, val):
  res = val << 1
  z = (res & 0xff) == 0
  c = res > 0xff
  cpu.regs.flags(z, 0, 0, c)
  return res & 0xff

def sra(cpu, val):
  res = val >> 1 | (val & 0x80)
  z = res == 0
  cpu.regs.flags(z, 0, 0, 0)
  return res & 0xff

def swap(cpu, val):
  hi = (val & 0xf0) >> 8
  lo = val & 0xf
  res = lo | hi
  z = res == 0
  cpu.regs.flags(z, 0, 0, 0)
  return res & 0xff

def srl(cpu, val):
  res = val >> 1
  z = res == 0
  c = val & 1
  cpu.regs.flags(z, 0, 0, c)
  return res & 0xff

def bit_op(cpu, pos, val):
  res = (val >> pos) & 1
  z = res == 0
  cpu.regs.flags(z, 0, 1, None)

def res_op(cpu, pos, val):
  res = val & ~(1 << pos)
  z = res == 0
  return res & 0xff

def set_op(cpu, pos, val):
  res = val | (1 << pos)
  z = res == 0
  return res & 0xff

def add(cpu, val0, val1):
  res = val0 + val1
  z = res == 0
  h = 1 if (val0 & 0xf) + (val1 & 0xf) > 0xf else 0
  c = 1 if res > 0xff else 0
  cpu.regs.flags(z, 0, h, c)
  return res

def adc(cpu, val0, val1):
  res = val0 + val1 + cpu.regs.f_c
  z = res == 0
  h = 1 if (val0 & 0xf) + (val1 & 0xf) + cpu.regs.f_c > 0xf else 0
  c = 1 if res > 0xff else 0
  cpu.regs.flags(z, 0, h, c)
  return res

def sub(cpu, val0, val1):
  res = val0 - val1
  z = res == 0
  h = 1 if (val0 & 0xf) - (val1 & 0xf) < 0 else 0
  c = 1 if res < 0 else 0
  cpu.regs.flags(z, 1, h, c)
  return res

def sbc(cpu, val0, val1):
  res = val0 - val1 - cpu.regs.f_c
  z = res == 0
  h = 1 if (val0 & 0xf) - (val1 & 0xf) - cpu.regs.f_c < 0 else 0
  c = 1 if res < 0 else 0
  cpu.regs.flags(z, 1, h, c)
  return res

def and_op(cpu, val0, val1):
  res = val0 & val1
  z = res == 0
  cpu.regs.flags(z, 0, 1, 0)
  return res

def xor_op(cpu, val0, val1):
  res = val0 ^ val1
  z = res == 0
  cpu.regs.flags(z, 0, 0, 0)
  return res

def or_op(cpu, val0, val1):
  res = val0 | val1
  z = res == 0
  cpu.regs.flags(z, 0, 0, 0)
  return res

def cp_op(cpu, val0, val1):
  return sub(cpu, val0, val1)

def nodef(cpu):
  # illegal instruction
  cpu.regs.pc -= 1

def nop(cpu):
  # 0x00
  return 4

def ld_bc_d16(cpu):
  # 0x01
  op0 = cpu.fetch_word()
  cpu.regs.bc = op0
  return 12

def ld_bc_a(cpu):
  # 0x02
  cpu.write(cpu.regs.bc, cpu.regs.a)
  return 8

def inc_bc(cpu):
  # 0x03
  cpu.regs.bc += 1
  return 8

def inc_b(cpu):
  # 0x04
  cpu.regs.b = inc_byte(cpu, cpu.regs.b)
  return 4

def dec_b(cpu):
  # 0x05
  cpu.regs.b = dec_byte(cpu, cpu.regs.b)
  return 4

def ld_b_d8(cpu):
  # 0x06
  op0 = cpu.fetch_byte()
  cpu.regs.b = op0
  return 8

def rlca(cpu):
  # 0x07
  cpu.regs.a = rlc(cpu, cpu.regs.a)
  return 4

def ld_a16_sp(cpu):
  # 0x08
  op0 = cpu.fetch_word()
  cpu.write(op0, cpu.regs.sp)
  return 20

def add_hl_bc(cpu):
  # 0x09
  cpu.regs.hl = add_word(cpu, cpu.regs.hl, cpu.regs.bc)
  return 8

def ld_a_bc(cpu):
  # 0x0a
  val = cpu.read(cpu.regs.bc)
  cpu.regs.a = val
  return 8

def dec_bc(cpu):
  # 0x0b
  cpu.regs.bc -= 1
  return 8

def inc_c(cpu):
  # 0x0c
  cpu.regs.c = inc_byte(cpu, cpu.regs.c)
  return 4

def dec_c(cpu):
  # 0x0d
  cpu.regs.c = dec_byte(cpu, cpu.regs.c)
  return 4

def ld_c_d8(cpu):
  # 0x0e
  op0 = cpu.fetch_byte()
  cpu.regs.c = op0
  logging.debug(f'ld c {hex(op0)}')
  return 8

def rrca(cpu):
  # 0x0f
  cpu.regs.a = rrc(cpu, cpu.regs.a)
  return 4

def stop_0(cpu):
  # 0x10
  cpu.regs.pc += 1
  return 4

def ld_de_d16(cpu):
  # 0x11
  op0 = cpu.fetch_word()
  cpu.regs.de = op0
  logging.debug(f'ld de {hex(op0)}')
  return 12

def ld_de_a(cpu):
  # 0x12
  cpu.write(cpu.regs.de, cpu.regs.a)
  logging.debug(f'ld (de), a')
  return 8

def inc_de(cpu):
  # 0x13
  cpu.regs.de += 1
  return 8

def inc_d(cpu):
  # 0x14
  cpu.regs.d = inc_byte(cpu, cpu.regs.d)
  return 4

def dec_d(cpu):
  # 0x15
  cpu.regs.d = dec_byte(cpu, cpu.regs.d)
  return 4

def ld_d_d8(cpu):
  # 0x16
  op0 = cpu.fetch_byte()
  cpu.regs.d = op0
  return 8

def rla(cpu):
  # 0x17
  cpu.regs.a = rl(cpu, cpu.regs.a)
  return 4

def jr_r8(cpu):
  # 0x18
  op0 = signed(cpu.fetch_byte())
  cpu.regs.pc += op0
  return 12

def add_hl_de(cpu):
  # 0x19
  cpu.regs.hl = add_word(cpu, cpu.regs.hl, cpu.regs.de)
  return 8

def ld_a_de(cpu):
  # 0x1a
  val = cpu.read(cpu.regs.de)
  cpu.regs.a = val
  return 8

def dec_de(cpu):
  # 0x1b
  cpu.regs.de -= 1
  return 8

def inc_e(cpu):
  # 0x1c
  cpu.regs.e = inc_byte(cpu, cpu.regs.e)
  logging.debug(f'inc e ({cpu.regs.e})')
  return 4

def dec_e(cpu):
  # 0x1d
  cpu.regs.e = dec_byte(cpu, cpu.regs.e)
  return 4

def ld_e_d8(cpu):
  # 0x1e
  op0 = cpu.fetch_byte()
  cpu.regs.e = op0
  return 8

def rra(cpu):
  # 0x1f
  cpu.regs.a = rr(cpu, cpu.regs.a)
  return 4

def jr_nz_r8(cpu):
  # 0x20
  op0 = signed(cpu.fetch_byte())
  logging.debug(f'jr nz {op0}')
  if not cpu.regs.f_z:
    cpu.regs.pc += op0
    return 12
  else:
    return 8

def ld_hl_d16(cpu):
  # 0x21
  op0 = cpu.fetch_word()
  cpu.regs.hl = op0
  logging.debug(f'ld hl {hex(op0)}')
  return 12

def ld_hlp_a(cpu):
  # 0x22
  cpu.write(cpu.regs.hl, cpu.regs.a)
  cpu.regs.hl += 1
  return 8

def inc_hl(cpu):
  # 0x23
  cpu.regs.hl += 1
  return 8

def inc_h(cpu):
  # 0x24
  cpu.regs.h = inc_byte(cpu, cpu.regs.h)
  return 4

def dec_h(cpu):
  # 0x25
  cpu.regs.h = dec_byte(cpu, cpu.regs.h)
  return 4

def ld_h_d8(cpu):
  # 0x26
  op0 = cpu.fetch_byte()
  cpu.regs.h = op0
  return 8

def daa(cpu):
  # 0x27
  # adapted from https://github.com/CTurt/Cinoop/blob/master/source/cpu.c
  val = cpu.regs.a
  if cpu.regs.f_n:
    if cpu.regs.f_h:
      val = (val - 6) & 0xff
    if cpu.regs.f_c:
      val -= 0x60
  else:
    if cpu.regs.f_h or (val & 0xf) > 9:
      val += 6
    if cpu.regs.f_c or val > 0x9f:
      val += 0x60
  z = 1 if val == 0 else 0
  c = 1 if val > 0x100 else 0
  cpu.regs.a = val
  cpu.regs.flags(z, None, 0, c)
  return 4

def jr_z_r8(cpu):
  # 0x28
  op0 = signed(cpu.fetch_byte())
  if cpu.regs.f_z:
    cpu.regs.pc += op0
    return 12
  else:
    return 8

def add_hl_hl(cpu):
  # 0x29
  cpu.regs.hl = add_word(cpu, cpu.regs.hl, cpu.regs.hl)
  return 8

def ld_a_hlp(cpu):
  # 0x2a
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = val
  cpu.regs.hl += 1
  logging.debug(f'ld a, (hl+)')
  return 8

def dec_hl(cpu):
  # 0x2b
  cpu.regs.hl -= 1
  return 8

def inc_l(cpu):
  # 0x2c
  cpu.regs.h = inc_byte(cpu, cpu.regs.h)
  return 4

def dec_l(cpu):
  # 0x2d
  cpu.regs.l = dec_byte(cpu, cpu.regs.l)
  return 4

def ld_l_d8(cpu):
  # 0x2e
  op0 = cpu.fetch_byte()
  cpu.regs.l = op0
  return 8

def cpl(cpu):
  # 0x2f
  cpu.regs.a = cpu.regs.a ^ 0xff
  cpu.regs.flags(None, 1, 1, None)
  return 4

def jr_nc_r8(cpu):
  # 0x30
  op0 = signed(cpu.fetch_byte())
  if not cpu.regs.f_c:
    cpu.regs.pc += op0
    return 12
  else:
    return 8

def ld_sp_d16(cpu):
  # 0x31
  op0 = cpu.fetch_word()
  cpu.regs.sp = op0
  return 12

def ld_hlm_a(cpu):
  # 0x32
  cpu.write(cpu.regs.hl, cpu.regs.a)
  cpu.regs.hl -= 1
  return 8

def inc_sp(cpu):
  # 0x33
  cpu.regs.sp += 1
  return 8

def inc_hlp(cpu):
  # 0x34
  val = cpu.read(cpu.regs.hl)
  val = inc_byte(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 12

def dec_hlp(cpu):
  # 0x35
  val = cpu.read(cpu.regs.hl)
  val = dec_byte(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 12

def ld_hl_d8(cpu):
  # 0x36
  op0 = cpu.fetch_byte()
  cpu.write(cpu.regs.hl, op0)
  return 12

def scf(cpu):
  # 0x37
  cpu.regs.flags(None, 0, 0, 1)
  return 4

def jr_c_r8(cpu):
  # 0x38
  op0 = signed(cpu.fetch_byte())
  if cpu.regs.f_c:
    cpu.regs.pc += op0
    return 12
  else:
    return 8

def add_hl_sp(cpu):
  # 0x39
  cpu.regs.hl = add_word(cpu, cpu.regs.hl, cpu.regs.sp)
  return 8

def ld_a_hlm(cpu):
  # 0x3a
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = val
  cpu.regs.hl -= 1
  return 8

def dec_sp(cpu):
  # 0x3b
  cpu.regs.sp -= 1
  return 8

def inc_a(cpu):
  # 0x3c
  cpu.regs.a = inc_byte(cpu, cpu.regs.a)
  return 4

def dec_a(cpu):
  # 0x3d
  cpu.regs.a = dec_byte(cpu, cpu.regs.a)
  return 4

def ld_a_d8(cpu):
  # 0x3e
  op0 = cpu.fetch_byte()
  cpu.regs.a = op0
  return 8

def ccf(cpu):
  # 0x3f
  c = cpu.regs.f_c ^ 1
  cpu.regs.flags(None, 0, 0, c)
  return 4

def ld_b_b(cpu):
  # 0x40
  cpu.regs.b = cpu.regs.b
  return 4

def ld_b_c(cpu):
  # 0x41
  cpu.regs.b = cpu.regs.c
  return 4

def ld_b_d(cpu):
  # 0x42
  cpu.regs.b = cpu.regs.d
  return 4

def ld_b_e(cpu):
  # 0x43
  cpu.regs.b = cpu.regs.e
  return 4

def ld_b_h(cpu):
  # 0x44
  cpu.regs.b = cpu.regs.h
  return 4

def ld_b_l(cpu):
  # 0x45
  cpu.regs.b = cpu.regs.l
  return 4

def ld_b_hl(cpu):
  # 0x46
  cpu.regs.b = cpu.read(cpu.regs.hl)
  return 8

def ld_b_a(cpu):
  # 0x47
  cpu.regs.b = cpu.regs.a
  logging.debug(f'ld b a')
  return 4

def ld_c_b(cpu):
  # 0x48
  cpu.regs.c = cpu.regs.b
  return 4

def ld_c_c(cpu):
  # 0x49
  cpu.regs.c = cpu.regs.c
  return 4

def ld_c_d(cpu):
  # 0x4a
  cpu.regs.c = cpu.regs.d
  return 4

def ld_c_e(cpu):
  # 0x4b
  cpu.regs.c = cpu.regs.e
  return 4

def ld_c_h(cpu):
  # 0x4c
  cpu.regs.c = cpu.regs.h
  return 4

def ld_c_l(cpu):
  # 0x4d
  cpu.regs.c = cpu.regs.l
  return 4

def ld_c_hl(cpu):
  # 0x4e
  cpu.regs.c = cpu.read(cpu.regs.hl)
  return 8

def ld_c_a(cpu):
  # 0x4f
  cpu.regs.c = cpu.regs.a
  return 4

def ld_d_b(cpu):
  # 0x50
  cpu.regs.d = cpu.regs.b
  return 4

def ld_d_c(cpu):
  # 0x51
  cpu.regs.d = cpu.regs.c
  return 4

def ld_d_d(cpu):
  # 0x52
  cpu.regs.d = cpu.regs.d
  return 4

def ld_d_e(cpu):
  # 0x53
  cpu.regs.d = cpu.regs.e
  return 4

def ld_d_h(cpu):
  # 0x54
  cpu.regs.d = cpu.regs.h
  return 4

def ld_d_l(cpu):
  # 0x55
  cpu.regs.d = cpu.regs.l
  return 4

def ld_d_hl(cpu):
  # 0x56
  cpu.regs.d = cpu.read(cpu.regs.hl)
  return 8

def ld_d_a(cpu):
  # 0x57
  cpu.regs.d = cpu.regs.a
  return 4

def ld_e_b(cpu):
  # 0x58
  cpu.regs.e = cpu.regs.b
  return 4

def ld_e_c(cpu):
  # 0x59
  cpu.regs.e = cpu.regs.c
  return 4

def ld_e_d(cpu):
  # 0x5a
  cpu.regs.e = cpu.regs.d
  return 4

def ld_e_e(cpu):
  # 0x5b
  cpu.regs.e = cpu.regs.e
  return 4

def ld_e_h(cpu):
  # 0x5c
  cpu.regs.e = cpu.regs.h
  return 4

def ld_e_l(cpu):
  # 0x5d
  cpu.regs.e = cpu.regs.l
  return 4

def ld_e_hl(cpu):
  # 0x5e
  cpu.regs.e = cpu.read(cpu.regs.hl)
  return 8

def ld_e_a(cpu):
  # 0x5f
  cpu.regs.e = cpu.regs.a
  return 4

def ld_h_b(cpu):
  # 0x60
  cpu.regs.h = cpu.regs.b
  return 4

def ld_h_c(cpu):
  # 0x61
  cpu.regs.h = cpu.regs.c
  return 4

def ld_h_d(cpu):
  # 0x62
  cpu.regs.h = cpu.regs.d
  return 4

def ld_h_e(cpu):
  # 0x63
  cpu.regs.h = cpu.regs.e
  return 4

def ld_h_h(cpu):
  # 0x64
  cpu.regs.h = cpu.regs.h
  return 4

def ld_h_l(cpu):
  # 0x65
  cpu.regs.h = cpu.regs.l
  return 4

def ld_h_hl(cpu):
  # 0x66
  cpu.regs.h = cpu.read(cpu.regs.hl)
  return 8

def ld_h_a(cpu):
  # 0x67
  cpu.regs.h = cpu.regs.a
  return 4

def ld_l_b(cpu):
  # 0x68
  cpu.regs.l = cpu.regs.b
  return 4

def ld_l_c(cpu):
  # 0x69
  cpu.regs.l = cpu.regs.c
  return 4

def ld_l_d(cpu):
  # 0x6a
  cpu.regs.l = cpu.regs.d
  return 4

def ld_l_e(cpu):
  # 0x6b
  cpu.regs.l = cpu.regs.e
  return 4

def ld_l_h(cpu):
  # 0x6c
  cpu.regs.l = cpu.regs.h
  return 4

def ld_l_l(cpu):
  # 0x6d
  cpu.regs.l = cpu.regs.l
  return 4

def ld_l_hl(cpu):
  # 0x6e
  cpu.regs.l = cpu.read(cpu.regs.hl)
  return 8

def ld_l_a(cpu):
  # 0x6f
  cpu.regs.l = cpu.regs.a
  return 4

def ld_hl_b(cpu):
  # 0x70
  cpu.write(cpu.regs.hl, cpu.regs.b)
  return 8

def ld_hl_c(cpu):
  # 0x71
  cpu.write(cpu.regs.hl, cpu.regs.c)
  return 8

def ld_hl_d(cpu):
  # 0x72
  cpu.write(cpu.regs.hl, cpu.regs.d)
  return 8

def ld_hl_e(cpu):
  # 0x73
  cpu.write(cpu.regs.hl, cpu.regs.e)
  return 8

def ld_hl_h(cpu):
  # 0x74
  cpu.write(cpu.regs.hl, cpu.regs.h)
  return 8

def ld_hl_l(cpu):
  # 0x75
  cpu.write(cpu.regs.hl, cpu.regs.l)
  return 8

def halt(cpu):
  # 0x76
  cpu.halted = True
  return 4

def ld_hl_a(cpu):
  # 0x77
  cpu.write(cpu.regs.hl, cpu.regs.a)
  return 8

def ld_a_b(cpu):
  # 0x78
  cpu.regs.a = cpu.regs.b
  return 4

def ld_a_c(cpu):
  # 0x79
  cpu.regs.a = cpu.regs.c
  return 4

def ld_a_d(cpu):
  # 0x7a
  cpu.regs.a = cpu.regs.d
  return 4

def ld_a_e(cpu):
  # 0x7b
  cpu.regs.a = cpu.regs.e
  return 4

def ld_a_h(cpu):
  # 0x7c
  cpu.regs.a = cpu.regs.h
  return 4

def ld_a_l(cpu):
  # 0x7d
  cpu.regs.a = cpu.regs.l
  return 4

def ld_a_hl(cpu):
  # 0x7e
  cpu.regs.a = cpu.read(cpu.regs.hl)
  return 8

def ld_a_a(cpu):
  # 0x7f
  cpu.regs.a = cpu.regs.a
  return 4

def add_a_b(cpu):
  # 0x80
  cpu.regs.a = add(cpu, cpu.regs.a, cpu.regs.b)
  return 4

def add_a_c(cpu):
  # 0x81
  cpu.regs.a = add(cpu, cpu.regs.a, cpu.regs.c)
  return 4

def add_a_d(cpu):
  # 0x82
  cpu.regs.a = add(cpu, cpu.regs.a, cpu.regs.d)
  return 4

def add_a_e(cpu):
  # 0x83
  cpu.regs.a = add(cpu, cpu.regs.a, cpu.regs.e)
  return 4

def add_a_h(cpu):
  # 0x84
  cpu.regs.a = add(cpu, cpu.regs.a, cpu.regs.h)
  return 4

def add_a_l(cpu):
  # 0x85
  cpu.regs.a = add(cpu, cpu.regs.a, cpu.regs.l)
  return 4

def add_a_hl(cpu):
  # 0x86
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = add(cpu, cpu.regs.a, val)
  return 8

def add_a_a(cpu):
  # 0x87
  cpu.regs.a = add(cpu, cpu.regs.a, cpu.regs.a)
  return 4

def adc_a_b(cpu):
  # 0x88
  cpu.regs.a = adc(cpu, cpu.regs.a, cpu.regs.b)
  return 4

def adc_a_c(cpu):
  # 0x89
  cpu.regs.a = adc(cpu, cpu.regs.a, cpu.regs.c)
  return 4

def adc_a_d(cpu):
  # 0x8a
  cpu.regs.a = adc(cpu, cpu.regs.a, cpu.regs.d)
  return 4

def adc_a_e(cpu):
  # 0x8b
  cpu.regs.a = adc(cpu, cpu.regs.a, cpu.regs.e)
  return 4

def adc_a_h(cpu):
  # 0x8c
  cpu.regs.a = adc(cpu, cpu.regs.a, cpu.regs.h)
  return 4

def adc_a_l(cpu):
  # 0x8d
  cpu.regs.a = adc(cpu, cpu.regs.a, cpu.regs.l)
  return 4

def adc_a_hl(cpu):
  # 0x8e
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = adc(cpu, cpu.regs.a, val)
  return 8

def adc_a_a(cpu):
  # 0x8f
  cpu.regs.a = adc(cpu, cpu.regs.a, cpu.regs.a)
  return 4

def sub_b(cpu):
  # 0x90
  cpu.regs.a = sub(cpu, cpu.regs.a, cpu.regs.b)
  return 4

def sub_c(cpu):
  # 0x91
  cpu.regs.a = sub(cpu, cpu.regs.a, cpu.regs.c)
  return 4

def sub_d(cpu):
  # 0x92
  cpu.regs.a = sub(cpu, cpu.regs.a, cpu.regs.d)
  return 4

def sub_e(cpu):
  # 0x93
  cpu.regs.a = sub(cpu, cpu.regs.a, cpu.regs.e)
  return 4

def sub_h(cpu):
  # 0x94
  cpu.regs.a = sub(cpu, cpu.regs.a, cpu.regs.h)
  return 4

def sub_l(cpu):
  # 0x95
  cpu.regs.a = sub(cpu, cpu.regs.a, cpu.regs.l)
  return 4

def sub_hl(cpu):
  # 0x96
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = sub(cpu, cpu.regs.a, val)
  return 8

def sub_a(cpu):
  # 0x97
  cpu.regs.a = sub(cpu, cpu.regs.a, cpu.regs.a)
  return 4

def sbc_a_b(cpu):
  # 0x98
  cpu.regs.a = sbc(cpu, cpu.regs.a, cpu.regs.b)
  return 4

def sbc_a_c(cpu):
  # 0x99
  cpu.regs.a = sbc(cpu, cpu.regs.a, cpu.regs.c)
  return 4

def sbc_a_d(cpu):
  # 0x9a
  cpu.regs.a = sbc(cpu, cpu.regs.a, cpu.regs.d)
  return 4

def sbc_a_e(cpu):
  # 0x9b
  cpu.regs.a = sbc(cpu, cpu.regs.a, cpu.regs.e)
  return 4

def sbc_a_h(cpu):
  # 0x9c
  cpu.regs.a = sbc(cpu, cpu.regs.a, cpu.regs.h)
  return 4

def sbc_a_l(cpu):
  # 0x9d
  cpu.regs.a = sbc(cpu, cpu.regs.a, cpu.regs.l)
  return 4

def sbc_a_hl(cpu):
  # 0x9e
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = sbc(cpu, cpu.regs.a, val)
  return 8

def sbc_a_a(cpu):
  # 0x9f
  cpu.regs.a = sbc(cpu, cpu.regs.a, cpu.regs.a)
  return 4

def and_b(cpu):
  # 0xa0
  cpu.regs.a = and_op(cpu, cpu.regs.a, cpu.regs.b)
  return 4

def and_c(cpu):
  # 0xa1
  cpu.regs.a = and_op(cpu, cpu.regs.a, cpu.regs.c)
  return 4

def and_d(cpu):
  # 0xa2
  cpu.regs.a = and_op(cpu, cpu.regs.a, cpu.regs.d)
  return 4

def and_e(cpu):
  # 0xa3
  cpu.regs.a = and_op(cpu, cpu.regs.a, cpu.regs.e)
  return 4

def and_h(cpu):
  # 0xa4
  cpu.regs.a = and_op(cpu, cpu.regs.a, cpu.regs.h)
  return 4

def and_l(cpu):
  # 0xa5
  cpu.regs.a = and_op(cpu, cpu.regs.a, cpu.regs.l)
  return 4

def and_hl(cpu):
  # 0xa6
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = and_op(cpu, cpu.regs.a, val)
  return 8

def and_a(cpu):
  # 0xa7
  cpu.regs.a = and_op(cpu, cpu.regs.a, cpu.regs.a)
  return 4

def xor_b(cpu):
  # 0xa8
  cpu.regs.a = xor_op(cpu, cpu.regs.a, cpu.regs.b)
  return 4

def xor_c(cpu):
  # 0xa9
  cpu.regs.a = xor_op(cpu, cpu.regs.a, cpu.regs.c)
  return 4

def xor_d(cpu):
  # 0xaa
  cpu.regs.a = xor_op(cpu, cpu.regs.a, cpu.regs.d)
  return 4

def xor_e(cpu):
  # 0xab
  cpu.regs.a = xor_op(cpu, cpu.regs.a, cpu.regs.e)
  return 4

def xor_h(cpu):
  # 0xac
  cpu.regs.a = xor_op(cpu, cpu.regs.a, cpu.regs.h)
  return 4

def xor_l(cpu):
  # 0xad
  cpu.regs.a = xor_op(cpu, cpu.regs.a, cpu.regs.l)
  return 4

def xor_hl(cpu):
  # 0xae
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = xor_op(cpu, cpu.regs.a, val)
  return 8

def xor_a(cpu):
  # 0xaf
  cpu.regs.a = xor_op(cpu, cpu.regs.a, cpu.regs.a)
  return 4

def or_b(cpu):
  # 0xb0
  cpu.regs.a = or_op(cpu, cpu.regs.a, cpu.regs.b)
  return 4

def or_c(cpu):
  # 0xb1
  cpu.regs.a = or_op(cpu, cpu.regs.a, cpu.regs.c)
  return 4

def or_d(cpu):
  # 0xb2
  cpu.regs.a = or_op(cpu, cpu.regs.a, cpu.regs.d)
  return 4

def or_e(cpu):
  # 0xb3
  cpu.regs.a = or_op(cpu, cpu.regs.a, cpu.regs.e)
  return 4

def or_h(cpu):
  # 0xb4
  cpu.regs.a = or_op(cpu, cpu.regs.a, cpu.regs.h)
  return 4

def or_l(cpu):
  # 0xb5
  cpu.regs.a = or_op(cpu, cpu.regs.a, cpu.regs.l)
  return 4

def or_hl(cpu):
  # 0xb6
  val = cpu.read(cpu.regs.hl)
  cpu.regs.a = or_op(cpu, cpu.regs.a, val)
  return 8

def or_a(cpu):
  # 0xb7
  cpu.regs.a = or_op(cpu, cpu.regs.a, cpu.regs.a)
  return 4

def cp_b(cpu):
  # 0xb8
  cp_op(cpu, cpu.regs.a, cpu.regs.b)
  return 4

def cp_c(cpu):
  # 0xb9
  cp_op(cpu, cpu.regs.a, cpu.regs.c)
  return 4

def cp_d(cpu):
  # 0xba
  cp_op(cpu, cpu.regs.a, cpu.regs.d)
  return 4

def cp_e(cpu):
  # 0xbb
  cp_op(cpu, cpu.regs.a, cpu.regs.e)
  return 4

def cp_h(cpu):
  # 0xbc
  cp_op(cpu, cpu.regs.a, cpu.regs.h)
  return 4

def cp_l(cpu):
  # 0xbd
  cp_op(cpu, cpu.regs.a, cpu.regs.lb)
  return 4

def cp_hl(cpu):
  # 0xbe
  val = cpu.read(cpu.regs.hl)
  cp_op(cpu, cpu.regs.a, val)
  return 8

def cp_a(cpu):
  # 0xbf
  cp_op(cpu, cpu.regs.a, cpu.regs.a)
  return 4

def ret_nz(cpu):
  # 0xc0
  if not cpu.regs.f_z:
    val = cpu.read(cpu.regs.sp)
    cpu.regs.pc = val
    cpu.regs.sp += 2
    return 20
  else:
    return 8

def pop_bc(cpu):
  # 0xc1
  val = cpu.read_word(cpu.regs.sp)
  cpu.regs.bc = val
  cpu.regs.sp += 2
  return 12

def jp_nz_a16(cpu):
  # 0xc2
  op0 = cpu.fetch_word()
  if not cpu.regs.f_z:
    cpu.regs.pc = op0
    return 16
  else:
    return 12


def jp_a16(cpu):
  # 0xc3
  op0 = cpu.fetch_word()
  cpu.regs.pc = op0
  logging.debug(f'jp {hex(op0)}')
  return 16

def call_nz_a16(cpu):
  # 0xc4
  op0 = cpu.fetch_word()
  if not cpu.regs.f_z:
    cpu.regs.sp -= 2
    cpu.write_word(cpu.regs.sp, cpu.regs.pc)
    cpu.regs.pc = op0
    return 24
  else:
    return 12

def push_bc(cpu):
  # 0xc5
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.bc)
  return 16

def add_a_d8(cpu):
  # 0xc6
  op0 = cpu.fetch_byte()
  cpu.regs.a = add(cpu, cpu.regs.a, op0)
  return 8

def rst_00h(cpu):
  # 0xc7
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = 0x00
  return 16

def ret_z(cpu):
  # 0xc8
  if cpu.regs.f_z:
    val = cpu.read(cpu.regs.sp)
    cpu.regs.pc = val
    cpu.regs.sp += 2
    return 20
  else:
    return 8

def ret(cpu):
  # 0xc9
  val = cpu.read(cpu.regs.sp)
  cpu.regs.pc = val
  cpu.regs.sp += 2
  return 16

def jp_z_a16(cpu):
  # 0xca
  op0 = cpu.fetch_word()
  if cpu.regs.f_z:
    cpu.regs.pc = op0
    return 16
  else:
    return 12

def prefix_cb(cpu):
  # 0xcb
  opcode = cpu.fetch_byte()
  return instructions_cb[opcode](cpu)

def call_z_a16(cpu):
  # 0xcc
  op0 = cpu.fetch_word()
  if cpu.regs.f_z:
    cpu.regs.sp -= 2
    cpu.write_word(cpu.regs.sp, cpu.regs.pc)
    cpu.regs.pc = op0
    return 24
  else:
    return 12

def call_a16(cpu):
  # 0xcd
  op0 = cpu.fetch_word()
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = op0
  return 24

def adc_a_d8(cpu):
  # 0xce
  op0 = cpu.fetch_byte()
  cpu.regs.a = adc(cpu, cpu.regs.a, op0)
  return 8

def rst_08h(cpu):
  # 0xcf
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = 0x08
  return 16

def ret_nc(cpu):
  # 0xd0
  if not cpu.regs.f_c:
    val = cpu.read(cpu.regs.sp)
    cpu.regs.pc = val
    cpu.regs.sp += 2
    return 20
  else:
    return 8

def pop_de(cpu):
  # 0xd1
  val = cpu.read_word(cpu.regs.sp)
  cpu.regs.de = val
  cpu.regs.sp += 2
  return 12

def jp_nc_a16(cpu):
  # 0xd2
  op0 = cpu.fetch_word()
  if not cpu.regs.f_c:
    cpu.regs.pc = op0
    return 16
  else:
    return 12

def op_0xd3(cpu):
  # 0xd3
  nodef(cpu)
  return 0

def call_nc_a16(cpu):
  # 0xd4
  op0 = cpu.fetch_word()
  if not cpu.regs.f_c:
    cpu.regs.sp -= 2
    cpu.write_word(cpu.regs.sp, cpu.regs.pc)
    cpu.regs.pc = op0
    return 24
  else:
    return 12

def push_de(cpu):
  # 0xd5
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.de)
  return 16

def sub_d8(cpu):
  # 0xd6
  op0 = cpu.fetch_byte()
  cpu.regs.a = sub(cpu, cpu.regs.a, op0)
  return 8

def rst_10h(cpu):
  # 0xd7
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = 0x10
  return 16

def ret_c(cpu):
  # 0xd8
  if cpu.regs.f_c:
    val = cpu.read(cpu.regs.sp)
    cpu.regs.pc = val
    cpu.regs.sp += 2
    return 20
  else:
    return 8

def reti(cpu):
  # 0xd9
  val = cpu.read(cpu.regs.sp)
  cpu.regs.pc = val
  cpu.regs.sp += 2
  cpu.int_master_enable = True
  return 16

def jp_c_a16(cpu):
  # 0xda
  op0 = cpu.fetch_word()
  if cpu.regs.f_c:
    cpu.regs.pc = op0
    return 16
  else:
    return 12

def op_0xdb(cpu):
  # 0xdb
  nodef(cpu)
  return 0

def call_c_a16(cpu):
  # 0xdc
  op0 = cpu.fetch_word()
  if cpu.regs.f_c:
    cpu.regs.sp -= 2
    cpu.write_word(cpu.regs.sp, cpu.regs.pc)
    cpu.regs.pc = op0
    return 24
  else:
    return 12

def op_0xdd(cpu):
  # 0xdd
  nodef(cpu)
  return 0

def sbc_a_d8(cpu):
  # 0xde
  op0 = cpu.fetch_byte()
  cpu.regs.a = sbc(cpu, cpu.regs.a, op0)
  return 8

def rst_18h(cpu):
  # 0xdf
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = 0x18
  return 16

def ldh_a8_a(cpu):
  # 0xe0
  op0 = 0xff00 + cpu.fetch_byte()
  cpu.write(op0, cpu.regs.a)
  return 12

def pop_hl(cpu):
  # 0xe1
  val = cpu.read_word(cpu.regs.sp)
  cpu.regs.hl = val
  cpu.regs.sp += 2
  return 12

def ld_c_a(cpu):
  # 0xe2
  val = 0xff00 + cpu.regs.c
  cpu.write(val, cpu.regs.a)
  cpu.pc += 1
  return 8

def op_0xe3(cpu):
  # 0xe3
  nodef(cpu)
  return 0

def op_0xe4(cpu):
  # 0xe4
  nodef(cpu)
  return 0

def push_hl(cpu):
  # 0xe5
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.hl)
  return 16

def and_d8(cpu):
  # 0xe6
  op0 = cpu.fetch_byte()
  cpu.regs.a = and_op(cpu, cpu.regs.a, op0)
  return 8

def rst_20h(cpu):
  # 0xe7
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = 0x20
  return 16

def add_sp_r8(cpu):
  # 0xe8
  val = signed(signed(cpu.fetch_byte()))
  cpu.regs.sp = add_word(cpu.regs.sp, val)
  return 16

def jp_hl(cpu):
  # 0xe9
  cpu.regs.pc = cpu.regs.hl
  return 4

def ld_a16_a(cpu):
  # 0xea
  op0 = cpu.fetch_word()
  cpu.write(op0, cpu.regs.a)
  return 16

def op_0xeb(cpu):
  # 0xeb
  nodef(cpu)
  return 0

def op_0xec(cpu):
  # 0xec
  nodef(cpu)
  return 0

def op_0xed(cpu):
  # 0xed
  nodef(cpu)
  return 0

def xor_d8(cpu):
  # 0xee
  op0 = cpu.fetch_byte()
  cpu.regs.a = xor_op(cpu, cpu.regs.a, op0)
  return 8

def rst_28h(cpu):
  # 0xef
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = 0x28
  return 16

def ldh_a_a8(cpu):
  # 0xf0
  op0 = 0xff00 + cpu.fetch_byte()
  cpu.write(cpu.regs.a, op0)
  return 12

def pop_af(cpu):
  # 0xf1
  val = cpu.read_word(cpu.regs.sp)
  cpu.regs.af = val
  cpu.regs.sp += 2
  return 12

def ld_a_c(cpu):
  # 0xf2
  val = 0xff00 + cpu.regs.c
  cpu.write(cpu.regs.a, val)
  cpu.pc += 1
  return 8

def di(cpu):
  # 0xf3
  cpu.int_master_enable = False
  return 4

def op_0xf4(cpu):
  # 0xf4
  nodef(cpu)
  return 0

def push_af(cpu):
  # 0xf5
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.af)
  return 16

def or_d8(cpu):
  # 0xf6
  op0 = cpu.fetch_byte()
  cpu.regs.a = or_op(cpu, cpu.regs.a, op0)
  return 8

def rst_30h(cpu):
  # 0xf7
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = 0x30
  return 16

def ld_hl_spr8(cpu):
  # 0xf8
  val = signed(cpu.fetch_byte())
  cpu.regs.hl = add_word(cpu.regs.sp, val)
  return 12


def ld_sp_hl(cpu):
  # 0xf9
  cpu.regs.sp = cpu.regs.hl
  return 8

def ld_a_a16(cpu):
  # 0xfa
  op0 = cpu.fetch_word()
  cpu.write(cpu.regs.a, op0)
  return 16

def ei(cpu):
  # 0xfb
  cpu.int_master_enable = True
  return 4

def op_0xfc(cpu):
  # 0xfc
  nodef(cpu)
  return 0

def op_0xfd(cpu):
  # 0xfd
  nodef(cpu)
  return 0

def cp_d8(cpu):
  # 0xfe
  op0 = cpu.fetch_byte()
  cp_op(cpu, cpu.regs.a, op0)
  return 8

def rst_38h(cpu):
  # 0xff
  cpu.regs.sp -= 2
  cpu.write_word(cpu.regs.sp, cpu.regs.pc)
  cpu.regs.pc = 0x38
  return 16

def rlc_b(cpu):
  # cb 0x00
  cpu.regs.b = rlc(cpu, cpu.regs.b)
  return 8

def rlc_c(cpu):
  # cb 0x01
  cpu.regs.c = rlc(cpu, cpu.regs.c)
  return 8

def rlc_d(cpu):
  # cb 0x02
  cpu.regs.d = rlc(cpu, cpu.regs.d)
  return 8

def rlc_e(cpu):
  # cb 0x03
  cpu.regs.e = rlc(cpu, cpu.regs.e)
  return 8

def rlc_h(cpu):
  # cb 0x04
  cpu.regs.h = rlc(cpu, cpu.regs.h)
  return 8

def rlc_l(cpu):
  # cb 0x05
  cpu.regs.l = rlc(cpu, cpu.regs.l)
  return 8

def rlc_hl(cpu):
  # cb 0x06
  val = cpu.read(cpu.regs.hl)
  val = rlc(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def rlc_a(cpu):
  # cb 0x07
  cpu.regs.a = rlc(cpu, cpu.regs.a)
  return 8

def rrc_b(cpu):
  # cb 0x08
  cpu.regs.b = rrc(cpu, cpu.regs.b)
  return 8

def rrc_c(cpu):
  # cb 0x09
  cpu.regs.c = rrc(cpu, cpu.regs.c)
  return 8

def rrc_d(cpu):
  # cb 0x0a
  cpu.regs.d = rrc(cpu, cpu.regs.d)
  return 8

def rrc_e(cpu):
  # cb 0x0b
  cpu.regs.e = rrc(cpu, cpu.regs.e)
  return 8

def rrc_h(cpu):
  # cb 0x0c
  cpu.regs.h = rrc(cpu, cpu.regs.h)
  return 8

def rrc_l(cpu):
  # cb 0x0d
  cpu.regs.l = rrc(cpu, cpu.regs.l)
  return 8

def rrc_hl(cpu):
  # cb 0x0e
  val = cpu.read(cpu.regs.hl)
  val = rrc(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def rrc_a(cpu):
  # cb 0x0f
  cpu.regs.a = rrc(cpu, cpu.regs.a)
  return 8

def rl_b(cpu):
  # cb 0x10
  cpu.regs.b = rl(cpu, cpu.regs.b)
  return 8

def rl_c(cpu):
  # cb 0x11
  cpu.regs.c = rl(cpu, cpu.regs.c)
  return 8

def rl_d(cpu):
  # cb 0x12
  cpu.regs.d = rl(cpu, cpu.regs.d)
  return 8

def rl_e(cpu):
  # cb 0x13
  cpu.regs.e = rl(cpu, cpu.regs.e)
  return 8

def rl_h(cpu):
  # cb 0x14
  cpu.regs.h = rl(cpu, cpu.regs.h)
  return 8

def rl_l(cpu):
  # cb 0x15
  cpu.regs.l = rl(cpu, cpu.regs.l)
  return 8

def rl_hl(cpu):
  # cb 0x16
  val = cpu.read(cpu.regs.hl)
  val = rl(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def rl_a(cpu):
  # cb 0x17
  cpu.regs.a = rl(cpu, cpu.regs.a)
  return 8

def rr_b(cpu):
  # cb 0x18
  cpu.regs.b = rr(cpu, cpu.regs.b)
  return 8

def rr_c(cpu):
  # cb 0x19
  cpu.regs.c = rr(cpu, cpu.regs.c)
  return 8

def rr_d(cpu):
  # cb 0x1a
  cpu.regs.d = rr(cpu, cpu.regs.d)
  return 8

def rr_e(cpu):
  # cb 0x1b
  cpu.regs.e = rr(cpu, cpu.regs.e)
  return 8

def rr_h(cpu):
  # cb 0x1c
  cpu.regs.h = rr(cpu, cpu.regs.h)
  return 8

def rr_l(cpu):
  # cb 0x1d
  cpu.regs.l = rr(cpu, cpu.regs.l)
  return 8

def rr_hl(cpu):
  # cb 0x1e
  val = cpu.read(cpu.regs.hl)
  val = rr(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def rr_a(cpu):
  # cb 0x1f
  cpu.regs.a = rr(cpu, cpu.regs.a)
  return 8

def sla_b(cpu):
  # cb 0x20
  cpu.regs.b = sla(cpu, cpu.regs.b)
  return 8

def sla_c(cpu):
  # cb 0x21
  cpu.regs.c = sla(cpu, cpu.regs.c)
  return 8

def sla_d(cpu):
  # cb 0x22
  cpu.regs.d = sla(cpu, cpu.regs.d)
  return 8

def sla_e(cpu):
  # cb 0x23
  cpu.regs.e = sla(cpu, cpu.regs.e)
  return 8

def sla_h(cpu):
  # cb 0x24
  cpu.regs.h = sla(cpu, cpu.regs.h)
  return 8

def sla_l(cpu):
  # cb 0x25
  cpu.regs.l = sla(cpu, cpu.regs.l)
  return 8

def sla_hl(cpu):
  # cb 0x26
  val = cpu.read(cpu.regs.hl)
  val = sla(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def sla_a(cpu):
  # cb 0x27
  cpu.regs.a = sla(cpu, cpu.regs.a)
  return 8

def sra_b(cpu):
  # cb 0x28
  cpu.regs.b = sra(cpu, cpu.regs.b)
  return 8

def sra_c(cpu):
  # cb 0x29
  cpu.regs.c = sra(cpu, cpu.regs.c)
  return 8

def sra_d(cpu):
  # cb 0x2a
  cpu.regs.d = sra(cpu, cpu.regs.d)
  return 8

def sra_e(cpu):
  # cb 0x2b
  cpu.regs.e = sra(cpu, cpu.regs.e)
  return 8

def sra_h(cpu):
  # cb 0x2c
  cpu.regs.h = sra(cpu, cpu.regs.h)
  return 8

def sra_l(cpu):
  # cb 0x2d
  cpu.regs.l = sra(cpu, cpu.regs.l)
  return 8

def sra_hl(cpu):
  # cb 0x2e
  val = cpu.read(cpu.regs.hl)
  val = sra(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def sra_a(cpu):
  # cb 0x2f
  cpu.regs.a = sra(cpu, cpu.regs.a)
  return 8

def swap_b(cpu):
  # cb 0x30
  cpu.regs.b = swap(cpu, cpu.regs.b)
  return 8

def swap_c(cpu):
  # cb 0x31
  cpu.regs.c = swap(cpu, cpu.regs.c)
  return 8

def swap_d(cpu):
  # cb 0x32
  cpu.regs.d = swap(cpu, cpu.regs.d)
  return 8

def swap_e(cpu):
  # cb 0x33
  cpu.regs.e = swap(cpu, cpu.regs.e)
  return 8

def swap_h(cpu):
  # cb 0x34
  cpu.regs.h = swap(cpu, cpu.regs.h)
  return 8

def swap_l(cpu):
  # cb 0x35
  cpu.regs.l = swap(cpu, cpu.regs.l)
  return 8

def swap_hl(cpu):
  # cb 0x36
  val = cpu.read(cpu.regs.hl)
  val = swap(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def swap_a(cpu):
  # cb 0x37
  cpu.regs.a = swap(cpu, cpu.regs.a)
  return 8

def srl_b(cpu):
  # cb 0x38
  cpu.regs.b = srl(cpu, cpu.regs.b)
  return 8

def srl_c(cpu):
  # cb 0x39
  cpu.regs.c = srl(cpu, cpu.regs.c)
  return 8

def srl_d(cpu):
  # cb 0x3a
  cpu.regs.d = srl(cpu, cpu.regs.d)
  return 8

def srl_e(cpu):
  # cb 0x3b
  cpu.regs.e = srl(cpu, cpu.regs.e)
  return 8

def srl_h(cpu):
  # cb 0x3c
  cpu.regs.h = srl(cpu, cpu.regs.h)
  return 8

def srl_l(cpu):
  # cb 0x3d
  cpu.regs.l = srl(cpu, cpu.regs.l)
  return 8

def srl_hl(cpu):
  # cb 0x3e
  val = cpu.read(cpu.regs.hl)
  val = srl(cpu, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def srl_a(cpu):
  # cb 0x3f
  cpu.regs.a = srl(cpu, cpu.regs.a)
  return 8

def bit_0_b(cpu):
  # cb 0x40
  bit_op(cpu, 0, cpu.regs.b)
  return 8

def bit_0_c(cpu):
  # cb 0x41
  bit_op(cpu, 0, cpu.regs.c)
  return 8

def bit_0_d(cpu):
  # cb 0x42
  bit_op(cpu, 0, cpu.regs.d)
  return 8

def bit_0_e(cpu):
  # cb 0x43
  bit_op(cpu, 0, cpu.regs.e)
  return 8

def bit_0_h(cpu):
  # cb 0x44
  bit_op(cpu, 0, cpu.regs.h)
  return 8

def bit_0_l(cpu):
  # cb 0x45
  bit_op(cpu, 0, cpu.regs.l)
  return 8

def bit_0_hl(cpu):
  # cb 0x46
  val = cpu.read(cpu.regs.hl)
  bit_op(cpu, 0, val)
  return 16

def bit_0_a(cpu):
  # cb 0x47
  bit_op(cpu, 0, cpu.regs.a)
  return 8

def bit_1_b(cpu):
  # cb 0x48
  bit_op(cpu, 1, cpu.regs.b)
  return 8

def bit_1_c(cpu):
  # cb 0x49
  bit_op(cpu, 1, cpu.regs.c)
  return 8

def bit_1_d(cpu):
  # cb 0x4a
  bit_op(cpu, 1, cpu.regs.d)
  return 8

def bit_1_e(cpu):
  # cb 0x4b
  bit_op(cpu, 1, cpu.regs.e)
  return 8

def bit_1_h(cpu):
  # cb 0x4c
  bit_op(cpu, 1, cpu.regs.h)
  return 8

def bit_1_l(cpu):
  # cb 0x4d
  bit_op(cpu, 1, cpu.regs.l)
  return 8

def bit_1_hl(cpu):
  # cb 0x4e
  val = cpu.read(cpu.regs.hl)
  bit_op(cpu, 1, val)
  return 16

def bit_1_a(cpu):
  # cb 0x4f
  bit_op(cpu, 1, cpu.regs.a)
  return 8

def bit_2_b(cpu):
  # cb 0x50
  bit_op(cpu, 2, cpu.regs.b)
  return 8

def bit_2_c(cpu):
  # cb 0x51
  bit_op(cpu, 2, cpu.regs.c)
  return 8

def bit_2_d(cpu):
  # cb 0x52
  bit_op(cpu, 2, cpu.regs.d)
  return 8

def bit_2_e(cpu):
  # cb 0x53
  bit_op(cpu, 2, cpu.regs.e)
  return 8

def bit_2_h(cpu):
  # cb 0x54
  bit_op(cpu, 2, cpu.regs.h)
  return 8

def bit_2_l(cpu):
  # cb 0x55
  bit_op(cpu, 2, cpu.regs.l)
  return 8

def bit_2_hl(cpu):
  # cb 0x56
  val = cpu.read(cpu.regs.hl)
  bit_op(cpu, 2, val)
  return 16

def bit_2_a(cpu):
  # cb 0x57
  bit_op(cpu, 2, cpu.regs.a)
  return 8

def bit_3_b(cpu):
  # cb 0x58
  bit_op(cpu, 3, cpu.regs.b)
  return 8

def bit_3_c(cpu):
  # cb 0x59
  bit_op(cpu, 3, cpu.regs.c)
  return 8

def bit_3_d(cpu):
  # cb 0x5a
  bit_op(cpu, 3, cpu.regs.d)
  return 8

def bit_3_e(cpu):
  # cb 0x5b
  bit_op(cpu, 3, cpu.regs.e)
  return 8

def bit_3_h(cpu):
  # cb 0x5c
  bit_op(cpu, 3, cpu.regs.h)
  return 8

def bit_3_l(cpu):
  # cb 0x5d
  bit_op(cpu, 3, cpu.regs.l)
  return 8

def bit_3_hl(cpu):
  # cb 0x5e
  val = cpu.read(cpu.regs.hl)
  bit_op(cpu, 3, val)
  return 16

def bit_3_a(cpu):
  # cb 0x5f
  bit_op(cpu, 3, cpu.regs.a)
  return 8

def bit_4_b(cpu):
  # cb 0x60
  bit_op(cpu, 4, cpu.regs.b)
  return 8

def bit_4_c(cpu):
  # cb 0x61
  bit_op(cpu, 4, cpu.regs.c)
  return 8

def bit_4_d(cpu):
  # cb 0x62
  bit_op(cpu, 4, cpu.regs.d)
  return 8

def bit_4_e(cpu):
  # cb 0x63
  bit_op(cpu, 4, cpu.regs.e)
  return 8

def bit_4_h(cpu):
  # cb 0x64
  bit_op(cpu, 4, cpu.regs.h)
  return 8

def bit_4_l(cpu):
  # cb 0x65
  bit_op(cpu, 4, cpu.regs.l)
  return 8

def bit_4_hl(cpu):
  # cb 0x66
  val = cpu.read(cpu.regs.hl)
  bit_op(cpu, 4, val)
  return 16

def bit_4_a(cpu):
  # cb 0x67
  bit_op(cpu, 4, cpu.regs.a)
  return 8

def bit_5_b(cpu):
  # cb 0x68
  bit_op(cpu, 5, cpu.regs.b)
  return 8

def bit_5_c(cpu):
  # cb 0x69
  bit_op(cpu, 5, cpu.regs.c)
  return 8

def bit_5_d(cpu):
  # cb 0x6a
  bit_op(cpu, 5, cpu.regs.d)
  return 8

def bit_5_e(cpu):
  # cb 0x6b
  bit_op(cpu, 5, cpu.regs.e)
  return 8

def bit_5_h(cpu):
  # cb 0x6c
  bit_op(cpu, 5, cpu.regs.h)
  return 8

def bit_5_l(cpu):
  # cb 0x6d
  bit_op(cpu, 5, cpu.regs.l)
  return 8

def bit_5_hl(cpu):
  # cb 0x6e
  val = cpu.read(cpu.regs.hl)
  bit_op(cpu, 5, val)
  return 16

def bit_5_a(cpu):
  # cb 0x6f
  bit_op(cpu, 5, cpu.regs.a)
  return 8

def bit_6_b(cpu):
  # cb 0x70
  bit_op(cpu, 6, cpu.regs.b)
  return 8

def bit_6_c(cpu):
  # cb 0x71
  bit_op(cpu, 6, cpu.regs.c)
  return 8

def bit_6_d(cpu):
  # cb 0x72
  bit_op(cpu, 6, cpu.regs.d)
  return 8

def bit_6_e(cpu):
  # cb 0x73
  bit_op(cpu, 6, cpu.regs.e)
  return 8

def bit_6_h(cpu):
  # cb 0x74
  bit_op(cpu, 6, cpu.regs.h)
  return 8

def bit_6_l(cpu):
  # cb 0x75
  bit_op(cpu, 6, cpu.regs.l)
  return 8

def bit_6_hl(cpu):
  # cb 0x76
  val = cpu.read(cpu.regs.hl)
  bit_op(cpu, 6, val)
  return 16

def bit_6_a(cpu):
  # cb 0x77
  bit_op(cpu, 6, cpu.regs.a)
  return 8

def bit_7_b(cpu):
  # cb 0x78
  bit_op(cpu, 7, cpu.regs.b)
  return 8

def bit_7_c(cpu):
  # cb 0x79
  bit_op(cpu, 7, cpu.regs.c)
  return 8

def bit_7_d(cpu):
  # cb 0x7a
  bit_op(cpu, 7, cpu.regs.d)
  return 8

def bit_7_e(cpu):
  # cb 0x7b
  bit_op(cpu, 7, cpu.regs.e)
  return 8

def bit_7_h(cpu):
  # cb 0x7c
  bit_op(cpu, 7, cpu.regs.h)
  return 8

def bit_7_l(cpu):
  # cb 0x7d
  bit_op(cpu, 7, cpu.regs.l)
  return 8

def bit_7_hl(cpu):
  # cb 0x7e
  val = cpu.read(cpu.regs.hl)
  bit_op(cpu, 7, val)
  return 16

def bit_7_a(cpu):
  # cb 0x7f
  bit_op(cpu, 7, cpu.regs.a)
  return 8

def res_0_b(cpu):
  # cb 0x80
  cpu.regs.b = res_op(cpu, 0, cpu.regs.b)
  return 8

def res_0_c(cpu):
  # cb 0x81
  cpu.regs.c = res_op(cpu, 0, cpu.regs.c)
  return 8

def res_0_d(cpu):
  # cb 0x82
  cpu.regs.d = res_op(cpu, 0, cpu.regs.d)
  return 8

def res_0_e(cpu):
  # cb 0x83
  cpu.regs.e = res_op(cpu, 0, cpu.regs.e)
  return 8

def res_0_h(cpu):
  # cb 0x84
  cpu.regs.h = res_op(cpu, 0, cpu.regs.h)
  return 8

def res_0_l(cpu):
  # cb 0x85
  cpu.regs.l = res_op(cpu, 0, cpu.regs.l)
  return 8

def res_0_hl(cpu):
  # cb 0x86
  val = cpu.read(cpu.regs.hl)
  val = res_op(cpu, 0, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def res_0_a(cpu):
  # cb 0x87
  cpu.regs.a = res_op(cpu, 0, cpu.regs.a)
  return 8

def res_1_b(cpu):
  # cb 0x88
  cpu.regs.b = res_op(cpu, 1, cpu.regs.b)
  return 8

def res_1_c(cpu):
  # cb 0x89
  cpu.regs.c = res_op(cpu, 1, cpu.regs.c)
  return 8

def res_1_d(cpu):
  # cb 0x8a
  cpu.regs.d = res_op(cpu, 1, cpu.regs.d)
  return 8

def res_1_e(cpu):
  # cb 0x8b
  cpu.regs.e = res_op(cpu, 1, cpu.regs.e)
  return 8

def res_1_h(cpu):
  # cb 0x8c
  cpu.regs.h = res_op(cpu, 1, cpu.regs.h)
  return 8

def res_1_l(cpu):
  # cb 0x8d
  cpu.regs.l = res_op(cpu, 1, cpu.regs.l)
  return 8

def res_1_hl(cpu):
  # cb 0x8e
  val = cpu.read(cpu.regs.hl)
  val = res_op(cpu, 1, val)
  bit_op(cpu, 1, val)
  return 16

def res_1_a(cpu):
  # cb 0x8f
  cpu.regs.a = res_op(cpu, 1, cpu.regs.a)
  return 8

def res_2_b(cpu):
  # cb 0x90
  cpu.regs.b = res_op(cpu, 2, cpu.regs.b)
  return 8

def res_2_c(cpu):
  # cb 0x91
  cpu.regs.c = res_op(cpu, 2, cpu.regs.c)
  return 8

def res_2_d(cpu):
  # cb 0x92
  cpu.regs.d = res_op(cpu, 2, cpu.regs.d)
  return 8

def res_2_e(cpu):
  # cb 0x93
  cpu.regs.e = res_op(cpu, 2, cpu.regs.e)
  return 8

def res_2_h(cpu):
  # cb 0x94
  cpu.regs.h = res_op(cpu, 2, cpu.regs.h)
  return 8

def res_2_l(cpu):
  # cb 0x95
  cpu.regs.l = res_op(cpu, 2, cpu.regs.l)
  return 8

def res_2_hl(cpu):
  # cb 0x96
  val = cpu.read(cpu.regs.hl)
  val = res_op(cpu, 2, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def res_2_a(cpu):
  # cb 0x97
  cpu.regs.a = res_op(cpu, 2, cpu.regs.a)
  return 8

def res_3_b(cpu):
  # cb 0x98
  cpu.regs.b = res_op(cpu, 3, cpu.regs.b)
  return 8

def res_3_c(cpu):
  # cb 0x99
  cpu.regs.c = res_op(cpu, 3, cpu.regs.c)
  return 8

def res_3_d(cpu):
  # cb 0x9a
  cpu.regs.d = res_op(cpu, 3, cpu.regs.d)
  return 8

def res_3_e(cpu):
  # cb 0x9b
  cpu.regs.e = res_op(cpu, 3, cpu.regs.e)
  return 8

def res_3_h(cpu):
  # cb 0x9c
  cpu.regs.h = res_op(cpu, 3, cpu.regs.h)
  return 8

def res_3_l(cpu):
  # cb 0x9d
  cpu.regs.l = res_op(cpu, 3, cpu.regs.l)
  return 8

def res_3_hl(cpu):
  # cb 0x9e
  val = cpu.read(cpu.regs.hl)
  val = res_op(cpu, 3, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def res_3_a(cpu):
  # cb 0x9f
  cpu.regs.a = res_op(cpu, 3, cpu.regs.a)
  return 8

def res_4_b(cpu):
  # cb 0xa0
  cpu.regs.b = res_op(cpu, 4, cpu.regs.b)
  return 8

def res_4_c(cpu):
  # cb 0xa1
  cpu.regs.c = res_op(cpu, 4, cpu.regs.c)
  return 8

def res_4_d(cpu):
  # cb 0xa2
  cpu.regs.d = res_op(cpu, 4, cpu.regs.d)
  return 8

def res_4_e(cpu):
  # cb 0xa3
  cpu.regs.e = res_op(cpu, 4, cpu.regs.e)
  return 8

def res_4_h(cpu):
  # cb 0xa4
  cpu.regs.h = res_op(cpu, 4, cpu.regs.h)
  return 8

def res_4_l(cpu):
  # cb 0xa5
  cpu.regs.l = res_op(cpu, 4, cpu.regs.l)
  return 8

def res_4_hl(cpu):
  # cb 0xa6
  val = cpu.read(cpu.regs.hl)
  val = res_op(cpu, 4, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def res_4_a(cpu):
  # cb 0xa7
  cpu.regs.a = res_op(cpu, 4, cpu.regs.a)
  return 8

def res_5_b(cpu):
  # cb 0xa8
  cpu.regs.b = res_op(cpu, 5, cpu.regs.b)
  return 8

def res_5_c(cpu):
  # cb 0xa9
  cpu.regs.c = res_op(cpu, 5, cpu.regs.c)
  return 8

def res_5_d(cpu):
  # cb 0xaa
  cpu.regs.d = res_op(cpu, 5, cpu.regs.d)
  return 8

def res_5_e(cpu):
  # cb 0xab
  cpu.regs.e = res_op(cpu, 5, cpu.regs.e)
  return 8

def res_5_h(cpu):
  # cb 0xac
  cpu.regs.h = res_op(cpu, 5, cpu.regs.h)
  return 8

def res_5_l(cpu):
  # cb 0xad
  cpu.regs.l = res_op(cpu, 5, cpu.regs.l)
  return 8

def res_5_hl(cpu):
  # cb 0xae
  val = cpu.read(cpu.regs.hl)
  val = res_op(cpu, 5, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def res_5_a(cpu):
  # cb 0xaf
  cpu.regs.a = res_op(cpu, 5, cpu.regs.a)
  return 8

def res_6_b(cpu):
  # cb 0xb0
  cpu.regs.b = res_op(cpu, 6, cpu.regs.b)
  return 8

def res_6_c(cpu):
  # cb 0xb1
  cpu.regs.c = res_op(cpu, 6, cpu.regs.c)
  return 8

def res_6_d(cpu):
  # cb 0xb2
  cpu.regs.d = res_op(cpu, 6, cpu.regs.d)
  return 8

def res_6_e(cpu):
  # cb 0xb3
  cpu.regs.e = res_op(cpu, 6, cpu.regs.e)
  return 8

def res_6_h(cpu):
  # cb 0xb4
  cpu.regs.h = res_op(cpu, 6, cpu.regs.h)
  return 8

def res_6_l(cpu):
  # cb 0xb5
  cpu.regs.l = res_op(cpu, 6, cpu.regs.l)
  return 8

def res_6_hl(cpu):
  # cb 0xb6
  val = cpu.read(cpu.regs.hl)
  val = res_op(cpu, 6, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def res_6_a(cpu):
  # cb 0xb7
  cpu.regs.a = res_op(cpu, 6, cpu.regs.a)
  return 8

def res_7_b(cpu):
  # cb 0xb8
  cpu.regs.b = res_op(cpu, 7, cpu.regs.b)
  return 8

def res_7_c(cpu):
  # cb 0xb9
  cpu.regs.c = res_op(cpu, 7, cpu.regs.c)
  return 8

def res_7_d(cpu):
  # cb 0xba
  cpu.regs.d = res_op(cpu, 7, cpu.regs.d)
  return 8

def res_7_e(cpu):
  # cb 0xbb
  cpu.regs.e = res_op(cpu, 7, cpu.regs.e)
  return 8

def res_7_h(cpu):
  # cb 0xbc
  cpu.regs.h = res_op(cpu, 7, cpu.regs.h)
  return 8

def res_7_l(cpu):
  # cb 0xbd
  cpu.regs.l = res_op(cpu, 7, cpu.regs.l)
  return 8

def res_7_hl(cpu):
  # cb 0xbe
  val = cpu.read(cpu.regs.hl)
  val = res_op(cpu, 7, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def res_7_a(cpu):
  # cb 0xbf
  cpu.regs.a = res_op(cpu, 7, cpu.regs.a)
  return 8

def set_0_b(cpu):
  # cb 0xc0
  cpu.regs.b = set_op(cpu, 0, cpu.regs.b)
  return 8

def set_0_c(cpu):
  # cb 0xc1
  cpu.regs.c = set_op(cpu, 0, cpu.regs.c)
  return 8

def set_0_d(cpu):
  # cb 0xc2
  cpu.regs.d = set_op(cpu, 0, cpu.regs.d)
  return 8

def set_0_e(cpu):
  # cb 0xc3
  cpu.regs.e = set_op(cpu, 0, cpu.regs.e)
  return 8

def set_0_h(cpu):
  # cb 0xc4
  cpu.regs.h = set_op(cpu, 0, cpu.regs.h)
  return 8

def set_0_l(cpu):
  # cb 0xc5
  cpu.regs.l = set_op(cpu, 0, cpu.regs.l)
  return 8

def set_0_hl(cpu):
  # cb 0xc6
  val = cpu.read(cpu.regs.hl)
  val = set_op(cpu, 0, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def set_0_a(cpu):
  # cb 0xc7
  cpu.regs.a = set_op(cpu, 0, cpu.regs.a)
  return 8

def set_1_b(cpu):
  # cb 0xc8
  cpu.regs.b = set_op(cpu, 1, cpu.regs.b)
  return 8

def set_1_c(cpu):
  # cb 0xc9
  cpu.regs.c = set_op(cpu, 1, cpu.regs.c)
  return 8

def set_1_d(cpu):
  # cb 0xca
  cpu.regs.d = set_op(cpu, 1, cpu.regs.d)
  return 8

def set_1_e(cpu):
  # cb 0xcb
  cpu.regs.e = set_op(cpu, 1, cpu.regs.e)
  return 8

def set_1_h(cpu):
  # cb 0xcc
  cpu.regs.h = set_op(cpu, 1, cpu.regs.h)
  return 8

def set_1_l(cpu):
  # cb 0xcd
  cpu.regs.l = set_op(cpu, 1, cpu.regs.l)
  return 8

def set_1_hl(cpu):
  # cb 0xce
  val = cpu.read(cpu.regs.hl)
  val = set_op(cpu, 1, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def set_1_a(cpu):
  # cb 0xcf
  cpu.regs.a = set_op(cpu, 1, cpu.regs.a)
  return 8

def set_2_b(cpu):
  # cb 0xd0
  cpu.regs.b = set_op(cpu, 2, cpu.regs.b)
  return 8

def set_2_c(cpu):
  # cb 0xd1
  cpu.regs.c = set_op(cpu, 2, cpu.regs.c)
  return 8

def set_2_d(cpu):
  # cb 0xd2
  cpu.regs.d = set_op(cpu, 2, cpu.regs.d)
  return 8

def set_2_e(cpu):
  # cb 0xd3
  cpu.regs.e = set_op(cpu, 2, cpu.regs.e)
  return 8

def set_2_h(cpu):
  # cb 0xd4
  cpu.regs.h = set_op(cpu, 2, cpu.regs.h)
  return 8

def set_2_l(cpu):
  # cb 0xd5
  cpu.regs.l = set_op(cpu, 2, cpu.regs.l)
  return 8

def set_2_hl(cpu):
  # cb 0xd6
  val = cpu.read(cpu.regs.hl)
  val = set_op(cpu, 2, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def set_2_a(cpu):
  # cb 0xd7
  cpu.regs.a = set_op(cpu, 2, cpu.regs.a)
  return 8

def set_3_b(cpu):
  # cb 0xd8
  cpu.regs.b = set_op(cpu, 3, cpu.regs.b)
  return 8

def set_3_c(cpu):
  # cb 0xd9
  cpu.regs.c = set_op(cpu, 3, cpu.regs.c)
  return 8

def set_3_d(cpu):
  # cb 0xda
  cpu.regs.d = set_op(cpu, 3, cpu.regs.d)
  return 8

def set_3_e(cpu):
  # cb 0xdb
  cpu.regs.e = set_op(cpu, 3, cpu.regs.e)
  return 8

def set_3_h(cpu):
  # cb 0xdc
  cpu.regs.h = set_op(cpu, 3, cpu.regs.h)
  return 8

def set_3_l(cpu):
  # cb 0xdd
  cpu.regs.l = set_op(cpu, 3, cpu.regs.l)
  return 8

def set_3_hl(cpu):
  # cb 0xde
  val = cpu.read(cpu.regs.hl)
  val = set_op(cpu, 3, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def set_3_a(cpu):
  # cb 0xdf
  cpu.regs.a = set_op(cpu, 3, cpu.regs.a)
  return 8

def set_4_b(cpu):
  # cb 0xe0
  cpu.regs.b = set_op(cpu, 4, cpu.regs.b)
  return 8

def set_4_c(cpu):
  # cb 0xe1
  cpu.regs.c = set_op(cpu, 4, cpu.regs.c)
  return 8

def set_4_d(cpu):
  # cb 0xe2
  cpu.regs.d = set_op(cpu, 4, cpu.regs.d)
  return 8

def set_4_e(cpu):
  # cb 0xe3
  cpu.regs.e = set_op(cpu, 4, cpu.regs.e)
  return 8

def set_4_h(cpu):
  # cb 0xe4
  cpu.regs.h = set_op(cpu, 4, cpu.regs.h)
  return 8

def set_4_l(cpu):
  # cb 0xe5
  cpu.regs.l = set_op(cpu, 4, cpu.regs.l)
  return 8

def set_4_hl(cpu):
  # cb 0xe6
  val = cpu.read(cpu.regs.hl)
  val = set_op(cpu, 4, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def set_4_a(cpu):
  # cb 0xe7
  cpu.regs.a = set_op(cpu, 4, cpu.regs.a)
  return 8

def set_5_b(cpu):
  # cb 0xe8
  cpu.regs.b = set_op(cpu, 5, cpu.regs.b)
  return 8

def set_5_c(cpu):
  # cb 0xe9
  cpu.regs.c = set_op(cpu, 5, cpu.regs.c)
  return 8

def set_5_d(cpu):
  # cb 0xea
  cpu.regs.d = set_op(cpu, 5, cpu.regs.d)
  return 8

def set_5_e(cpu):
  # cb 0xeb
  cpu.regs.e = set_op(cpu, 5, cpu.regs.e)
  return 8

def set_5_h(cpu):
  # cb 0xec
  cpu.regs.h = set_op(cpu, 5, cpu.regs.h)
  return 8

def set_5_l(cpu):
  # cb 0xed
  cpu.regs.l = set_op(cpu, 5, cpu.regs.l)
  return 8

def set_5_hl(cpu):
  # cb 0xee
  val = cpu.read(cpu.regs.hl)
  val = set_op(cpu, 5, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def set_5_a(cpu):
  # cb 0xef
  cpu.regs.a = set_op(cpu, 5, cpu.regs.a)
  return 8

def set_6_b(cpu):
  # cb 0xf0
  cpu.regs.b = set_op(cpu, 6, cpu.regs.b)
  return 8

def set_6_c(cpu):
  # cb 0xf1
  cpu.regs.c = set_op(cpu, 6, cpu.regs.c)
  return 8

def set_6_d(cpu):
  # cb 0xf2
  cpu.regs.d = set_op(cpu, 6, cpu.regs.d)
  return 8

def set_6_e(cpu):
  # cb 0xf3
  cpu.regs.e = set_op(cpu, 6, cpu.regs.e)
  return 8

def set_6_h(cpu):
  # cb 0xf4
  cpu.regs.h = set_op(cpu, 6, cpu.regs.h)
  return 8

def set_6_l(cpu):
  # cb 0xf5
  cpu.regs.l = set_op(cpu, 6, cpu.regs.l)
  return 8

def set_6_hl(cpu):
  # cb 0xf6
  val = cpu.read(cpu.regs.hl)
  val = set_op(cpu, 6, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def set_6_a(cpu):
  # cb 0xf7
  cpu.regs.a = set_op(cpu, 6, cpu.regs.a)
  return 8

def set_7_b(cpu):
  # cb 0xf8
  cpu.regs.b = set_op(cpu, 7, cpu.regs.b)
  return 8

def set_7_c(cpu):
  # cb 0xf9
  cpu.regs.c = set_op(cpu, 7, cpu.regs.c)
  return 8

def set_7_d(cpu):
  # cb 0xfa
  cpu.regs.d = set_op(cpu, 7, cpu.regs.d)
  return 8

def set_7_e(cpu):
  # cb 0xfb
  cpu.regs.e = set_op(cpu, 7, cpu.regs.e)
  return 8

def set_7_h(cpu):
  # cb 0xfc
  cpu.regs.h = set_op(cpu, 7, cpu.regs.h)
  return 8

def set_7_l(cpu):
  # cb 0xfd
  cpu.regs.l = set_op(cpu, 7, cpu.regs.l)
  return 8

def set_7_hl(cpu):
  # cb 0xfe
  val = cpu.read(cpu.regs.hl)
  val = set_op(cpu, 7, val)
  cpu.write(cpu.regs.hl, val)
  return 16

def set_7_a(cpu):
  # cb 0xff
  cpu.regs.a = set_op(cpu, 7, cpu.regs.a)
  return 8

instructions = [
  # 0x0_
  nop,
  ld_bc_d16,
  ld_bc_a,
  inc_bc,
  inc_b,
  dec_b,
  ld_b_d8,
  rlca,
  ld_a16_sp,
  add_hl_bc,
  ld_a_bc,
  dec_bc,
  inc_c,
  dec_c,
  ld_c_d8,
  rrca,
  # 0x1_
  stop_0,
  ld_de_d16,
  ld_de_a,
  inc_de,
  inc_d,
  dec_d,
  ld_d_d8,
  rla,
  jr_r8,
  add_hl_de,
  ld_a_de,
  dec_de,
  inc_e,
  dec_e,
  ld_e_d8,
  rra,
  # 0x2_
  jr_nz_r8,
  ld_hl_d16,
  ld_hlp_a,
  inc_hl,
  inc_h,
  dec_h,
  ld_h_d8,
  daa,
  jr_z_r8,
  add_hl_hl,
  ld_a_hlp,
  dec_hl,
  inc_l,
  dec_l,
  ld_l_d8,
  cpl,
  # 0x3_
  jr_nc_r8,
  ld_sp_d16,
  ld_hlm_a,
  inc_sp,
  inc_hlp,
  dec_hlp,
  ld_hl_d8,
  scf,
  jr_c_r8,
  add_hl_sp,
  ld_a_hlm,
  dec_sp,
  inc_a,
  dec_a,
  ld_a_d8,
  ccf,
  # 0x4_
  ld_b_b,
  ld_b_c,
  ld_b_d,
  ld_b_e,
  ld_b_h,
  ld_b_l,
  ld_b_hl,
  ld_b_a,
  ld_c_b,
  ld_c_c,
  ld_c_d,
  ld_c_e,
  ld_c_h,
  ld_c_l,
  ld_c_hl,
  ld_c_a,
  # 0x5_
  ld_d_b,
  ld_d_c,
  ld_d_d,
  ld_d_e,
  ld_d_h,
  ld_d_l,
  ld_d_hl,
  ld_d_a,
  ld_e_b,
  ld_e_c,
  ld_e_d,
  ld_e_e,
  ld_e_h,
  ld_e_l,
  ld_e_hl,
  ld_e_a,
  # 0x6_
  ld_h_b,
  ld_h_c,
  ld_h_d,
  ld_h_e,
  ld_h_h,
  ld_h_l,
  ld_h_hl,
  ld_h_a,
  ld_l_b,
  ld_l_c,
  ld_l_d,
  ld_l_e,
  ld_l_h,
  ld_l_l,
  ld_l_hl,
  ld_l_a,
  # 0x7_
  ld_hl_b,
  ld_hl_c,
  ld_hl_d,
  ld_hl_e,
  ld_hl_h,
  ld_hl_l,
  halt,
  ld_hl_a,
  ld_a_b,
  ld_a_c,
  ld_a_d,
  ld_a_e,
  ld_a_h,
  ld_a_l,
  ld_a_hl,
  ld_a_a,
  # 0x8_
  add_a_b,
  add_a_c,
  add_a_d,
  add_a_e,
  add_a_h,
  add_a_l,
  add_a_hl,
  add_a_a,
  adc_a_b,
  adc_a_c,
  adc_a_d,
  adc_a_e,
  adc_a_h,
  adc_a_l,
  adc_a_hl,
  adc_a_a,
  # 0x9_
  sub_b,
  sub_c,
  sub_d,
  sub_e,
  sub_h,
  sub_l,
  sub_hl,
  sub_a,
  sbc_a_b,
  sbc_a_c,
  sbc_a_d,
  sbc_a_e,
  sbc_a_h,
  sbc_a_l,
  sbc_a_hl,
  sbc_a_a,
  # 0xa_
  and_b,
  and_c,
  and_d,
  and_e,
  and_h,
  and_l,
  and_hl,
  and_a,
  xor_b,
  xor_c,
  xor_d,
  xor_e,
  xor_h,
  xor_l,
  xor_hl,
  xor_a,
  # 0xb_
  or_b,
  or_c,
  or_d,
  or_e,
  or_h,
  or_l,
  or_hl,
  or_a,
  cp_b,
  cp_c,
  cp_d,
  cp_e,
  cp_h,
  cp_l,
  cp_hl,
  cp_a,
  # 0xc_
  ret_nz,
  pop_bc,
  jp_nz_a16,
  jp_a16,
  call_nz_a16,
  push_bc,
  add_a_d8,
  rst_00h,
  ret_z,
  ret,
  jp_z_a16,
  prefix_cb,
  call_z_a16,
  call_a16,
  adc_a_d8,
  rst_08h,
  # 0xd_
  ret_nc,
  pop_de,
  jp_nc_a16,
  op_0xd3,
  call_nc_a16,
  push_de,
  sub_d8,
  rst_10h,
  ret_c,
  reti,
  jp_c_a16,
  op_0xdb,
  call_c_a16,
  op_0xdd,
  sbc_a_d8,
  rst_18h,
  # 0xe_
  ldh_a8_a,
  pop_hl,
  ld_c_a,
  op_0xe3,
  op_0xe4,
  push_hl,
  and_d8,
  rst_20h,
  add_sp_r8,
  jp_hl,
  ld_a16_a,
  op_0xeb,
  op_0xec,
  op_0xed,
  xor_d8,
  rst_28h,
  # 0xf_
  ldh_a_a8,
  pop_af,
  ld_a_c,
  di,
  op_0xf4,
  push_af,
  or_d8,
  rst_30h,
  ld_hl_spr8,
  ld_sp_hl,
  ld_a_a16,
  ei,
  op_0xfc,
  op_0xfd,
  cp_d8,
  rst_38h,
]

instructions_cb = [
  # cb 0x0_
  rlc_b,
  rlc_c,
  rlc_d,
  rlc_e,
  rlc_h,
  rlc_l,
  rlc_hl,
  rlc_a,
  rrc_b,
  rrc_c,
  rrc_d,
  rrc_e,
  rrc_h,
  rrc_l,
  rrc_hl,
  rrc_a,
  # cb 0x1_
  rl_b,
  rl_c,
  rl_d,
  rl_e,
  rl_h,
  rl_l,
  rl_hl,
  rl_a,
  rr_b,
  rr_c,
  rr_d,
  rr_e,
  rr_h,
  rr_l,
  rr_hl,
  rr_a,
  # cb 0x2_
  sla_b,
  sla_c,
  sla_d,
  sla_e,
  sla_h,
  sla_l,
  sla_hl,
  sla_a,
  sra_b,
  sra_c,
  sra_d,
  sra_e,
  sra_h,
  sra_l,
  sra_hl,
  sra_a,
  # cb 0x3_
  swap_b,
  swap_c,
  swap_d,
  swap_e,
  swap_h,
  swap_l,
  swap_hl,
  swap_a,
  srl_b,
  srl_c,
  srl_d,
  srl_e,
  srl_h,
  srl_l,
  srl_hl,
  srl_a,
  # cb 0x4_
  bit_0_b,
  bit_0_c,
  bit_0_d,
  bit_0_e,
  bit_0_h,
  bit_0_l,
  bit_0_hl,
  bit_0_a,
  bit_1_b,
  bit_1_c,
  bit_1_d,
  bit_1_e,
  bit_1_h,
  bit_1_l,
  bit_1_hl,
  bit_1_a,
  # cb 0x5_
  bit_2_b,
  bit_2_c,
  bit_2_d,
  bit_2_e,
  bit_2_h,
  bit_2_l,
  bit_2_hl,
  bit_2_a,
  bit_3_b,
  bit_3_c,
  bit_3_d,
  bit_3_e,
  bit_3_h,
  bit_3_l,
  bit_3_hl,
  bit_3_a,
  # cb 0x6_
  bit_4_b,
  bit_4_c,
  bit_4_d,
  bit_4_e,
  bit_4_h,
  bit_4_l,
  bit_4_hl,
  bit_4_a,
  bit_5_b,
  bit_5_c,
  bit_5_d,
  bit_5_e,
  bit_5_h,
  bit_5_l,
  bit_5_hl,
  bit_5_a,
  # cb 0x7_
  bit_6_b,
  bit_6_c,
  bit_6_d,
  bit_6_e,
  bit_6_h,
  bit_6_l,
  bit_6_hl,
  bit_6_a,
  bit_7_b,
  bit_7_c,
  bit_7_d,
  bit_7_e,
  bit_7_h,
  bit_7_l,
  bit_7_hl,
  bit_7_a,
  # cb 0x8_
  res_0_b,
  res_0_c,
  res_0_d,
  res_0_e,
  res_0_h,
  res_0_l,
  res_0_hl,
  res_0_a,
  res_1_b,
  res_1_c,
  res_1_d,
  res_1_e,
  res_1_h,
  res_1_l,
  res_1_hl,
  res_1_a,
  # cb 0x9_
  res_2_b,
  res_2_c,
  res_2_d,
  res_2_e,
  res_2_h,
  res_2_l,
  res_2_hl,
  res_2_a,
  res_3_b,
  res_3_c,
  res_3_d,
  res_3_e,
  res_3_h,
  res_3_l,
  res_3_hl,
  res_3_a,
  # cb 0xa_
  res_4_b,
  res_4_c,
  res_4_d,
  res_4_e,
  res_4_h,
  res_4_l,
  res_4_hl,
  res_4_a,
  res_5_b,
  res_5_c,
  res_5_d,
  res_5_e,
  res_5_h,
  res_5_l,
  res_5_hl,
  res_5_a,
  # cb 0xb_
  res_6_b,
  res_6_c,
  res_6_d,
  res_6_e,
  res_6_h,
  res_6_l,
  res_6_hl,
  res_6_a,
  res_7_b,
  res_7_c,
  res_7_d,
  res_7_e,
  res_7_h,
  res_7_l,
  res_7_hl,
  res_7_a,
  # cb 0xc_
  set_0_b,
  set_0_c,
  set_0_d,
  set_0_e,
  set_0_h,
  set_0_l,
  set_0_hl,
  set_0_a,
  set_1_b,
  set_1_c,
  set_1_d,
  set_1_e,
  set_1_h,
  set_1_l,
  set_1_hl,
  set_1_a,
  # cb 0xd_
  set_2_b,
  set_2_c,
  set_2_d,
  set_2_e,
  set_2_h,
  set_2_l,
  set_2_hl,
  set_2_a,
  set_3_b,
  set_3_c,
  set_3_d,
  set_3_e,
  set_3_h,
  set_3_l,
  set_3_hl,
  set_3_a,
  # cb 0xe_
  set_4_b,
  set_4_c,
  set_4_d,
  set_4_e,
  set_4_h,
  set_4_l,
  set_4_hl,
  set_4_a,
  set_5_b,
  set_5_c,
  set_5_d,
  set_5_e,
  set_5_h,
  set_5_l,
  set_5_hl,
  set_5_a,
  # cb 0xf_
  set_6_b,
  set_6_c,
  set_6_d,
  set_6_e,
  set_6_h,
  set_6_l,
  set_6_hl,
  set_6_a,
  set_7_b,
  set_7_c,
  set_7_d,
  set_7_e,
  set_7_h,
  set_7_l,
  set_7_hl,
  set_7_a
]