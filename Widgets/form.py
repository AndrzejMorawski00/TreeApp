from uuid import UUID
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from typing import Any, Dict, Optional, Type,  Literal
from tree_nodes import DataHandler, Person
from event_aggregator import IEventAggregator


class FormWidget(QWidget):
    def __init__(self, data_handler: DataHandler, event_aggregator: IEventAggregator, parent=None):
        super().__init__()
        self.data_handler = data_handler
        self.event_aggregator = event_aggregator
        self.form_dict: Dict[QLabel, Any] = {}
        self.form_layout = QVBoxLayout()

    def generate_form(self, dict_key: Type[Person], id: UUID | None, form_type: Literal['Edit', 'Add']) -> QVBoxLayout:
        fields = dict_key.fields
        print(fields)
        user_data: Optional[Person] = None

        if id:
            user_data = self.data_handler.get_item(dict_key, id)
            for idx, (key, value) in enumerate(user_data.data.items()):
                if idx > 0:
                    print(key, value)

        return self.form_layout
