# Есть карта Австралии, на которой обозначено 7 регионов.
# Нужно раскрасить регионы разными цветами так,
# чтобы никакие два смежных региона не были окрашены в одинаковый цвет
# При этом всего есть 3 цвета

# Карта Австралии:
# Западная Австралия -- Северная территория - Квинсленд
# Западная Австралия -- Южная Австралия --- Новый Южный Уэльс
# Западная Австралия -- Южная Австралия --- Виктория
#                    --                 --- Тасмания

from structure import Constraint, CSP


# Переменные - регионы
# Области определения - цвета
# Ограничения - смежность регионов
class MapColoringConstraint(Constraint):
    def __init__(self, place1, place2):
        # place1 и place2 - это две смежные области
        super().__init__([place1, place2])
        self.p1 = place1
        self.p2 = place2

    def satisfied(self, configuration):
        if (self.p1 not in configuration) or (self.p2 not in configuration):
            # конфликт невозможен, если одна из областей ещё не раскрашена
            return True
        else:
            #  проверяем не совпадает ли цвет
            return configuration[self.p1] != configuration[self.p2]

variables = ['Западная Австралия', 'Северная территория', 'Южная Австралия',
             'Новый Южный Уэльс', 'Виктория', 'Тасмания', 'Квинсленд']
domains = dict()
for v in variables:
    domains[v] = ['Красный', 'Зеленый', 'Синий']

csp = CSP(variables, domains)
csp.add_constraint(MapColoringConstraint('Западная Австралия', 'Северная территория'))
csp.add_constraint(MapColoringConstraint('Западная Австралия', 'Южная Австралия'))
csp.add_constraint(MapColoringConstraint('Южная Австралия', 'Северная территория'))
csp.add_constraint(MapColoringConstraint('Квинсленд', 'Северная территория'))
csp.add_constraint(MapColoringConstraint('Квинсленд', 'Южная Австралия'))
csp.add_constraint(MapColoringConstraint('Квинсленд', 'Новый Южный Уэльс'))
csp.add_constraint(MapColoringConstraint('Новый Южный Уэльс', 'Южная Австралия'))
csp.add_constraint(MapColoringConstraint('Виктория', 'Южная Австралия'))
csp.add_constraint(MapColoringConstraint('Виктория', 'Новый Южный Уэльс'))
csp.add_constraint(MapColoringConstraint('Виктория', 'Тасмания'))

solution = csp.backtracking_search({})
for region in solution.keys():
    if region != 'padding':
        print(f'The color of <<{region}>> is {solution[region]}')

# В более сложной постановке задача звучит так:
# какое количество цветов потребуется для раскраски заданной карты?
# Существует "теорема о четырех красках", которая говорит:
# для раскраски любой карты (вне зависимости от количества регионов)
# потребуется не более четырех цветов. При этом раскрашиваемая местность должна быть представима
# в виде планарного графа (это необходимое и достаточное условие)
#
# Планарный граф - граф, в котором никакие ребра не пересекаются
# (можно *положить* на плоскость и не будет пересечений рёбер)