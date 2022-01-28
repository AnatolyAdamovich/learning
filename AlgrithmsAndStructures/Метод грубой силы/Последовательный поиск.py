"""
Поочередное сравнение элементов
заданного массива с ключом поиска до тех пор,
пока не будет найден искомый ключ
или пока весь массив не будет проверен
"""

def SequentialSearch(Array, K):
    length = len(Array)
    # добавим ключ поиска для того,
    # чтобы поиск был всегда успешный
    Array.append(K)
    i = 0
    while Array[i] != K:
        i += 1
    if i < length:
        return i
    else:
        return -1

example = [i for i in range(10,100,10)]
print('example = ', example)
print('index of 20: ', SequentialSearch(example, 20))
print('index of 90: ', SequentialSearch(example, 90))
print('index of 45: ', SequentialSearch(example, 45))


# Алгоритм последовательного поиска линейный по времени
# как в среднем, так и в худшем случаях
# O(n)
