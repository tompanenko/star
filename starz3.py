from z3 import *
import itertools

def get_adj_coords(cell,offsets):
    ans = []
    for x in offsets:
        if cell[0] + x[0] >= 0 and cell[0] + x[0] <= 9 and cell[1] + x[1] >= 0 and cell[1] + x[1] <= 9:
            ans.append((cell[0] + x[0], cell[1] + x[1]))
    return ans

def solvez3(regions,dim,stars):
    # 10x10 matrix of ints
    X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(dim) ] for i in range(dim) ]
    # each cell contains a value in {0,1}
    cells_c  = [ And(0 <= X[i][j], X[i][j] <= 1) for i in range(dim) for j in range(dim)]
    # each row sums to star count
    rows_c   = [And(sum(X[i]) == stars) for i in range(dim)]
    # each column sums to 2
    cols_c   = [ And(sum([ X[i][j] for i in range(dim) ]) == stars) for j in range(dim)]
    # each region sums to 2
    regions_c = [And(sum(X[row][col] for (col,row) in region) == stars) for region in regions]
    # no 1s are adjacent
    adj_c = []
    offsets = list(itertools.product((-1, 1, 0), (-1, 1, 0)))
    offsets.pop()
    for x in range(dim):
        for y in range(dim):
            for z in get_adj_coords((x,y),offsets):
                adj_c.append(Or(X[x][y] == 0 , X[x][y] != X[z[0]][z[1]]))
    
    
    starbattle_c = cells_c + rows_c + cols_c + regions_c + adj_c     
    
    s = Solver()
    s.add(starbattle_c)
    if s.check() == sat:
        m = s.model()
        r = [ [ m.evaluate(X[i][j]) for j in range(dim) ] 
              for i in range(dim) ]
        print_matrix(r)
        return r
    else:
        print("failed to solve")