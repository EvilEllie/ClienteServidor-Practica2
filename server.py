import socket
import threading


# LISTAS DE CLIENTES, USUARIOS E HISTORIAL

clientes = []  # Sockets de clientes conectados
usuarios = []  # Nombres de usuario
historial = [] # Últimos 20 mensajes