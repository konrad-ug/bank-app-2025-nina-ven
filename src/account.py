class Account:
    def __init__(self, first_name, last_name, pesel, balance=0.0, promo_code = None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel
        self.balance = balance
        if type(pesel) != "string" and len(self.pesel) != 11:
            self.pesel = "Invalid"
        self.promo_code = promo_code
        if promo_code and len(promo_code)==8 and promo_code.startswith("PROM_") and yob_from_pesel(self.pesel)>1960:
            self.balance += 50

    def transfer_in(self, amount: float):
        if amount > 0:
            self.balance += amount
            return
        else:
            return "Niewłaściwe dane do transferu"
            raise TypeError("Niewłaściwe dane do transferu")

    def transfer_out(self, amount: float):
        if amount > 0:
            if amount > self.balance:
                return "Brak fundów do transferu"
                raise ValueError("Brak fundów do transferu")
            self.balance -= amount
            return
        else:
            return "Niewłaściwe dane do transferu"
            raise TypeError("Niewłaściwe dane do transferu")



def yob_from_pesel(pesel): # dla roku 1900+
    if pesel.isdigit() : # isinstance(pesel, str) możnaby ale pesel jest już sprawdzany czy jest stringiem o długości 11
        if int(pesel[2:4]) > 12:
            return 2000 + int(pesel[:2])
        else:
            return 1900 + int(pesel[:2])
    else:
        return 0
