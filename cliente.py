import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                break

            # Mensajes de actualización de usuarios
            if mensaje.startswith("USUARIOS:"):
                lista = mensaje.replace("USUARIOS:", "").split(",")
                lista_usuarios.delete(0, tk.END)
                for u in lista:
                    if u:
                        lista_usuarios.insert(tk.END, u)

            # Mensajes del historial
            elif mensaje.startswith("[HISTORIAL]"):
                texto = mensaje.replace("[HISTORIAL]", "")
                area_chat.insert(tk.END, texto, "historial")
                area_chat.yview(tk.END)

            # Notificaciones de sistema
            elif "se ha unido al chat" in mensaje or "ha salido del chat" in mensaje:
                area_chat.insert(tk.END, mensaje + "\n", "notificacion")
                area_chat.yview(tk.END)

            # Mensajes propios
            elif mensaje.startswith(nombre_usuario + ":"):
                area_chat.insert(tk.END, mensaje + "\n", "propio")
                area_chat.yview(tk.END)

            # Mensajes de otros
            else:
                area_chat.insert(tk.END, mensaje + "\n", "otros")
                area_chat.yview(tk.END)

        except:
            messagebox.showerror("Error", "Se perdió la conexión con el servidor")
            break

# =====================================
# FUNCION PARA ENVIAR MENSAJES
# =====================================
def enviar_mensaje(event=None):
    mensaje = entrada_mensaje.get()
    if mensaje:
        try:
            cliente.send(f"{nombre_usuario}: {mensaje}".encode())
            # Mostrar mensaje propio en el chat local
            area_chat.insert(tk.END, f"{nombre_usuario}: {mensaje}\n", "propio")
            area_chat.yview(tk.END)
            entrada_mensaje.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "No se pudo enviar el mensaje")
