import sys

import pymongo
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QApplication, QToolBar, \
    QMessageBox

from MyEnum.AvailabilityStatus import AvailabilityStatus
from interfaces.afficherChambre import AfficherRoomMenu
from model.Building import Building
from session.session_manager import get_current_user_id, get_current_user_building_ids


class MainForm(QWidget):
    switch_to_update = pyqtSignal()
    switch_to_updatePwd = pyqtSignal()
    switch_to_createBuild = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.room_interface = None
        self.layout = None
        self.central_layout = None
        self.central_widget = None
        self.navbar_layout = None
        self.setWindowTitle("Gestionnaire de Bâtiments Étudiants")
        self.setGeometry(220, 100, 900, 600)
        self.setStyleSheet("background-color: silver;")

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.client["buildManager"]

        self.setup_ui()

    def setup_ui(self):
        # Barre de navigation
        self.navbar_layout = QHBoxLayout()
        self.navbar_layout.setContentsMargins(10, 10, 10, 10)

        btn_my_account = QPushButton("Mon Compte")
        btn_my_sites = QPushButton("Mes Cités")
        btn_rooms = QPushButton("Chambres")

        btns = [btn_my_account, btn_my_sites, btn_rooms]
        for btn in btns:
            btn.setStyleSheet("""
                                        QPushButton {
                                            background-color: orange;
                                            color: black;
                                            font-size: 16px;
                                            font-weight: bold;
                                        }
                                        QPushButton:hover {
                                            background-color: #ff8c00;
                                            color: white;
                                        }
                                    """)

        self.navbar_layout.addWidget(btn_my_account)
        self.navbar_layout.addWidget(btn_my_sites)
        self.navbar_layout.addWidget(btn_rooms)

        # Zone centrale
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.central_widget.setStyleSheet("border: 1px solid black;")

        # Layout principal de la fenêtre
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.navbar_layout)
        self.layout.addWidget(self.central_widget)
        self.setLayout(self.layout)

        # Connecter les boutons de la barre de navigation aux fonctions correspondantes
        btn_my_account.clicked.connect(self.show_my_account)
        btn_my_account.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_my_sites.clicked.connect(self.show_my_sites)
        btn_my_sites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_rooms.clicked.connect(self.show_rooms)
        btn_rooms.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def show_my_account(self):
        self.clear_central_layout()

        # Créer une barre de navigation
        navigation_bar = QToolBar()
        navigation_bar.setStyleSheet("""
                QToolBar {
                    background-color: #d3d3d3;
                    padding: 5px;
                }
            """)

        # Ajouter le texte "Mes informations" au widget conteneur
        title_label = QLabel("Mes Informations")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-family: Algerian;
                color: green;
                margin: 0px;
                margin-left: 300%;
                background-color: #d3d3d3;
                border: none;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajouter le widget à la barre de navigation
        navigation_bar.addWidget(title_label)

        # Ajouter la barre de navigation à la mise en page centrale
        self.central_layout.addWidget(navigation_bar)

        # Créer les widgets QLabel et les initialiser
        nom_label = QLabel("")
        prenom_label = QLabel("")
        email_label = QLabel("")
        phone_label = QLabel("")

        nomforlabel = QLabel("Nom:")
        prenomforlabel = QLabel("Prénom:")
        emailforlabel = QLabel("Email:")
        phoneforlabel = QLabel("Téléphone:")

        labels = [nomforlabel, prenomforlabel, emailforlabel, phoneforlabel]

        # Appliquer les styles aux QLabel
        for label in labels:
            label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 20px; font-family: Algerian;")

        nom_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")
        prenom_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")
        email_label.setStyleSheet("color: blue; font-weight: bold; font-size: 18px;")
        phone_label.setStyleSheet("color: green; font-weight: bold; font-size: 18px;")

        # Récupérer les informations du compte de l'utilisateur depuis la base de données
        owners_collection = self.database["Owners"]
        user_id = get_current_user_id()
        owner = owners_collection.find_one({"_id": user_id})
        if not user_id:
            QMessageBox.critical(self, "Erreur", "Aucun utilisateur connecté ou session expirée.")
            return

        nom = owner['_firstName']
        prenom = owner['_lastName']
        email = owner['_email']
        tel = owner['_phone']

        nom_label.setText(nom)
        prenom_label.setText(prenom)
        email_label.setText(email)
        phone_label.setText(tel)

        # Créer un QVBoxLayout pour afficher les informations du compte
        info_layout = QVBoxLayout()

        # Ajouter les informations du compte au QVBoxLayout
        info_layout.addWidget(nomforlabel)
        info_layout.addWidget(nom_label)
        info_layout.addWidget(prenomforlabel)
        info_layout.addWidget(prenom_label)
        info_layout.addWidget(emailforlabel)
        info_layout.addWidget(email_label)
        info_layout.addWidget(phoneforlabel)
        info_layout.addWidget(phone_label)

        # Créer un QVBoxLayout pour les boutons
        button_layout = QVBoxLayout()

        # Ajouter les boutons au QVBoxLayout
        modifier_button = QPushButton("Modifier")
        modifier_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        modifier_button.clicked.connect(self.switchToUpdate)
        modifier_button.setStyleSheet("""
            QPushButton {
                background-color: orange;
                color: white;
                font-size: 16px;
                height: 35px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #ff8c00;
            }
        """)

        changer_mdp_button = QPushButton("Changer mot de passe")
        changer_mdp_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        changer_mdp_button.clicked.connect(self.switchToUpdatePwd)
        changer_mdp_button.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                font-size: 16px;
                height: 35px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #707070;
            }
        """)

        button_layout.addWidget(modifier_button)
        button_layout.addWidget(changer_mdp_button)

        # Créer un QHBoxLayout po ur la disposition horizontale
        main_layout = QHBoxLayout()

        # Ajouter le QVBoxLayout des informations du compte à la gauche
        info_widget = QWidget()
        info_widget.setLayout(info_layout)
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 2px solid #d3d3d3;
                padding-right: 10px;
            }
        """)
        main_layout.addWidget(info_widget)

        # Ajouter le QVBoxLayout des boutons à la droite
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        button_widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                padding-left: 30px;
                border: 2px solid #ffffff;
            }
        """)
        main_layout.addWidget(button_widget)

        # Ajouter le QHBoxLayout à la mise en page centrale
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 2px solid #ffffff;
            }
        """)

        self.central_layout.addWidget(main_widget)

        # Rafraîchir la mise en page centrale
        self.central_layout.update()
        self.central_widget.update()

    def show_my_sites(self):
        self.clear_central_layout()

        # Créer une barre de navigation
        navigation_bar = QToolBar()
        navigation_bar.setStyleSheet("""
            QToolBar {
                background-color: #d3d3d3;
                padding: 5px;
            }
        """)

        # Ajouter le texte "Mes cités" au widget conteneur
        title_label = QLabel("Mes Cités")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-family: Algerian;
                color: green;
                margin: 0px;
                background-color: #d3d3d3;
                border: none;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        creer_button = QPushButton("Ajouter Une Cité")
        creer_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        creer_button.clicked.connect(self.switchToCreateBl)
        creer_button.setStyleSheet("""
            QPushButton {
                background-color: #008000;
                color: white;
                font-size: 16px;
                height: 30px;
                width: 130px;
                margin-left: 580px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: orange;
            }
        """)

        # Ajouter le widget à la barre de navigation
        navigation_bar.addWidget(title_label)
        navigation_bar.addWidget(creer_button)

        # Ajouter la barre de navigation à la mise en page centrale
        self.central_layout.addWidget(navigation_bar)

        # Récupérer les IDs des bâtiments appartenant à l'owner
        user_id = get_current_user_id()
        owner = self.database["Owners"].find_one({"_id": user_id})
        building_dicts = owner["_buildings"]
        buildings = [Building.from_dict(building_dict) for building_dict in
                     building_dicts]  # Convertir en instances de Building
        if not buildings:
            QMessageBox.information(self, "Info", "Vous n'avez pas de cité pour le moment")
        buildings_layout = QVBoxLayout()

        for i, building in enumerate(buildings):
            # Utiliser directement l'objet building récupéré de la base de données
            # pour accéder à ses propriétés et créer les widgets correspondants
            titleLabel = QLabel("Building: " + str(i + 1))
            titleLabel.setStyleSheet(
                "font-weight: bold; text-transform: uppercase; font-size: 22px; font-family: times;")

            name_label = QLabel("Nom: " + building.name)
            name_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")

            city_label = QLabel("Ville: " + building.city)
            city_label.setStyleSheet("color: blue; font-weight: bold; font-size: 18px;")

            quater_label = QLabel("Quartier: " + building.quarter)
            quater_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")

            # Ajouter les widgets QLabel au QVBoxLayout des informations du bâtiment
            info_layout = QVBoxLayout()
            info_layout.addWidget(titleLabel)
            info_layout.addWidget(name_label)
            info_layout.addWidget(city_label)
            info_layout.addWidget(quater_label)

            # Créer un QHBoxLayout pour les boutons
            button_layout = QHBoxLayout()

            # Créer les boutons Modifier et Supprimer
            modifier_button = QPushButton("Modifier")
            modifier_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # modifier_button.clicked.connect(self.switchToUpdate)
            modifier_button.setStyleSheet("""
                QPushButton {
                    background-color: orange;
                    color: white;
                    font-size: 16px;
                    height: 35px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #ff8c00;
                }
            """)

            changer_mdp_button = QPushButton("Supprimer")
            changer_mdp_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # changer_mdp_button.clicked.connect(self.switch_to_updatePwd)
            changer_mdp_button.setStyleSheet("""
                QPushButton {
                    background-color: gray;
                    color: white;
                    font-size: 16px;
                    height: 35px;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #707070;
                }
            """)

            # Créer les boutons Modifier et Supprimer
            self.room_interface = AfficherRoomMenu(building)

            chambre_button = QPushButton("Chambres")
            chambre_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            chambre_button.clicked.connect(self.display_rooms)
            chambre_button.setStyleSheet("""
                            QPushButton {
                                background-color: #008000;
                                color: white;
                                font-size: 16px;
                                height: 35px;
                                border-radius: 15px;
                            }
                            QPushButton:hover {
                                background-color: orange;
                            }
                        """)

            # Ajouter les boutons au QHBoxLayout des boutons
            button_layout.addWidget(modifier_button)
            button_layout.addWidget(changer_mdp_button)
            button_layout.addWidget(chambre_button)

            # Créer un QVBoxLayout pour la disposition horizontale
            main_layout = QHBoxLayout()

            # Ajouter le QVBoxLayout des informations du bâtiment à gauche
            info_widget = QWidget()
            info_widget.setLayout(info_layout)
            info_widget.setStyleSheet("""
    ```python
                QWidget {
                    background-color: #f0f0f0;
                    border: 2px solid #d3d3d3;
                    padding-right: 10px;
                }
            """)
            main_layout.addWidget(info_widget)

            # Ajouter le QHBoxLayout des boutons à droite
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            button_widget.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    padding-left: 30px;
                    border: 2px solid #ffffff;
                }
            """)
            main_layout.addWidget(button_widget)

            # Ajouter le QHBoxLayout à la mise en page centrale
            main_widget = QWidget()
            main_widget.setLayout(main_layout)
            main_widget.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    border: 2px solid #ffffff;
                }
            """)

            # Ajouter le QWidget du bâtiment au QVBoxLayout des bâtiments
            buildings_layout.addWidget(main_widget)

        # Ajouter le QVBoxLayout des bâtiments à la mise en page centrale
        self.central_layout.addLayout(buildings_layout)

        # Rafraîchir la mise en page centrale
        self.central_layout.update()
        self.central_widget.update()

    def show_rooms(self):
        self.clear_central_layout()

        # Créer une barre de navigation
        navigation_bar = QToolBar()
        navigation_bar.setStyleSheet("""
                   QToolBar {
                       background-color: #d3d3d3;
                       padding: 5px;
                   }
               """)

        # Ajouter le texte "Mes cités" au widget conteneur
        title_label = QLabel("Mes Chambres")
        title_label.setStyleSheet("""
                   QLabel {
                       font-size: 24px;
                       font-family: Algerian;
                       color: green;
                       margin: 0px;
                       background-color: #d3d3d3;
                       border: none;
                   }
               """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        creer_button = QPushButton("Ajouter Une Chambre")
        creer_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # creer_button.clicked.connect(self.switchToCreateBl)
        creer_button.setStyleSheet("""
                   QPushButton {
                       background-color: #008000;
                       color: white;
                       font-size: 16px;
                       height: 30px;
                       width: 170px;
                       margin-left: 500px;
                       border-radius: 15px;
                   }
                   QPushButton:hover {
                       background-color: orange;
                   }
               """)

        # Ajouter le widget à la barre de navigation
        navigation_bar.addWidget(title_label)
        navigation_bar.addWidget(creer_button)

        # Ajouter la barre de navigation à la mise en page centrale
        self.central_layout.addWidget(navigation_bar)

        # Récupérer les IDs des bâtiments appartenant à l'owner
        building_ids = get_current_user_building_ids()
        rooms = self.get_rooms_for_building_ids(building_ids)

        if not rooms:
            QMessageBox.information(self, "Info", "Vous n'avez pas de chambre pour le moment")
        buildings_layout = QVBoxLayout()

        for i, room in enumerate(rooms):
            # Utiliser directement l'objet building récupéré de la base de données
            # pour accéder à ses propriétés et créer les widgets correspondants
            titleLabel = QLabel("Chambre: " + str(i + 1))
            titleLabel.setStyleSheet(
                "font-weight: bold; text-transform: uppercase; font-size: 22px; font-family: times;")

            number_label = QLabel("Numbre: " + room.number)
            number_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")

            price_label = QLabel("Prix: " + room.price + " FCFA")
            price_label.setStyleSheet("color: blue; font-weight: bold; font-size: 18px;")

            description_label = QLabel("Description: " + room.description)
            description_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")

            status_label = QLabel("Statut de disponibilité: " + room.availabilityStatus)
            status_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")

            # Ajouter les widgets QLabel au QVBoxLayout des informations du bâtiment
            info_layout = QVBoxLayout()
            info_layout.addWidget(titleLabel)
            info_layout.addWidget(number_label)
            info_layout.addWidget(price_label)
            info_layout.addWidget(description_label)
            info_layout.addWidget(status_label)

            if room.availabilityStatus == AvailabilityStatus.RESERVED:
                if room.amountAdvanced is not None:
                    montantAdv_label = QLabel("Montant avancé: " + room.amountAdvanced)
                    montantAdv_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")
                    info_layout.addWidget(montantAdv_label)
                if room.leftToPay is not None:
                    resteapayer_label = QLabel("Reste à payer: " + room.leftToPay)
                    resteapayer_label.setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 18px;")
                    info_layout.addWidget(resteapayer_label)

            # Créer un QHBoxLayout pour les boutons
            button_layout = QHBoxLayout()

            # Créer les boutons Modifier et Supprimer
            modifier_button = QPushButton("Modifier")
            modifier_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # modifier_button.clicked.connect(self.switchToUpdate)
            modifier_button.setStyleSheet("""
                       QPushButton {
                           background-color: orange;
                           color: white;
                           font-size: 16px;
                           height: 35px;
                           border-radius: 15px;
                       }
                       QPushButton:hover {
                           background-color: #ff8c00;
                       }
                   """)

            changer_mdp_button = QPushButton("Supprimer")
            changer_mdp_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # changer_mdp_button.clicked.connect(self.switch_to_updatePwd)
            changer_mdp_button.setStyleSheet("""
                       QPushButton {
                           background-color: gray;
                           color: white;
                           font-size: 16px;
                           height: 35px;
                           border-radius: 15px;
                       }
                       QPushButton:hover {
                           background-color: #707070;
                       }
                   """)

            # Créer les boutons Modifier et Supprimer
            self.room_interface = AfficherRoomMenu(room)

            proprietaire_button = QPushButton("Proprietaire")
            proprietaire_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            # proprietaire_button.clicked.connect(self.display_rooms)
            proprietaire_button.setStyleSheet("""
                                   QPushButton {
                                       background-color: #008000;
                                       color: white;
                                       font-size: 16px;
                                       height: 35px;
                                       border-radius: 15px;
                                   }
                                   QPushButton:hover {
                                       background-color: orange;
                                   }
                               """)

            # Ajouter les boutons au QHBoxLayout des boutons
            button_layout.addWidget(modifier_button)
            button_layout.addWidget(changer_mdp_button)
            button_layout.addWidget(proprietaire_button)

            # Créer un QVBoxLayout pour la disposition horizontale
            main_layout = QHBoxLayout()

            # Ajouter le QVBoxLayout des informations du bâtiment à gauche
            info_widget = QWidget()
            info_widget.setLayout(info_layout)
            info_widget.setStyleSheet("""
           ```python
                       QWidget {
                           background-color: #f0f0f0;
                           border: 2px solid #d3d3d3;
                           padding-right: 10px;
                       }
                   """)
            main_layout.addWidget(info_widget)

            # Ajouter le QHBoxLayout des boutons à droite
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            button_widget.setStyleSheet("""
                       QWidget {
                           background-color: #ffffff;
                           padding-left: 30px;
                           border: 2px solid #ffffff;
                       }
                   """)
            main_layout.addWidget(button_widget)

            # Ajouter le QHBoxLayout à la mise en page centrale
            main_widget = QWidget()
            main_widget.setLayout(main_layout)
            main_widget.setStyleSheet("""
                       QWidget {
                           background-color: #ffffff;
                           border: 2px solid #ffffff;
                       }
                   """)

            # Ajouter le QWidget du bâtiment au QVBoxLayout des bâtiments
            buildings_layout.addWidget(main_widget)

        # Ajouter le QVBoxLayout des bâtiments à la mise en page centrale
        self.central_layout.addLayout(buildings_layout)

        # Rafraîchir la mise en page centrale
        self.central_layout.update()
        self.central_widget.update()

    def show_rooms_of_building(self, building_id):
        # Cette fonction n'est pas implémentée dans votre code d'origine
        # Vous pouvez ajouter ici le code pour afficher les chambres d'un bâtiment spécifique
        pass

    def clear_central_layout(self):
        # Effacer tous les widgets de la zone centrale
        while self.central_layout.count():
            widget_item = self.central_layout.takeAt(0)
            if widget_item is not None:
                widget = widget_item.widget()
                if widget is not None:
                    widget.deleteLater()

    def show_principal(self):
        self.show()

        if self.connexion.isVisible():
            self.connexion.close()

    def switchToUpdate(self):
        self.switch_to_update.emit()

    def switchToUpdatePwd(self):
        self.switch_to_updatePwd.emit()

    def switchToCreateBl(self):
        self.switch_to_createBuild.emit()

    def display_rooms(self):
        # Affichez l'interface des chambres
        self.room_interface.show()

    def get_rooms_for_building_ids(self, building_ids):
        rooms = []  # Cette liste va stocker les chambres de tous les bâtiments

        for building_id in building_ids:
            # Supposons que tu aies une méthode ou une fonction pour récupérer un bâtiment par son ID
            building = self.get_building_by_id(building_id)

            # Vérifie si le bâtiment a des chambres listées
            if building and building._rooms:
                # Étend la liste des chambres avec les chambres de ce bâtiment
                rooms.extend(building._rooms)

        return rooms

    def get_building_by_id(self, building_id):
        # Utilise la collection de bâtiments pour récupérer le document correspondant
        building_dict = self.database["Buildings"].find_one({"_id": building_id})
        if building_dict:
            # Convertit le dictionnaire en objet Building
            return Building.from_dict(building_dict)
        else:
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec())
