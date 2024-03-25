from uuid import uuid4


class Owner:
    def __init__(self, firstName="", lastName="", phone="", email="", password=""):
        self._id = str(uuid4())
        self._firstName = firstName
        self._lastName = lastName
        self._phone = phone
        self._email = email
        self._password = password
        self._buildings = []

    @property
    def id(self):
        return self._id

    @property
    def firstName(self):
        return self._firstName

    @firstName.setter
    def firstName(self, firstname):
        self._firstName = firstname

    @property
    def lastName(self):
        return self._lastName

    @lastName.setter
    def lastName(self, lastname):
        self._lastName = lastname

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
    def buildings(self):
        return self._buildings

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def addBuilding(self, building):
        if building not in self._buildings:
            self._buildings.append(building)
            building.owner = self

    def removeBuilding(self, building):
        if building in self._buildings:
            self._buildings.remove(building)
            building.setOwner(None)

    @classmethod
    def from_dict(cls, owner_dict):
        owner = cls(
            owner_dict["_firstName"],
            owner_dict["_lastName"],
            owner_dict["_phone"],
            owner_dict["_email"],
            owner_dict["_password"]
        )
        owner._id = owner_dict["_id"]
        owner._buildings = owner_dict["_buildings"]
        return owner

    def to_dict(self):
        owner_dict = {
            "_id": self._id,
            "_firstName": self._firstName,
            "_lastName": self._lastName,
            "_phone": self._phone,
            "_email": self._email,
            "_password": self._password,
            "_buildings": [building for building in self.buildings]
        }
        return owner_dict

    def display(self):
        print(f"Name: {self.firstName.upper()} {self.lastName.capitalize()}\nPhone: {self.phone}\n"
              f"Email: {self.email}\nBuildings: {', '.join([building.name for building in self._buildings])}")
