from creditcard import CreditCard
from debitcard import DebitCard
from coin_machine import IKEAMyntAtare2000
from ui_info import UIClass, UIWay, UIDiscount, UIInfo
from abc import ABC, abstractmethod
from tariefeenheden import Tariefeenheden
from pricing_table import PricingTable

#aggregation with vending machine
class Oracle:
    @staticmethod
    def get_price(info: UIInfo):
        # get number of tariefeenheden
        if info.from_station == info.to_station:
            return False
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

        # round price to the nearest 5 cents
        price = round(price * 20) / 20

        # format price with 2 decimals
        formatted_price = "{:.2f}".format(price)

        return formatted_price

# Strategy design pattern
    
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
        # Round up to counts of 5
        coin.betala(self.price)
        coin.stoppa()

class Debit_Card(Payment_System):
    def pay(self):
        d = DebitCard()
        d.connect()
        dcid: int = d.begin_transaction(self.price)
        d.end_transaction(dcid)
        d.disconnect()

class Credit_Card(Payment_System):
    def pay(self):
        c = CreditCard()
        c.connect()
        ccid: int = c.begin_transaction(self.price)
        c.end_transaction(ccid)
        c.disconnect()