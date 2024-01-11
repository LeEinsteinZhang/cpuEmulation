from memory import *

# D   = Destination register (8 bit)
# S   = Source register (8 bit)
# RP  = Register pair (16 bit)
# I   = 8 or 16 bit immediate operand
# a   = 16 bit Memory address
# p   = 8 bit port address
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

    def sta(self, addr):
        self.mem.io(1, addr, 0, self.reg['A'])

    def lhld(self, addr):
        self.reg['H'], self.reg['L'] = self.mem.io(0, addr, 1)

    def shld(self, addr):
        self.mem.io(1, addr, 1, self.reg['H'], self.reg['L'])

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

    def add(self, S):
        pass

    def adi(self, value):
        pass

    def adc(self, S):
        pass

    def aci(self, value):
        pass

    def sub(self, S):
        pass

    def sui(self, value):
        pass

    def sbb(self, S):
        pass

    def sbi(self, value):
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

    def ani(self, value):
        pass

    def ora(self, S):
        pass

    def ori(self, value):
        pass

    def xra(self, S):
        pass

    def xri(self, value):
        pass

    def cmp(self, S):
        pass

    def cpi(self, value):
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

    def in_(self, p):
        pass

    def out(self, p):
        pass

    def ei(self):
        pass

    def di(self):
        pass

    def hlt(self):
        pass

    def nop(self):
        pass


c1 = CPU(1)
c1.reg['A'] = [0, 0, 0, 0, 0, 0, 0, 1]
c1.mov('A', 'B')
print(c1.reg['B'])