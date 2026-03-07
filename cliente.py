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


ventana = tk.Tk()
ventana.title(f"Chat - {nombre_usuario}")
ventana.geometry("700x400")

# FRAME PRINCIPAL
frame = tk.Frame(ventana)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# AREA DE CHAT
area_chat = scrolledtext.ScrolledText(frame)
area_chat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

area_chat.tag_config("propio", foreground="blue")
area_chat.tag_config("otros", foreground="green")
area_chat.tag_config("notificacion", foreground="gray", font=("Arial", 9, "italic"))
area_chat.tag_config("historial", foreground="purple", font=("Arial", 9, "italic"))

# PANEL LATERAL DE USUARIOS
frame_usuarios = tk.Frame(frame)
frame_usuarios.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
tk.Label(frame_usuarios, text="Usuarios Conectados").pack()
lista_usuarios = tk.Listbox(frame_usuarios)
lista_usuarios.pack(fill=tk.Y, expand=True)

# ENTRADA DE TEXTO Y BOTON
entrada_mensaje = tk.Entry(ventana, width=60)
entrada_mensaje.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
entrada_mensaje.bind("<Return>", enviar_mensaje)  # Enter también envía
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje)
boton_enviar.pack(side=tk.LEFT, padx=5, pady=10)