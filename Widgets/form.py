from uuid import UUID
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QDateTimeEdit, QTimeEdit, QDateEdit
from typing import Dict, Optional, Type, Literal
from PyQt6.QtCore import QDate, QDateTime, QTime
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
        input_dict = {
            'str': QLineEdit(),
            'int': QLineEdit(),
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

    def generate_form(self, dict_key: Type[Person], id: UUID | None, form_type: Literal['Edit', 'Add']):
        self.clear_form()

        fields = dict_key.fields
        self.form_dict: Dict[QLabel, QWidget] = {}
        user_data: Optional[Person] = None

        if id:
            user_data = self.data_handler.get_item(dict_key, id)
            for idx, (_, value) in enumerate(user_data.data.items()):
                if idx > 0:
                    label = QLabel(f'{fields[idx]}:')
                    input = self.get_input(type(value).__name__)
                    self.form_dict[label] = input
                    if form_type == 'Edit':
                        self.set_input_value(input, value)
                    self.form_layout.addWidget(label)
                    self.form_layout.addWidget(input)
        else:
            data = list(zip(list(dict_key.get_data_types().values()), fields))
            for idx, (cls, field) in enumerate(data):
                if idx > 0:
                    label = QLabel(field)
                    input = self.get_input(cls)
                    self.form_dict[label] = input
                    self.form_layout.addWidget(label)
                    self.form_layout.addWidget(input)

        self.submit_button = QPushButton(form_type)
        self.cancel_button = QPushButton('Cancel')
        try:
            self.submit_button.clicked.connect(
                lambda: self.handle_form_button_click(form_type, dict_key))
            self.cancel_button.clicked.connect(
                lambda: self.handle_form_button_click('Cancel', dict_key))
        except Exception as e:
            print(e)
        self.form_layout.addWidget(self.submit_button)
        self.form_layout.addWidget(self.cancel_button)

    def handle_form_button_click(self, action: Literal['Edit', 'Add', 'Cancel'], type: Type[Person]):
        print('Handle Click', action)
        if action == 'Add':
            data = []
            for value in self.form_dict.values():
                print(value)
        elif action == 'Edit':
            data = []
            for value in self.form_dict.values():
                print(value)
        elif action == 'Cancel':
            print("Close Form")
            self.event_aggregator.publish('CloseForm')
        else:
            raise ValueError('Invalid Action')
