# imports
from widgets.button import MenuButton, CustomButton

import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG


class MainScreen(QtW.QFrame):
    
    def __init__(self, root: QtW.QWidget, *args, **kargs) -> None:
        super(MainScreen, self).__init__(*args, **kargs)
        
        # main variables
        self.w = 1200
        self.h = 750
        hmenu = int(self.h * 0.05)
        
        # size
        self.setFixedSize(QtC.QSize(self.w,self.h))
        
        # layout
        self.main_layout = QtW.QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        
        self.main_layout.addWidget(MenuBar(root=root, width=self.w, height=hmenu))
        self.main_layout.addWidget(CentralFrame(width=self.w, height=self.h - hmenu))
        
        self.setLayout(self.main_layout)


class MenuBar(QtW.QFrame):
    
    def __init__(
        self, root: QtW.QWidget, 
        width: int, 
        height: int, 
        *args, 
        **kargs
        ) -> None:
        super(MenuBar, self).__init__(*args, **kargs)
        
        # main variables
        BG_COLOR = '#D9D9D9'
        
        self.dragging = False
        self.offset = None
        self.root = root
        
        # size
        self.setFixedSize(QtC.QSize(width,height))
        
        # color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtG.QPalette.ColorRole.Window, QtG.QColor(BG_COLOR))
        self.setPalette(palette)
        
        # buttons
        self.exit_button = MenuButton(root=root, btype='exit')
        self.exit_button.move(width - 20, self.exit_button.pos().y())
        
        # layout
        self.main_layout = QtW.QHBoxLayout()
        self.main_layout.setAlignment(QtC.Qt.AlignmentFlag.AlignRight)
        self.main_layout.setContentsMargins(1,1,15,1)
        
        self.main_layout.addWidget(self.exit_button)
        
        self.setLayout(self.main_layout)
    
    def mousePressEvent(self, event: QtG.QMouseEvent) -> None:
        if event.button() == QtC.Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.root.pos()
    
    def mouseMoveEvent(self, event: QtG.QMouseEvent) -> None:
        if self.dragging:
            new_pos = event.globalPos() - self.offset
            self.root.move(new_pos)

    def mouseReleaseEvent(self, event: QtG.QMouseEvent) -> None:
        if event.button() == QtC.Qt.MouseButton.LeftButton:
            self.dragging = False


class CentralFrame(QtW.QFrame):
    
    def __init__(
        self,
        width: int, 
        height: int,  
        *args, 
        **kargs
        ) -> None:
        super(CentralFrame, self).__init__(*args, **kargs)
        
        # main variables
        BG_COLOR = '#D9D9D9'

        img_w = int(width * 0.6)
        
        # size
        self.setFixedSize(QtC.QSize(width,height))
        
        # color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtG.QPalette.ColorRole.Window, QtG.QColor(BG_COLOR))
        self.setPalette(palette)

        # layout
        self.main_layout = QtW.QHBoxLayout()
        self.main_layout.setContentsMargins(30,30,30,30)
        self.main_layout.setSpacing(80)

        self.opt_border = OptionFrame()

        self.frame = ImageFrame(width=img_w)

        self.main_layout.addWidget(self.opt_border)
        self.main_layout.addWidget(self.frame)

        self.setLayout(self.main_layout)


class ImageFrame(QtW.QFrame):
    
    def __init__(
        self, 
        width: int, 
        *args, 
        **kargs
        ) -> None:
        super(ImageFrame, self).__init__(*args, **kargs)

        # main variables
        BG_COLOR = '#CBCBCB'

        # size
        self.setFixedWidth(width)

        # color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtG.QPalette.ColorRole.Window, QtG.QColor(BG_COLOR))
        self.setPalette(palette)

        # shadow
        self.shadow = QtW.QGraphicsDropShadowEffect(self)
        self.shadow.setColor('#959595')
        self.shadow.setBlurRadius(30)
        self.shadow.setOffset(0)
        self.setGraphicsEffect(self.shadow)


