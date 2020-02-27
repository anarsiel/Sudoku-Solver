import sys
import copy
import random


class Sudoku_Table:

    #
    #   public methods
    #
    def __init__(self, table=None, sz=9):
        self.sz = sz

        if table is None:
            table = [[0] * self.sz for i in range(sz)]
        self.table = table

    # reads table from stdin
    def read_from_sys(self):
        for i in range(self.sz):
            self.table[i] = [int(char) for char in
                             sys.stdin.readline().rstrip()]
        return self

    # reads table from stdin
    def print_to_sys(self):
        [print(*line, sep='') for line in self.table]

    # fills all empty cells of Sudoku table
    # self.table --> correct full-filled Sudoku.
    def solve(self):
        ij_to_values = dict()
        for i in range(self.sz):
            for j in range(self.sz):
                ij_to_values[(i, j)] = set(range(1, 10))

        for i in range(self.sz):
            for j in range(self.sz):
                if self.table[i][j] != 0:
                    self.__remove_value_from_ij((i, j), self.table[i][j],
                                                ij_to_values)

        self.table = self.__recursive_substitute(ij_to_values)
        return self

    #
    #   private
    #

    # checks before removing from dict of sets,
    # if the element being removed exists.
    def __secure_remove(self, value, ij, ij_to_values):
        if ij in ij_to_values.keys() and value in ij_to_values[ij]:
            ij_to_values[ij].remove(value)

    # checks if two cells of Sudoku table
    # are in one Sudoku's square 3x3.
    def __ijs_in_one_square(self, ij_1, ij_2):
        return (ij_1[0] // 3 == ij_2[0] // 3) and \
               (ij_1[1] // 3 == ij_2[1] // 3)

    # finds next cell for substitution.
    # this is the cell with the smallest number of available values
    # that can be inserted into it at the current time.
    def __find_next(self, ij_to_values):
        next_ij = min(ij_to_values.keys(),
                      key=lambda ij: len(ij_to_values[ij]))

        if len(ij_to_values[next_ij]) == 0:
            return None
        return next_ij

    # changes available values for all cells
    # when we substitute 'value' to some cell
    def __remove_value_from_ij(self, ij, value, ij_to_values):
        i, j = ij
        for k in range(self.sz):
            self.__secure_remove(value, (k, j), ij_to_values)
            self.__secure_remove(value, (i, k), ij_to_values)

        for k in range(self.sz):
            for h in range(self.sz):
                if self.__ijs_in_one_square(ij, (k, h)):
                    self.__secure_remove(value, (k, h), ij_to_values)

        del ij_to_values[ij]

    # substitutes recursively cell by cell values into table.
    # value of current cell is brute-forced in randomized order
    def __recursive_substitute(self, ij_to_values):
        # if there are no free cells -- we got a correct solution
        if len(ij_to_values) == 0:
            return copy.deepcopy(self.table)

        # if there is an empty cell
        # with no available values -- we got a wrong solution
        ij = self.__find_next(ij_to_values)
        if ij is None:
            return None

        i, j = ij

        # shuffling available values order
        for_shuffle = list(ij_to_values[ij].copy())
        random.shuffle(for_shuffle)

        for value in for_shuffle.copy():
            self.table[i][j] = value

            new_ij_to_values = copy.deepcopy(ij_to_values)

            self.__remove_value_from_ij(ij, value, new_ij_to_values)

            returned_table = self.__recursive_substitute(new_ij_to_values)
            if returned_table is not None:
                return returned_table

            self.table[i][j] = 0
        return None


Sudoku_Table().read_from_sys().solve().print_to_sys()
