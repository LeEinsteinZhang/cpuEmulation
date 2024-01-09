class Byte:
    def __init__(self):
        self.data = [0, 0, 0, 0, 0, 0, 0, 0]

    def write(self, data):
        if len(data) == 8 and all(bit in [0, 1] for bit in data):
            self.data = data
            return True
        else:
            return False

    def read(self):
        return self.data


class Memory:
    def __init__(self):
        self.size = 4 * 1024 * 1024 # 4MB memory
        self.cells = [Byte() for i in range(self.size)]


M = Memory()
for i in range(4 * 1024 * 1024):
    print(M.cells[i].data)