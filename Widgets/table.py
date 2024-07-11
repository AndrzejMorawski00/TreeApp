from typing import List, Type, Optional
from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QBoxLayout

from event_aggregator import IEventAggregator
from tree_nodes import DataHandler, Person


class TableWidget(QWidget):
    def __init__(self, data_handler: DataHandler, event_aggregator: IEventAggregator, parent=None):
        super().__init__()
        self.data = data_handler.get_data()
        self.table_layout = QBoxLayout(QBoxLayout.Direction.Down)
        self.table: Optional[QTableWidget] = None
        self.setLayout(self.table_layout)

    def generate_table_widget(self, data_type: Type[Person]):
        table_data: List[Person] = []
        for key, values in self.data.items():
            if key.__name__ == data_type.__name__:
                table_data = values
                break

        if self.table:
            self.table_layout.removeWidget(self.table)

        table_header = data_type.fields
        new_table = QTableWidget(len(table_data), len(table_header) - 1)
        new_table.setHorizontalHeaderLabels(table_header[1:])
        header = new_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for col, person in enumerate(table_data):
            for row, (key, value) in enumerate(person.data.items()):
                if row > 0:
                    new_table.setItem(
                        col, row - 1, QTableWidgetItem(str(value)))

        new_table.cellClicked.connect(self.handle_table_row_click)
        self.table = new_table

        self.table_layout.addWidget(self.table)

    def handle_table_row_click(self):
        pass
