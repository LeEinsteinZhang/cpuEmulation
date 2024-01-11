# 8-bit CPU 8080 like

class CPU:
    def __init__(self, memory) -> None:
        self.mem = memory
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
    
    def int_to_bits(self, value):
        return [int(bit) for bit in '{:08b}'.format(value)]

    def bits_to_int(self, bits):
        return int(''.join(str(bit) for bit in bits), 2)

    def mov(self, D, S):
        self.reg[D] = self.reg[S]
    
    def mvi(self, D, I):
        val = self.int_to_bits(I)
        self.reg[D] = val
        
    def lxi(self, RP, value):
        pass

    def lda(self, addr):
        pass

    def sta(self, addr):
        pass

    def lhld(self, addr):
        pass

    def shld(self, addr):
        pass

    def ldax(self, RP):
        pass

    def stax(self, RP):
        pass

    def xchg(self):
        pass

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