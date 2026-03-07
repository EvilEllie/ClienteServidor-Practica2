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


ventana_login = tk.Tk()
ventana_login.title("Conectar al Chat")
ventana_login.geometry("300x180")
ventana_login.resizable(False, False)

tk.Label(ventana_login, text="Nombre de usuario:").pack(pady=(20, 2))
entrada_nombre = tk.Entry(ventana_login, width=30)
entrada_nombre.pack()

tk.Label(ventana_login, text="IP del servidor:").pack(pady=(10, 2))
entrada_ip = tk.Entry(ventana_login, width=30)
entrada_ip.insert(0, "192.168.1.78")  # IP por defecto
entrada_ip.pack()

nombre_usuario = ""
conectado = False

def intentar_conectar():
    global nombre_usuario, conectado
    nombre = entrada_nombre.get().strip()
    ip = entrada_ip.get().strip()

    if not nombre:
        messagebox.showwarning("Aviso", "Ingresa un nombre de usuario")
        return
    if not ip:
        messagebox.showwarning("Aviso", "Ingresa la IP del servidor")
        return

    try:
        cliente.connect((ip, 5000))
        cliente.send(nombre.encode())
        nombre_usuario = nombre
        conectado = True
        ventana_login.destroy()
    except:
        messagebox.showerror("Error", "No se pudo conectar al servidor.\nVerifica la IP y que el servidor esté activo.")

boton_conectar = tk.Button(ventana_login, text="Conectar", command=intentar_conectar)
boton_conectar.pack(pady=15)

ventana_login.mainloop()

if not conectado:
    exit()
