from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QPlainTextEdit, QCalendarWidget, QTimeEdit, QLabel, QComboBox
from PyQt6.QtCore import QDateTime
from datetime import datetime
import pytz

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        self.clear_widgets()

        self.setWindowTitle("mods t calculator")
        self.note = QLabel("Select timezone first, then press 'Next'")
        self.layout.addWidget(self.note)

        self.cb = QComboBox(self)
        self.cb.addItems(['US/Pacific', 'US/Eastern', 'Europe/Zurich', 'Asia/Kolkata', 'Australia/Sydney'])
        self.layout.addWidget(self.cb)

        self.next = QPushButton('Next', self)
        self.next.clicked.connect(self.ask_datetime)
        self.layout.addWidget(self.next)

    def ask_datetime(self):
        self.clear_widgets()

        self.note = QLabel("Select Date and Time, then press 'Convert'")
        self.layout.addWidget(self.note)

        self.calendar = QCalendarWidget(self)
        self.layout.addWidget(self.calendar)

        self.timeEdit = QTimeEdit(self)
        self.timeEdit.setDisplayFormat("hh:mm:ss AP")
        self.layout.addWidget(self.timeEdit)

        self.convert = QPushButton('Convert', self)
        self.convert.clicked.connect(self.show_result)
        self.layout.addWidget(self.convert)

    def show_result(self):
        date = self.calendar.selectedDate().toPyDate()
        time = self.timeEdit.time().toPyTime()

        dt = datetime.combine(date, time)

        unix_time = int(dt.timestamp())

        self.clear_widgets()

        self.result = QPlainTextEdit(self)
        self.result.setPlainText(str(unix_time))
        self.result.setReadOnly(True)
        self.layout.addWidget(self.result)

        self.back = QPushButton('Back', self)
        self.back.clicked.connect(self.initUI)
        self.layout.addWidget(self.back)

    def clear_widgets(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    ex = MyApp()
    ex.show()

    sys.exit(app.exec())
