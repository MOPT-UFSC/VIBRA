from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QStyleOptionViewItem
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen, QPainter
from PySide6.QtCore import Qt, QSize, QRect

class BorderItemDelegate(QStyledItemDelegate):
    def __init__(self, parent, borderRole):
        super(BorderItemDelegate, self).__init__(parent)
        self.borderRole = borderRole

    def initStyleOption(self, option, index):
        super(BorderItemDelegate, self).initStyleOption(option, index)
        option.decorationAlignment = Qt.AlignRight
        option.decorationPosition = QStyleOptionViewItem.Right

    def sizeHint(self, option, index):        
        size = super(BorderItemDelegate, self).sizeHint(option, index)
        pen = index.data(self.borderRole)
        if pen is not None:        
            # Make some room for the border
            # When width is 0, it is a cosmetic pen which
            # will be 1 pixel anyways, so set it to 1
            width = max(pen.width(), 1)            
            size = size + QSize(2 * width, 2 * width)
        return size
    
    def size(self, item):
        separator_size = QSize()
        separator_size.setHeight(2)
        return item.setSizeHint(0, separator_size)

    def paint(self, painter: QPainter, option, index):
        pen = index.data(self.borderRole)
        rect = QRect(option.rect)

        if pen is not None:
            width = max(pen.width(), 1)
            # ...and remove the extra room we added in sizeHint...
            option.rect.adjust(width, width, -width, -width)      

        icon = QIcon()
        tree = index.model().parent()
        if tree:
            item = tree.itemFromIndex(index)
            if item.parent():
                icon = item.icon(0)
                item.setIcon(0, QIcon())
        
        super(BorderItemDelegate, self).paint(painter, option, index)

        item.setIcon(0, icon)
        
        icon_size = option.decorationSize
        pixmap = icon.pixmap(icon_size)
        x = rect.x() + (rect.width() - pixmap.width()) - 3
        y = rect.y() + (rect.height() - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)    
        
        if pen is not None:
            painter.save() # Saves previous status
            
            # Align rect 
            painter.setClipRect(rect, Qt.ReplaceClip)       
            pen.setWidth(2 * width)

            # Paint the borders
            painter.setPen(pen)
            rect.adjust(0, 0, 0, 0)
            painter.drawRoundedRect(rect, 7, 7)
            painter.fillRect(rect, QBrush(QColor(10, 10, 10)))
            
            painter.restore() # Recovers previous status