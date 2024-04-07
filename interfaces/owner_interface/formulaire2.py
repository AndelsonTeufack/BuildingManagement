from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QHBoxLayout, \
    QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from model.Owner import Owner
import sys
import re, pymongo, bcrypt


class Formulaire(QWidget):
    switch_to_connexion = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inscription")
        self.setGeometry(380, 200, 600, 400)
        self.setStyleSheet("background-color: silver;")

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["buildManager"]

        layout = QVBoxLayout()

        # Titre
        title_label = QLabel("CREER UN COMPTE")
        title_label.setStyleSheet("font-family: algerian; font-size: 22px; font-weight: bold; color: #FF8C00;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Champs du formulaire
        form_layout = QVBoxLayout()

        fields = [("Prenom:", QLineEdit()),
                  ("Nom:", QLineEdit()),
                  ("Telephone:", QLineEdit()),
                  ("Email:", QLineEdit()),
                  ("Password:", QLineEdit()),
                  ("Confirm Password:", QLineEdit())]

        self.edit_fields = []  # Garder une référence aux champs de texte
        for label_text, line_edit in fields:
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            line_edit.setStyleSheet("font-size: 14px;")
            form_layout.addWidget(label)

            if "Password" in label_text:  # Vérifier si le champ est un mot de passe
                line_edit.setEchoMode(QLineEdit.EchoMode.Password)  # Masquer le texte

            form_layout.addWidget(line_edit)
            self.edit_fields.append(line_edit)

        layout.addLayout(form_layout)

        # Checkbox
        self.checkbox = QCheckBox("J'accepte les conditions et les termes")
        self.checkbox.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.checkbox)

        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        btn_creer = QPushButton("Créer")
        btn_creer.setStyleSheet("font-size: 16px; font-weight: bold; background-color: cyan; color: black;")
        btn_creer.clicked.connect(self.creer)
        btn_creer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        btn_connexion = QPushButton("Connexion")
        btn_connexion.setStyleSheet("font-size: 16px; font-weight: bold; background-color: orange; color: black;")
        btn_connexion.clicked.connect(self.switchToConnexion)
        btn_connexion.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        buttons_layout.addWidget(btn_creer)
        buttons_layout.addWidget(btn_connexion)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def creer(self):
        # Récupérer les valeurs des champs
        prenom = self.edit_fields[0].text()
        nom = self.edit_fields[1].text()
        telephone = self.edit_fields[2].text()
        email = self.edit_fields[3].text()
        password = self.edit_fields[4].text()
        confirm_password = self.edit_fields[5].text()

        # Vérifier si les champs ne sont pas vides
        if not prenom or not nom or not telephone or not email or not password or not confirm_password:
            QMessageBox.critical(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            QMessageBox.critical(self, "Erreur", "Les mots de passe ne correspondent pas.")
            return

        # Vérifier la longueur du mot de passe
        if len(password) < 8:
            QMessageBox.critical(self, "Erreur", "Le mot de passe doit contenir au moins 8 caractères.")
            return

        # Vérifier le format de l'adresse e-mail avec une expression régulière
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            QMessageBox.critical(self, "Erreur", "Veuillez saisir une adresse e-mail valide.")
            return

        # Vérifier si le numéro de téléphone commence par "237" et a une longueur totale de 9 chiffres
        if not telephone.startswith("237") or len(telephone) != 12:
            QMessageBox.critical(self, "Erreur",
                                 "Veuillez saisir un numéro de téléphone valide commençant par '237' et comportant au "
                                 "total 9 chiffres.")
            return

        # Vérifier si les conditions sont acceptées
        if not self.checkbox.isChecked():
            QMessageBox.critical(self, "Erreur", "Veuillez accepter les conditions et les termes.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_owner = Owner(firstName=prenom, lastName=nom, phone=telephone, email=email,
                          password=hashed_password.decode('utf-8'))

        owners_collection = self.database["Owners"]
        owners_collection.insert_one(new_owner.__dict__)

        QMessageBox.information(self, "Succès", "Votre compte a été créé avec succès.")
        self.close()  # Fermer la fenêtre d'inscription

        self.switch_to_connexion.emit()  # Émettre le signal pour passer à la fenêtre de connexion

    def handle_accepted(self):
        self.switch_to_connexion.emit()  # Émettre le signal pour passer à la fenêtre de connexion

    def switchToConnexion(self):
        self.close()
        self.switch_to_connexion.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Formulaire()
    window.show()
    sys.exit(app.exec())
