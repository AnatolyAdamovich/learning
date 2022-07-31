'''
Последовательное сравнение и обмен элементов,
находящихся в неправильном порядке,
приведут к тому, что наибольший (наименьший) элемент
будет всплывать (падать) в конец (начало) списка
'''

def bubble_sort_up(A):
    n = len(A)
    for i in range(0, n-1):
        for j in range(0, n-1-i):
            if A[j+1] < A[j]:
                A[j], A[j+1] = A[j+1], A[j]

# Внешний цикл показывает: по какой части списка делаем перебор
# на i-том шаге просматриваем n-i-1 элементов
# (i = [0 to (n-2)])

# Таким образом, на каждой i-м проходе внешнего цикла
# внутренний цикл делает перебор из n-i-1 элемента так,
# что к концу внутреннего цикла наибольший элемент
# всплывает на место n-i-1 в списке

example = [89, 45, 68, 90, 29, 34, 17]
print(f'example before bubble sort: {example}')
bubble_sort_up(example)
print(f'example after bubble sort (up): {example}')


## Другой вариант
def bubble_sort_down(A):
    n = len(A)
    for i in range(0, n-1):
        for j in range(n-1, i, -1):
            if A[j] > A[j-1]:
                A[j], A[j-1] = A[j-1], A[j]

bubble_sort_down(example)
print(f'example after bubble sort (down): {example}')


# Трудоемкость данного алгоритма зависит как от количественной,
# так и от параметрической составляющих, поскольку
# количество сравнений зависит только от длины входного списка (T(n)=teta(n^2)),
# а количество обменов зависит от содержания списка (T(n)=teta(n^2)
# в случае "обратноотсортированного" списка)

def bubble_sort_better(A):
    n = len(A)
    for i in range(0, n-1):
        flag = False
        for j in range(0, n-1-i):
            if A[j+1] < A[j]:
                flag = True
                A[j], A[j+1] = A[j+1], A[j]
        if flag == False:
            print('List is already sorted')
            return

# Улучшенная сортировка дает прирост по времени
# (позволяет остановиться в том случае, когда список уже отсортирован)
# но для худшего случая сложность остается такой же

example = [4, 3, 2, 1]
print('Second example: {}'.format(example))
bubble_sort_better(example)
print(f'Second example after sort: ', example)


example = [10, 20, 30, 50, 60]
print('Third example: {}'.format(example))
bubble_sort_better(example)
print(f'Third example after sort: ', example)