from typing import List, Optional

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTreeWidget, QTreeWidgetItem

from event_aggregator import IEventAggregator
from tree_nodes import DataHandler, Person
from remove_objects import remove_objects


class TreeWidget(QWidget):
    def __init__(self, data_handler: DataHandler, event_aggregator: IEventAggregator, parent=None):
        super().__init__(parent)
        self.event_aggregator = event_aggregator
        self.data_handler = data_handler
        self.data = data_handler.get_data()

        # Layout
        self.tree_layout = QVBoxLayout()
        self.setLayout(self.tree_layout)

        # Widgets
        self.label: Optional[QLabel] = None
        self.combo_box: Optional[QComboBox] = None
        self.tree: Optional[QTreeWidget] = None
        self.generate_widget()

    def generate_widget(self):
        remove_objects(self.tree_layout)
        self.label = QLabel('Add New Value to the Tree:')
        self.combo_box = self.generate_combo_box_widget()
        self.tree = self.generate_tree_widget()

        self.tree_layout.addWidget(self.label)
        self.tree_layout.addWidget(self.combo_box)
        self.tree_layout.addWidget(self.tree)

    def generate_combo_box_widget(self) -> QComboBox:
        combo_box = QComboBox()
        for key in self.data.keys():
            combo_box.addItem(key.__name__)
            combo_box.setItemData(combo_box.count() - 1, key)
        combo_box.activated.connect(self.handle_combo_box_click)
        return combo_box

    def generate_tree_widget(self) -> QTreeWidget:
        header_labels: List[str] = [key.__name__ for key in self.data.keys()]
        tree_items: List[QTreeWidgetItem] = []
        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        tree.setColumnCount(len(header_labels))
        tree.setHeaderLabels(header_labels)

        for idx, (key, values) in enumerate(self.data.items()):
            tree_item = QTreeWidgetItem([header_labels[idx]])
            tree_item.setData(0, 1, key)
            for value in values:
                child = QTreeWidgetItem([str(value)])
                child.setData(1, 1, value)
                tree_item.addChild(child)
            tree_items.append(tree_item)

        tree.insertTopLevelItems(0, tree_items)
        tree.itemClicked.connect(self.handle_tree_item_click)
        return tree

    def handle_combo_box_click(self, idx: int) -> None:
        if not self.combo_box:
            raise ValueError('Combo box is undefined')
        self.event_aggregator.publish(
            'NewUserClicked', data_type=self.combo_box.itemData(idx), data=None)

    def handle_tree_item_click(self, x: QTreeWidgetItem) -> None:
        root_data: str = x.data(0, 1)
        node_data: Person = x.data(1, 1)
        if root_data:
            self.event_aggregator.publish('GenerateTable', root_data)
        elif node_data:
            self.event_aggregator.publish(
                'TreeNodeClicked', type(node_data), data=node_data)
        else:
            raise ValueError('Invalid Tree Data')
