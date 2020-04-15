__author__ = "KhodeXenon"
__email__ = "KhodeXenon@gmail.com"

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import socket
import threading
from threading import Thread

connection_status = None

class ServerManager():
    def __init__(self,main_win):
        # clients socket connection list
        self.clients_list = []
        self.clients_num = 0
        # clients name list
        self.clients_name = []

        self.main_win = main_win
        self.main_win.title("Messenger (Server)")
        self.main_win.geometry("500x555")
        self.main_win.resizable(0, 0)
        self.server_ip_label = Label(self.main_win,font=("Tahoma",15),text="Server IP")
        self.server_ip_label.pack()
        self.server_ip_entry = Entry(self.main_win,font=("Tahoma",15))
        self.server_ip_entry.pack()

        self.server_port_num_label = Label(self.main_win,font=("Tahoma",15),text="Port")
        self.server_port_num_label.pack()
        self.server_port_num_entry = Entry(self.main_win,font=("Tahoma",15))
        self.server_port_num_entry.pack()

        self.server_start_button = Button(self.main_win,text = "           Start           ", font = ("Tahoma",15),fg = "Green",command = self.check_input_values)
        self.server_start_button.pack()

        self.server_stop_button = Button(self.main_win,text ="           stop           ", font = ("Tahoma",15),fg = "Red",command = self.server_stop_to_listening)
        self.server_stop_button.pack()
        self.server_stop_button.config(state ="disabled")

        self.client_list_label = Label(text = "Clients list",font=("Tahoma",15))
        self.client_list_label.pack()

        self.client_list_text_box = Text(self.main_win)
        self.client_list_text_box.pack()
        self.client_list_text_box.config(height = "13",width = "40",state = "disabled",font = ("Tahoma",15))

    def check_input_values(self):
        try :
            self.server_ip = self.server_ip_entry.get()
            self.server_port = int(self.server_port_num_entry.get())
        except ValueError:
            messagebox.showerror("Error","You must enter integer in port field e.g. (6969)")
        else:
            if len(self.server_ip) >= 7 :
                self.server_start_to_listening()
            else:
                messagebox.showerror("Error","Enter IP address correctly !")

    def server_start_to_listening(self):
        global connection_status
        connection_status = 1
        try :
            self.server_socket = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
            self.server_socket.bind((self.server_ip,self.server_port))
            self.server_socket.listen(10)
            Thread(target=self.connection_accept).start()

        except:
            messagebox.showerror("Error", "Listening failed !")
        else:
            connection_status = 1
            self.server_start_button.config(state="disabled")
            self.server_stop_button.config(state="normal")
            messagebox.showinfo("Connection",("listening on " + str(self.server_ip) + ":" + str(self.server_port)))

    def connection_accept(self):
        while True :
            if connection_status == 0 :
                break
            try:
                self.client_connection , client_ip = self.server_socket.accept()
                client_name = self.client_connection.recv(4096).decode()
                self.clients_name.append(client_name)
                self.update_clinets_list_display()
                for c in self.clients_list :
                    if c != self.client_connection :
                        c.sendall(client_name.encode() + b" joined")
                new_client_msg = "New client -> Name :"+ client_name + ", IP : " + client_ip[0]
                print(new_client_msg)
                # messagebox.showinfo("New client",new_client_msg)
                self.clients_num += 1
                self.clients_list.append(self.client_connection)
                self.client_connection.sendall(b"Welcome " + client_name.encode())
                print("Number of clients : " + str(self.clients_num))
                Thread(target=self.send_recv_clients_msg,args=(self.client_connection,client_name,client_ip[0])).start()
            except OSError :
                print("Connection is closed !")

    def send_recv_clients_msg(self,client_connection,client_name,client_ip):
        client = client_connection
        client_name = client_name
        client_ip = client_ip
        try:
            while True:
                data = client.recv(4096)
                print(data.decode())
                if not data : break
                if data == b"quit": break
                client_msg = data
                for c in self.clients_list :
                    if c != client :
                        c.sendall(client_msg)
        except ConnectionResetError :
            print("Connection is closed ! name :" + client_name + " with IP:" + client_ip)
            if client in self.clients_list:
                self.clients_list.remove(client)
            if client_name in self.clients_name:
                self.clients_name.remove(client_name)
            self.update_clinets_list_display()
            for c in self.clients_list:
                c.sendall(client_name.encode() + b" left")
        except OSError :
            print("Connection is closed ! name :" + client_name + " with IP:" + client_ip)
            if client in self.clients_list :
                self.clients_list.remove(client)
            if client_name in self.clients_name :
                self.clients_name.remove(client_name)
            self.update_clinets_list_display()
            for c in self.clients_list:
                c.sendall(client_name.encode() + b" left")
        except ConnectionAbortedError :
            print("Connection is closed ! name :" + client_name + " with IP:" + client_ip)
            if client in self.clients_list :
                self.clients_list.remove(client)
                if client_name in self.clients_name:
                    self.clients_name.remove(client_name)
            self.update_clinets_list_display()
            for c in self.clients_list:
                c.sendall(client_name.encode() + b" left")

    def update_clinets_list_display(self):
        self.client_list_text_box.config(state="normal")
        self.client_list_text_box.delete(1.0 ,tk.END)
        for client_name in self.clients_name :
            self.client_list_text_box.insert(tk.END,client_name + "\n")
        self.client_list_text_box.config(state="disabled")

    def server_stop_to_listening(self):
        global connection_status
        connection_status = 0
        self.server_socket.close()
        for client in self.clients_list :
            client.close()
        self.server_start_button.config(state="normal")
        self.server_stop_button.config(state="disabled")
        self.client_list_text_box.config(state="normal")
        self.client_list_text_box.delete("1.0", END)
        self.client_list_text_box.config(state="disabled")

root = Tk()
Gui = ServerManager(root)
Thread(target=root.mainloop()).start()
