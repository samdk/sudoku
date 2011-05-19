from __future__ import division

class Board(object):
    """Base class for a sudoku board.
    
    All squares are stored in a flat list of values. Has many Rows/Cols/Boxes
    (collectively: "structs") that allow more interesting structural access."""
    def __init__(self,values,logfile=None):
        self.values = [Val(v) for v in values]
        self.rows =  [Row(n,self) for n in range(9)]
        self.cols =  [Col(n,self) for n in range(9)]
        self.boxes = [Box(n,self) for n in range(9)]
        self.logfile = logfile
        self.structs = self.rows + self.cols + self.boxes
    def is_solved(self):
        for struct in self.structs:
            if not set(struct.values()) == set(range(1,10)): return False
        return True
    # replace a Val 'old_val' with an (int) new_val
    def replace(self,old_val,new_val):
        if self.logfile: self.logfile.write('inserting '+str(new_val)+' at '+str(old_val.coords())+'\n')
        index = old_val.index()
        self.values[index] = self.values[index].replace(new_val)
    # return rows/cols/boxes by number
    def row(self,n): return self.rows[n]
    def col(self,n): return self.cols[n]
    # box indices: 0 1 2
    #              3 4 5
    #              6 7 8
    def box(self,n): return self.boxes[n]
    # get a struct of a given type t and number n
    def struct(self,t,n): return {Row:self.row,Col:self.col,Box:self.box}[t](n)
    # return a cloned version of the board
    def clone(self):
        b = Board(self.values)
        b.logfile = self.logfile
        return b
    # return a cloned version of the board with places that the value 'n'
    # can't go in blocked off
    def block(self,n):
        blocked = self.clone()
        for struct in self.structs:
            blocked.struct(type(struct),struct.num).block(n,struct)
        return blocked
    def __repr__(self):
        return '\nBoard ' + '\n      '.join(str(r) for r in self.rows)
    def __eq__(self,other):
        return self.values == other.values

class Val(int):
    """Wrapper around ints with convenience functions.
    
    Allows us to easily get the structs a value fits into."""
    OPEN = 0
    BLOCKED = -1
    def coords(self):
        return (self.col_num,self.row_num)
    # returns a new Val in the same position
    def replace(self,val):
        v = Val(val)
        v.col,v.col_num = self.col,self.col_num
        v.row,v.row_num = self.row,self.row_num
        v.box,v.box_num = self.box,self.box_num
        return v
    # replaces with a block
    def block(self): return self.replace(Val.BLOCKED)
    # index into board.values
    def index(self):
        return self.row.indices[self.col_num]
    # set of values that can go into this space
    def possible_values(self):
        return self.col.open_values() & self.row.open_values() & self.box.open_values()
    def __str__(self):
        if   self == Val.BLOCKED:  return 'x'
        elif self == Val.OPEN:     return ' '
        else:                      return str(int(self))

class Struct(object):
    """Generic struct class. Extended by Row/Col/Box."""
    def block(self,n,reference):
        # we store indices of the values in self.board so that we can
        # update them properly
        for i in self.blocked_indices(n,reference):
            v = self.board.values[i]
            self.board.values[i] = v.block()
    def block_on(self,n,spaces):
        self.blocks[n] = list(set(self.indices)-set([s.index() for s in spaces]))
    def blocked_indices(self,n,reference):
        if n in reference: return self.indices
        else: return self.blocks[n]
    def values(self):
        return [self.board.values[i] for i in self.indices]
    def open_count(self):
        return len(self.open_spaces())
    def open_spaces(self):
        return filter(lambda x: x == 0,self.values())
    def open_values(self):
        return set(range(1,10)) - set(self.values())
    def __eq__(self,other):
        return type(self) == type(other) and self.values() == other.values()
    def __contains__(self,elem):
        return elem in self.values()
    def __repr__(self):
        return '[' + ' '.join(str(x) for x in self.values()) + ']'
    def is_box(self): return True if type(self) == Box else False

class Row(Struct):
    """Class for representing a row in a Board.
    
    Constructor takes a row index and a Board."""
    def __init__(self,n,board):
        self.board = board
        self.blocks = {n:[] for n in range(1,10)}
        self.indices = range(n*9,n*9+9)
        self.num = n
        for val in self.values():
            val.row = self
            val.row_num = n

class Col(Struct):
    """Class for representing a column in a Board.
    
    Constructor takes a column index and a board."""
    def __init__(self,n,board):
        self.board = board
        self.blocks = {n:[] for n in range(1,10)}
        self.indices = range(n,81,9)
        self.num = n
        for val in self.values():
            val.col = self
            val.col_num = n

class Box(Struct):
    """Class for representing a 3x3 box in a Board.
    
    Constructor takes a box index and a board."""
    def __init__(self,n,board):
        self.board = board
        # top left square for a given box index
        s = n//3*3*9 + n%3*3
        self.blocks = {n:[] for n in range(1,10)}
        self.indices = range(s,s+3)+range(s+9,s+12)+range(s+18,s+21)
        self.num = n
        for val in self.values():
            val.box = self
            val.box_num = n

# an (easy) sample board for testing
def get_test_board():
    x = Val.OPEN
    vals = [7,x,3,  2,9,x,  x,x,x,
            x,1,x,  8,5,x,  3,x,x,
            x,x,5,  x,x,x,  x,x,1,

            x,8,x,  x,6,3,  x,4,2,
            6,x,7,  x,4,x,  8,x,3,
            3,2,x,  9,8,x,  x,5,x,

            2,x,x,  x,x,x,  5,x,x,
            x,x,1,  x,3,5,  x,6,x,
            x,x,x,  x,2,8,  9,x,7]
    return Board(vals)

