import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# CREAR VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("Chat Cliente-Servidor")
ventana.geometry("500x400")

# AREA DONDE SE MOSTRARAN LOS MENSAJES
area_chat = scrolledtext.ScrolledText(ventana)
area_chat.pack(padx=10, pady=10)

# CAMPO PARA ESCRIBIR MENSAJE
entrada_mensaje = tk.Entry(ventana, width=40)
entrada_mensaje.pack(side=tk.LEFT, padx=10, pady=10)

# BOTON ENVIAR
boton_enviar = tk.Button(ventana, text="Enviar")
boton_enviar.pack(side=tk.LEFT)

# MANTENER LA VENTANA ABIERTA
ventana.mainloop()