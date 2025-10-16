class Account:
    def __init__(self, first_name, last_name, pesel, balance=0.0, promo_code = None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel
        self.balance = balance
        if type(pesel) != 'string' and len(self.pesel) != 11:
            self.pesel = "Invalid"
        self.promo_code = promo_code
        if promo_code and len(promo_code)==7 and promo_code.startswith("PROM_"):
            self.balance += 50


