from datetime import datetime
from ui_info import UIInfo
from tkinter import messagebox

class Ticket_Printer:
    def __init__(self, info: UIInfo, prijs):
        self.info = info
        self.prijs = prijs
        pass
    
    def print_ticket(self, info, prijs):
        # the GUI only allows for one ticket to be printed, this code allows the 1 to be changed to a variable
        to_print = 1
        
        price = prijs
        carriage_class = info.travel_class
        # for now it will print the day the ticket is printed
        # https://stackoverflow.com/q/32490629
        print_date = datetime.today().strftime('%d-%m-%Y')
        # the GUI only prints tickets for today, otherwise print_date can be changed to a variable for another date
        travel_date = print_date
        return_ticket = info.way
        # rename the boolean value to an understandable, printable one
        if return_ticket == 2:
            return_ticket = 'Return trip'
        elif return_ticket == 1:
            return_ticket = 'Single trip'
        starting_location = info.from_station
        ending_location =  info.to_station
        discount = info.discount
        if discount == 1:
            discount = 'No discount applied'
        elif discount == 2:
            discount = '20% discount applied'
        elif discount == 3: 
            discount = '40% discount applied'
        messagebox.showinfo(title="Ticket", message = f"Print date: {print_date}\nTicket amount: {to_print}\nTicket cost:{price} euro\nApplied discount: {discount}\nYou are travelling {carriage_class} class\nThe ticket is valid on: {travel_date}\nReturn ticket: {return_ticket}\nFrom: {starting_location}\nTo: {ending_location}")
