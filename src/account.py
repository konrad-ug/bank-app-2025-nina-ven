from smtp.smtp import SMTPClient
import datetime

class Account:
    express_outgoing_transfer_fee = 0.0
    history_email_text_template = "General account history: {}"
    def __init__(self):
        self.history:list[float] = []
        self.balance:float = 0.0


    def transfer_in(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
            self.history.append(amount)

    def transfer_out(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)

    def express_transfer_out(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount + self.express_outgoing_transfer_fee
            self.history.append(-amount)
            self.history.append(-self.express_outgoing_transfer_fee)

    def send_history_via_email(self, email:str) -> bool:
        today = datetime.date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        text = self.history_email_text_template.format(self.history)
        return SMTPClient.send(subject, text, email)





