# Головоломка "Поиск-слова" - это сетка букв со скрытыми словами,
# расположенными по строкам, столбцам и диагоналям. Это классическая игра.
#
# Поиск мест для размещения слов так, чтобы они все
# помещались в сетку, является своего рода задачей с ограничениями

from collections import namedtuple
from string import ascii_uppercase
from random import choice
from structure import CSP, Constraint


GridLocation = namedtuple('GridLocation', ['row', 'col'])


class Grid:
    def __init__(self, rows_number, cols_number):
        self.grid = [[choice(ascii_uppercase) for _ in range(cols_number)]
                     for _ in range(rows_number)]

    def size(self):
        # возвращается число строк и число столбцов
        return [len(self.grid), len(self.grid[0])]

    def __repr__(self):
        res = ''
        for row in self.grid:
            res += '  '.join(row)
            res += '\n'
        return res

    def set_config(self, config):
        print(config)
        for wrd, grid_locs in config.items():
            # if choice([True, False]):
            #     grid_locs.reverse()
            for index, letter in enumerate(wrd):
                row, col = grid_locs[index].row, grid_locs[index].col
                self.grid[row][col] = letter


G = Grid(4, 7)
print(G)

# переменные - слова

# ограничения: слова должны быть либо на одной строке, либо на одном столбце,
# либо на одной диагонали
# слова не должны пересекаться

# область определения: для каждого слова будет список списков (каждой букве по списку)
# в этих списках будут возможные положения всех букв с учетом первого ограничения

words = ["CAT", "PENCIL", "SCHOOL", "HOME", "SUMMER"]
locations = dict()


def generate_domain(word, grid):
    domain = []
    h, w = grid.size()
    length_of_word = len(word)

    for row in range(h):
        for col in range(w):
            columns = range(col, col+length_of_word+1)
            rows = range(row, row+length_of_word+1)
            # если справа есть место
            if col + length_of_word <= w:
                # слева направо
                domain.append([GridLocation(row, c) for c in columns])
                if row + length_of_word <= h:
                    # по диагонали, двигаясь слева направо вверх
                    domain.append([GridLocation(r, col + (r-row)) for r in rows])
            # если снизу есть место
            if row + length_of_word <= h:
                # сверху вниз
                domain.append([GridLocation(r, col) for r in rows])
                if col - length_of_word >= 0:
                    # по диагонали справа налево вверх
                    domain.append([GridLocation(r, col - (r-row)) for r in rows])
    return domain


for word in words:
    locations[word] = generate_domain(word, G)
wordsearch_problem = CSP(words, locations)


# Переопределим ограничение
class WordSearchConstraint(Constraint):
    def __init__(self, searching_words):
        super().__init__(searching_words)

    def satisfied(self, configuration):
    # совпадают ли положения, предложенные для одного слова,
    # с положением, предложенным для другого слова
    # иными словами, проверяем: не пересеклись ли слова
        all_locs = []
        for value in configuration.values():
            for loc in value:
                all_locs.append(loc)
        # полученный список содержит все занятые ячейки на данный момент
        # если в полученном списке будут дубликаты, то это значит
        # что какие-то слова пересеклись
        return len(set(all_locs)) == len(all_locs)


wordsearch_problem.add_constraint(WordSearchConstraint(words))
solution = wordsearch_problem.backtracking_search({})
if solution is None:
    print('No solution')
else:
    G.set_config(solution)
    print(G)


