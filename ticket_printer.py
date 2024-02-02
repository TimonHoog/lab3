from datetime import datetime
from ui_info import UIInfo
from tkinter import messagebox

# inheritance with vending machine logic
class Ticket_Printer:
    def __init__(self, info: UIInfo, prijs):
        self.info = info
        self.prijs = prijs
        pass
    
    def print_ticket(self, info, prijs):
        # for now it will print the day the ticket is printed
        # https://stackoverflow.com/q/32490629
        ticket_date = datetime.today().strftime('%d-%m-%Y')
        
        # the GUI only allows for one ticket to be printed, this code allows the 1 to be changed to a variable
        to_print = 1
        price = prijs
        carriage_class = info.travel_class
        return_ticket = info.way
        starting_location = info.from_station
        ending_location =  info.to_station
        discount = info.discount

        # rename the boolean value to an understandable, printable one
        if return_ticket == 2:
            return_ticket = 'Return trip'
        elif return_ticket == 1:
            return_ticket = 'Single trip'

        # same for the discounts        
        if discount == 1:
            discount = 'No discount applied'
        elif discount == 2:
            discount = '20% discount applied'
        elif discount == 3: 
            discount = '40% discount applied'
        
        # This is to display the correct price including the supplement on the ticket
        if info.payment == 2:
            price = float(price) + 0.5

        messagebox.showinfo(
            title="Ticket", 
            message = f"Print date: {ticket_date}\nTicket amount: {to_print}\nTicket cost:{price} euro\nApplied discount: {discount}\nYou are travelling {carriage_class} class\nThe ticket is valid on: {ticket_date}\n Ticket type: {return_ticket}\nFrom: {starting_location}\nTo: {ending_location}"
            )
