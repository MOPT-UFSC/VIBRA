from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class BorderItemDelegate(QStyledItemDelegate):
    def __init__(self, parent, borderRole):
        super(BorderItemDelegate, self).__init__(parent)
        self.borderRole = borderRole

    def initStyleOption(self, option, index):
        super(BorderItemDelegate, self).initStyleOption(option, index)
        option.decorationAlignment = Qt.AlignRight
        option.decorationPosition = QStyleOptionViewItem.Right

        # clear the icon from view. We're drawing it later
        option.icon = QIcon()

    def sizeHint(self, option, index):        
        size = super(BorderItemDelegate, self).sizeHint(option, index)
        pen = index.data(self.borderRole)
        
        default_size = super().sizeHint(option, index)
        tree = index.model().parent()
        item = tree.itemFromIndex(index)
        if item and item.parent():
            return QSize(default_size.width(), 22)

        if pen is not None:        
            # Make some room for the border
            # When width is 0, it is a cosmetic pen which
            # will be 1 pixel anyways, so set it to 1
            width = max(pen.width(), 1)            
            size = size + QSize(2 * width, 2 * width)
            size.setHeight(size.height() + 4)
        return size
    
    def size(self, item):
        separator_size = QSize()
        separator_size.setHeight(2)
        return item.setSizeHint(0, separator_size)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()

        super().paint(painter, option, index)

        original_icon: QIcon = index.data(Qt.DecorationRole)
        if original_icon and not original_icon.isNull():
            new_icon_size = QSize(20, 20)
            scaled_pixmap: QPixmap = original_icon.pixmap(new_icon_size, QIcon.Normal, QIcon.On)
            
            x_offset = option.rect.left()
            x_offset += option.rect.width() - 32
            y_offset = option.rect.top() + (option.rect.height() - new_icon_size.height()) // 2

            painter.drawPixmap(x_offset, y_offset, scaled_pixmap)

        painter.restore()