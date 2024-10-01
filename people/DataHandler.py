from datetime import date
from typing import List,  Type, Dict
from uuid import UUID
from people.people import Person, Student, Lecturer


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
                x for x in item_list if x.id != id]
        else:
            raise KeyError("This Data Type wasn't registred in dict")

    def get_item(self, dict_key: Type[Person], id: UUID) -> Person:
        if self.in_dict(dict_key):
            item = list(filter(lambda x: x.id
                               == id, self.data_dict[dict_key]))
            if item:
                return item[0]
            else:
                raise ValueError("Object doesn't exist")
        else:
            raise KeyError("This Data Type wasn't registred in dict")

    def modyfy_item(self, dict_key: Type[Person], id: UUID, new_values: Person.TypedPerson) -> None:
        if not dict_key.is_valid_data(new_values):
            raise ValueError('Invalid Person Data')

        if self.in_dict(dict_key):
            for item in self.data_dict[dict_key]:
                if item.id == id:
                    item.data = new_values
                    return
        raise KeyError("This Data Type wasn't registred in dict")

    def get_data(self) -> Dict[Type[Person], List[Person]]:
        return self.data_dict


def get_initial_data() -> DataHandler:
    data_handler: DataHandler = DataHandler()

    students: List[Student] = [
        Student('Jan', 'Kowalski', '00474340210', date(2001, 2, 4), 434222),
        Student('Tomasz', 'Nowak', '12345678901', date(2000, 3, 12), 434223),
        Student('Michał', 'Wiśniewski', '56789012345',
                date(1999, 5, 6), 434224),
        Student('Anna', 'Zielińska', '98765432109', date(2002, 7, 19), 434225),
        Student('Krzysztof', 'Mazur', '65432198765',
                date(2001, 11, 22), 434226),
        Student('Ewa', 'Kaczmarek', '34567890123', date(2000, 9, 15), 434227),
        Student('Bożydar', 'Górski', '23456789012', date(1999, 12, 2), 434228),
        Student('Janina', 'Wojciechowska',
                '10987654321', date(2001, 4, 17), 434229)
    ]

    lecturers: List[Lecturer] = [
        Lecturer('Tomasz', 'Kot', '78021298652',
                 date(1978, 7, 4), 'Full professor'),
        Lecturer('Agnieszka', 'Maj', '67010394821',
                 date(1980, 2, 13), 'Associate professor'),
        Lecturer('Piotr', 'Zawadzki', '89032145867',
                 date(1965, 10, 22), 'Assistant professor'),
        Lecturer('Maria', 'Lipska', '55042365489',
                 date(1975, 5, 30), 'Full professor'),
        Lecturer('Adam', 'Jankowski', '78091234765',
                 date(1982, 1, 11), 'Lecturer'),
        Lecturer('Barbara', 'Lewandowska', '65081245632',
                 date(1970, 8, 23), 'Senior lecturer')
    ]

    for student in students:
        data_handler.add_item(student)

    for lecturer in lecturers:
        data_handler.add_item(lecturer)

    return data_handler
