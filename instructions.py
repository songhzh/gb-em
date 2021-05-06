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

def nodef():
  # illegal instruction
  pass

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
	cpu.bus_write(cpu.regs.bc, cpu.regs.a)
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
	cpu.write_mem(op0, cpu.regs.sp)
	return 20

def add_hl_bc(cpu):
	# 0x09
	cpu.regs.hl = add_word(cpu, cpu.regs.hl, cpu.regs.bc)
	return 8

def ld_a_bc(cpu):
	# 0x0a
	val = cpu.read_mem(cpu.regs.bc)
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
	cpu.bus_write(cpu.regs.de, cpu.regs.a)
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
	op0 = cpu.fetch_byte()
	cpu.regs.pc += signed(op0)
	return 12

def add_hl_de(cpu):
	# 0x19
	cpu.regs.hl = add_word(cpu, cpu.regs.hl, cpu.regs.de)
	return 8

def ld_a_de(cpu):
	# 0x1a
	val = cpu.read_mem(cpu.regs.de)
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
	op0 = cpu.fetch_byte()
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
	cpu.bus_write(cpu.regs.hl, cpu.regs.a)
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
	op0 = cpu.fetch_byte()
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
	val = cpu.read_mem(cpu.regs.hl)
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
	op0 = cpu.fetch_byte()
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
	cpu.bus_write(cpu.regs.hl, cpu.regs.a)
	cpu.regs.hl -= 1
	return 8

def inc_sp(cpu):
	# 0x33
	cpu.regs.sp += 1
	return 8

def inc_hlp(cpu):
	# 0x34
	val = cpu.bus_read(cpu.regs.hl)
	val = inc_byte(cpu, val)
	cpu.bus_write(cpu.regs.hl, val)
	return 12

def dec_hlp(cpu):
	# 0x35
	val = cpu.bus_read(cpu.regs.hl)
	val = dec_byte(cpu, val)
	cpu.bus_write(cpu.regs.hl, val)
	return 12

def ld_hl_d8(cpu):
	# 0x36
	op0 = cpu.fetch_byte()
	cpu.bus_write(cpu.regs.hl, op0)
	return 12

def scf(cpu):
	# 0x37
	pass

def jr_c_r8(cpu):
	# 0x38
	op0 = cpu.fetch_byte()
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
	val = cpu.read_mem(cpu.regs.hl)
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
	pass

def ld_b_c(cpu):
	# 0x41
	pass

def ld_b_d(cpu):
	# 0x42
	pass

def ld_b_e(cpu):
	# 0x43
	pass

def ld_b_h(cpu):
	# 0x44
	pass

def ld_b_l(cpu):
	# 0x45
	pass

def ld_b_hl(cpu):
	# 0x46
	pass

def ld_b_a(cpu):
	# 0x47
	pass

def ld_c_b(cpu):
	# 0x48
	pass

def ld_c_c(cpu):
	# 0x49
	pass

def ld_c_d(cpu):
	# 0x4a
	pass

def ld_c_e(cpu):
	# 0x4b
	pass

def ld_c_h(cpu):
	# 0x4c
	pass

def ld_c_l(cpu):
	# 0x4d
	pass

def ld_c_hl(cpu):
	# 0x4e
	pass

def ld_c_a(cpu):
	# 0x4f
	pass

def ld_d_b(cpu):
	# 0x50
	pass

def ld_d_c(cpu):
	# 0x51
	pass

def ld_d_d(cpu):
	# 0x52
	pass

def ld_d_e(cpu):
	# 0x53
	pass

def ld_d_h(cpu):
	# 0x54
	pass

def ld_d_l(cpu):
	# 0x55
	pass

def ld_d_hl(cpu):
	# 0x56
	pass

def ld_d_a(cpu):
	# 0x57
	pass

def ld_e_b(cpu):
	# 0x58
	pass

def ld_e_c(cpu):
	# 0x59
	pass

def ld_e_d(cpu):
	# 0x5a
	pass

def ld_e_e(cpu):
	# 0x5b
	pass

def ld_e_h(cpu):
	# 0x5c
	pass

def ld_e_l(cpu):
	# 0x5d
	pass

def ld_e_hl(cpu):
	# 0x5e
	pass

def ld_e_a(cpu):
	# 0x5f
	pass

def ld_h_b(cpu):
	# 0x60
	pass

def ld_h_c(cpu):
	# 0x61
	pass

def ld_h_d(cpu):
	# 0x62
	pass

def ld_h_e(cpu):
	# 0x63
	pass

def ld_h_h(cpu):
	# 0x64
	pass

def ld_h_l(cpu):
	# 0x65
	pass

