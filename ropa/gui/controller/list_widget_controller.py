from PyQt4 import QtGui as qg, QtCore as qc

try:
    _fromUtf8 = qc.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ListWidgetController(object):
    def __init__(self, widget):
        self.widget = widget

    def count(self):
        return self.widget.count()

    def get_item(self, index):
        return self.widget.item(index)

    def set_gadgets(self, gadgets):
        self.widget.clear()
        for gadget in gadgets:
            cell = '<pre>'
            cell += '<b>%s</b>\n' % gadget['address']
            for instruction in gadget['instructions']:
                cell += '%s\n' % instruction
            cell += '</pre>'
            cell = qc.QString(cell)

            item = qg.QListWidgetItem(cell, self.widget)
            self.widget.insertItem(self.widget.count(), item)

    def key_press_event(self, e):
        if e.key() == qc.Qt.Key_Control:
            self.control = True
        if e.key() == qc.Qt.Key_Up:
            index = self.list_widget.currentRow()
            if index == 0:
                return
            if self.control:
                item = self.list_widget.takeItem(index)
                self.list_widget.insertItem(index - 1, item)
            self.list_widget.setCurrentRow(index - 1)
        if e.key() == qc.Qt.Key_Down:
            index = self.list_widget.currentRow()
            if index == self.list_widget.count() - 1:
                return
            if self.control:
                item = self.list_widget.takeItem(index)
                self.list_widget.insertItem(index + 1, item)
            self.list_widget.setCurrentRow(index + 1)
        if e.key() == qc.Qt.Key_Delete:
            # delete
            self.list_widget.takeItem(self.list_widget
                                      .selectedIndexes()[0].row())

    def key_release_event(self, e):
        if e.key() == qc.Qt.Key_Control:
            self.control = False
