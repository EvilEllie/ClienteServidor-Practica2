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

  
        for m in historial:
            try:
                cliente.send(f"[HISTORIAL]{m}".encode())
            except:
                pass


        notificacion = f"{nombre} se ha unido al chat".encode()
        for c in clientes:
            try:
                c.send(notificacion)
            except:
                pass


        actualizar_usuarios()

        hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
        hilo.daemon = True
        hilo.start()


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("0.0.0.0", 5000))  
servidor.listen(5)                 
print("Servidor esperando conexiones...")
recibir()