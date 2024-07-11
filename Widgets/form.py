from uuid import UUID
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QDateTimeEdit, QLayout, QLayoutItem, QTimeEdit, QDateEdit
from typing import Any, Dict, Optional, Type, Literal
from PyQt6.QtCore import QDate, QDateTime, QTime
from tree_nodes import DataHandler, Person
from event_aggregator import IEventAggregator


def remove_objects(layout: QLayout):
    for i in reversed(range(layout.count())):
        layout_item: Optional[QLayoutItem] = layout.itemAt(i)
        if layout_item:
            widget = layout_item.widget()
            if widget:
                widget.setParent(None)
                layout.removeWidget(widget)
            else:
                next_layout = layout_item.layout()
                if next_layout:
                    remove_objects(next_layout)


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
        remove_objects(self.form_layout)

        fields = dict_key.fields
        form_dict: Dict[QLabel, QWidget] = {}
        user_data: Optional[Person] = None

        if id:
            user_data = self.data_handler.get_item(dict_key, id)
            for idx, (_, value) in enumerate(user_data.data.items()):
                if idx > 0:
                    label = QLabel(fields[idx])
                    input = self.get_input(type(value).__name__)
                    form_dict[label] = input
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
                    form_dict[label] = input
                    self.form_layout.addWidget(label)
                    self.form_layout.addWidget(input)

        submit_button = QPushButton(form_type)
        cancel_button = QPushButton('Cancel')
        self.form_layout.addWidget(submit_button)
        self.form_layout.addWidget(cancel_button)
