from typing import List, Type
from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QTableWidgetItem

from event_aggregator import IEventAggregator
from tree_nodes import DataHandler, Person


class TableWidget(QWidget):
    def __init__(self, data_handler: DataHandler, event_aggregator: IEventAggregator, parent=None):
        super().__init__(parent)
        self.data = data_handler.get_data()

    def generate_table_widget(self, data_type: Type[Person]) -> QTableWidget:
        table_data: List[Person] = []
        for key, values in self.data.items():
            if key.__name__ == data_type.__name__:
                table_data = values
                break

        table_header = data_type.fields
        table = QTableWidget(len(table_data), len(table_header) - 1)
        table.setHorizontalHeaderLabels(table_header[1:])
        header = table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for col, person in enumerate(table_data):
            for row, (key, value) in enumerate(person.data.items()):
                if row > 0:
                    table.setItem(col, row - 1, QTableWidgetItem(str(value)))

        table.cellClicked.connect(self.handle_table_row_click)
        return table

    def handle_table_row_click(self):
        pass
