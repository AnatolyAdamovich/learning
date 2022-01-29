"""
Задача:
во множестве из n точек найти две, расположенные друг к другу ближе всего
Применяется Евклидова метрика (сумма квадратов разницы)

ClosestPoints:
вычислить расстояние между каждой парой точек
и найти пару с наименьшим расстоянием
для того, чтобы избежать повтороного вычисления расстояния,
рассматриваются только пары P_i, P_j
где i < j
"""
from math import sqrt, inf

def ClosestPoints(P):
    min_distance = inf
    n = len(P)
    result = (-1,-1)
    for i in range(n-1):
        x_i, y_i = P[i]
        for j in range(i+1, n):
            x_j, y_j = P[j]
            distance = sqrt((x_i-x_j)**2+(y_i-y_j)**2)
            if distance < min_distance:
                min_distance = distance
                result = (i, j)
    return result

example = [(1, 1), (10, 20), (92, 10), (10, 3), (5, 3), (0.5, 3)]
index1, index2 = ClosestPoints(example)
print(f'Индексы ближайших точек: {index1}, {index2}')
print(f'Ближайшие точки - {example[index1]} и {example[index2]}')


# Базовой (основной) операцией в данном алгоритме
# является вычисление Евклидовой метрики
# (особенность в том, что квадратный корень - это почти всегда иррациональнео число)
# Однако в случае этой задачи можно избежать вычисление квадратного корня, просто сравнивая суммы квадратов

def ClosestPointsWithoutSqrt(P):
    min_distance = inf
    n = len(P)
    result = (-1,-1)
    for i in range(n-1):
        x_i, y_i = P[i]
        for j in range(i+1, n):
            x_j, y_j = P[j]
            distance = (x_i-x_j)**2+(y_i-y_j)**2
            if distance < min_distance:
                min_distance = distance
                result = (i, j)
    return result


index1, index2 = ClosestPointsWithoutSqrt(example)
print(f'Индексы ближайших точек: {index1}, {index2}')
print(f'Ближайшие точки - {example[index1]} и {example[index2]}')

# Теперь базовой операцией является возведение в квадрат
# На каждую пару по два возведения
# Значит общее число: 2 * [(n-1) + (n-2) + ... + 1] = n * (n-1)
# Время работы - Teta(n^2)
