class CompteBancaire:
    def __init__(self, name="Wambe", balance=1000.0):
        self._name = name
        self._balance = balance

    def depot(self, montant):
        self._balance += montant
        print(f"Depot de {montant} effectue avec succes!")

    def retrait(self, montant):
        self._balance -= montant
        print(f"Retrait de {montant} effectue avec succes!")

    def display(self):
        print(f"Name: {self._name}\nBalance: {self._balance}")


compte1 = CompteBancaire()
compte1.depot(100)
compte1.retrait(25)
compte1.display()
print()
compte2 = CompteBancaire("YONKEU", 5000.0)
compte2.depot(100)
compte2.retrait(25)
compte2.display()
