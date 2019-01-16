# Script von Michael

import numpy as np

v0 = np.array([0.0, 0.0, 0.0])

D = 20.0
L = 198.0
w = 1.65
p = 4.35
N = 8

vlist = []
flist = []

def assemble():
    global D, L, w, p, N
    #
    # define vertices of one electrode
    #
    vlist.append(v0)
    v = v0 + [0.0, D, 0.0] # current vertex position
    vlist.append(v.copy())
    v += [-p, 0.0, 0.0]
    for i in range(N):
        vlist.append(v.copy())
        v += [0.0, L, 0.0]
        vlist.append(v.copy())
        v += [-w, 0.0, 0.0]
        vlist.append(v.copy())
        v += [0.0, -L, 0.0]
        vlist.append(v.copy())
        v += [-p, 0.0, 0.0]
    vlist.append(v.copy())
    v += [0.0, -D, 0.0]
    vlist.append(v.copy())
    v += [p, 0.0, 0.0]
    for i in range(N):
        vlist.append(v.copy())
        v += [w, 0.0, 0.0]
        vlist.append(v.copy())
        v += [p, 0.0, 0.0]
    #
    # define faces of one electrode
    #
    m = len(vlist)
    flist.append([1, 2, 3, m])
    i = 3
    for j in range(N):
        flist.append([i, i + 1, i + 2, i + 3])
        flist.append([i, i + 3, m - 2*j - 1, m - 2*j])
        flist.append([i + 3, i + 4, m - 2*j - 2, m - 2*j - 1])
        i += 4
    
def write_simple():
    f = open('idt_layout.obj', 'w')
    f.write('o idt\n')
    for v in vlist:
        s = 'v {:f} {:f} {:f}\n'.format(v[0], v[1], v[2])
        f.write(s)
    for ff in flist:
        s = 'f {:d} {:d} {:d} {:d}\n'.format(ff[0], ff[1], ff[2], ff[3])
        f.write(s)
    f.close()

assemble()
write_simple()
