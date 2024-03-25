from dataclasses import dataclass

import pymongo
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QApplication, QMessageBox

from interfaces.mainForm import MainForm
from model.Building import Building
from model.Owner import Owner
import json


class CreateBuildingMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créer cité")
        self.setGeometry(380, 200, 400, 300)
        self.setStyleSheet("background-color: silver;")

        self.mainForm = MainForm()
        self.mainForm.switch_to_update.connect(self.showCreatBl)

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["buildManager"]

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Titre
        title_label = QLabel("CREER UNE CITE")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-family: algerian; font-size: 22px; font-weight: bold; color: orange;")
        layout.addWidget(title_label)

        # Champs de saisie
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        nom_label = QLabel("Nom De La Cité:")
        nom_label.setStyleSheet("font-size: 14px;")
        self.nom_input = QLineEdit()
        input_layout.addWidget(nom_label)
        input_layout.addWidget(self.nom_input)

        city_label = QLabel("Ville:")
        city_label.setStyleSheet("font-size: 14px;")
        self.city_input = QLineEdit()
        input_layout.addWidget(city_label)
        input_layout.addWidget(self.city_input)

        quater_label = QLabel("Quartier:")
        quater_label.setStyleSheet("font-size: 14px;")
        self.quarter_input = QLineEdit()
        input_layout.addWidget(quater_label)
        input_layout.addWidget(self.quarter_input)

        layout.addLayout(input_layout)

        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        creer_button = QPushButton("Enregistrer")
        creer_button.setStyleSheet("font-size: 16px; font-weight: bold; background-color: cyan; color: black;")
        creer_button.clicked.connect(self.creer)
        creer_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttons_layout.addWidget(creer_button)

        close_button = QPushButton("Fermer")
        close_button.setStyleSheet("font-size: 16px; font-weight: bold; background-color: orange; color: black;")
        close_button.clicked.connect(self.cancelWindow)
        close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttons_layout.addWidget(close_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def creer(self):
        name = self.nom_input.text()
        city = self.city_input.text()
        quater = self.quarter_input.text()

        # Vérifier si les champs ne sont pas vides
        if not name or not city or not quater:
            QMessageBox.critical(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        owners_collection = self.database["Owners"]
        # Récupérer le propriétaire depuis la base de données
        owner_document = owners_collection.find_one({"_id": "2c31634f-8b10-4886-88ce-56fb637a26c5"})

        if owner_document:
            owner = Owner.from_dict(owner_document)  # Convertir le document en instance de propriétaire
            # Créer un nouvel immeuble
            new_building = Building(name=name, city=city, quarter=quater)

            # Ajouter le nouvel immeuble au propriétaire
            owner.addBuilding(new_building)

            building_dict = new_building.to_dict()
            # owner_dict = owner.to_dict()

            building_collection = self.database["Buildings"]
            building_collection.insert_one(building_dict)

            # Mettre à jour le propriétaire dans la base de données en utilisant l'opérateur $set
            owners_collection.update_one(
                {"_id": "2c31634f-8b10-4886-88ce-56fb637a26c5"},
                {"$push": {"_buildings": building_dict}}
            )
            QMessageBox.information(self, "Succès", "Votre Cité a été créée avec succès.")
            self.close()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de trouver le propriétaire dans la base de données.")

    def cancelWindow(self):
        self.close()

    def showCreatBl(self):
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    create_building_menu = CreateBuildingMenu()
    create_building_menu.show()
    app.exec()
