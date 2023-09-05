# imports
from widgets.button import MenuButton, CustomButton, SliderWithLabels
from utils import load_predict, load_nii
from pathlib import Path
from PIL import Image

import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG

import numpy as np


class MainScreen(QtW.QFrame):
    
    def __init__(self, root: QtW.QWidget, *args, **kargs) -> None:
        super(MainScreen, self).__init__(*args, **kargs)
        
        # main variables
        self.w = 1450
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

        img_w = int(width * 0.7)
        
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
        self.main_layout.setSpacing(30)

        self.frame = ImageFrame(width=img_w)

        self.opt_border = OptionFrame(self.frame)

        self.main_layout.addWidget(self.opt_border)
        self.main_layout.addWidget(self.frame)

        self.setLayout(self.main_layout)
        
        # initializing image
        self.frame.multi_viewer.currentWidget().update_slice()


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
        
        # layout
        self.sliced_image_frame = SlicedView()
        
        self.multi_slice_image_frame = MultiView()
        
        self.multi_viewer = QtW.QStackedLayout()
        self.multi_viewer.addWidget(self.sliced_image_frame)
        self.multi_viewer.addWidget(self.multi_slice_image_frame)
        self.multi_viewer.setCurrentIndex(0)
        self.setLayout(self.multi_viewer)

        # shadow
        self.shadow = QtW.QGraphicsDropShadowEffect(self)
        self.shadow.setColor('#959595')
        self.shadow.setBlurRadius(30)
        self.shadow.setOffset(0)
        self.setGraphicsEffect(self.shadow)
        
        
class SlicedView(QtW.QFrame):
    
    def __init__(self, *args, **kargs) -> None:
        super(SlicedView, self).__init__(*args, **kargs)
        
        # main variables
        self.index = 0
        
        # layout
        self.real_frame = QtW.QLabel()
        self.pred_frame = QtW.QLabel()
        self.real_frame.setFixedHeight(500)
        self.pred_frame.setFixedHeight(500)
        
        self.frame_layout = QtW.QHBoxLayout()
        self.frame_layout.addWidget(self.real_frame)
        self.frame_layout.addWidget(self.pred_frame)
        
        self.image_frame = QtW.QFrame()
        self.image_frame.setLayout(self.frame_layout)
        
        self.slice_slider = SliderWithLabels(init_value=0, min=0, max=155)
        self.slice_slider.slider.valueChanged.connect(self.update_slice)
        
        self.main_layout = QtW.QVBoxLayout()
        self.main_layout.addWidget(self.image_frame)
        self.main_layout.addWidget(self.slice_slider)
        self.setLayout(self.main_layout)
    
    def update_slice(self, index: int = 0) -> None:
        root = self.parent().parent()
        info = root.opt_border
        content = info.content
        threshold = info.info_label.limit * 100
        
        self.index = index
        sliced_image = content['image'][:,:,self.index - 1]
        sliced_mask = content['label'][:,:,self.index - 1]
        sliced_pred = content['predict'][:,:,self.index - 1,:]
        
        label1 = (sliced_mask == 1).astype(dtype=np.int8)
        label2 = (sliced_mask == 2).astype(dtype=np.int8)
        label3 = (sliced_mask == 4).astype(dtype=np.int8)
        
        sliced_image_rgb_label = np.asarray(a=Image.fromarray(obj=sliced_image, mode='L').convert(mode='RGB'), dtype=np.int8)
        
        sliced_image_rgb_label[:,:,0][label1 == 1] = 255
        sliced_image_rgb_label[:,:,1][label2 == 1] = 255
        sliced_image_rgb_label[:,:,2][label3 == 1] = 255
        
        sliced_image_rgb_label = Image.fromarray(obj=sliced_image_rgb_label, mode='RGB')
        
        real = QtG.QImage(
            sliced_image_rgb_label.tobytes(), 
            sliced_image_rgb_label.width, 
            sliced_image_rgb_label.height, 
            sliced_image_rgb_label.width * 3, 
            QtG.QImage.Format.Format_RGB888
        )
        real = QtG.QPixmap.fromImage(real)
        
        self.real_frame.setPixmap(real)
        self.real_frame.setScaledContents(True)
        
        sliced_image_rgb_pred = np.asarray(a=Image.fromarray(obj=sliced_image, mode='L').convert(mode='RGB'), dtype=np.int8)
        
        pred1 = (sliced_pred[:,:,0] >= threshold).astype(dtype=np.int8)
        pred2 = (sliced_pred[:,:,1] >= threshold).astype(dtype=np.int8)
        pred3 = (sliced_pred[:,:,2] >= threshold).astype(dtype=np.int8)
        
        sliced_image_rgb_pred[:,:,0][pred1 == 0] = 255
        sliced_image_rgb_pred[:,:,1][pred2 == 0] = 255
        sliced_image_rgb_pred[:,:,2][pred3 == 0] = 255
        
        sliced_image_rgb_pred = Image.fromarray(obj=sliced_image_rgb_pred, mode='RGB')
        
        pred = QtG.QImage(
            sliced_image_rgb_pred.tobytes(), 
            sliced_image_rgb_pred.width, 
            sliced_image_rgb_pred.height, 
            sliced_image_rgb_pred.width * 3, 
            QtG.QImage.Format.Format_RGB888
        )
        pred = QtG.QPixmap.fromImage(pred)
        
        self.pred_frame.setPixmap(pred)
        self.pred_frame.setScaledContents(True)


