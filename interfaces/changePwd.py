import bcrypt
import pymongo
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QApplication, QMessageBox

from interfaces.mainForm import MainForm


class ChangePwdMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mise a Jour")
        self.setGeometry(380, 200, 400, 300)
        self.setStyleSheet("background-color: silver;")

        self.mainForm = MainForm()
        self.mainForm.switch_to_updatePwd.connect(self.showUpdatePwd)

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["buildManager"]

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Titre
        title_label = QLabel("MODIFIER LE MOT DE PASSE")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-family: algerian; font-size: 22px; font-weight: bold; color: orange;")
        layout.addWidget(title_label)

        # Champs de saisie
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        ancien_pwd_label = QLabel("Ancien Mot De Passe:")
        ancien_pwd_label.setStyleSheet("font-size: 14px;")
        self.ancien_pwd_input = QLineEdit()
        self.ancien_pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        input_layout.addWidget(ancien_pwd_label)
        input_layout.addWidget(self.ancien_pwd_input)

        nouveau_pwd_label = QLabel("Nouveau Mot De Passe:")
        nouveau_pwd_label.setStyleSheet("font-size: 14px;")
        self.nouveau_pwd_input = QLineEdit()
        self.nouveau_pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        input_layout.addWidget(nouveau_pwd_label)
        input_layout.addWidget(self.nouveau_pwd_input)

        confirm_nouveau_pwd_label = QLabel("Confirmer Nouveau Mot De Passe:")
        confirm_nouveau_pwd_label.setStyleSheet("font-size: 14px;")
        self.confirm_nouveau_pwd_input = QLineEdit()
        self.confirm_nouveau_pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        input_layout.addWidget(confirm_nouveau_pwd_label)
        input_layout.addWidget(self.confirm_nouveau_pwd_input)

        layout.addLayout(input_layout)

        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        connexion_button = QPushButton("Enregistrer")
        connexion_button.setStyleSheet("font-size: 16px; font-weight: bold; background-color: cyan; color: black;")
        connexion_button.clicked.connect(self.modifier)
        connexion_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttons_layout.addWidget(connexion_button)

        inscription_button = QPushButton("Fermer")
        inscription_button.setStyleSheet("font-size: 16px; font-weight: bold; background-color: orange; color: black;")
        inscription_button.clicked.connect(self.cancelWindow)
        inscription_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttons_layout.addWidget(inscription_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def modifier(self):
        old_pwd = self.ancien_pwd_input.text()
        new_pwd = self.nouveau_pwd_input.text()
        conf_new_pwd = self.confirm_nouveau_pwd_input.text()

        owners_collection = self.database["Owners"]
        owner = owners_collection.find_one({"_id": "2c31634f-8b10-4886-88ce-56fb637a26c5"})

        hashed_password = owner["_password"].encode('utf-8')

        if not bcrypt.checkpw(old_pwd.encode('utf-8'), hashed_password):
            QMessageBox.critical(self, "Erreur", "L'ancien Mot De Passe Est Incorrect.")
            return
        else:
            if new_pwd != conf_new_pwd:
                QMessageBox.critical(self, "Erreur", "Les nouveaux mots de passe doivent etre identiques.")
                return

            if len(new_pwd) < 8:
                QMessageBox.critical(self, "Erreur", "Le mot de passe doit contenir au moins 8 caractères.")
                return

            if old_pwd == new_pwd:
                QMessageBox.critical(self, "Erreur", "Le nouveau mot de passe ressemble a l'ancien.")
                return

            hashed_password = bcrypt.hashpw(new_pwd.encode('utf-8'), bcrypt.gensalt())
            owner["_password"] = hashed_password.decode('utf-8')
            QMessageBox.information(self, "Succès", "Le mot de passe a été mis à jour avec succès.")
            self.close()

    def cancelWindow(self):
        self.close()

    def showUpdatePwd(self):
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    changePwd_menu = ChangePwdMenu()
    changePwd_menu.show()
    app.exec()
