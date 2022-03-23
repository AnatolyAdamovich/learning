from abc import abstractmethod

# базовый класс для всех ограничений
# variables - переменные, на которые наложено данное ограничение
# satisfied - абстрактный метод (тот, который нужно будет переопределить в производных классах)
# метод будет проверять выполнение ограничения для определенной конфигурации
# под configuration понимается определенный набор значений переменных


class Constraint:
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, configuration):
        pass


# общий класс для задач с ограничениями
class CSP:
    def __init__(self, variables, domains):
        self.variables = variables # список переменных
        self.domains = domains  # словарик с областью определения для каждой переменной
        self.constraints = dict()  # словарик с ограничениями (на каждую переменную список ограничений)
        for v in variables:
            self.constraints[v] = []

    def add_constraint(self, constraint):
        for v in constraint.variables:
            self.constraints[v].append(constraint)

    def checking(self, variable, configuration):
        # variable - переменная из configuration
        # для нее устраивается проверка на выполнение ограничений
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(configuration):
                return False
        return True

    # поиск с возвратами - подход, при котором, если поиск зашел в тупик,
    # то он возвращается к последней известной точки, где было принято решение перед тем,
    # как зайти в тупик, и выбирает другой путь (очень похож на DFS)
    # будем использовать поиск с возвратами для нахождения ДОПУСТИМОЙ конфигурации
    def backtracking_search(self, configuration):
        if len(configuration) == len(self.variables):
            # допустимая конфигурация найдена (все переменные имеют значение)
            return configuration
        not_used = [v for v in self.variables if v not in configuration.keys()]
        element_with_no_value = not_used[0]
        for value in self.domains[element_with_no_value]:
            # будем присваивать значения из обл. определения
            new_configuration = configuration.copy()
            new_configuration[element_with_no_value] = value
            if self.checking(element_with_no_value, new_configuration):
                # если подставленное значение не нарушает ограничений, то спускаемся дальше
                result_config = self.backtracking_search(new_configuration)
                if result_config is not None:
                    return result_config
        return None


