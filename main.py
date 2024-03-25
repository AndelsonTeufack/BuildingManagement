from model.Owner import Owner
from model.Building import Building
from model.RoomOwner import RoomOwner
from model.Room import Room



def main():
    # Création d'un propriétaire
    owner1 = Owner("John", "Doe", "123456789", "john@example.com", "password")

    # Création de deux bâtiments
    building1 = Building("Building 1", "City 1", "Quarter 1")
    building2 = Building("Building 2", "City 2", "Quarter 2")

    # Ajout des bâtiments à la liste des bâtiments du propriétaire
    owner1.addBuilding(building1)
    owner1.addBuilding(building2)

    # Création de deux chambres dans le premier bâtiment
    room1 = Room("101", 100.0, "Description for Room 101")
    room2 = Room("102", 150.0, "Description for Room 102")

    # Ajout des chambres au premier bâtiment
    building1.addRoom(room1)
    building1.addRoom(room2)

    # Création d'un locataire pour la chambre 101
    tenant1 = RoomOwner("Alice", "Smith", "987654321", "alice@example.com")
    room1.addRoomOwner(tenant1)
    tenant1.buyRoom(room1)

    # Affichage des informations
    owner1.afficher()
    print("\n")

    for building in owner1.buildings:
        building.afficher()
        print("\n")
        for room in building._rooms:
            room.afficher()
            print("\n")
            for owner in room._roomOwner:
                owner.afficher()
                print("\n")


if __name__ == "__main__":
    main()
