#### Задача о 8 ферзях
# Есть шахматная доска размерами 8х8.
# Необходимо расставить 8 ферзей так, чтобы ни один ферзь не смог атаковать другого.
#
# Ферзь - это фигура, которая может перемещаться
# на любое количество клеток по горизонтали, по вертикали и по диагонали.
# Если за один ход ферзь может переместиться на клетку, на которой стоит другая фигура,
# то считается, что ферзь наносит атаку этой фигуре

from structure import CSP, Constraint


class Place:
    def __init__(self):
        self.place = [[0 for _ in range(8)] for _ in range(8)]

    def update_config(self, configuration):
        for i in configuration.keys():
            self.place[i][configuration[i]] = 1

    def __repr__(self):
        res = 'Шахматная доска: \n    '
        for i in range(len(self.place)):
            res += f'{i + 1}  '
        res += "\n"
        for i in range(len(self.place)):
            res += f'{i + 1}  {self.place[i]}\n'
        return res


game = Place()
print(game)
# Переменными являются ферзи, которые можно описать координатой по горизонтали
# Тогда областью определения являются возможные вертикальные координаты (их всего 8)
queens = [i for i in range(8)]
queen_cols = dict()
for q in queens:
    queen_cols[q] = [i for i in range(8)]

queen_problem = CSP(variables=queens, domains=queen_cols)


class QueenConstraint(Constraint):
    def __init__(self, queen_rows):
        super().__init__(queen_rows)

    def satisfied(self, configuration):
        # надо сделать проверку только на возможность переместить по столбцу
        # и по диагонали
        for q1_rows, q1_cols in configuration.items():
            for q2_rows in range(q1_rows+1, len(self.variables)+1):
                if q2_rows in configuration:
                    q2_cols = configuration[q2_rows]
                    if q2_cols == q1_cols:
                        return False
                    if abs(q1_rows-q2_rows) == abs(q2_cols-q1_cols):
                        # ТЕОРЕМА: два ферзя на одной диагонали тогда и только тогда
                        # когда модуль разности их координат по строкам и по столбцам
                        # одинаков: |row(f1) - row(f2)| == |col(f1) - col(f2)|
                        return False
        return True


queen_problem.add_constraint(QueenConstraint(queens))
solution = queen_problem.backtracking_search({})
if solution is not None:
    game.update_config(solution)
    print(game)
else:
    print('Нет решений')
