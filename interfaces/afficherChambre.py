import pymongo
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QHBoxLayout, QPushButton
from MyEnum.AvailabilityStatus import AvailabilityStatus
from model.Building import Building


class AfficherRoomMenu(QWidget):
    switch_to_addRoom = pyqtSignal()

    def __init__(self, building):
        super().__init__()
        self.building = building

        # Créer un QVBoxLayout pour afficher les chambres
        self.rooms_layout = QVBoxLayout()

        # Appeler la méthode pour afficher les chambres
        self.display_rooms()

        # Titre
        title_label = QLabel("MES CHAMBRES")
        title_label.setStyleSheet("font-family: algerian; font-size: 22px; font-weight: bold; color: #FF8C00;")
        self.rooms_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        btn_ajouter = QPushButton("Ajouter")
        btn_ajouter.setStyleSheet("font-size: 16px; font-weight: bold; background-color: cyan; color: black;")
        btn_ajouter.clicked.connect(self.switchToAddRoom)
        btn_ajouter.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        btn_fermer = QPushButton("Fermer")
        btn_fermer.setStyleSheet("font-size: 16px; font-weight: bold; background-color: orange; color: black;")
        btn_fermer.clicked.connect(self.cancelWindow)
        btn_fermer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        buttons_layout.addWidget(btn_ajouter)
        buttons_layout.addWidget(btn_fermer)
        self.rooms_layout.addLayout(buttons_layout)

        self.setWindowTitle("Chambres")
        self.setGeometry(380, 200, 600, 400)
        self.setStyleSheet("background-color: silver;")

        # Ajouter le QVBoxLayout des chambres au widget principal
        self.setLayout(self.rooms_layout)

    def display_rooms(self):
        # Supprimer le contenu actuel du QVBoxLayout
        for i in reversed(range(self.rooms_layout.count())):
            self.rooms_layout.itemAt(i).widget().setParent(None)

        # Récupérer les chambres du bâtiment
        rooms = self.building.rooms

        # Parcourir les chambres et afficher leurs informations
        for room in rooms:
            # Créer un QLabel pour afficher les informations de la chambre
            room_label = QLabel()
            room_label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 16px;
                }
            """)

            # Construire la chaîne de texte avec les informations de la chambre
            room_info = f"Numéro de chambre: {room.number}\n" \
                        f"Prix: {room.price}\n" \
                        f"Description: {room.description}\n" \
                        f"Statut de disponibilité: {room.availabilityStatus.value}"

            # Vérifier si la chambre est réservée ou occupée
            if room.availabilityStatus == AvailabilityStatus.RESERVED:
                if room.amountAdvanced is not None:
                    room_info += f"\nMontant avancé: {room.amountAdvanced}"
                if room.leftToPay is not None:
                    room_info += f"\nReste à payer: {room.leftToPay}"

            # Afficher les informations de la chambre dans le QLabel
            room_label.setText(room_info)

            # Ajouter le QLabel au QVBoxLayout des chambres
            self.rooms_layout.addWidget(room_label)

    def switchToAddRoom(self):
        self.switch_to_addRoom.emit()

    def cancelWindow(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    building1 = Building("Building A", "yaounde", "123 Main Street")
    afficher_chambre_menu = AfficherRoomMenu(building1)
    afficher_chambre_menu.show()
    app.exec()