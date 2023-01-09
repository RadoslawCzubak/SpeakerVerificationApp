from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class ResultDialog(QDialog):
    def __init__(self, result):
        super().__init__()

        self.setWindowTitle("Result!")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(result)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
