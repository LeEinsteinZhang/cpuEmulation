from memory import *

# D   = Destination register (8 bit)
# S   = Source register (8 bit)
# RP  = Register pair (16 bit)
# I   = 8 or 16 bit immediate operand
# addr   = 16 bit Memory address
# port   = 8 bit port address
# ccc = Conditional

# 8-bit CPU 8080 like

EXIT_SUCESS = 1
EXIT_FAIL = 0
EXIT_ERROR = -1

class CPU:
    def __init__(self) -> None:
        self.port = [0] * 40
        self.mem = Memory()
        self.reg = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 0  F:[0...7] A:[8...15]   16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 1  C:[0...7] B:[8...15]   16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 2  E:[0...7] D:[8...15]   16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 3  L:[0...7] H:[8...15]   16-bits
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # <- 4  SP:[0...15]            16-bits
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # <- 5  PC:[0...15]            16-bits
                #    ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^
                #    00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15
                    ]

    def reg_reader(self, num, start, end):
        result = []
        for i in range(start, end + 1):
            result.append(self.reg[num][i])
        return result

    def reg_writer(self, num, start, end, data):
        data_size = len(data)
        dest_size = end - start + 1
        if data_size > dest_size:
            return EXIT_ERROR
        else:
            for i in range(dest_size):
                if i < data_size:
                    self.reg[num][start + i] = data[i]
                else:
                    self.reg[num][start + i] = 0
            return EXIT_SUCESS

    def reg_r(self, reg):
        if reg == 'A':
            return self.reg_reader(0,8,15)
        elif reg == 'F':
            return self.reg_reader(0, 0, 7)
        elif reg == 'B':
            return self.reg_reader(1,8,15)
        elif reg == 'C':
            return self.reg_reader(1,0,7)
        elif reg == 'D':
            return self.reg_reader(2,8,15)
        elif reg == 'E':
            return self.reg_reader(2,0,7)
        elif reg == 'H':
            return self.reg_reader(3,8,15)
        elif reg == 'L':
            return self.reg_reader(3,0,7)
        elif reg == 'BC':
            return self.reg_reader(1,0,15)
        elif reg == 'DE':
            return self.reg_reader(2,0,15)
        elif reg == 'HL' or reg == 'M':
            return self.reg_reader(3,0,15)
        elif reg == 'SP':
            return self.reg_reader(4,0,15)
        elif reg == 'PC':
            return self.reg_reader(5,0,15)
        else:
            return EXIT_ERROR

    def reg_w(self, reg, data):
        if reg == 'A':
            self.reg_writer(0,8,15,data)
        elif reg == 'F':
            self.reg_writer(0, 0, 7,data)
        elif reg == 'B':
            self.reg_writer(1,8,15,data)
        elif reg == 'C':
            self.reg_writer(1,0,7,data)
        elif reg == 'D':
            self.reg_writer(2,8,15,data)
        elif reg == 'E':
            self.reg_writer(2,0,7,data)
        elif reg == 'H':
            self.reg_writer(3,8,15,data)
        elif reg == 'L':
            self.reg_writer(3,0,7,data)
        elif reg == 'BC':
            self.reg_writer(1,0,15,data)
        elif reg == 'DE':
            self.reg_writer(2,0,15,data)
        elif reg == 'HL' or reg == 'M':
            self.reg_writer(3,0,15,data)
        elif reg == 'SP':
            self.reg_writer(4,0,15,data)
        elif reg == 'PC':
            self.reg_writer(5,0,15,data)
        else:
            return EXIT_ERROR

    def set_C(self):
        self.reg[0][0] = 1

    def get_C(self):
        return self.reg[0][0]

    def set_P(self):
        self.reg[0][2] = 1

    def get_P(self):
        return self.reg[0][2]
    def set_A(self):
        self.reg[0][4] = 1

    def get_A(self):
        return self.reg[0][4]

    def set_Z(self):
        self.reg[0][6] = 1

    def get_Z(self):
        return self.reg[0][6]
    def set_S(self):
        self.reg[0][7] = 1

    def get_S(self):
        return self.reg[0][7]

    def int_to_bits_8b(self, value):
        if value < 0:
            self.reset_flags()
            self.set_S()
        return [int(bit) for bit in '{:08b}'.format(value & 0xFF)]

    def int_to_bits_16b(self, value):
        if value < 0:
            self.set_S()
        return [int(bit) for bit in '{:016b}'.format(value & 0xFFFF)]

    def reset_flags(self):
        self.reg[0][0] = 0
        self.reg[0][2] = 0
        self.reg[0][4] = 0
        self.reg[0][6] = 0
        self.reg[0][7] = 0

    def bits_to_int(self, bits):
        return int(''.join(str(bit) for bit in bits), 2)

    def adder(self, v1, v2):
        size = len(v1)
        result = []
        carry = 0
        for i in range(size):
            bit1 = v1[-(i + 1)] if i < size else 0
            bit2 = v2[-(i + 1)] if i < size else 0
            total = bit1 + bit2 + carry
            result_bit = total % 2
            carry = total // 2
            result.insert(0, result_bit)
        if carry != 0:
            result.insert(0, carry)
        return result
    
    def two_complement(self, binary_number):
        one_complement = [1 if bit == 0 else 0 for bit in binary_number]
        return self.adder(one_complement, [0] * (len(binary_number) - 1) + [1])

    def subtractor(self, v1, v2):
        twos_complement_v2 = self.two_complement(v2)
        result = self.adder(v1, twos_complement_v2)
        if len(result) > len(v1):
            result = result[1:]
        return result

    def mov(self, D, S):
        self.reg_w(D, self.reg_r(S))
        return EXIT_SUCESS

    def mvi(self, D, I):
        self.reg_w(D, I)
        return EXIT_SUCESS

    def lxi(self, RP, I):
        self.reg_w(RP, I)

    def lda(self, addr):
        self.reg_w('A', self.mem.io(0, addr))
        return EXIT_SUCESS

    def sta(self, addr):
        self.mem.io(1, addr, self.reg_r('A'))
        return EXIT_SUCESS

    def lhld(self, addr):
        addr_1 = self.adder(addr, self.int_to_bits_16b(1))
        self.reg_w('HL', self.mem.io(0,addr) + self.mem.io(0,addr_1))

    def shld(self, addr):
        addr_1 = self.adder(addr, self.int_to_bits_16b(1))
        self.mem.io(1, addr, self.reg_r('HL')[:8])
        self.mem.io(1, addr_1, self.reg_r('HL')[8:])

    def ldax(self, RP):
        addr = self.reg_r(RP)
        self.lda(addr)

    def stax(self, RP):
        addr = self.reg_r(RP)
        self.sta(addr)

    def xchg(self):
        for i in range(16):
            self.reg[2][i] = self.reg[2][i] ^ self.reg[3][i]
            self.reg[3][i] = self.reg[2][i] ^ self.reg[3][i]
            self.reg[2][i] = self.reg[2][i] ^ self.reg[3][i]

    def add(self, S):
        val = self.reg_r(S)
        val_A = self.reg_r('A')
        self.reg_w('A', self.adder(val, val_A))
        return EXIT_SUCESS

    def adi(self, I):
        val_A = self.reg_r('A')
        self.reg_w('A', self.adder(val_A, I))
        return EXIT_SUCESS

    def adc(self, S):
        pass

    def aci(self, I):
        pass

    def sub(self, S):
        val_A = self.reg_r('A')
        val = self.reg_r(S)
        self.reg_w('A', self.subtractor(val_A, val))
        return EXIT_SUCESS

    def sui(self, I):
        val = self.int_to_bits_8b(I)
        val_A = self.reg_r('A')
        self.reg_w('A', self.subtractor(val_A, val))
        return EXIT_SUCESS

    def sbb(self, S):
        pass

    def sbi(self, I):
        pass

    def inr(self, D):
        self.reg_w(D, self.adder(self.reg_r(D), self.int_to_bits_8b(1)))

    def dcr(self, D):
        self.reg_w(D, self.subtractor(self.reg_r(D), self.int_to_bits_8b(1)))

    def inx(self, RP):
        self.reg_w(RP, self.adder(self.reg_r(RP), self.int_to_bits_16b(1)))

    def dcx(self, RP):
        self.reg_w(RP, self.subtractor(self.reg_r(RP), self.int_to_bits_16b(1)))

    def dad(self, RP):
        self.reg_w('HL', self.adder(self.reg_r('HL'), self.reg_r(RP)))

    def daa(self):
        pass

    def ana(self, S):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] and self.reg_r(S)[i]

    def ani(self, I):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] and I[i]

    def ora(self, S):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] or self.reg_r(S)[i]

    def ori(self, I):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] or I[i]

    def xra(self, S):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] ^ self.reg_r(S)[i]

    def xri(self, I):
        for i in range(8):
            self.reg[0][8+i] = self.reg[0][8+i] ^ I[i]

    def cmp(self, S):
        pass

    def cpi(self, I):
        pass

    def rlc(self):
        pass

    def rrc(self):
        pass

    def ral(self):
        pass

    def rar(self):
        pass

    def cma(self):
        self.reg_w('A', [1 if bit == 0 else 0 for bit in self.reg_r('A')])

    def cmc(self):
        self.reg[0][0] = not self.reg[0][0]

    def stc(self):
        self.set_C()

    def jmp(self, addr):
        pass

    def jccc(self, addr, ccc):
        pass

    def call(self, addr):
        pass

    def cccc(self, addr, ccc):
        pass

    def ret(self):
        pass

    def rccc(self, ccc):
        pass

    def rst(self, n):
        pass

    def pchl(self):
        pass

    def push(self, RP):
        pass

    def pop(self, RP):
        pass

    def xthl(self):
        pass

    def sphl(self):
        pass

    def in_(self, port):
        pass

    def out(self, port):
        pass

    def ei(self):
        pass

    def di(self):
        pass

    def hlt(self):
        pass

    def nop(self):
        pass
