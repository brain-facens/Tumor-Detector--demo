# imports
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG


class MenuButton(QtW.QToolButton):
    
    def __init__(
        self, 
        btype: str, 
        root: QtW.QWidget = None, 
        *args, 
        **kargs
        ) -> None:
        super(MenuButton, self).__init__(*args, **kargs)
        
        # main variables
        BG_COLOR = '#D9D9D9'
        HOVER_BG_COLOR = '#E4E4E4'
        SHADOW_COLOR = '#D80000'
        ICON_COLOR = '#A6A6A6'
        HOVER_ICON_COLOR = '#D80000'
        
        self.brush = QtG.QColor(BG_COLOR)
        self.hover_brush = QtG.QColor(HOVER_BG_COLOR)
        self.color = QtG.QColor(ICON_COLOR)
        self.hover_color = QtG.QColor(HOVER_ICON_COLOR)
        
        self.w = 24
        self.h = 24
        self.len_i = 4
        self.root = root
        
        # size
        self.setFixedSize(QtC.QSize(self.w, self.h))

        # actions
        actions = {
            'exit': self._exit
        }
        self.clicked.connect(actions[btype])
        
        self.shadow = QtW.QGraphicsDropShadowEffect(self)
        self.shadow.setColor(QtG.QColor(SHADOW_COLOR))
        self.shadow.setOffset(0,0)
        self.setGraphicsEffect(self.shadow)
    
    def _exit(self) -> None:
        self.root.close()

    def paintEvent(self, arg__1: QtG.QPaintEvent) -> None:
        
        # initializing painter
        painter = QtG.QPainter(self)
        if not painter.isActive():
            painter.begin(self)
        
        pen = QtG.QPen()
        pen.setWidthF(1.5)
        
        # defining color
        painter.setRenderHint(QtG.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtG.Qt.PenStyle.NoPen)
        
        if self.underMouse():
            painter.setBrush(self.hover_brush)
            pen.setColor(self.hover_color)
            self.shadow.setBlurRadius(15)
        else:
            painter.setBrush(self.brush)
            pen.setColor(self.color)
            self.shadow.setBlurRadius(0)
        
        # drawing button
        rect = self.rect()
        painter.drawRoundedRect(rect, self.w // 2, self.h // 2)
        
        # drawing icon
        painter.setPen(pen)
        
        cx, cy = rect.width() // 2, rect.height() // 2
        path = QtG.QPainterPath()
        path.moveTo(cx-self.len_i, cy-self.len_i)
        path.lineTo(cx+self.len_i,cy+self.len_i)
        path.moveTo(cx+self.len_i, cy-self.len_i)
        path.lineTo(cx-self.len_i,cy+self.len_i)
        painter.drawPath(path)
        
        painter.end()