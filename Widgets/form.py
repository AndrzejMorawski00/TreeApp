from uuid import UUID
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QDateTimeEdit, QTimeEdit, QDateEdit
from typing import Any, Dict, Optional, Type, Literal, cast
from PyQt6.QtCore import QDate, QDateTime, QTime
from PyQt6.QtGui import QIntValidator
from datetime import date, datetime, time
from people.people import Person
from people.DataHandler import DataHandler
from event_aggregator import IEventAggregator


from remove_objects import remove_objects


class FormWidget(QWidget):
    def __init__(self, data_handler: DataHandler, event_aggregator: IEventAggregator, parent=None) -> None:
        super().__init__()
        self.data_handler = data_handler
        self.event_aggregator = event_aggregator
        self.form_layout = QVBoxLayout()
        self.setLayout(self.form_layout)

    def get_input(self, data_type: str) -> QWidget:
        int_input = QLineEdit()
        int_input.setValidator(QIntValidator(100000, 999999))
        input_dict = {
            'str': QLineEdit(),
            'int': int_input,
            'date': QDateEdit(),
            'datetime': QDateTimeEdit(),
            'time': QTimeEdit(),
            'bool': QCheckBox()
        }
        return input_dict.get(data_type, QLineEdit())

    def clear_form(self) -> None:
        remove_objects(self.form_layout)

    def set_input_value(self, input_widget: QWidget, value: Any) -> None:
        if isinstance(input_widget, QLineEdit):
            input_widget.setText(str(value))
            print('xD-1')
        elif isinstance(input_widget, QCheckBox):
            input_widget.setChecked(value)
            print('xD0')
        elif isinstance(input_widget, QDateEdit) and isinstance(value, date):
            qt_date = QDate(value.year, value.month, value.day)
            input_widget.setDate(qt_date)
            input_widget.setDisplayFormat("dd/MM/yyyy")
        elif isinstance(input_widget, QDateTimeEdit) and isinstance(value, datetime):
            qt_datetime = QDateTime(
                value.year, value.month, value.day, value.hour, value.minute, value.second)
            input_widget.setDateTime(qt_datetime)
            input_widget.setDisplayFormat("dd/MM/yyyy, hh::mm:ss")
        elif isinstance(input_widget, QTimeEdit) and isinstance(value, time):
            qt_time = QTime(value.hour, value.second)
            input_widget.setTime(qt_time)
            input_widget.setDisplayFormat('hh:mm')

    def get_input_value(self, input_widget: QWidget) -> Any:
        if isinstance(input_widget, QLineEdit):
            value = input_widget.text() or ''
            if input_widget.validator():
                return int(value)
            return value
        elif isinstance(input_widget, QCheckBox):
            return input_widget.isChecked()
        elif isinstance(input_widget, QDateEdit):
            return input_widget.date().toPyDate()
        elif isinstance(input_widget, QDateTimeEdit):
            return input_widget.dateTime().toPyDateTime()
        elif isinstance(input_widget, QTimeEdit):
            return input_widget.time().toPyTime()

    def return_input_values(self, form_dict: Dict[QLabel, QWidget], person_type: Type[Person]) -> Person.TypedPerson:
        dict_keys = list(person_type.get_data_types().keys())
        values = {}
        for idx, (_, widget) in enumerate(form_dict.items()):
            values[dict_keys[idx]] = self.get_input_value(widget)
        return cast(Person.TypedPerson, values)

    def generate_form(self, dict_key: Type[Person], id: Optional[UUID], form_type: Literal['Edit', 'Add']) -> None:
        self.clear_form()

        fields = dict_key.fields
        self.form_dict: Dict[QLabel, QWidget] = {}
        user_data: Optional[Person] = None

        if id:
            user_data = self.data_handler.get_item(dict_key, id)
            for idx, (_, value) in enumerate(user_data.data.items()):
                label = QLabel(f'{fields[idx + 1]}:')
                input = self.get_input(type(value).__name__)
                self.form_dict[label] = input
                if form_type == 'Edit':
                    print(input, type(value))
                    self.set_input_value(input, value)
                self.form_layout.addWidget(label)
                self.form_layout.addWidget(input)
        else:
            data = list(
                zip(list(dict_key.get_data_types().values()), fields[1:]))
            for idx, (cls, field) in enumerate(data):
                label = QLabel(field)
                input = self.get_input(cls)
                self.form_dict[label] = input
                self.form_layout.addWidget(label)
                self.form_layout.addWidget(input)

        self.submit_button = QPushButton(form_type)
        self.cancel_button = QPushButton('Cancel')
        self.submit_button.clicked.connect(
            lambda: self.handle_form_button_click(form_type, id,  dict_key))
        self.cancel_button.clicked.connect(
            lambda: self.handle_form_button_click('Cancel', None,  dict_key))

        self.form_layout.addWidget(self.submit_button)
        self.form_layout.addWidget(self.cancel_button)

    def handle_form_button_click(self, action: Literal['Edit', 'Add', 'Cancel'], id: Optional[UUID],  data_type: Type[Person]) -> None:
        person_dict = self.return_input_values(self.form_dict, data_type)
        if action == 'Add':
            new_person = data_type.create_instance(person_dict)
            self.data_handler.add_item(new_person)
            self.event_aggregator.publish('CloseForm')
            self.event_aggregator.publish('GenerateTree')
        elif action == 'Edit' and id:
            self.data_handler.modyfy_item(data_type, id, person_dict)
            self.event_aggregator.publish('CloseForm')
            self.event_aggregator.publish('GenerateTree')
        elif action == 'Cancel':
            self.event_aggregator.publish('CloseForm')
        else:
            raise ValueError('Invalid Action')
