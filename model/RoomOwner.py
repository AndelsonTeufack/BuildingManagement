from uuid import uuid4

from MyEnum.AvailabilityStatus import AvailabilityStatus


class RoomOwner:
    def __init__(self, firstName, lastName, phone, email):
        self._id = str(uuid4())
        self._firstName = firstName
        self._lastName = lastName
        self._phone = phone
        self._email = email
        self._buildingName = None
        self._room = None

    @property
    def firstName(self):
        return self._firstName

    @firstName.setter
    def firstName(self, firstName):
        self._firstName = firstName

    @property
    def lastName(self):
        return self._lastName

    @lastName.setter
    def lastName(self, lastName):
        self._lastName = lastName

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def buildingName(self):
        return self._buildingName

    @buildingName.setter
    def buildingName(self, buildingName):
        self._buildingName = buildingName

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, room):
        self._room = room

    def removeRoom(self, room):
        if self._room == room:
            self._room.removeRoomOwner(self)
            self._room = None
        else:
            print("Error: The specified room is not associated with this room owner.")

    def buyRoom(self, room):
        if room.availabilityStatus == AvailabilityStatus.AVAILABLE:
            if self._room:
                self._room.removeRoomOwner(self)
            self._room = room
            room.clearRoomOwners()
            room.addRoomOwner(self)
            room.availabilityStatus = AvailabilityStatus.OCCUPIED
        else:
            print("Error: The specified room is not available for purchase.")

    def display(self):
        if self._room:
            building_name = self._room.building.name if self._room.building else "N/A"
            print(f"Name: {self._firstName.upper()} {self._lastName.capitalize()}")
            print(f"Phone: {self._phone}")
            print(f"Email: {self._email}")
            print(f"Building Name: {building_name}")
            print(f"Room Number: {self._room.number}")
        else:
            print(f"Name: {self._firstName.upper()} {self._lastName.capitalize()}")
            print(f"Phone: {self._phone}")
            print(f"Email: {self._email}")
            print("Building Name: N/A")
            print("Room Number: N/A")