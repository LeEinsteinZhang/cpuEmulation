class Byte:
    def __init__(self):
        self.data = [0, 0, 0, 0, 0, 0, 0, 0]

    def write(self, data):
        if len(data) == 8 and all(bit in [0, 1] for bit in data):
            self.data = data
            return 1
        else:
            return 0

    def read(self):
        return self.data


class Memory:
    def __init__(self):
        self.size = 4 * 1024 # 4KB memory [0x000 to 0xFFF]
        self.cells = [Byte() for i in range(self.size)]
