from exceptions.AmountAdvancedError import AmountAdvancedError
from uuid import uuid4
from MyEnum.AvailabilityStatus import AvailabilityStatus


class Room:
    def __init__(self, number="", price=0.0, description="", amountAdvanced=None):
        self._id = str(uuid4())
        self._number = number
        self._price = price
        self._description = description
        self._building = None
        self._amountAdvanced = amountAdvanced
        self._leftToPay = None
        self._availabilityStatus = AvailabilityStatus.AVAILABLE
        self._roomOwner = []
        self.updateAvailabilityStatus()

    def updateAvailabilityStatus(self):
        try:
            if self._amountAdvanced is not None:
                if self._amountAdvanced < self._price:
                    self._availabilityStatus = AvailabilityStatus.RESERVED
                    self._leftToPay = self._price - self._amountAdvanced
                elif self._amountAdvanced == self._price:
                    self._availabilityStatus = AvailabilityStatus.OCCUPIED
                else:
                    raise AmountAdvancedError("Amount advanced exceeds the room price.")
        except AmountAdvancedError as e:
            print(f"Error: {str(e)}")
            raise

    @property
    def availabilityStatus(self):
        return self._availabilityStatus

    @availabilityStatus.setter
    def availabilityStatus(self, availabilityStatus):
        self._availabilityStatus = availabilityStatus

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price
        self.updateAvailabilityStatus()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def building(self):
        return self._building

    @building.setter
    def building(self, building):
        self._building = building

    @property
    def amountAdvanced(self):
        return self._amountAdvanced

    @amountAdvanced.setter
    def amountAdvanced(self, amountAdvanced):
        self._amountAdvanced = amountAdvanced
        self.updateAvailabilityStatus()

    def makeAdvancement(self, amount):
        self._amountAdvanced = amount
        self.updateAvailabilityStatus()

    @property
    def leftToPay(self):
        return self._leftToPay

    @leftToPay.setter
    def leftToPay(self, leftToPay):
        self._leftToPay = leftToPay

    def addRoomOwner(self, roomOwner):
        if roomOwner not in self._roomOwner:
            self._roomOwner.append(roomOwner)
            roomOwner.room = self
        else:
            print("Error: The specified room owner is already associated with this room.")

    def clearRoomOwners(self):
        self._roomOwner = []

    def removeRoomOwner(self, roomOwner):
        if roomOwner in self._roomOwner:
            self._roomOwner.remove(roomOwner)
            roomOwner.room = None
        else:
            print("Error: The specified room owner is not associated with this room.")

    def display(self):
        building_name = self.building.name if self.building else "N/A"
        print(f"Room Number: {self.number}\nRoom Price: {self.price}\nRoom Description: {self.description}\n"
              f"Room Building: {building_name}\nAvailability: {self._availabilityStatus.value}")

        if self._availabilityStatus == AvailabilityStatus.RESERVED:
            if self.amountAdvanced is not None:
                print(f"Amount Advanced: {self.amountAdvanced}")
            if self.leftToPay is not None:
                print(f"Left to Pay: {self.leftToPay}")

        if self._availabilityStatus == AvailabilityStatus.OCCUPIED or self._availabilityStatus == AvailabilityStatus.RESERVED:
            for owner in self._roomOwner:
                print(f"Owner Name: {owner.firstName.upper()} {owner.lastName.capitalize()}")
                print(f"Phone: {owner.phone}")

    def to_dict(self):
        room_dict = {
            "_id": self._id,
            "_number": self._number,
            "_price": self._price,
            "_description": self._description,
            "_roomOwner": [roomOwner for roomOwner in self._roomOwner],
            "_building_name": (f"{self.building.name}" if self._building else None),
            "_amountAdvanced": self._amountAdvanced,
            "_leftToPay": self._leftToPay,
            "_availabilityStatus": self._availabilityStatus

        }
        return room_dict

    @classmethod
    def from_dict(cls, room_dict):
        room = cls(
            room_dict["_number"],
            room_dict["_price"],
            room_dict["_description"],
            room_dict["_amountAdvanced"],
        )
        room._id = room_dict["_id"]
        room._roomOwner = room_dict["_roomOwner"]
        return room

