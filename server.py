import socket
import threading

# Lista de clientes conectados
clientes = []

# Lista de nombres de usuario
usuarios = []

# Historial de mensajes
historial = []


# FUNCION PARA ENVIAR MENSAJE A TODOS
def broadcast(mensaje, cliente_actual=None):
    for cliente in clientes:
        if cliente != cliente_actual:
            cliente.send(mensaje)


# FUNCION PARA MANEJAR CADA CLIENTE
def manejar_cliente(cliente):

    while True:
        try:
            mensaje = cliente.recv(1024)

            if not mensaje:
                break

            texto = mensaje.decode()

            # Guardar en historial
            historial.append(texto)

            # Solo guardar los últimos 20
            if len(historial) > 20:
                historial.pop(0)

            # Enviar a todos
            broadcast(mensaje, cliente)

        except:
            break

    # Si sale del while significa que el cliente se desconectó
    index = clientes.index(cliente)
    clientes.remove(cliente)
    usuario = usuarios[index]
    usuarios.remove(usuario)

    mensaje = f"{usuario} ha salido del chat"
    broadcast(mensaje.encode())

    cliente.close()


# FUNCION PARA RECIBIR NUEVOS CLIENTES
def recibir():

    while True:

        cliente, direccion = servidor.accept()

        print("Conectado con", direccion)

        # Recibir nombre
        nombre = cliente.recv(1024).decode()

        usuarios.append(nombre)
        clientes.append(cliente)

        print(nombre, "se conectó")

        # Notificar a todos
        mensaje = f"{nombre} se ha unido al chat"
        broadcast(mensaje.encode())

        # Enviar historial al nuevo cliente
        for m in historial:
            cliente.send(m.encode())

        hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
        hilo.start()


# CREAR SERVIDOR
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((""localhost"", 5000))

servidor.listen(5)

print("Servidor esperando conexiones...")

recibir()