import socket
import threading

# =====================================
# LISTAS DE CLIENTES, USUARIOS E HISTORIAL
# =====================================
clientes = []  # Sockets de clientes conectados
usuarios = []  # Nombres de usuario
historial = [] # Últimos 20 mensajes

# =====================================
# FUNCION PARA ENVIAR MENSAJE A TODOS
# =====================================
def broadcast(mensaje, cliente_actual=None):
    for cliente in clientes:
        if cliente != cliente_actual:
            try:
                cliente.send(mensaje)
            except:
                pass

# =====================================
# FUNCION PARA ACTUALIZAR LISTA DE USUARIOS (a TODOS)
# =====================================
def actualizar_usuarios():
    lista = ",".join(usuarios)
    for cliente in clientes:
        try:
            cliente.send(f"    USUARIOS: {lista}".encode())
        except:
            pass

# =====================================
# FUNCION PARA MANEJAR CADA CLIENTE
# =====================================
def manejar_cliente(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:
                break
            texto = mensaje.decode()

            # Guardar en historial CON salto de linea
            historial.append(texto + "\n")
            if len(historial) > 20:
                historial.pop(0)

            # Enviar a todos menos al remitente
            broadcast(mensaje, cliente)
        except:
            break

    # Cliente se desconecta
    if cliente in clientes:
        index = clientes.index(cliente)
        usuario = usuarios[index]
        clientes.remove(cliente)
        usuarios.remove(usuario)
        print(usuario, "se desconectó")

        # Notificación de salida
        broadcast(f"{usuario} ha salido del chat".encode())
        actualizar_usuarios()
        cliente.close()

# =====================================
# FUNCION PARA RECIBIR NUEVOS CLIENTES
# =====================================
def recibir():
    while True:
        cliente, direccion = servidor.accept()
        print("Conectado con", direccion)

        try:
            nombre = cliente.recv(1024).decode()
        except:
            cliente.close()
            continue

        clientes.append(cliente)
        usuarios.append(nombre)
        print(nombre, "se conectó")

        # Enviar historial al nuevo cliente PRIMERO
        for m in historial:
            try:
                cliente.send(f"[HISTORIAL]{m}".encode())
            except:
                pass

        # Notificar a todos (incluyendo al nuevo cliente)
        notificacion = f"{nombre} se ha unido al chat".encode()
        for c in clientes:
            try:
                c.send(notificacion)
            except:
                pass

        # Actualizar lista de usuarios para todos
        actualizar_usuarios()

        hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
        hilo.daemon = True
        hilo.start()

# =====================================
# CREAR SERVIDOR
# =====================================
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("0.0.0.0", 5000))  # Escucha en todas las interfaces
servidor.listen(5)                 # Hasta 5 conexiones simultáneas
print("Servidor esperando conexiones...")
recibir()