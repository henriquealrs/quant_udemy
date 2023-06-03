import numpy as np
def pretty_print(m):
    tab = '\t'
    for row in m:
        s = ''
        for n in row:
            s += "{}{:.4f}".format(tab, n)
        print(s)

def prinf_diag_diff(m: np.ndarray):
    a = np.abs(m - m.T)
    thresh = np.vectorize(lambda n: n if n>0.005 else 0.)
    pretty_print(thresh(a))

def print_MI(mat, labels):
    s = "\t\t"
    # tab = '\t'
    for l in labels:
        s += "{}{}".format('   ', l)
    print(s)
    for i, row in enumerate(mat):
        s = labels[i]
        for n in row:
            s += "{}{:.4f}".format('     ', n)
        print(s)
