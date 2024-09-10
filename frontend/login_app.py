import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login - Simulación de Semiconductores')
        self.setGeometry(100, 100, 300, 150)

        # Layout principal
        layout = QVBoxLayout()

        # Campos de usuario y contraseña
        self.label_username = QLabel('Nombre de usuario')
        self.input_username = QLineEdit(self)

        self.label_password = QLabel('Contraseña')
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)

        # Botón de inicio de sesión
        self.button_login = QPushButton('Iniciar sesión', self)
        self.button_login.clicked.connect(self.login)

        # Añadir widgets al layout
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        # Hacer la solicitud al backend Flask para autenticar
        try:
            response = requests.post('http://127.0.0.1:5000/login', data={'username': username, 'password': password})

            if response.status_code == 200:
                QMessageBox.information(self, 'Login exitoso', 'Has iniciado sesión exitosamente!')
                # Aquí podrías abrir la ventana principal de la aplicación
            else:
                QMessageBox.warning(self, 'Error', 'Usuario o contraseña incorrectos')

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Error de conexión', 'No se pudo conectar con el servidor.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
