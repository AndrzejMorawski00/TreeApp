from typing import List, TypedDict, Type, Dict
from uuid import uuid4, UUID
from datetime import date


class Person:
    class TypedPerson(TypedDict):
        id: UUID
        f_name: str
        l_name: str
        pesel: str
        birth_date: date

    fields: List[str] = ['id', 'First Name',
                         'Last Name', 'Pesel', 'Birth Date']

    def __init__(self, f_name: str, l_name: str, pesel: str, birth_date: date) -> None:

        self.data: Person.TypedPerson = {
            'id': uuid4(),
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
            index=data['index'],
            f_name=data['f_name'],
            l_name=data['l_name'],
            pesel=data['pesel'],
            birth_date=data['birth_date']
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
            degree=data['degree'],
            f_name=data['f_name'],
            l_name=data['l_name'],
            pesel=data['pesel'],
            birth_date=data['birth_date']
        )

    @staticmethod
    def get_data_types() -> Dict[str, str]:
        return Lecturer.TypedLecturer.__annotations__


class DataHandler:
    def __init__(self) -> None:
        self.data_dict: Dict[Type[Person], List[Person]] = {}

    def add_item(self, item: Person) -> None:
        object_type: Type[Person] = type(item)
        if object_type not in self.data_dict:
            self.data_dict[object_type] = []
        self.data_dict[object_type].append(item)

    def in_dict(self, dict_key: Type[Person]) -> bool:
        return dict_key in self.data_dict

    def remove_item(self, dict_key: Type[Person], id: UUID) -> None:
        if self.in_dict(dict_key):
            item_list = self.data_dict[dict_key]
            self.data_dict[dict_key] = [
                x for x in item_list if x.data['id'] != id]
        else:
            raise KeyError("This Data Type wasn't registred in dict")

    def get_item(self, dict_key: Type[Person], id: UUID) -> Person:
        if self.in_dict(dict_key):
            item = list(filter(lambda x: x.data['id']
                               == id, self.data_dict[dict_key]))
            if item:
                return item[0]
            else:
                raise ValueError("Object doesn't exist")
        else:
            raise KeyError("This Data Type wasn't registred in dict")

    def modyfy_item(self, dict_key: Type[Person], id: UUID, new_value: Person) -> None:
        if self.in_dict(dict_key):
            for index, item in enumerate(self.data_dict[dict_key]):
                if item.data['id'] == id:
                    self.data_dict[dict_key][index] = new_value
        else:
            raise KeyError("This Data Type wasn't registred in dict")

    def get_data(self) -> Dict[Type[Person], List[Person]]:
        return self.data_dict


def get_initial_data() -> DataHandler:
    data_handler: DataHandler = DataHandler()
    students: List[Student] = [Student('Jan', 'Kowalski', '00474340210', date(2001, 2, 4), 434222),
                               Student('Tomasz', 'Kowalski', '00474340210',
                                       date(2001, 2, 4), 434222),
                               Student('Michał', 'Kowalski', '00474340210',
                                       date(2001, 2, 4), 434222),
                               Student('Jan', 'Kowalski', '00474340210',
                                       date(2001, 2, 4), 434222),
                               Student('Krzysztof', 'Kowalski', '00474340210',
                                       date(2001, 2, 4), 434222),
                               Student('Jan', 'Kowalski', '00474340210',
                                       date(2001, 2, 4), 434222),
                               Student('Bożydar', 'Kowalski', '00474340210',
                                       date(2001, 2, 4), 434222),
                               Student('Jan', 'Kowalski', '00474340210',  date(2001, 2, 4), 434222)]

    lecturers: List[Lecturer] = [Lecturer('Tomasz', 'Kot', '78021298652', date(1978, 7, 4), 'Full professor'),
                                 Lecturer('Tomasz', 'Kot', '78021298652',
                                          date(1978, 7, 4), 'Full professor'),
                                 Lecturer('Tomasz', 'Kot', '78021298652',
                                          date(1978, 7, 4), 'Full professor'),
                                 Lecturer('Tomasz', 'Kot', '78021298652',
                                          date(1978, 7, 4), 'Full professor'),
                                 Lecturer('Tomasz', 'Kot', '78021298652',
                                          date(1978, 7, 4), 'Full professor'),
                                 Lecturer('Tomasz', 'Kot', '78021298652', date(1978, 7, 4), 'Full professor')]
    for student in students:
        data_handler.add_item(student)

    for lecturer in lecturers:
        data_handler.add_item(lecturer)

    return data_handler
