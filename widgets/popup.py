# imports
from utils import load_nii, load_predict
from widgets.extras import LoadingIcon
from threading import Thread
from pathlib import Path

import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG


class Initializer(QtW.QFrame):
    
    def __init__(self, root=None, *args, **kargs) -> None:
        super(Initializer, self).__init__(*args, **kargs)
        
        # main variables
        BG_COLOR = '#D9D9D9'
        ICON_COLOR = '#009494'
        
        self.w = 500
        self.h = 300
        
        self.anim_time = 6
        self.counter = 0
        self.done = False

        self.root = root
        self.file_path = Path('/app/data')
        
        # size
        self.setFixedSize(QtC.QSize(self.w,self.h))
        
        # color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtG.QPalette.ColorRole.Window, QtG.QColor(BG_COLOR))
        self.setPalette(palette)

        # files checker
        self.checker = Thread(target=self.files_checker)
        
        # layout
        self.brain_logo = QtW.QLabel()
        self.png = QtG.QPixmap('/app/assets/brain.png').scaled(QtC.QSize(130,130))
        self.brain_logo.setPixmap(self.png)
        
        self.title = QtW.QLabel()
        self.title.setText('Tumor Detector')
        self.title.setStyleSheet(f'color: {ICON_COLOR};')
        font = QtG.QFont()
        font.setBold(True)
        font.setPixelSize(15)
        font.setWordSpacing(2)
        self.title.setFont(font)
        
        self.load = LoadingIcon()
        
        self.main_layout = QtW.QVBoxLayout()
        self.main_layout.setAlignment(QtC.Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addWidget(self.brain_logo)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.load)
        
        self.setLayout(self.main_layout)
        self.checker.start()
        self.checker.join()
    
    def initialization(self) -> bool:
        if self.done:
            print('Initialization Complete!')
            return True
        return False
    
    def files_checker(self) -> None:
        
        print('Initializing..')
        
        # looking for files
        files = {'t1': [], 't1ce': [], 't2': [], 'seg': [], 'flair': [], 'predict': []}
        for file in self.file_path.rglob(pattern='*.*'):
            name = file.name
            if name.endswith('.npy') and name.startswith('predict'):
                files['predict'].append(file)
            else:
                if name.endswith('.nii'):
                    _ntype = name.split('_')[-1].replace('.nii', '')
                    if _ntype in files:
                        files[_ntype].append(file)
        if not all(len(files[k]) == 3 for k in files):
            print('ERROR: there are missing files in demo')
            print(f'Files: {files}')
            self.root.close()
        
        # checking files
        for ftype in files:
            for path in files[ftype]:
                path = str(path)
                try:
                    if ftype == 'predict':
                        build = load_predict(file_path=path)
                    else:
                        build = load_nii(file_path=path)
                except Exception as error:
                    print(f'ERROR: {error}')
                else:
                    del build
        self.done = True