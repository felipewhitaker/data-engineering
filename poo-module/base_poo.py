import datetime
from typing import List

class Person:

    def __init__(self, name: str, surname: str, birthday: datetime.date):
        self.name = name
        self.surname = surname
        self.birthday = birthday

    @property
    def age(self) -> int:
        return int((datetime.date.today() - self.birthday).days / 365.2425)

    def __str__(self) -> str:
        return f'{self.name} {self.surname} born in {self.birthday} has {self.age} years'

class Professional(Person):

    def __init__(self, name: str, surname: str, birthday: datetime.date, exp: List[str]):
        super().__init__(name, surname, birthday)
        self.exp = exp
        return

    @property
    def current_job(self) -> str:
        return self.exp[-1]

    def __str__(self) -> str:
        return super(Professional, self).__str__() + f' and the current job is {self.current_job}, having had {len(self.exp)} experiences'

    def add_job(self, exp: str) -> None:
        self.exp.append(exp)
        return 



if __name__ == '__main__':
    pe = Person('Luiza', 'Ferraz', datetime.date(1997, 12, 4))
    print(pe.age)
    print(pe)

    pro = Professional('Felipe', 'Whitaker', datetime.date(1998, 6, 26), ['intern', 'engineer'])
    print(pro)

    pro.add_job('scientist')
    print(pro)