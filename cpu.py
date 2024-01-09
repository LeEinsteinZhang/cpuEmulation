# 8-bit CPU

class CPU:
    def __init__(self, memory) -> None:
        self.memory = memory
        self.PC = [0, 0, 0, 0, 0, 0, 0, 0]