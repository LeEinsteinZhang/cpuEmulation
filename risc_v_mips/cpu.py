BITS_WIDE = 32
class CPU:
    def __init__(self) -> None:
        self.reg_int = [[0] * BITS_WIDE] * 32
        self.reg_float = [[0] * BITS_WIDE] * 32
        
