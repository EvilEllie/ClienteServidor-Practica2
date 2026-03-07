import socket
import threading



clientes = []  
usuarios = []  
historial = [] 

def broadcast(mensaje, cliente_actual=None):
    for cliente in clientes:
        if cliente != cliente_actual:
            try:
                cliente.send(mensaje)
            except:
                pass

def actualizar_usuarios():
    lista = ",".join(usuarios)
    for cliente in clientes:
        try:
            cliente.send(f"    USUARIOS: {lista}".encode())
        except:
            pass
