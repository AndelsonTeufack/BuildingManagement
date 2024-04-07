# from model.Owner import Owner
# from model.Building import Building
# from model.Room import Room
# from model.RoomOwner import RoomOwner
#
# # Création des propriétaires de bâtiments
# owner1 = Owner("John", "Doe", "237690", "john@example.com", "123")
# owner2 = Owner("Jane", "Smith", "237680", "jane@example.com", "123")
#
# # Création des bâtiments
# building1 = Building("Building A", "yaounde", "123 Main Street")
# building2 = Building("Building B", "douala", "456 Oak Avenue")
#
# # Création des chambres
# room1 = Room("101", 250000.0, "Chambre standard", 200000)
# room2 = Room("102", 150.0, "Chambre de luxe")
#
# # Création des locataires de chambre
# room_owner1 = RoomOwner("Alice", "Johnson", "111111111", "alice@example.com")
# room_owner2 = RoomOwner("Bob", "Smith", "222222222", "bob@example.com")
#
# # Affichage des détails des propriétaires de bâtiments
# owner1.display()
# print()
# owner2.display()
# print()
#
# # Affichage des détails des bâtiments
# building1.display()
# print()
# building2.display()
# print()
#
# # Affichage des détails des chambres
# room1.display()
# print()
# room2.display()
# print()
#
# # Affichage des détails des locataires de chambre
# room_owner1.display()
# print()
# room_owner2.display()
# print()
#
# owner1.addBuilding(building1)
# owner2.addBuilding(building2)
#
# building1.addRoom(room1)
# building2.addRoom(room2)
#
# room2.addRoomOwner(room_owner2)
#
# room_owner1.buyRoom(room1)
#
# owner1.display()
# print()
# owner2.display()
# print()
#
# # Affichage des détails des bâtiments
# building1.display()
# print()
# building2.display()
# print()
#
# # Affichage des détails des chambres
# room1.display()
# print()
# room2.display()
# print()
#
# # Affichage des détails des locataires de chambre
# room_owner1.display()
# print()
# room_owner2.display()
# print()


from PyQt6.QtWidgets import QApplication
from interfaces.owner_interface.formulaire2 import Formulaire
from interfaces.owner_interface.formulaireConnexion import ConnexionMenu
from interfaces.owner_interface.changePwd import ChangePwdMenu
from interfaces.building_interface.createBuilding import CreateBuildingMenu
from interfaces.mainForm import MainForm
from interfaces.owner_interface.updateForm import UpdateMenu

if __name__ == "__main__":
    app = QApplication([])

    #building = Building("Building A", "yaounde", "123 Main Street")
    formulaire = Formulaire()
    connexion_menu = ConnexionMenu()
    principal = MainForm()
    update = UpdateMenu()
    updatePwd = ChangePwdMenu()
    createBuild = CreateBuildingMenu()
    #afficherRoom = AfficherRoomMenu(building)
    #createRoom = CreateRoomMenu(building)

    # Connecter les signaux pour la transition entre les fenêtres
    formulaire.switch_to_connexion.connect(connexion_menu.show)  # Connecter le signal de Formulaire à la méthode
    # show de ConnexionMenu
    connexion_menu.switch_to_formulaire.connect(formulaire.show)  # Connecter le signal de ConnexionMenu à la méthode
    # show de Formulaire
    connexion_menu.switch_to_principal.connect(principal.show)
    # show de UpdateMenu
    principal.switch_to_update.connect(update.show)
    # show de ChangePwdMenu
    principal.switch_to_updatePwd.connect(updatePwd.show)
    # show de CreateBuildMenu
    principal.switch_to_createBuild.connect(createBuild.show)
    #afficherRoom.switch_to_addRoom.connect(createRoom.show)

    formulaire.show()  # Afficher le formulaire au démarrage

    app.exec()
