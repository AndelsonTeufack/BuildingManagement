import bcrypt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
import pymongo
from interfaces.formulaire2 import Formulaire


class ConnexionMenu(QWidget):
    switch_to_formulaire = pyqtSignal()
    switch_to_principal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setGeometry(380, 200, 400, 300)
        self.setStyleSheet("background-color: silver;")

        self.formulaire = Formulaire()
        self.formulaire.switch_to_connexion.connect(self.show_connexion)

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["buildManager"]

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Titre
        title_label = QLabel("CONNEXION")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-family: algerian; font-size: 22px; font-weight: bold; color: orange;")
        layout.addWidget(title_label)

        # Champs de saisie
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        numero_email_label = QLabel("Numero / Email:")
        numero_email_label.setStyleSheet("font-size: 14px;")
        self.numero_email_input = QLineEdit()
        input_layout.addWidget(numero_email_label)
        input_layout.addWidget(self.numero_email_input)

        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 14px;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        input_layout.addWidget(password_label)
        input_layout.addWidget(self.password_input)

        layout.addLayout(input_layout)

        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        connexion_button = QPushButton("Connexion")
        connexion_button.setStyleSheet("font-size: 16px; font-weight: bold; background-color: cyan; color: black;")
        connexion_button.clicked.connect(self.creer)
        connexion_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttons_layout.addWidget(connexion_button)

        inscription_button = QPushButton("Inscription")
        inscription_button.setStyleSheet("font-size: 16px; font-weight: bold; background-color: orange; color: black;")
        inscription_button.clicked.connect(self.switchToForm)
        inscription_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttons_layout.addWidget(inscription_button)

        forgot_password_button = QPushButton("Forgot Password")
        forgot_password_button.setStyleSheet("font-size: 12px; color: gray;")
        buttons_layout.addWidget(forgot_password_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def creer(self):
        # Récupérer les informations saisies
        login = self.numero_email_input.text()
        password = self.password_input.text()

        if not login or not password:
            QMessageBox.critical(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        owners_collection = self.database["Owners"]
        owner = owners_collection.find_one({"$or": [{"_email": login}, {"_phone": login}]})

        # Vérifier si l'utilisateur existe dans la base de données
        if not owner:
            QMessageBox.critical(self, "Erreur", "Adresse e-mail ou numéro de téléphone incorrect.")
            return

        hashed_password = owner["_password"].encode('utf-8')

        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            QMessageBox.critical(self, "Erreur", "Mot de passe incorrect.")
            return

        QMessageBox.information(self, "Succès", "Connexion Établie!")
        self.close()  # Fermer la fenêtre d'inscription

        self.switch_to_principal.emit()  # Émettre le signal pour passer à la fenêtre de connexion

    def show_connexion(self):
        self.show()
        self.formulaire.close()

    def switchToForm(self):
        self.close()
        self.switch_to_formulaire.emit()


if __name__ == "__main__":
    app = QApplication([])
    connexion_menu = ConnexionMenu()
    connexion_menu.show()
    app.exec()
