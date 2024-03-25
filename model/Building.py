from uuid import uuid4

from model.Room import AvailabilityStatus


class Building:
    def __init__(self, name="", city="", quarter=""):
        self._owner = None
        self._id = str(uuid4())
        self._name = name
        self._city = city
        self._quarter = quarter
        self._rooms = []

    @property
    def id(self):
        return self._id

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = owner

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    @property
    def quarter(self):
        return self._quarter

    @quarter.setter
    def quarter(self, quarter):
        self._quarter = quarter

    @property
    def rooms(self):
        return self._rooms

    @rooms.setter
    def rooms(self, rooms):
        self._rooms = rooms

    @property
    def nbrOfRooms(self):
        return len(self._rooms)

    @property
    def nbrOfFreeRooms(self):
        return sum(room.availabilityStatus == AvailabilityStatus.AVAILABLE for room in self._rooms)

    def display(self):
        owner_name = f"{self.owner.firstName.upper()} {self.owner.lastName.capitalize()}" if self.owner else "N/A"
        print(f"Name: {self.name}\nQuarter: {self.quarter}\nCity: {self.city}\nOwner: {owner_name}\n"
              f"Number of Rooms: {self.nbrOfRooms}\nNumber of Free Rooms: {self.nbrOfFreeRooms}")

    def addRoom(self, room):
        if room not in self._rooms:
            self._rooms.append(room)
            room.building = self
        else:
            print("Erreur: le numero existe deja!")

    def removeRoom(self, room):
        if room in self._rooms:
            self._rooms.remove(room)
            room.setBuilding(None)

    def to_dict(self):
        room_dicts = [room for room in self._rooms]
        building_dict = {
            "_id": self._id,
            "_name": self._name,
            "_city": self._city,
            "_quarter": self._quarter,
            "_rooms": room_dicts,
            "_owner_name": (f"{self._owner.firstName.upper()} {self._owner.lastName.capitalize()}"
                            if self._owner else None)
        }
        return building_dict

    @classmethod
    def from_dict(cls, building_dict):
        building = cls(
            building_dict["_name"],
            building_dict["_city"],
            building_dict["_quarter"],
        )
        building._id = building_dict["_id"]
        building._rooms = building_dict["_rooms"]
        return building
