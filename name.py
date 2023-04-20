# создание класса
class Person:
    # статические атрибуты
    name = "Lena"
    surname = "Shorokhova"

    def __init__(self, grade, work=None): #атрибут work не нужно явно передавать в классе-наследнике, так как у него есть значение(по умолчанию None)
        # динамические атрибуты
        self.work = work
        self._grade = grade #protected атрибут

    # методы класса
    def working(self, hours):
        if hours > 8:
            return 'Дайте умереть спокойно'
        else:
            return 'Ушла погулять'

    def sleeping(self, hours):
        if hours > 8:
            return 'Переспала, голова болит'
        elif hours == 8:
            return 'Намана, но работать не хочу'
        elif hours < 8:
            return 'Недоспала, голова болит'

    def get_grade(self):
        return self._grade

    def set_grade(self, new_grade):
        self._grade = new_grade
        return new_grade


Lena = Person("QA", "middle")
print(Lena.sleeping(9))  # выводим результат работы метода sleeping
print(Lena.work)  # выводим значение атрибута экземпляра класса
print(Lena.set_grade("Senior"))

# класс-наследник
class AutoQA(Person):
    def __init__(self, grade, work, language):
        super().__init__(grade, work)
        self.language = language

    def write_code(self): #не передаем атрибут language
        if self.language == 'Python': #используем атрибут экземпляра класса
            return "Молодец"
        else:
            return "Фу!"


LenaQA = AutoQA("junior", "QA", "Java")
print(LenaQA.write_code()) # не передаем никаких атрибутов, так как они переданы в экземпляр класса(строчка 47)
print(LenaQA.name)
print(LenaQA.sleeping(8))