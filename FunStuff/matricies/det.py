def det(m):
    a=len(m)
    b=len(m[0])
    if a != b:
        return False
    if a == 2:
        return m[0][0]*m[1][1] - m[0][1]*m[1][0]
    else:
        sign = 1
        d = 0
        for i in range(a):
            # Ignore 0th row (y!=0)
            # ignore the 'i' column (x!=1)
            nx, ny = -1, -1
            mini = []
            for y in range(a -1):
                mini.append([])
                for x in range(a - 1):
                    mini[y].append(0)
            for y in range(a):
                if y != 0:
                    ny += 1
                    nx = -1
                    for x in range(a):
                        if not(y == 0 or x == i):
                            nx += 1
                            mini[ny][nx] = m[y][x]
            d  += m[0][i] * sign * det(mini)
            sign *= -1
        return d

m = [[1,1,3,4,9],
     [3,4,5,6,8],
     [5,6,7,8,7],
     [7,8,9,0,6],
     [2,2,2,2,1]]

print(det(m))