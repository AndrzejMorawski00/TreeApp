from PyQt6.QtWidgets import QLayout, QLayoutItem
from typing import Optional


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
