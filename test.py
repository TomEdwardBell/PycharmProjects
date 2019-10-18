A = ['+', '4', '*', '9', '6']
B = [2,0,4,0,0]
C = [3,0,5,0,0]


def t(pos):
    print(pos)
    A = ['','+', '4', '*', '9', '6']
    B = [0, 2, 0, 4, 0, 0]
    C = [0, 3, 0, 5, 0, 0]

    if B[pos] > 0: t(B[pos])
    if C[pos] > 0: t(C[pos])

    print("OUTPUT", A[pos])
    return

t(1)