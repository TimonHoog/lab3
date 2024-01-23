from creditcard import CreditCard
from debitcard import DebitCard
from coin_machine import IKEAMyntAtare2000
from ui_info import UIPayment, UIClass, UIWay, UIDiscount, UIPayment, UIInfo
from abc import ABC, abstractmethod
from tariefeenheden import Tariefeenheden
from pricing_table import PricingTable
from ui_info import UIPayment, UIClass, UIWay, UIDiscount, UIPayment, UIInfo

class Oracle:
    @staticmethod
    def get_price(info: UIInfo):
        # get number of tariefeenheden
        tariefeenheden: int = Tariefeenheden.get_tariefeenheden(info.from_station, info.to_station)

        # compute the column in the table based on choices
        table_column = 0
        if info.travel_class == UIClass.FirstClass:
            table_column = 3

        # then, on the discount
        if info.discount == UIDiscount.TwentyDiscount:
            table_column += 1
        elif info.discount == UIDiscount.FortyDiscount:
            table_column += 2

        # compute price
        price: float = PricingTable.get_price(tariefeenheden, table_column)
        if info.way == UIWay.Return:
            price *= 2

        return price

class Payment_System(ABC):
    def __init__(self, price):
        self.price = price

    @abstractmethod
    def pay(self):
        pass

class Cash_Payment(Payment_System):
    def pay(self):
        coin = IKEAMyntAtare2000()
        coin.starta()
        coin.betala(int(round(self.price * 100))) #prijs wordt nog op centen gerekend, wij hadden volgens mij requirement op 10/5 centen. Moet nog even checken. 
        coin.stoppa()

class Debit_Card(Payment_System):
    def pay(self):
        d = DebitCard()
        d.connect()
        dcid: int = d.begin_transaction(round(self.price, 2))
        d.end_transaction(dcid)
        d.disconnect()

class Credit_Card(Payment_System):
    def pay(self):
        c = CreditCard()
        c.connect()
        ccid: int = c.begin_transaction(round(self.price, 2))
        c.end_transaction(ccid)
        c.disconnect()

def payment_handling(info: UIInfo, price: float):
    # add 50 cents if paying with credit card
    if info.payment == UIPayment.CreditCard:
        price += 0.50

    # pay
    if info.payment == UIPayment.CreditCard:
        payment_system = Credit_Card(price)
    elif info.payment == UIPayment.DebitCard:
        payment_system = Debit_Card(price)
    elif info.payment == UIPayment.Cash:
        payment_system = Cash_Payment(price)

    payment_system.pay()
    

# Als we de payment handling als class willen hebben:
"""class PaymentHandler:
    def __init__(self, info: UIInfo, price: float):
        self.info = info
        self.price = price

    def handle_payment(self):
        # add 50 cents if paying with credit card
        if self.info.payment == UIPayment.CreditCard:
            self.price += 0.50

        # pay
        if self.info.payment == UIPayment.CreditCard:
            payment_system = Credit_Card(self.price)
        elif self.info.payment == UIPayment.DebitCard:
            payment_system = Debit_Card(self.price)
        elif self.info.payment == UIPayment.Cash:
            payment_system = Cash_Payment(self.price)

        payment_system.pay()"""
        
#In UI.py moeten we dan doen:
"""
from sale import PaymentHandler
def handle_payment(self, info: UIInfo):
        price = Oracle.get_price(info)
        handler = PaymentHandler(info, price)
        handler.handle_payment()"""

