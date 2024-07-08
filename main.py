from typing import TypedDict


class Person(TypedDict):
    id: str


class Student(TypedDict):
    index: int
    first_name: str
    last_name: str
    pesel: str
    birth_date: str


