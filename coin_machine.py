from tkinter import messagebox

class IKEAMyntAtare2000:

	def starta(self):
		messagebox.showinfo(message = "Insert cash")

	def stoppa(self):
		messagebox.showinfo(message = "Payment succesful!")
		
	def betala(self, pris: int):
		messagebox.showinfo(message = f"{pris} euro")