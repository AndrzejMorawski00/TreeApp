from uuid import UUID
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QDateTimeEdit, QTimeEdit, QDateEdit
from typing import Any, Dict, Optional, Type, Literal, cast
from PyQt6.QtCore import QDate, QDateTime, QTime
from PyQt6.QtGui import QIntValidator
from tree_nodes import DataHandler, Person
from event_aggregator import IEventAggregator


from remove_objects import remove_objects


class FormWidget(QWidget):
    def __init__(self, data_handler: DataHandler, event_aggregator: IEventAggregator, parent=None):
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

    def clear_form(self):
        remove_objects(self.form_layout)

    def set_input_value(self, input_widget: QWidget, value):
        if isinstance(input_widget, QLineEdit):
            input_widget.setText(str(value))
        elif isinstance(input_widget, QCheckBox):
            input_widget.setChecked(value)
        elif isinstance(input_widget, QDateEdit) and isinstance(value, QDate):
            input_widget.setDate(value)
        elif isinstance(input_widget, QDateTimeEdit) and isinstance(value, QDateTime):
            input_widget.setDateTime(value)
        elif isinstance(input_widget, QTimeEdit) and isinstance(value, QTime):
            input_widget.setTime(value)

    def get_input_value(self, input_widget: QWidget):
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

    def return_input_values(self, form_dict: Dict[QLabel, QWidget], type: Type[Person]):
        dict_keys = list(type.__annotations__.keys())
        print(form_dict, dict_keys)
        values = {}
        for idx, (_, widget) in enumerate(form_dict.items()):
            values[dict_keys[idx]] = self.get_input_value(widget)
        return cast(type.TypedPerson, values)

    def generate_form(self, dict_key: Type[Person], id: Optional[UUID], form_type: Literal['Edit', 'Add']):
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
        try:
            self.submit_button.clicked.connect(
                lambda: self.handle_form_button_click(form_type, id,  dict_key))
            self.cancel_button.clicked.connect(
                lambda: self.handle_form_button_click('Cancel', None,  dict_key))
        except Exception as e:
            print(e)
        self.form_layout.addWidget(self.submit_button)
        self.form_layout.addWidget(self.cancel_button)

    def handle_form_button_click(self, action: Literal['Edit', 'Add', 'Cancel'], id: Optional[UUID],  type: Type[Person]):
        values = self.return_input_values(self.form_dict, type)
        if action == 'Add':
            new_person = type.create_instance(values)
            self.data_handler.add_item(new_person)
            self.event_aggregator.publish('CloseForm')
            self.event_aggregator.publish('GenerateTree')
        elif action == 'Edit' and id:
            new_instance = type.create_instance(values)
            self.data_handler.modyfy_item(type, id, new_instance)
            self.event_aggregator.publish('CloseForm')
            self.event_aggregator.publish('GenerateTree')
        elif action == 'Cancel':
            self.event_aggregator.publish('CloseForm')
        else:
            raise ValueError('Invalid Action')
