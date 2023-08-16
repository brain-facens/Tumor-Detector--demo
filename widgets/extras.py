# imports
import PySide6.QtWidgets as QtW
import PySide6.QtCore as QtC
import PySide6.QtGui as QtG


class LoadingIcon(QtW.QFrame):
    
    def __init__(self, *args, **kargs) -> None:
        super(LoadingIcon, self).__init__(*args, **kargs)
        