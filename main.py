from typing import Optional
import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QStackedWidget


from Widgets.form import FormWidget
from Widgets.table import TableWidget
from Widgets.tree import TreeWidget
from event_aggregator import EventAggregator, IEventAggregator
from tree_nodes import DataHandler, Person,  get_initial_data
from PyQt6.QtGui import QPalette, QColor


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class AppWindow(QMainWindow):
    def __init__(self, data_handler: DataHandler, event_aggregator: IEventAggregator):
        super().__init__()
        self.data_handler = data_handler
        self.event_aggregator = event_aggregator
        self.subscribe_events()
        self.app_widget = QWidget()
        self.app_layout = QHBoxLayout()

        self.main_widget = QStackedWidget()
        self.tree_widget = TreeWidget(data_handler, event_aggregator)
        self.form_widget = FormWidget(data_handler, event_aggregator)
        self.table_widget = TableWidget(data_handler, event_aggregator)
        self.main_widget.addWidget(self.form_widget)
        self.main_widget.addWidget(self.table_widget)

        self.app_layout.addWidget(self.tree_widget)
        self.app_layout.addWidget(self.main_widget)

        self.setMinimumWidth(1200)
        self.setMinimumHeight(700)

        self.app_widget.setLayout(self.app_layout)
        self.setCentralWidget(self.app_widget)

    def subscribe_events(self):
        self.event_aggregator.add_subscriber(
            'TreeRootClicked', self.generate_table)

        self.event_aggregator.add_subscriber(
            'TreeNodeClicked', self.generate_form)

        self.event_aggregator.add_subscriber(
            'NewUserClicked', self.generate_form)

        self.event_aggregator.add_subscriber('CloseForm', self.close_form)

    def generate_table(self, data_type: type[Person]):
        self.table_widget.generate_table_widget(data_type)
        self.main_widget.setCurrentIndex(1)

    def generate_form(self, data_type: type[Person], data: Optional[Person]):
        form_type = 'Edit' if data else 'Add'
        id = data.data['id'] if data else None
        self.form_widget.generate_form(data_type, id, form_type)
        self.main_widget.setCurrentIndex(0)

    def close_form(self):
        self.form_widget.clear_form()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow(data_handler=get_initial_data(),
                       event_aggregator=EventAggregator())
    window.show()
    app.exec()
