
class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def see(self):
        for i in range(9):
            aa = " "
            for j in range(9):
                if len(self.board[(i,j)])==1:
                    aa += str(next(iter(self.board[(i,j)]))) + " "
                else:
                    aa += "* "
                if j==2 or j==5:
                    aa += "| "
            print(aa)
            if i==2 or i==5: 
                print("-----------------------")
                
                
    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1,cell2) not in self.ARCS:
            return False
        if len(self.get_values(cell2))==1 and len(self.get_values(cell2)&self.get_values(cell1)):
            self.board[cell1] = self.get_values(cell1) - self.get_values(cell2)
            return True
        return False
        
    def infer_ac3(self):
        arcs = set(self.ARCS)
        while arcs:
            arc = arcs.pop()
            if self.remove_inconsistent_values(arc[0],arc[1]):
                if len(self.get_values(arc[0]))==0:
                    return False
                arcs|=self.get_neighbors(arc[0])
        return True
        
    def infer_helper(self, cell0, newboard,potentialval):
        for val in potentialval:
            possible=[]
            for cell in cell0:
                if val in self.get_values(cell):
                    possible.append(cell)
            if len(possible)==1:
                self.board[possible[0]] = {val}
                newboard[possible[0]] = val
                cell0.remove(possible[0])
                    

    def infer_improved(self):
        if not self.infer_ac3():
            return False
        if max(map(len, self.board.values()))==1:
            return True
        new_board = {key:0 if len(self.board[key])>1 else next(iter(self.board[key])) for key,val in self.board.items()}
        changed = True
        temp = [(i,j) for i in [0,3,6] for j in [0,3,6]]
        blocks = [[(tup[0]+i, tup[1]+j) for i in range(3) for j in range(3)] for tup in temp]
        cols = [[(i,j) for i in range(9)] for j in range(9)]
        rows = [[(j,i) for i in range(9)] for j in range(9)]
        board_copy = copy.deepcopy(self.board)
        while changed:
            for block in blocks:
                cell0 = {tup for tup in block if not new_board[tup]}
                potential_val = {i for i in range(1,10)}-{new_board[tup] for tup in block if new_board[tup]}
                self.infer_helper(cell0,new_board,potential_val)
            for row in rows:
                cell1 = {tup for tup in row if not new_board[tup]}
                potential_val1 = {i for i in range(1,10)}-{new_board[tup] for tup in row if new_board[tup]}
                self.infer_helper(cell1,new_board,potential_val1)
            for col in cols:
                cell2 = {tup for tup in col if not new_board[tup]}
                potential_val2 = {i for i in range(1,10)}-{new_board[tup] for tup in col if new_board[tup]}
                self.infer_helper(cell2,new_board,potential_val2)
            if not self.infer_ac3():
                return False
            if self.board == board_copy:
                changed = False
            board_copy = copy.deepcopy(self.board)
            
        return True
    
    def backtrack(self, assignment, unsolved):
        if len(unsolved) == 0:
            return assignment #solutionsssss
        dic = {key:[] for key in range(2,10)}
        for tup, val in unsolved.items():
            dic[len(val)].append(tup)
        dic = {ind:val for ind, val in dic.items() if len(val)>0}
        rand_var = random.choice(dic[min(dic.keys())])
        for value in unsolved[rand_var]:
            for atup,aval in assignment.items():   #consistent 
                if (rand_var, atup) in self.ARCS and value==aval:##this is inconsistent when they can not be the same while the same
                    continue ##skip to first for loop
            assignment[rand_var] =value
            temp = unsolved.pop(rand_var)
            self_copy = copy.deepcopy(self)##
            self_copy.board[rand_var] = {value}
            temp2 = {tup for tup,val in self_copy.board.items() if len(val)==1}
            new_assignment = set()
            if self_copy.infer_improved():
                temp3 = {tup for tup,val in self_copy.board.items() if len(val)==1}
                new_assignment = temp3 - temp2
                for i in new_assignment:
                    assignment[i] = self_copy.get_values(i)
                result = self_copy.backtrack(assignment, unsolved)
                if result:
                    return result
            assignment.pop(rand_var)
            for i in new_assignment:
                assignment.pop(i)
            unsolved[rand_var] = temp
        return False
            
                    
    def infer_with_guessing(self):
        if not self.infer_improved():
            return False
        if max(map(len, self.board.values()))==1:
            return True
        unsolved = {key:val for key, val in self.board.items() if len(val)>1}
        assignment = self.backtrack({},unsolved)
        if assignment:
            for ind, val in assignment.items():
                self.board[ind] = {val}
            return True
        return False
        
    def get_neighbors(self, cell):
        neighbors = {((cell[0],j), cell) for j in range(9)}
        neighbors |= {((j, cell[1]), cell) for j in range(9)}
        dic = {i:0 if  i <3 else 3 if i<6 else 6 for i in range(9)}
        where = (dic[cell[0]],dic[cell[1]])
        neighbors|= {((where[0]+i,where[1]+j), cell) for i in range(3) for j in range(3)}
        neighbors.remove((cell,cell))
        return neighbors
