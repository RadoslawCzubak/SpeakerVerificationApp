import sys

from PySide6.QtWidgets import QApplication

from ui.RecordWindow import RecordWindow

app = QApplication(sys.argv)
window = RecordWindow()
window.show()
app.exec()
