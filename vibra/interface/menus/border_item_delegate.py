from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QStyleOptionViewItem, QStyle
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

    def paint(self, painter: QPainter, option, index):
        pen = index.data(self.borderRole)
        rect = QRect(option.rect)
        icon = index.data(Qt.DecorationRole)
        
        # if configuration not enabled, reduce opacity
        if not (option.state & QStyle.State_Enabled):
            painter.setOpacity(0.4)
        else:
            painter.setOpacity(1)
            
        child = False
        tree = index.model().parent()
        if tree:
            item = tree.itemFromIndex(index)
            if item.parent():

                child = True
                text = index.data()
                painter.drawText(rect, option.displayAlignment, text)

                # draw icons
                if icon is not None:
                    icon_size = option.decorationSize.width() + 7
                    spacing = 5
                    icon_rect = QRect(option.rect.right() - icon_size - spacing, option.rect.top() + (option.rect.height() - icon_size)//2, icon_size, icon_size)
                    icon.paint(painter, icon_rect)
        
        # to not draw it twice
        if not child:
            super(BorderItemDelegate, self).paint(painter, option, index)
        
        if pen is not None:
            painter.save() # Saves previous status
            
            painter.setClipRect(rect, Qt.ReplaceClip)
            
            painter.restore() # Recovers previous status