class OptionFrame(QtW.QFrame):

    def __init__(
        self, 
        *args, 
        **kargs
        ) -> None:
        super(OptionFrame, self).__init__(*args, **kargs)

        # main variables
        BG_COLOR = '#CBCBCB'

        self.color = QtG.QColor(BG_COLOR)

        # shadow
        self.shadow = QtW.QGraphicsDropShadowEffect(self)
        self.shadow.setColor('#959595')
        self.shadow.setBlurRadius(30)
        self.shadow.setOffset(0)
        self.setGraphicsEffect(self.shadow)

        # layout
        self.main_layout = QtW.QVBoxLayout()
        self.main_layout.setAlignment(QtC.Qt.AlignmentFlag.AlignCenter | QtC.Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(5,20,5,5)

        self.list_box_title = QtW.QLabel()
        font = QtG.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.list_box_title.setFont(font)
        self.list_box_title.setText('Choose the file (.NII)')

        self.list_box = ListBox()
        self.list_box.addItem('patient_01_12082023.nii')
        self.list_box.addItem('patient_02_12082023.nii')
        self.list_box.addItem('patient_03_12082023.nii')

        self.apply_button = CustomButton(
            width=100, 
            height=25, 
            color='#009494', 
            hover_color='#00A3A3', 
            clicked_color='#009494', 
            action=self._apply_file_func, 
            text='apply file'
        )

        self.info = QtW.QFrame()
        self.info_layout = QtW.QVBoxLayout()
        self.info_layout.setContentsMargins(5,10,5,10)
        self.info_layout.setSpacing(0)
        info = InfoLabel(200)
        self.info_layout.addWidget(info)
        self.info.setLayout(self.info_layout)

        self.main_layout.addWidget(self.list_box_title)
        self.main_layout.addWidget(self.list_box)
        self.main_layout.addWidget(self.apply_button)
        self.main_layout.addWidget(self.info)

        self.setLayout(self.main_layout)

    def paintEvent(self, arg__1: QtG.QPaintEvent) -> None:
        
        # initializing painter
        painter = QtG.QPainter(self)
        if not painter.isActive():
            painter.begin(self)
        painter.setRenderHint(QtG.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtG.Qt.PenStyle.NoPen)

        # color
        painter.setBrush(self.color)

        # drawing rectangle
        rect = self.rect()
        painter.drawRoundedRect(rect, 20, 20)

        painter.end()
    
    def _apply_file_func(self) -> None:
        ...


class ListBox(QtW.QComboBox):

    def __init__(self, *args, **kargs) -> None:
        super(ListBox, self).__init__(*args, **kargs)

        # main variables
        BG_COLOR = '#D9D9D9'

        # design
        self.setObjectName('list-box')
        self.setStyleSheet(
                    f'''
        #list-box {{
            background-color: {BG_COLOR};
            width: 280px;
            height: 20px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: bold;
            padding-left: 15px;
        }}

        #list-box::down-arrow {{
            background-color: {BG_COLOR};
        }}
        '''
        )


class InfoLabel(QtW.QLabel):

    def __init__(
        self, 
        height: int, 
        *args, 
        **kargs
        ) -> None:
        super(InfoLabel, self).__init__(*args, **kargs)

        # main variables
        self.color = '#D9D9D9'

        self.setFixedHeight(height)

        # shadow
        self.shadow = QtW.QGraphicsDropShadowEffect(self)
        self.shadow.setColor('#959595')
        self.shadow.setBlurRadius(5)
        self.shadow.setOffset(0)
        self.setGraphicsEffect(self.shadow)
        
    def paintEvent(self, arg__1: QtG.QPaintEvent) -> None:
        
        # initializing painter
        painter = QtG.QPainter(self)
        if not painter.isActive():
            painter.begin(self)
        painter.setRenderHint(QtG.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtG.Qt.PenStyle.NoPen)

        # color
        painter.setBrush(QtG.QColor(self.color))

        # drawing rectangle
        rect = self.rect()
        painter.drawRoundedRect(rect, 20, 20)

        painter.end()