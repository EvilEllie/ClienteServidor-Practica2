import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
