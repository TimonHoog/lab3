from tariefeenheden import Tariefeenheden
import tkinter as tk
from ui_info import UIClass, UIWay, UIDiscount, UIPayment, UIInfo
from sale import Credit_Card, Debit_Card, Cash_Payment, Oracle
from ticket_printer import Ticket_Printer
from tkinter import messagebox

class Vending_Machine_logic(tk.Frame):

	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.widgets()

	def payment_handling(self, info: UIInfo, price: float):
		if info.payment == UIPayment.CreditCard:
			price = float(price) + 0.50
			payment_system = Credit_Card(price)
		elif info.payment == UIPayment.DebitCard:
			payment_system = Debit_Card(price)
		elif info.payment == UIPayment.Cash:
			payment_system = Cash_Payment(price)
		payment_system.pay()

	# amount of tickets that are available in the printer to be printed.
	amount_of_tickets = 100

	def handle_payment(self, info: UIInfo):
		# the design patterns are applied in sale.py, but referenced here
		price = Oracle.get_price(info)
		if price == False:
			messagebox.showwarning(title="Warning", message = "You cannot travel to the same station")
		else:
			self.payment_handling(info, price)
			# printing the ticket and subtracting the available tickets
			Ticket_Printer(info, price).print_ticket(info, price)
			Vending_Machine_logic.amount_of_tickets = Vending_Machine_logic.amount_of_tickets - 1

	def widgets(self):
		self.master.title("Ticket machine")
		menubar = tk.Menu(self.master)
		self.master.config(menu=menubar)
		color = '#FFC917'
		fileMenu = tk.Menu(menubar)
		fileMenu.add_command(label="Exit", command=self.on_exit)
		menubar.add_cascade(label="File", menu=fileMenu)

		# retrieve the list of stations
		data2 = Tariefeenheden.get_stations()

		stations_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1,bg=color)
		stations_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
		# From station
		tk.Label(stations_frame, text = "From station:",bg=color).grid(row=0, padx=5, sticky=tk.W)
		self.from_station = tk.StringVar(value=data2[0])
		tk.OptionMenu(stations_frame, self.from_station, *data2,).grid(row=1, padx=5, sticky=tk.W)
  

		# To station
		tk.Label(stations_frame, text = "To station:",bg=color).grid(row=0, column=1, sticky=tk.W)
		self.to_station = tk.StringVar(value=data2[0])
		tk.OptionMenu(stations_frame, self.to_station, *data2).grid(row=1, column=1, sticky=tk.W)

		ticket_options_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1,bg= color)
		ticket_options_frame.pack(fill=tk.BOTH, expand=1, padx=10)

		# Class
		tk.Label(ticket_options_frame, text = "Travel class:", bg=color).grid(row=1, sticky=tk.W)
		self.travel_class = tk.IntVar(value=UIClass.SecondClass.value)
		tk.Radiobutton(ticket_options_frame, text="First class", variable=self.travel_class, value=UIClass.FirstClass.value, bg=color).grid(row=5, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="Second class", variable=self.travel_class, value=UIClass.SecondClass.value, bg=color).grid(row=6, sticky=tk.W)

		# Way
		tk.Label(ticket_options_frame, text = "Way:", bg=color).grid(row=7, sticky=tk.W)
		self.way = tk.IntVar(value=UIWay.OneWay.value)
		tk.Radiobutton(ticket_options_frame, text="One-way", variable=self.way, value=UIWay.OneWay.value,bg=color).grid(row=8, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="Return", variable=self.way, value=UIWay.Return.value,bg=color).grid(row=9, sticky=tk.W)

		# Discount
		tk.Label(ticket_options_frame, text = "Discount:",bg=color).grid(row=10, sticky=tk.W)
		self.discount = tk.IntVar(value=UIDiscount.NoDiscount.value)
		tk.Radiobutton(ticket_options_frame, text="No discount", variable=self.discount, value=UIDiscount.NoDiscount.value,bg=color).grid(row=11, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="20% discount", variable=self.discount, value=UIDiscount.TwentyDiscount.value,bg=color).grid(row=12, sticky=tk.W)
		tk.Radiobutton(ticket_options_frame, text="40% discount", variable=self.discount, value=UIDiscount.FortyDiscount.value,bg=color).grid(row=13, sticky=tk.W)

		payment_frame = tk.Frame(self.master, highlightbackground="#cccccc", highlightthickness=1,bg=color)
		payment_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

		# Payment
		tk.Label(payment_frame, text = "Payment:",bg=color).grid(row=14, sticky=tk.W)
		self.payment = tk.IntVar(value=UIPayment.Cash.value)
		tk.Radiobutton(payment_frame, text="Cash", variable=self.payment, value=UIPayment.Cash.value,bg=color).grid(row=15, sticky=tk.W)
		tk.Radiobutton(payment_frame, text="Credit Card", variable=self.payment, value=UIPayment.CreditCard.value,bg=color).grid(row=16, sticky=tk.W)
		tk.Radiobutton(payment_frame, text="Debit Card", variable=self.payment, value=UIPayment.DebitCard.value,bg=color).grid(row=17, sticky=tk.W)

		# Pay button
		tk.Button(self.master, text="Pay", bg=color ,command=self.on_click_pay).pack(side=tk.RIGHT, ipadx=10, padx=10, pady=10)

		self.pack(fill=tk.BOTH, expand=1)
	
	def on_click_pay(self):
		self.handle_payment(self.get_ui_info())


	def get_ui_info(self) -> UIInfo:
		return UIInfo(from_station=self.from_station.get(),
			to_station=self.to_station.get(),
			travel_class=self.travel_class.get(),
			way=self.way.get(),
			discount=self.discount.get(),
			payment=self.payment.get())

	def on_exit(self):
		self.quit()

#endregion

def main():

	root = tk.Tk()
	root.configure(background="#0063D3")
	Vending_Machine_logic(root)

	root.mainloop()


if __name__ == '__main__':
	main()