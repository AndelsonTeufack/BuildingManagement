# class CompteBancaire:
#     def __init__(self, name="Wambe", balance=1000.0):
#         self._name = name
#         self._balance = balance
#
#     def depot(self, montant):
#         try:
#             self._balance += montant
#             if montant<=0:
#                 raise Exception("Le montant doit etre supperieur a 0")
#             print(f"Depot de {montant} effectue avec succes!")
#         except Exception as e:
#             print(e)
#
#     def retrait(self, montant):
#         self._balance -= montant
#         print(f"Retrait de {montant} effectue avec succes!")
#
#     def display(self):
#         print(f"Name: {self._name}\nBalance: {self._balance}")
#
#
# compte1 = CompteBancaire()
# compte1.depot(100)
# compte1.retrait(25)
# compte1.display()
# print()
# compte2 = CompteBancaire("YONKEU", 5000.0)
# compte2.depot(100)
# compte2.retrait(25)
# compte2.display()

class Voiture:
    def __init__(self, marque="Yaris", couleur="Rouge"):
        self._marque = marque
        self._couleur = couleur
        self._pilote = "personne"
        self._vitesse = 0

    def choixDuConducteur(self, nom):
        self._pilote = nom

    def accelerer(self, taux, duree):
        try:
            if self._pilote == "personne":
                raise Exception("Vous devez avoir un pilote pour accelerer!")
            self._vitesse = (taux * duree)
        except Exception as e:
            print("Erreur:", e)

    def afficheTout(self):
        print(f"Marque:{self._marque}\nCouleur: {self._couleur}\nVitesse: {self._vitesse}\nConducteur: {self._pilote}")


v1 = Voiture()
v1.accelerer(1.3, 20)
v2 = Voiture("Toyota", "Rose")
v2.choixDuConducteur("Andy")
v2.accelerer(1.3, 20)
v2.afficheTout()
