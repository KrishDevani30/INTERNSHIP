import firebase_admin
from firebase_admin import credentials, db
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
cred = credentials.Certificate("C:/Users/yashb/Downloads/sample-a0718-firebase-adminsdk-fbsvc-3dc9efe0d9.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sample-a0718-default-rtdb.firebaseio.com/'
})
class Sample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sample PyQt Form")
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def submit_data(self):
        name = self.name_input.text()
        email = self.email_input.text()
        if name and email:
            ref = db.reference('users')
            ref.push({'name': name, 'email': email})
            self.result_label.setText("✅ Data saved to Firebase!")
            self.name_input.clear()
            self.email_input.clear()
        else:
            self.result_label.setText("⚠ Please fill in both fields.")
    def keyPressEvent(self, event):
        if event.key() == 16777216:  # Qt.Key_Escape
            self.showNormal()

app = QApplication(sys.argv)
window = Sample()
window.show()
sys.exit(app.exec_())