'''
-- Сортировка
Исходный массив делится на две половины
Каждая из половин сортируется
Слияние двух половин

-- Слияние
Поэлементное сравнение элементов сливаемых массивов (от начала)
Меньший из сравниваемых элементов добавляется в результат
В массиве, из которого был выбран меньший элемент,
происходит сдвиг указателя на 1 элемент вправо
Операция повторяется до тех пор,
пока один из сливаемых массивов не будет исчерпан
'''

def mergesort(array):
    ## сортировка
    length = len(array)
    if length > 1:
        temp_first_half = array[:length//2]
        temp_second_half = array[length//2:]

        temp_first_half = mergesort(temp_first_half)
        temp_second_half = mergesort(temp_second_half)

        array = merge(temp_first_half, temp_second_half, array)
    return array

def merge(first, second, main):
    ## слияние
    p = len(first)
    q = len(second)
    i, j, k = 0, 0, 0

    # основной цикл
    while i < p and j < q:
        if first[i] < second[j]:
            main[k] = first[i]
            i += 1
        else:
            main[k] = second[j]
            j += 1
        k += 1
    # если один из массивов исчерпан
    if i == p:
        main[k:] = second[j:]
    else:
        main[k:] = first[i:]

    return main

example = [8, 3, 2, -10, 202, 0, 1.1, 9, 7, 1, 28, 4, 5, 2, -21, 0.4]
print(f'Пример: {example}')
print(f'После сортировки: {mergesort(example)}')


# Время работы: T(n) = 2 * T(n/2) + (n-1)
# где T(n/2) означает, что задача каждый раз разбивается на 2 подзадачи
# (n-1) - количество сравнений при слиянии в худшем случае
#
# Решая данное уравнение, получим: T(n) = n * (log_2(n) - 1) + 1
# Основной недостаток - необходимость доп. памяти,
# количество которой пропорционально размеру входных данных