class MultiView(QtW.QFrame):
    
    def __init__(self, *args, **kargs) -> None:
        super(MultiView, self).__init__(*args, **kargs)
        self.setStyleSheet('background-color: black; color: white; font-size: 16px;')
        
        # layout
        self.text = QtW.QLabel()
        self.text.setText('Not Available.')
        
        layout = QtW.QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)
        
    def update_slice(self, index: int = 0) -> None:
        ...

class OptionFrame(QtW.QFrame):

    def __init__(
        self, 
        frame_viewer: ImageFrame, 
        *args, 
        **kargs
        ) -> None:
        super(OptionFrame, self).__init__(*args, **kargs)

        # main variables
        BG_COLOR = '#CBCBCB'

        self.data_path = Path('/app/data')
        self.color = QtG.QColor(BG_COLOR)
        
        self.frame_viewer = frame_viewer

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
        self.main_layout.setContentsMargins(10,20,10,5)

        self.list_box_title = QtW.QLabel()
        font = QtG.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.list_box_title.setFont(font)
        self.list_box_title.setText('Choose a register')

        self.list_box = ListBox()
        self.list_box.addItem('patient_001')
        self.list_box.addItem('patient_002')
        self.list_box.addItem('patient_003')

        self.apply_button = CustomButton(
            width=100, 
            height=25, 
            color='#009494', 
            hover_color='#00A3A3', 
            clicked_color='#009494', 
            action=self.apply_file, 
            text='apply'
        )

        self.info = QtW.QFrame()
        self.info_layout = QtW.QVBoxLayout()
        self.info_layout.setContentsMargins(5,10,5,10)
        self.info_layout.setSpacing(0)
        
        self.info_label = InfoLabel(self.frame_viewer, 100)
        self.info_layout.addWidget(self.info_label)
        self.info.setLayout(self.info_layout)

        self.main_layout.addWidget(self.list_box_title)
        self.main_layout.addWidget(self.list_box)
        self.main_layout.addWidget(self.apply_button)
        self.main_layout.addWidget(self.info)

        self.setLayout(self.main_layout)
        self.apply_file()

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
    
    def apply_file(self) -> None:
        patient_path = self.data_path.joinpath(self.list_box.currentText())
        self.image = load_nii(file_path=list(iter(patient_path.glob(pattern=f'*_t2.nii')))[0])
        self.label = load_nii(file_path=list(iter(patient_path.glob(pattern=f'*_seg.nii')))[0])
        self.predict = load_predict(file_path=list(iter(patient_path.glob(pattern=f'predict_*')))[0])
        
        self.image = ((self.image - self.image.min()) / (self.image.max() - self.image.min()) * 255).astype(dtype=np.int8)

        self.predict[:,:,:,0] = 1 - 1 + np.exp(-self.predict[:,:,:,0])
        self.predict[:,:,:,1] = 1 - 1 + np.exp(-self.predict[:,:,:,1])
        self.predict[:,:,:,2] = 1 - 1 + np.exp(-self.predict[:,:,:,2])
        self.predict = self.predict * 100
        
        try:
            root = self.parent().frame.multi_viewer.currentWidget()
            root.update_slice(root.index)
        except:
            ...
    
    @property
    def content(self) -> dict:
        return {
            'image': self.image, 
            'label': self.label, 
            'predict': self.predict
        }


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
        frame_viewer: ImageFrame, 
        height: int, 
        *args, 
        **kargs
        ) -> None:
        super(InfoLabel, self).__init__(*args, **kargs)

        # main variables
        self.color = '#D9D9D9'
        self.th = 0.5
        self.viewer = frame_viewer

        self.setFixedHeight(height)
        
        # layout
        self.title = QtW.QLabel()
        self.title.setText(f'Confidence score: {self.th:.2f}')
        
        self.threshold = SliderWithLabels(init_value=self.th)
        self.threshold.slider.valueChanged.connect(self.update_threshold)
        
        self.sliced_viewer = QtW.QRadioButton()
        self.sliced_viewer.toggled.connect(lambda: self.update_view(0))
        self.sliced_viewer.setText('Sliced view')
        self.multi_viewer = QtW.QRadioButton()
        self.multi_viewer.toggled.connect(lambda: self.update_view(1))
        self.multi_viewer.setText('3D view')
        
        self.sliced_viewer.setChecked(True)
        
        self.view_frame_layout = QtW.QHBoxLayout()
        self.view_frame_layout.addWidget(self.sliced_viewer)
        self.view_frame_layout.addWidget(self.multi_viewer)
        
        self.view_frame = QtW.QFrame()
        self.view_frame.setLayout(self.view_frame_layout)
        
        self.main_layout = QtW.QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.threshold)
        self.main_layout.addWidget(self.view_frame)
        self.setLayout(self.main_layout)

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
    
    def update_threshold(self, value: float) -> None:        
        self.th = value / 100
        self.title.setText(f'{self.title.text().split(":")[0]}: {self.th:.2f}')
        
        root = self.parent().parent().parent().frame.multi_viewer.currentWidget()
        root.update_slice(root.index)
    
    def update_view(self, index: int) -> None:
        self.viewer.multi_viewer.setCurrentIndex(index)
    
    @property
    def limit(self) -> float:
        return self.th
