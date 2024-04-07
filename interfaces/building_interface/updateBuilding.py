import sys

import pymongo
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QApplication, QMessageBox
from bson import ObjectId

import re

from session.session_manager import get_current_user_id


class UpdateBuildingMenu(QWidget):

    def __init__(self, building_id=None):
        super().__init__()
        self.setWindowTitle("Mise a Jour")
        self.setGeometry(380, 200, 400, 300)
        self.setStyleSheet("background-color: silver;")

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["buildManager"]

        self.building_id = building_id

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

        name_label = QLabel("Nom:")
        name_label.setStyleSheet("font-size: 14px;")
        self.name_input = QLineEdit()
        input_layout.addWidget(name_label)
        input_layout.addWidget(self.name_input)

        city_label = QLabel("Ville:")
        city_label.setStyleSheet("font-size: 14px;")
        self.city_input = QLineEdit()
        input_layout.addWidget(city_label)
        input_layout.addWidget(self.city_input)

        quarter_label = QLabel("Quartier:")
        quarter_label.setStyleSheet("font-size: 14px;")
        self.quarter_input = QLineEdit()
        input_layout.addWidget(quarter_label)
        input_layout.addWidget(self.quarter_input)

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
        name = self.name_input.text()
        city = self.city_input.text()
        quarter = self.quarter_input.text()

        user_id = get_current_user_id()
        owner = self.database["Owners"].find_one({"_id": user_id})

        if owner:
            for building in owner["_buildings"]:
                if building["_id"] == self.building_id:
                    if name or city or quarter:
                        if name:
                            building["_name"] = name
                        if city:
                            building["_city"] = city
                        if quarter:
                            building["_quarter"] = quarter
                    else:
                        # Afficher un message d'erreur si aucun champ n'a été rempli
                        QMessageBox.critical(self, "Erreur", "Aucune donnée à mettre à jour.")
                self.database["Owners"].update_one({"_id": owner["_id"]}, {"$set": {"_buildings": owner["_buildings"]}})
            QMessageBox.information(self, "Succès", "Les données ont été mises à jour avec succès.")
            self.close()

        else:
            QMessageBox.critical(self, "Erreur", "Aucune propriétaire trouvé.")

    def cancelWindow(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateBuildingMenu()
    window.show()
    sys.exit(app.exec())
