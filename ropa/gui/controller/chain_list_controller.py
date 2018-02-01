from list_widget_controller import ListWidgetController
from ropa.ui import HTMLDelegate


class ChainListController(ListWidgetController):
    def __init__(self, widget):
        super(ChainListController, self).__init__(widget)
        self.widget.setDragEnabled(True)
        self.widget.setAcceptDrops(True)
        self.widget.setDropIndicatorShown(True)
        self.widget.setItemDelegate(
            HTMLDelegate(self.widget))
        self.widget.keyPressEvent = self.key_press_event
        self.widget.keyReleaseEvent = self.key_release_event
