import tkinter as tk

ventana = tk.Tk()
ventana.title("Prueba Tkinter")

texto = tk.Label(ventana, text="Tkinter funciona")
texto.pack()

ventana.mainloop()