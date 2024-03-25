import pymongo
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QApplication, QMessageBox

from interfaces.mainForm import MainForm

import re


class UpdateMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mise a Jour")
        self.setGeometry(380, 200, 400, 300)
        self.setStyleSheet("background-color: silver;")

        self.mainForm = MainForm()
        self.mainForm.switch_to_update.connect(self.showUpdate)

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["buildManager"]

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Titre
        title_label = QLabel("MODIFIER LES INFORMATIONS")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-family: algerian; font-size: 20px; font-weight: bold; color: orange;")
        layout.addWidget(title_label)

        # Champs de saisie
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        nom_label = QLabel("Nom:")
        nom_label.setStyleSheet("font-size: 14px;")
        self.nom_input = QLineEdit()
        input_layout.addWidget(nom_label)
        input_layout.addWidget(self.nom_input)

        prenom_label = QLabel("Prénom:")
        prenom_label.setStyleSheet("font-size: 14px;")
        self.prenom_input = QLineEdit()
        input_layout.addWidget(prenom_label)
        input_layout.addWidget(self.prenom_input)

        email_label = QLabel("Email:")
        email_label.setStyleSheet("font-size: 14px;")
        self.email_input = QLineEdit()
        input_layout.addWidget(email_label)
        input_layout.addWidget(self.email_input)

        numero_label = QLabel("Numéro:")
        numero_label.setStyleSheet("font-size: 14px;")
        self.numero_input = QLineEdit()
        input_layout.addWidget(numero_label)
        input_layout.addWidget(self.numero_input)

        layout.addLayout(input_layout)

        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        register_button = QPushButton("Enregistrer")
        register_button.setStyleSheet("font-size: 16px; font-weight: bold; background-color: cyan; color: black;")
        register_button.clicked.connect(self.updateData)
        register_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttons_layout.addWidget(register_button)

        close_button = QPushButton("Fermer")
        close_button.setStyleSheet("font-size: 16px; font-weight: bold; background-color: orange; color: black;")
        close_button.clicked.connect(self.cancelWindow)
        close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttons_layout.addWidget(close_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def updateData(self):
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        email = self.email_input.text()
        numero = self.numero_input.text()

        owners_collection = self.database["Owners"]
        owner = owners_collection.find_one({"_id": "2c31634f-8b10-4886-88ce-56fb637a26c5"})

        # Vérifier si au moins un champ est non vide
        if nom or prenom or email or numero:
            if nom:
                owner["_firstName"] = nom
            if prenom:
                owner["_lastName"] = prenom
            if numero:
                if not numero.startswith("237") or len(numero) != 12:
                    QMessageBox.critical(self, "Erreur",
                                         "Veuillez saisir un numéro de téléphone valide commençant par '237' et "
                                         "comportant au total 9 chiffres.")
                    return
                owner["_phone"] = numero
            if email:
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, email):
                    QMessageBox.critical(self, "Erreur", "Veuillez saisir une adresse e-mail valide.")
                    return
                owner["_email"] = email

            # Mettez ici votre code pour mettre à jour les données de l'objet Owner dans la base de données
            owners_collection.update_one({"_id": "2c31634f-8b10-4886-88ce-56fb637a26c5"}, {"$set": owner})

            # Afficher un message de réussite à l'écran
            QMessageBox.information(self, "Succès", "Les données ont été mises à jour avec succès.")
            self.close()
        else:
            # Afficher un message d'erreur si aucun champ n'a été rempli
            QMessageBox.critical(self, "Erreur", "Aucune donnée à mettre à jour.")

    def cancelWindow(self):
        self.close()

    def showUpdate(self):
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    update_menu = UpdateMenu()
    update_menu.show()
    app.exec()
