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
        self.mem = Memory()
        self.reg = {
            'A': [0, 0, 0, 0, 0, 0, 0, 0],
            'B': [0, 0, 0, 0, 0, 0, 0, 0], 
            'C': [0, 0, 0, 0, 0, 0, 0, 0],
            'D': [0, 0, 0, 0, 0, 0, 0, 0],
            'E': [0, 0, 0, 0, 0, 0, 0, 0], 
            'H': [0, 0, 0, 0, 0, 0, 0, 0],
            'L': [0, 0, 0, 0, 0, 0, 0, 0],
            'Flags': [0, 0, 0, 0, 0, 0, 0, 0]
        }
        self.sp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.flags = [0, 0, 0, 0, 0, 0, 0, 0]
    
    def int_to_bits_8b(self, value):
        return [int(bit) for bit in '{:08b}'.format(value)]
    
    def int_to_bits_16b(self, value):
        ans = [int(bit) for bit in '{:16b}'.format(value)]
        return ans[:8], ans[8:], ans

    def bits_to_int(self, bits):
        return int(''.join(str(bit) for bit in bits), 2)

    def mov(self, D, S):
        self.reg[D] = self.reg[S]
        return EXIT_SUCESS
    
    def mvi(self, D, I):
        val = self.int_to_bits_8b(I)
        self.reg[D] = val
        return EXIT_SUCESS
        
    def lxi(self, RP, I):
        val1, val2, two_bytes = self.int_to_bits_16b(I)
        if RP == 'BC':
            self.reg['B'] = val1
            self.reg['C'] = val2
            return EXIT_SUCESS
        elif RP == 'DE':
            self.reg['D'] = val1
            self.reg['E'] = val2
            return EXIT_SUCESS
        elif RP == 'HL':
            self.reg['H'] = val1
            self.reg['L'] = val2
            return EXIT_SUCESS
        else:
            return EXIT_FAIL

    def lda(self, addr):
        self.reg['A'] = self.mem.io(0, addr, 0)
        return EXIT_SUCESS

    def sta(self, addr):
        self.mem.io(1, addr, 0, self.reg['A'])
        return EXIT_SUCESS

    def lhld(self, addr):
        self.reg['H'], self.reg['L'] = self.mem.io(0, addr, 1)
        return EXIT_SUCESS

    def shld(self, addr):
        self.mem.io(1, addr, 1, self.reg['H'], self.reg['L'])
        return EXIT_SUCESS

    def ldax(self, RP):
        pass

    def stax(self, RP):
        pass

    def xchg(self):
        val1 = self.reg['D']
        self.reg['D'] = self.reg['H']
        self.reg['H'] = val1
        val1 = self.reg['E']
        self.reg['E'] = self.reg['L']
        self.reg['L'] = val1
        return EXIT_SUCESS

    def add(self, S):
        val_A = self.reg['A']
        val_S = self.reg[S]
        result = []
        carry = 0
        for i in range(8):
            bit1 = val_A[-(i+1)] if i < len(val_A) else 0
            bit2 = val_S[-(i+1)] if i < len(val_S) else 0
            total = bit1 + bit2 + carry
            result_bit = total % 2
            carry = total // 2
            result.insert(0, result_bit)
        if carry != 0:
            result.insert(0, carry)
        
        self.reg['A'] = result
        return EXIT_SUCESS

    def adi(self, I):
        pass

    def adc(self, S):
        pass

    def aci(self, I):
        pass

    def sub(self, S):
        pass

    def sui(self, I):
        pass

    def sbb(self, S):
        pass

    def sbi(self, I):
        pass

    def inr(self, D):
        pass

    def dcr(self, D):
        pass

    def inx(self, RP):
        pass

    def dcx(self, RP):
        pass

    def dad(self, RP):
        pass

    def daa(self):
        pass

    def ana(self, S):
        pass

    def ani(self, I):
        pass

    def ora(self, S):
        pass

    def ori(self, I):
        pass

    def xra(self, S):
        pass

    def xri(self, I):
        pass

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
        pass

    def cmc(self):
        pass

    def stc(self):
        pass

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


c1 = CPU() # initial
c1.mem.cells[32].write([1, 0, 1, 1, 0, 0, 1, 1])              # set 32 cells
address = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]    # pre define a address use 16-bit list
address_31 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1] # pre define a address use 16-bit list
c1.reg['A'] = [0, 0, 0, 0, 0, 0, 0, 1]                        # set reg A value

c1.mov('B', 'A')
c1.lda(address)

print(c1.reg['B'] == [0, 0, 0, 0, 0, 0, 0, 1])
print(c1.reg['A'] == [1, 0, 1, 1, 0, 0, 1, 1])

c1.reg['A'] = [1, 0, 0, 0, 0, 0, 0, 0]
c1.sta(address_31)
print(c1.mem.cells[31].read() == [1, 0, 0, 0, 0, 0, 0, 0])

c1.reg['A'] = [0, 0, 0, 0, 0, 0, 0, 1]
c1.reg['B'] = [0, 0, 0, 0, 0, 0, 0, 1]
c1.add('B')
print(c1.reg['A'] == [0, 0, 0, 0, 0, 0, 1, 0])