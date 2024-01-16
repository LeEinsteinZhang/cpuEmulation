from cpu import *

c1 = CPU() # initial
c1.mem.cells[32].write([1, 0, 1, 1, 0, 0, 1, 1])              # set 32 cells
address = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]    # pre define a address use 16-bit list
address_31 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1] # pre define a address use 16-bit list
c1.reg_w('A', [0, 0, 0, 0, 0, 0, 0, 1])                        # set reg A value

#mov lda test
c1.mov('B', 'A')
c1.lda(address)

print(c1.reg_r('B') == [0, 0, 0, 0, 0, 0, 0, 1])
print(c1.reg_r('A') == [1, 0, 1, 1, 0, 0, 1, 1])

#sta test
c1.reg_w('A', [1, 0, 0, 0, 0, 0, 0, 0])
c1.sta(address_31)
print(c1.mem.cells[31].read() == [1, 0, 0, 0, 0, 0, 0, 0])

#add test
c1.reg_w('A', c1.int_to_bits_8b(1))
c1.reg_w('B', c1.int_to_bits_8b(1))
c1.add('B')
print(c1.reg_r('A') == c1.int_to_bits_8b(2))

#adi test
c1.adi(c1.int_to_bits_8b(16))
print(c1.reg_r('A') == c1.int_to_bits_8b(18))

#lhld shld
address_128 = c1.int_to_bits_16b(128)
address_129 = c1.int_to_bits_16b(129)

address_256 = c1.int_to_bits_16b(256)
address_257 = c1.int_to_bits_16b(257)

val_255 = c1.int_to_bits_8b(255)

c1.mem.io(1, address_128, [0, 0, 0, 0, 0, 0, 0, 1])
c1.mem.io(1, address_129, val_255)

c1.lhld(address_128)
print(c1.reg_r('HL') == c1.int_to_bits_16b(511))
c1.shld(address_256)
print(c1.mem.cells[256].read() == c1.mem.cells[128].read())
print(c1.mem.cells[257].read() == c1.mem.cells[129].read())

#ldax test
c1.reg_w('BC', address_256)
c1.ldax('BC')
print(c1.reg_r('A') == c1.mem.cells[256].read())

#sdax test
address_512 = c1.int_to_bits_16b(512)
c1.reg_w('DE', address_512)
c1.stax('DE')
print(c1.reg_r('A') == c1.mem.cells[512].read())

#xchg test
old_de = c1.reg_r('DE')
old_hl = c1.reg_r('HL')
c1.xchg()
print(c1.reg_r('DE') == old_hl)
print(c1.reg_r('HL') == old_de)

# def adc(self, S):
    

# def aci(self, I):
    

#sub test
c1.reg_w('A', c1.int_to_bits_8b(2))
c1.reg_w('B', c1.int_to_bits_8b(1))
c1.sub('B')
print(c1.reg_r('A') == c1.int_to_bits_8b(1))

#sui test
c1.reg_w('A', c1.int_to_bits_8b(129))
c1.sui(1)
print(c1.reg_r('A') == c1.int_to_bits_8b(128))

# def sbb(self, S):
    

# def sbi(self, I):
    

# def inr(self, D):
    

# def dcr(self, D):
    

# def inx(self, RP):
    

# def dcx(self, RP):
    

# def dad(self, RP):
    

# def daa(self):
    

# def ana(self, S):
    

# def ani(self, I):
    

#ora test
c1.reg_w('A', [1,0,1,0,1,0,1,0])
c1.reg_w('B', [0,1,0,1,0,1,0,1])
c1.ora('B')
print(c1.reg_r('A') == [1,1,1,1,1,1,1,1])

# def adc(self, S):
#     pass

# def aci(self, I):
#     pass

# def sub(self, S):
#     pass

# def sui(self, I):
#     pass

# def sbb(self, S):
#     pass

# def sbi(self, I):
#     pass

# def inr(self, D):
#     pass

# def dcr(self, D):
#     pass

#inx test
c1.reg_w('DE', c1.int_to_bits_16b(1))
c1.inx('DE')
print(c1.reg_r('DE') == c1.int_to_bits_16b(2))