def ld_h_hl(cpu):
	# 0x66
	pass

def ld_h_a(cpu):
	# 0x67
	pass

def ld_l_b(cpu):
	# 0x68
	pass

def ld_l_c(cpu):
	# 0x69
	pass

def ld_l_d(cpu):
	# 0x6a
	pass

def ld_l_e(cpu):
	# 0x6b
	pass

def ld_l_h(cpu):
	# 0x6c
	pass

def ld_l_l(cpu):
	# 0x6d
	pass

def ld_l_hl(cpu):
	# 0x6e
	pass

def ld_l_a(cpu):
	# 0x6f
	pass

def ld_hl_b(cpu):
	# 0x70
	pass

def ld_hl_c(cpu):
	# 0x71
	pass

def ld_hl_d(cpu):
	# 0x72
	pass

def ld_hl_e(cpu):
	# 0x73
	pass

def ld_hl_h(cpu):
	# 0x74
	pass

def ld_hl_l(cpu):
	# 0x75
	pass

def halt(cpu):
	# 0x76
	pass

def ld_hl_a(cpu):
	# 0x77
	pass

def ld_a_b(cpu):
	# 0x78
	pass

def ld_a_c(cpu):
	# 0x79
	pass

def ld_a_d(cpu):
	# 0x7a
	pass

def ld_a_e(cpu):
	# 0x7b
	pass

def ld_a_h(cpu):
	# 0x7c
	pass

def ld_a_l(cpu):
	# 0x7d
	pass

def ld_a_hl(cpu):
	# 0x7e
	pass

def ld_a_a(cpu):
	# 0x7f
	pass

def add_a_b(cpu):
	# 0x80
	pass

def add_a_c(cpu):
	# 0x81
	pass

def add_a_d(cpu):
	# 0x82
	pass

def add_a_e(cpu):
	# 0x83
	pass

def add_a_h(cpu):
	# 0x84
	pass

def add_a_l(cpu):
	# 0x85
	pass

def add_a_hl(cpu):
	# 0x86
	pass

def add_a_a(cpu):
	# 0x87
	pass

def adc_a_b(cpu):
	# 0x88
	pass

def adc_a_c(cpu):
	# 0x89
	pass

def adc_a_d(cpu):
	# 0x8a
	pass

def adc_a_e(cpu):
	# 0x8b
	pass

def adc_a_h(cpu):
	# 0x8c
	pass

def adc_a_l(cpu):
	# 0x8d
	pass

def adc_a_hl(cpu):
	# 0x8e
	pass

def adc_a_a(cpu):
	# 0x8f
	pass

def sub_b(cpu):
	# 0x90
	pass

def sub_c(cpu):
	# 0x91
	pass

def sub_d(cpu):
	# 0x92
	pass

def sub_e(cpu):
	# 0x93
	pass

def sub_h(cpu):
	# 0x94
	pass

def sub_l(cpu):
	# 0x95
	pass

def sub_hl(cpu):
	# 0x96
	pass

def sub_a(cpu):
	# 0x97
	pass

def sbc_a_b(cpu):
	# 0x98
	pass

def sbc_a_c(cpu):
	# 0x99
	pass

def sbc_a_d(cpu):
	# 0x9a
	pass

def sbc_a_e(cpu):
	# 0x9b
	pass

def sbc_a_h(cpu):
	# 0x9c
	pass

def sbc_a_l(cpu):
	# 0x9d
	pass

def sbc_a_hl(cpu):
	# 0x9e
	pass

def sbc_a_a(cpu):
	# 0x9f
	pass

def and_b(cpu):
	# 0xa0
	pass

def and_c(cpu):
	# 0xa1
	pass

def and_d(cpu):
	# 0xa2
	pass

def and_e(cpu):
	# 0xa3
	pass

def and_h(cpu):
	# 0xa4
	pass

def and_l(cpu):
	# 0xa5
	pass

def and_hl(cpu):
	# 0xa6
	pass

def and_a(cpu):
	# 0xa7
	pass

def xor_b(cpu):
	# 0xa8
	pass

def xor_c(cpu):
	# 0xa9
	pass

def xor_d(cpu):
	# 0xaa
	pass

def xor_e(cpu):
	# 0xab
	pass

def xor_h(cpu):
	# 0xac
	pass

def xor_l(cpu):
	# 0xad
	pass

def xor_hl(cpu):
	# 0xae
	pass

def xor_a(cpu):
	# 0xaf
	pass

def or_b(cpu):
	# 0xb0
	pass

def or_c(cpu):
	# 0xb1
	pass

def or_d(cpu):
	# 0xb2
	pass

