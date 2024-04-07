import pymongo
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QApplication, QMessageBox

from interfaces.afficherChambre import AfficherRoomMenu
from model.Building import Building
from model.Room import Room


class CreateRoomMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créer chambre")
        self.setGeometry(380, 200, 400, 300)
        self.setStyleSheet("background-color: silver;")
        self.building = None

        self.afficherRooMenu = AfficherRoomMenu(self.building)
        self.afficherRooMenu.switch_to_addRoom.connect(self.showRoomMenu)

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["buildManager"]

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Titre
        title_label = QLabel("CREER UNE Chambre")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-family: algerian; font-size: 22px; font-weight: bold; color: orange;")
        layout.addWidget(title_label)

        # Champs de saisie
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        numero_label = QLabel("Numéro De La Chambre (*) :")
        numero_label.setStyleSheet("font-size: 14px;")
        self.numero_input = QLineEdit()
        input_layout.addWidget(numero_label)
        input_layout.addWidget(self.numero_input)

        prix_label = QLabel("Prix (*) :")
        prix_label.setStyleSheet("font-size: 14px;")
        self.prix_input = QLineEdit()
        input_layout.addWidget(prix_label)
        input_layout.addWidget(self.prix_input)

        description_label = QLabel("Description:")
        description_label.setStyleSheet("font-size: 14px;")
        self.description_input = QLineEdit()
        input_layout.addWidget(description_label)
        input_layout.addWidget(self.description_input)

        avance_label = QLabel("Montant Avance:")
        avance_label.setStyleSheet("font-size: 14px;")
        self.avance_input = QLineEdit()
        input_layout.addWidget(avance_label)
        input_layout.addWidget(self.avance_input)

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

        numero = self.numero_input.text()
        prix = int(self.prix_input.text())
        description = self.description_input.text()
        montantAvance = int(self.avance_input.text())

        if not numero or not prix:
            QMessageBox.critical(self, "Erreur", "Les champs Numéro et Prix sont obligatoires.")
            return

        # Vérifier si le numéro de chambre existe déjà dans le bâtiment
        # if numero in [room.number for room in building.rooms]:
        #     QMessageBox.critical(self, "Erreur", "Le numéro de chambre existe déjà dans ce bâtiment.")
        #     return

        building_collection = self.database["Buildings"]
        # Récupérer le propriétaire depuis la base de données
        building_document = building_collection.find_one({"_id": self.building.id})
        if not building_document:
            self.building = Building(name=self.building.name, city=self.building.city, quarter=self.building.quarter)
            building_dict = self.building.to_dict()
            building_collection = self.database["Buildings"]
            building_collection.insert_one(building_dict)
        if montantAvance:
            new_room = Room(number=numero, price=prix, description=description, amountAdvanced=montantAvance)
            new_room.updateAvailabilityStatus()
        else:
            new_room = Room(number=numero, price=prix, description=description)

        # Ajouter la chambre au bâtiment
        self.building.addRoom(new_room)

        room_dic = new_room.to_dict()
        room_dic['_availabilityStatus'] = new_room.availabilityStatus.value

        room_collection = self.database["Rooms"]
        room_collection.insert_one(room_dic)

        building_collection.update_one(
            {"_id": self.building.id},
            {"$push": {"_rooms": room_dic}}
        )
        QMessageBox.information(self, "Succès", "Votre Chambre a été créée avec succès.")
        self.close()

    def cancelWindow(self):
        self.close()

    def showRoomMenu(self):
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    building1 = Building("Jungle", "Yaounde", "Awae")
    create_room_menu = CreateRoomMenu(building1)
    create_room_menu.show()
    app.exec()
