from bus import *
from bios import *
from cpu_bins import *
from memory import *

b1 = BINS()
m1 = Memory(b1)
c1 = CPU(b1, m1)

c1.mem.cells[0].write([0, 1, 1, 1, 1, 0, 0, 0])

c1.lda([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
print(b1.D)
print(c1.reg_r('A'))
c1.mem.cells[0].write([0,0,0,0,0,0,0,0])
print(c1.mem.cells[0].read())
c1.sta([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
print(c1.mem.cells[0].read())