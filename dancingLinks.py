# dancingLinks.py
# Retrieved from http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
# on 18 Decmeber 2014

def solve(X, Y, solution=[]):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)
                    
'''
Comments by Spatz:

In the above, X is a set, and Y a family of subsets of X.  The exact cover
problem is to find a subset of Y that partitions X.  In the matrix formulation,
X represents the columns of a zero-one matrix, and Y its rows.  The problem
is to choose a subset of the rows, such that a one appears exactly once in
each column of the submatrix comprising those rows.

Both X and Y are represented as dicts, with the key a column id in the
case of X or a row id in the case of Y.  In X the value is a set of row ids, 
and for Y the value is a list of column ids.  The ids in the collection are those
with a one in the indicated line.

Of the difference in data structure, Assaf says, "The sharp eye will notice this 
is slightly different from how we represented Y. Indeed, we need to be able to 
quickly remove and add rows to each column, which is why we use sets. 
On the other hand, and Knuth doesn't mention this, rows actually remain 
intact throughout the algorithm."

Of course the rows remain intact.  The rows are the problem statement, and the
problem deosn't change.  To say that the columns change isn't really true,
either.  What changes is the links in the columns, which reflect what rwos are
tentatively included in, or excluded from, the solution. Algorithm X is elegant, but 
it's just backtrack when all is said and done.
'''