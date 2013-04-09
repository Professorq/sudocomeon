

class Grid:
  grid = None # two dimensional list
  df = None # dictionary of coordinates listed by degrees of freedom (key)
  row_fill = None # one dict per row of candidate values in that row
  col_fill = None # one dict per column of candidate values in that column
  subgrid_fill = None # one dict of column candidates per 3x3 section
  
  def smallgrid(self, threebythree = None):
      unique = [True for x in range(10)]
      try:
        for r in threebythree:
          for c in r:
              if not unique[c]:
                  return False
              elif c > 0 and unique[c]:
                  unique[c] = False
              else:
                  assert c == 0
      except TypeError as err:
        print(err)
        return None
      else:
        return True

  def smallSolvedgrid(self, threebythree = None):
      unique = [True for x in range(10)]
      try:
        for r in threebythree:
          for c in r:
              if not unique[c]:
                  return False
              elif c > 0 and unique[c]:
                  unique[c] = False
              else:
                  assert c == 0
                  return None
      except TypeError as err:
        print(err)
        return None
      else:
        return True
      
  def testSubGrids(self, grid):
      for column in range(0,3):
          sub_row = [row[column*3:column*3 + 3] for row in grid]
          for sect in range(0,3):
              sector = sub_row[sect*3:sect*3+3]
              ok = self.smallgrid(sector)
              if ok:
                  pass
              else:
                  print(grid)
                  print(sector)
                  return False
      return True

  def testSolvedSubGrids(self, grid):
      for column in range(0,3):
          sub_row = [row[column*3:column*3 + 3] for row in grid]
          for sect in range(0,3):
              sector = sub_row[sect*3:sect*3+3]
              ok = self.smallSolvedgrid(sector)
              if ok:
                  pass
              else:
                  print(grid)
                  print(sector)
                  return False
      return True

  def path_test(self, nineline = None):
      if not len(nineline) == 9:
          return None
      unique = [True for x in range(10)]
      for v in nineline:
          if not unique[v]:
              return False
          elif v > 0 and unique[v]:
              unique[v] = False
          else:
              assert v == 0
      return True

  def path_solved_test(self, nineline = None):
      if not len(nineline) == 9:
          return None
      unique = [True for x in range(10)]
      for v in nineline:
          if not unique[v]:
              return False
          elif v > 0 and unique[v]:
              unique[v] = False
          else:
              assert v == 0
              return None
      return True

  def testRows(self, grid):
      for row in grid:
          ok = self.path_test(row)
          if ok:
              pass
          elif ok is None:
              return None
          else:
              print("Row")
              print(row)
              return False
      return True

  def testSolvedRows(self, grid):
      for row in grid:
          ok = self.path_solved_test(row)
          if ok:
              pass
          elif ok is None:
              return None
          else:
              print("Row")
              print(row)
              return False
      return True

  def testCols(self, grid):
      for index in range(0,9):
          col = [row[index] for row in grid]
          ok = self.path_test(col)
          if ok:
              pass
          else:
              print("Column")
              print(grid)
              print(index)
              print(col)
              return False
      return True

  def testSolvedCols(self, grid):
      for index in range(0,9):
          col = [row[index] for row in grid]
          ok = self.path_solved_test(col)
          if ok:
              pass
          else:
              print("Column")
              print(grid)
              print(index)
              print(col)
              return False
      return True          

  def check_sudoku(self, grid = None):
    if grid is None:
      grid = self.grid
    rows = self.testRows(grid)
    if rows is None:
        return None
    elif rows is False:
        return False
    else:
        return self.testCols(grid) and self.testSubGrids(grid) and rows

  def check_sudoku_solved(self, grid = None):
    if grid is None:
      grid = self.grid
    rows = self.testSolvedRows(grid)
    if rows is None:
        return None
    elif rows is False:
        return False
    else:
        return self.testSolvedCols(grid) and self.testSolvedSubGrids(grid)
        
  def count_zeros(self, grid = None):
    if grid is None:
      grid = self.grid
    return sum([len(self.df[x]) for x in self.df.keys()])
  
  def altsolve(self,grid = None):
    success = None
    if grid is None:
      grid = self.grid
    if self.count_zeros(grid) == 0 and self.check_sudoku_solved(grid):
        print('Solved!')
        success = grid
        for r in grid:
          print(r)
        return grid
    try:
      key = min(self.df)
      coord = self.df[key].pop()
      if len(self.df[key]) == 0:
        del self.df[key]
    except KeyError as err:
      print(err)
      print('key = min(self.df) was not a viable key in df')
      return False
    except IndexError as err:
      print(err)
      print('tried to pop() too many coordinates from the df[{0}] list'.format(key))
      return False
    possible_values_at_coord = self.candidate_list(coord)
    print("Coordinates: {0}".format(coord))
    solved = False
    while not solved:
      try:
        value = possible_values_at_coord.pop()
      except IndexError as err:
        print("All candidates failed for coord {0}".format(coord))
        print(err)
        return False
      print("try value {0}".format(value))
      attempt = self.insert_value_at(value, coord)
      if attempt and attempt.check_sudoku():
        if attempt.check_sudoku_solved():
          self = attempt
          return attempt
        else:
          assert not 0 in attempt.df
          solved = attempt.altsolve()
          if solved and solved.check_sudoku_solved():
            return solved.grid

  def solve(self, grid = None):
    if grid is None:
      grid = self.grid
    if self.count_zeros(grid) == 0 and self.check_sudoku_solved(grid):
        print('Solved!')
        for r in grid:
          print(r)
        return grid
    # Find set of (blank value) coordinates with fewest degrees of freedom
    for key in self.df.keys():
      for low_hanging_fruit in self.df[key]:
        attempt = self.simple_coord(low_hanging_fruit)
        if attempt:
          return attempt.solve()
        else:
          pass
    return False
    
  def insert_value_at(self, value, coord):
    x,y = coord
    if self.grid[y][x] == 0:
      attempt = Grid(self.grid)
      try:
        if value in attempt.row_fill[y] or value in attempt.col_fill[x] or value in attempt.subgrid_fill[int(y/3)][int(x/3)]:
          return False
        else:
          attempt.row_fill[y][value] = coord
          attempt.col_fill[x][value] = coord
          attempt.subgrid_fill[int(y/3)][int(x/3)][value] = coord
          attempt.grid[y][x] = value
          attempt.build_df_map()
        if 0 in attempt.df:
          return False
      except TypeError as err:
        print(err)
        return None
      for r in attempt.grid:
        print(r)
      print('\n\n')
      return attempt
    else:
      return False

  def simple_coord(self, coordinates):
    x,y = coordinates
    value = self.grid[y][x]
    if value > 0 and value < 10:
      print("value at {0}, {1} = {2}".format(x,y,value))
      return False
    elif value == 0:
      candidates = self.candidate_list(coordinates)
      key = len(candidates)
      if key == 1:
        attempt = self.insert_value_at(candidates[0], coordinates)
        if attempt:
          return attempt
        else:
          # raise Exception('Insert into self.grid failed','You had one job to do')
          return False
      elif len(candidates) == 0:
        return False
      else:
        for can in candidates:
          attempt = self.insert_value_at(can, coordinates)
          if attempt:
            return attempt
          else:
            pass
        return False

  def taken_one_dimension(self, sudokuItem = None):
    if sudokuItem is None:
      return None
    taken = {}
    for value in sudokuItem:
      if value > 0 and value < 10:
        taken[value] = True
      elif value == 0:
        pass
      else:
        return False
    return taken

  def flatten(self, subgrid):
    one_dimension = []
    for row in subgrid:
      one_dimension.extend(row)
    return one_dimension

  def getSubgrid(self, coordinates = None):
    if coordinates is None:
      return None
    try:
      x,y = coordinates
    except TypeError as err: 
      x, y = coordinates, coordinates
      print(err)
    except ValueError as err:
      x,y = coordinates[0:2]
      print(err)
    columnSection = int(x/3)
    rowSection = int(y/3)
    try:
      sub_rows = [rowSection[columnSection*3:columnSection*3 + 3] for rowSection in self.grid]
      sub_grid = sub_rows[rowSection*3:rowSection*3+3]
      return sub_grid
    except TypeError as err:
      print(err)
      return False
    
  def candidate_list(self, coordinates = None):
    """Returns a list of available values that could be placed at coordinates.

    Combines row_fill, col_fill, and subgrid_fill dictionaries to find non-included
    numbers. Only one number returned means that only this value satisfies constraints.

    Degrees of freedom for a coordinate can be determined with len(candidatel_list((x,y)))

    Returns None on error condition resulting from issue with coordinates.
    Returns a non-empty list of length < 10 in normal operation.

    """
    # collate the dictionaries of conflicts - this is a lossy process
    # Note: this process is lossy - duplicates are overridden
    # Note: Later index items overwrite earlier index items in conversion to dict
    try:
      x,y = coordinates
    except(TypeError, ValueError):
      return None
    conflictList = []
    try:
      conflictList.extend(self.row_fill[y].items())
      conflictList.extend(self.col_fill[x].items())
      conflictList.extend(self.subgrid_fill[int(y/3)][int(x/3)].items())
    except AttributeError as err:
      print(err)
      print("Coordinates: {0}".format(coordinates))
    conflict = dict(conflictList)
    candidates = [x for x in range(1,10)]
    for key in conflict.keys():
      try:
        candidates.remove(key)
      except ValueError as err:
        print(err)
        print('This value was not in the range(1,10): {0}'.format(key))
    return candidates

  def build_fill_map(self):
    self.row_fill = [None for y in range(9)]
    self.col_fill = [None for x in range(9)]
    self.subgrid_fill = [[None for x in range(3)] for y in range(3)]
    for x in range(9):
      for y in range(9):
        coordinates = (x,y)
        self.build_fill(coordinates)

  def build_df_map(self):
    self.df = {}
    for x in range(9):
      for y in range(9):
        coordinates = (x,y)
        if self.grid[y][x] == 0:
          degrees_of_freedom = len(self.candidate_list(coordinates))
          if degrees_of_freedom in self.df:
            self.df[degrees_of_freedom].append(coordinates)
          else:
            self.df[degrees_of_freedom] = [coordinates]
        else:
          pass # No need to add non-zeros to the df dictionary.

  def build_fill(self, coordinates):
    """For a given index, determine row, grid, and subgrid degress of freedom"""
    try:
      x, y = coordinates
    except(TypeError, ValueError) as err:
      print(err)
      return False
    if self.row_fill[y] is None:
      self.row_fill[y] = self.taken_one_dimension(self.grid[y])
    if self.col_fill[x] is None:
      column = [row[x] for row in self.grid]
      self.col_fill[x] = self.taken_one_dimension(column)
    if self.subgrid_fill[int(y/3)][int(x/3)] is None: 
      subgrid = self.getSubgrid(coordinates)
      list_subgrid = self.flatten(subgrid)
      self.subgrid_fill[int(y/3)][int(x/3)] = self.taken_one_dimension(list_subgrid)

  def __init__(self, grid = None):
    self.grid = [row[:] for row in grid]
    self.build_fill_map()
    self.build_df_map()

