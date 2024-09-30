from typing import List, Type, Optional
from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QBoxLayout, QTableWidget, QPushButton

from event_aggregator import IEventAggregator
from people.DataHandler import DataHandler
from people.people import Person


class TableWidget(QWidget):
    def __init__(self, data_handler: DataHandler, event_aggregator: IEventAggregator, parent=None) -> None:
        super().__init__()
        self.data_handler = data_handler
        self.event_aggregator = event_aggregator
        self.table_layout = QBoxLayout(QBoxLayout.Direction.Down)
        self.table: Optional[QTableWidget] = None
        self.setLayout(self.table_layout)

    def generate_table_widget(self, data_type: Type[Person]) -> None:
        data = self.data_handler.get_data()
        table_data: List[Person] = []
        for key, values in data.items():
            if key.__name__ == data_type.__name__:
                table_data = values
                break

        if self.table:
            self.table_layout.removeWidget(self.table)

        table_header = data_type.fields + ['Delete']
        new_table = QTableWidget(len(table_data), len(table_header) - 1)
        new_table.setHorizontalHeaderLabels(table_header[1:])
        header = new_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for col, person in enumerate(table_data):
            for row, (key, value) in enumerate(person.data.items()):
                if row == len(person.data.items()) - 1:
                    delete_button = QPushButton()
                    delete_button.setText('Delete')
                    delete_button.clicked.connect(
                        lambda checked, p=person: self.handle_delete_button_clicked(p))
                    new_table.setCellWidget(col, row + 1, delete_button)

                new_table.setItem(
                    col, row, QTableWidgetItem(str(value)))

        self.table = new_table

        self.table_layout.addWidget(self.table)

    def handle_delete_button_clicked(self, person: Person) -> None:
        self.data_handler.remove_item(type(person), person.id)
        self.event_aggregator.publish('GenerateTable', type(person))
        self.event_aggregator.publish('GenerateTree')
