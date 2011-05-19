import sys
import sudoku as s
import solver as sol

if __name__=='__main__':
    print 'Enter a puzzle:'
    puzzle = [int(x) for x in ''.join([raw_input() for i in range(9)]).replace('.','0')]
    if len(sys.argv) > 1:
        lf = open(sys.argv[1],'w')
        b = s.Board(puzzle,lf)
    else: b = s.Board(puzzle)
    print 'Initial Puzzle:'
    print b
    bs = sol.solve(b)
    lf.close()
    if bs.is_solved():
        print '\n\nPuzzle solved:'
    else:
        print "\n\nCouldn't solve puzzle:"
    print bs

