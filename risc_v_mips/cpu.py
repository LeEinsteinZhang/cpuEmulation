BITS_WIDE = 32

class CPU:
    def __init__(self) -> None:
        self.pc = [0] * BITS_WIDE
        self.reg = {
            '00000': [0] * BITS_WIDE, '00001': [0] * BITS_WIDE, '00010': [0] * BITS_WIDE, '00011': [0] * BITS_WIDE,
            '00100': [0] * BITS_WIDE, '00101': [0] * BITS_WIDE, '00110': [0] * BITS_WIDE, '00111': [0] * BITS_WIDE,
            '01000': [0] * BITS_WIDE, '01001': [0] * BITS_WIDE, '01010': [0] * BITS_WIDE, '01011': [0] * BITS_WIDE,
            '01100': [0] * BITS_WIDE, '01101': [0] * BITS_WIDE, '01110': [0] * BITS_WIDE, '01111': [0] * BITS_WIDE,
            '10000': [0] * BITS_WIDE, '10001': [0] * BITS_WIDE, '10010': [0] * BITS_WIDE, '10011': [0] * BITS_WIDE,
            '10100': [0] * BITS_WIDE, '10101': [0] * BITS_WIDE, '10110': [0] * BITS_WIDE, '10111': [0] * BITS_WIDE,
            '11000': [0] * BITS_WIDE, '11001': [0] * BITS_WIDE, '11010': [0] * BITS_WIDE, '11011': [0] * BITS_WIDE,
            '11100': [0] * BITS_WIDE, '11101': [0] * BITS_WIDE, '11110': [0] * BITS_WIDE, '11111': [0] * BITS_WIDE
        }

    def IF(self):
        instruction = self.read_mem(self.pc)
        self.ID(instruction)
        self.pc += 4

    def ID(self, instruction):
        opcode = instruction[0:6]
        rs = instruction[6:11]
        rt = instruction[11:16]
        rd = instruction[16:21]
        shamt = instruction[21:26]
        funct = instruction[26:32]
        immediate = instruction[16:32]
        address = instruction[6:32]
        self.EXE(opcode, rs, rt, rd, shamt, funct, immediate, address)

    def EXE(self, opcode, rs, rt, rd, shamt, funct, immediate, address):
        # 执行阶段的具体实现将根据不同的指令来处理
        pass

    def MEM(self):
        # 存储器访问阶段的具体实现
        pass

    def WB(self):
        # 写回阶段的具体实现
        pass

    def read_mem(self, address):
        # 模拟内存读取，这里你需要根据你的内存模型来实现
        pass

    def _word(self):
        pass

    def add(self, rs, rt, rd):
        pass

    def sub(self, rs, rt, rd):
        pass

    def mult(self, rs, rt):
        pass

    def multu(self, rs, rt):
        pass

    def div(self, rs, rt):
        pass

    def divu(self, rs, rt):
        pass

    def mfhi(self, rd):
        pass

    def mflo(self, rd):
        pass

    def lis(self, rd):
        pass

    def lw(self, rs, rt, i):
        pass

    def sw(self, rs, rt, i):
        pass

    def sltu(self, rs, rt, rd):
        pass

    def beq(self, rs, rt, i):
        pass

    def bne(self, rs, rt, i):
        pass

    def jr(self, rs):
        pass

    def jalr(self, rs):
        pass

    def addi(self, rs, rt, i):
        pass

    def j(self, i):
        pass

    def jal(self, i):
        pass