def or_e(cpu):
	# 0xb3
	pass

def or_h(cpu):
	# 0xb4
	pass

def or_l(cpu):
	# 0xb5
	pass

def or_hl(cpu):
	# 0xb6
	pass

def or_a(cpu):
	# 0xb7
	pass

def cp_b(cpu):
	# 0xb8
	pass

def cp_c(cpu):
	# 0xb9
	pass

def cp_d(cpu):
	# 0xba
	pass

def cp_e(cpu):
	# 0xbb
	pass

def cp_h(cpu):
	# 0xbc
	pass

def cp_l(cpu):
	# 0xbd
	pass

def cp_hl(cpu):
	# 0xbe
	pass

def cp_a(cpu):
	# 0xbf
	pass

def ret_nz(cpu):
	# 0xc0
	pass

def pop_bc(cpu):
	# 0xc1
	pass

def jp_nz_a16(cpu):
	# 0xc2
	pass

def jp_a16(cpu):
	# 0xc3
	pass

def call_nz_a16(cpu):
	# 0xc4
	pass

def push_bc(cpu):
	# 0xc5
	pass

def add_a_d8(cpu):
	# 0xc6
	pass

def rst_00h(cpu):
	# 0xc7
	pass

def ret_z(cpu):
	# 0xc8
	pass

def ret(cpu):
	# 0xc9
	pass

def jp_z_a16(cpu):
	# 0xca
	pass

def prefix_cb(cpu):
	# 0xcb
	pass

def call_z_a16(cpu):
	# 0xcc
	pass

def call_a16(cpu):
	# 0xcd
	pass

def adc_a_d8(cpu):
	# 0xce
	pass

def rst_08h(cpu):
	# 0xcf
	pass

def ret_nc(cpu):
	# 0xd0
	pass

def pop_de(cpu):
	# 0xd1
	pass

def jp_nc_a16(cpu):
	# 0xd2
	pass

def op_0xd3(cpu):
	# 0xd3
	pass

def call_nc_a16(cpu):
	# 0xd4
	pass

def push_de(cpu):
	# 0xd5
	pass

def sub_d8(cpu):
	# 0xd6
	pass

def rst_10h(cpu):
	# 0xd7
	pass

def ret_c(cpu):
	# 0xd8
	pass

def reti(cpu):
	# 0xd9
	pass

def jp_c_a16(cpu):
	# 0xda
	pass

def op_0xdb(cpu):
	# 0xdb
	pass

def call_c_a16(cpu):
	# 0xdc
	pass

def op_0xdd(cpu):
	# 0xdd
	pass

def sbc_a_d8(cpu):
	# 0xde
	pass

def rst_18h(cpu):
	# 0xdf
	pass

def ldh_a8_a(cpu):
	# 0xe0
	pass

def pop_hl(cpu):
	# 0xe1
	pass

def ld_c_a(cpu):
	# 0xe2
	pass

def op_0xe3(cpu):
	# 0xe3
	pass

def op_0xe4(cpu):
	# 0xe4
	pass

def push_hl(cpu):
	# 0xe5
	pass

def and_d8(cpu):
	# 0xe6
	pass

def rst_20h(cpu):
	# 0xe7
	pass

def add_sp_r8(cpu):
	# 0xe8
	pass

def jp_hl(cpu):
	# 0xe9
	pass

def ld_a16_a(cpu):
	# 0xea
	pass

def op_0xeb(cpu):
	# 0xeb
	pass

def op_0xec(cpu):
	# 0xec
	pass

def op_0xed(cpu):
	# 0xed
	pass

def xor_d8(cpu):
	# 0xee
	pass

def rst_28h(cpu):
	# 0xef
	pass

def ldh_a_a8(cpu):
	# 0xf0
	pass

def pop_af(cpu):
	# 0xf1
	pass

def ld_a_c(cpu):
	# 0xf2
	pass

def di(cpu):
	# 0xf3
	pass

def op_0xf4(cpu):
	# 0xf4
	pass

def push_af(cpu):
	# 0xf5
	pass

def or_d8(cpu):
	# 0xf6
	pass

def rst_30h(cpu):
	# 0xf7
	pass

def ld_hl_spr8(cpu):
	# 0xf8
	pass

def ld_sp_hl(cpu):
	# 0xf9
	pass

def ld_a_a16(cpu):
	# 0xfa
	pass

def ei(cpu):
	# 0xfb
	pass

def op_0xfc(cpu):
	# 0xfc
	pass

def op_0xfd(cpu):
	# 0xfd
	pass

def cp_d8(cpu):
	# 0xfe
	pass

def rst_38h(cpu):
	# 0xff
	pass

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