class Test:
  hard = [[1,0,0,0,0,7,0,9,0],
         [0,3,0,0,2,0,0,0,8],
         [0,0,9,6,0,0,5,0,0],
         [0,0,5,3,0,0,9,0,0],
         [0,1,0,0,8,0,0,0,2],
         [6,0,0,0,0,4,0,0,0],
         [3,0,0,0,0,0,0,1,0],
         [0,4,0,0,0,0,0,0,7],
         [0,0,7,0,0,0,3,0,0]]

  easy = [[2,9,0,0,0,0,0,7,0],
          [3,0,6,0,0,8,4,0,0],
          [8,0,0,0,4,0,0,0,2],
          [0,2,0,0,3,1,0,0,7],
          [0,0,0,0,8,0,0,0,0],
          [1,0,0,9,5,0,0,6,0],
          [7,0,0,0,9,0,0,0,1],
          [0,0,1,2,0,0,3,0,6],
          [0,3,0,0,0,0,0,5,9]]

  # solve_sudoku should return None
  ill_formed = [[5,3,4,6,7,8,9,1,2],
                [6,7,2,1,9,5,3,4,8],
                [1,9,8,3,4,2,5,6,7],
                [8,5,9,7,6,1,4,2,3],
                [4,2,6,8,5,3,7,9],  # <---
                [7,1,3,9,2,4,8,5,6],
                [9,6,1,5,3,7,2,8,4],
                [2,8,7,4,1,9,6,3,5],
                [3,4,5,2,8,6,1,7,9]]

  # solve_sudoku should return valid unchanged
  valid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,4,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

  # solve_sudoku should return False
  invalid = [[5,3,4,6,7,8,9,1,2],
             [6,7,2,1,9,5,3,4,8],
             [1,9,8,3,8,2,5,6,7],
             [8,5,9,7,6,1,4,2,3],
             [4,2,6,8,5,3,7,9,1],
             [7,1,3,9,2,4,8,5,6],
             [9,6,1,5,3,7,2,8,4],
             [2,8,7,4,1,9,6,3,5],
             [3,4,5,2,8,6,1,7,9]]
  
  def check(self):
    print("Test valid/invalid checks")
    g = Grid()
    print(g.check_sudoku(self.ill_formed))
    print(g.check_sudoku(self.valid))
    print(g.check_sudoku(self.invalid))
    print(g.check_sudoku(self.easy))
    print(g.check_sudoku(self.hard))

  def solve(self):
    easy = Grid(self.easy)
    hard = Grid(self.hard)
    return easy.solve(), hard.solve()

  def access(self):
    easy = Grid(self.easy)
    hard = Grid(self.hard)
    return easy, hard
