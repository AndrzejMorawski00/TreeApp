from typing import Dict
from typing import List, TypedDict, Dict
from uuid import uuid4, UUID
from datetime import date


class Person:
    class TypedPerson(TypedDict):
        f_name: str
        l_name: str
        pesel: str
        birth_date: date

    fields: List[str] = ['id', 'First Name',
                         'Last Name', 'Pesel', 'Birth Date']

    def __init__(self, f_name: str, l_name: str, pesel: str, birth_date: date) -> None:
        self.id: UUID = uuid4()
        self.data: Person.TypedPerson = {
            'f_name': f_name,
            'l_name': l_name,
            'pesel': pesel,
            'birth_date': birth_date,
        }

    @classmethod
    def create_instance(cls, data: TypedPerson):
        return cls(
            f_name=data['f_name'],
            l_name=data['l_name'],
            pesel=data['pesel'],
            birth_date=data['birth_date']
        )

    @staticmethod
    def get_data_types() -> Dict[str, str]:
        return Person.TypedPerson.__annotations__

    def __str__(self) -> str:
        return f'{self.data['f_name']} {self.data['l_name']}'


class Student(Person):
    class TypedStudent(Person.TypedPerson):
        index: int

    fields = Person.fields + ['Index']

    def __init__(self, f_name: str, l_name: str, pesel: str, birth_date: date, index: int) -> None:
        super().__init__(f_name, l_name, pesel, birth_date)
        self.data: Student.TypedStudent = {
            **self.data,
            'index': index
        }

    @classmethod
    def create_instance(cls, data: TypedStudent):
        return cls(
            f_name=data['f_name'],
            l_name=data['l_name'],
            pesel=data['pesel'],
            birth_date=data['birth_date'],
            index=data['index'],
        )

    @staticmethod
    def get_data_types() -> Dict[str, str]:
        return Student.TypedStudent.__annotations__


class Lecturer(Person):
    class TypedLecturer(Person.TypedPerson):
        degree: str

    fields = Person.fields + ['Degree']

    def __init__(self, f_name: str, l_name: str, pesel: str, birth_date: date, degree: str) -> None:
        super().__init__(f_name, l_name, pesel, birth_date)
        self.data: Lecturer.TypedLecturer = {
            **self.data,
            'degree': degree
        }

    @classmethod
    def create_instance(cls, data: TypedLecturer):
        return cls(
            f_name=data['f_name'],
            l_name=data['l_name'],
            pesel=data['pesel'],
            birth_date=data['birth_date'],
            degree=data['degree'],
        )

    @staticmethod
    def get_data_types() -> Dict[str, str]:
        return Lecturer.TypedLecturer.__annotations__
