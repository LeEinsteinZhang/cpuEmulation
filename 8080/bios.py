from cpu import *
def BIOS(cpu, memory):
    cpu.mem = memory
    cpu.mem.io(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 1])        # lxi sp,I
    cpu.mem.io(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1])        # I_1
    cpu.mem.io(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1])        # I_2
    
    # set program start location (1024)
    cpu.mem.io(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 1, 0, 0, 0, 0, 1])        # lxi m,I
    cpu.mem.io(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0])        # I_1
    cpu.mem.io(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0])        # I_2

    #
    cpu.mem.io(1, [1, 1, 0, 0, 1, 0, 0, 0])
    cpu.mem.io(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [1, 1, 0, 1, 1, 0, 1, 1])        # in 255
    cpu.mem.io(1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1])
    cpu.run()

