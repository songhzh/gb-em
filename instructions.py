def signed(byte):
	return int.from_bytes(byte, byteorder='little', signed=True)

def inc_byte(cpu, val):
	z = 1 if val + 1 == 0 else 0
	h = 1 if val & 0xf == 0xf else 0
	cpu.flags(z, 0, h, None)
	return val + 1

def dec_byte(cpu, val):
	z = 1 if val + 1 == 0 else 0
	h = 0 if val & 0xf else 1
	cpu.flags(z, 1, h, None)
	return val + 1

def add_word(cpu, val0, val1):
	res = val0 + val1
	h = 1 if (val0 & 0xfff) + (val1 & 0xfff) > 0xfff else 0
	c = 1 if res > 0xffff else 0
	cpu.flags(None, 0, h, c)
	return res

def rlc(cpu, val):
	c = 1 if val & 0x80 else 0
	res = (val << 1) | c
	cpu.flags(0, 0, 0, c)
	return res

def rl(cpu, val):
	c = 1 if val & 0x80 else 0
	res = (val << 1) | (cpu.regs.f_c)
	cpu.flags(0, 0, 0, c)
	return res

def rrc(cpu, val):
	c = val & 1
	res = (val >> 1) | (c << 7)
	cpu.flags(0, 0, 0, c)
	return res

def rr(cpu, val):
	c = val & 1
	res = (val >> 1) | (cpu.regs.f_c << 7)
	cpu.flags(0, 0, 0, c)
	return res

def add(cpu, val0, val1):
	res = val0 + val1
	z = res == 0
	h = 1 if (val0 & 0xf) + (val1 & 0xf) > 0xf else 0
	c = 1 if res > 0xff else 0
	cpu.flags(z, 0, h, c)
	return res

def adc(cpu, val0, val1):
	res = val0 + val1 + cpu.regs.f_c
	z = res == 0
	h = 1 if (val0 & 0xf) + (val1 & 0xf) + cpu.regs.f_c > 0xf else 0
	c = 1 if res > 0xff else 0
	cpu.flags(z, 0, h, c)
	return res

def sub(cpu, val0, val1):
	res = val0 - val1
	z = res == 0
	h = 1 if (val0 & 0xf) - (val1 & 0xf) < 0 else 0
	c = 1 if res < 0 else 0
	cpu.flags(z, 1, h, c)
	return res

def sbc(cpu, val0, val1):
	res = val0 - val1 - cpu.regs.f_c
	z = res == 0
	h = 1 if (val0 & 0xf) - (val1 & 0xf) - cpu.regs.f_c < 0 else 0
	c = 1 if res < 0 else 0
	cpu.flags(z, 1, h, c)
	return res

def and_op(cpu, val0, val1):
	res = val0 & val1
	z = res == 0
	cpu.flags(z, 0, 1, 0)
	return res

def xor_op(cpu, val0, val1):
	res = val0 ^ val1
	z = res == 0
	cpu.flags(z, 0, 0, 0)
	return res

def or_op(cpu, val0, val1):
	res = val0 | val1
	z = res == 0
	cpu.flags(z, 0, 0, 0)
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
	return 8

def rrca(cpu):
	# 0x0f
	cpu.regs.a = rrc(cpu, cpu.regs.a)
	return 4

def stop_0(cpu):
	# 0x10
	pass

def ld_de_d16(cpu):
	# 0x11
	op0 = cpu.fetch_word()
	cpu.regs.de = op0
	return 12

def ld_de_a(cpu):
	# 0x12
	cpu.write(cpu.regs.de, cpu.regs.a)
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
	if not cpu.regs.f_z:
		cpu.regs.pc += op0
		return 12
	else:
		return 8

def ld_hl_d16(cpu):
	# 0x21
	op0 = cpu.fetch_word()
	cpu.regs.hl = op0
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
	pass

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
	cpu.flags(None, 1, 1, None)
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
	pass

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
	pass

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
	pass

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
	pass

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
	pass

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
	pass

def pop_hl(cpu):
	# 0xe1
	val = cpu.read_word(cpu.regs.sp)
	cpu.regs.hl = val
	cpu.regs.sp += 2
	return 12

def ld_c_a(cpu):
	# 0xe2
	cpu.write(cpu.regs.c, cpu.regs.a)
	cpu.regs.pc += 1
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
	pass

def pop_af(cpu):
	# 0xf1
	val = cpu.read_word(cpu.regs.sp)
	cpu.regs.af = val
	cpu.regs.sp += 2
	return 12

def ld_a_c(cpu):
	# 0xf2
	val = cpu.read(cpu.regs.c)
	cpu.regs.a = val
	cpu.regs.pc += 1
	return 8

def di(cpu):
	# 0xf3
	pass

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
	pass

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