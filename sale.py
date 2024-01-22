def handle_payment(self, info: UIInfo):
    # **************************************
    # Below is the code you need to refactor test
    # **************************************
    class Oracle_Database():
        
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
        price: float = PricingTable.get_price (tariefeenheden, table_column)
        if info.way == UIWay.Return:
            price *= 2

    class Payment_System(ABC):
        # pay
        def __init__(self, payment):
            self.payment = payment
            pass
        def choose(self, info):
            if info.payment == UIPayment.CreditCard:
                Credit_Card()
            elif info.payment == UIPayment.DebitCard:
                Debit_Card()
            elif info.payment == UIPayment.Cash:
                Cash_Payment()

    class Cash_Payment(Payment_System):
        coin = IKEAMyntAtare2000()
        coin.starta()
        coin.betala(int(round(price * 100)))
        coin.stoppa()

    class Debit_Card(Payment_System):
        d = DebitCard()
        d.connect()
        dcid: int = d.begin_transaction(round(price, 2))
        d.end_transaction(dcid)
        d.disconnect()

    class Credit_Card(Payment_System):
        c = CreditCard()
        c.connect()
        ccid: int = c.begin_transaction(round(price, 2))
        c.end_transaction(ccid)
        c.disconnect()
        
        # add 50 cents if paying with credit card
        if info.payment == UIPayment.CreditCard:
            price += 0.50
