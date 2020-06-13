#!/bin/python3
__author__ = "KhodeXenon"
__email__ = "KhodeXenon@gmail.com"

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import socket
from threading import Thread

server_ip = ""
port_num = ""
username = ""
password = ""
server_status = None

#class for main GUI
class LoginGui():
    def __init__(self,main_win):
        # define GUI options
        self.chat_win_exist = None
        self.main_win = main_win
        self.main_win.title("Messenger (Client)")
        self.main_win.geometry("610x150")
        self.main_win.resizable(0,0)
        self.lbl_user = Label(main_win, text="Name", padx=10, pady=10, font=("Tahoma", 15))
        self.lbl_user.grid(row=0, column=0)
        self.lbl_user_entry = Entry(main_win, font=("Tahoma", 11))
        self.lbl_user_entry.grid(row=0, column=1)

        self.lbl_pass = Label(main_win, text="Password", padx=10, pady=10, font=("Tahoma", 15))
        self.lbl_pass.grid(row=0, column=2)
        self.lbl_pass_entry = Entry(main_win, show="*", font=("Tahoma", 11))
        self.lbl_pass_entry.grid(row=0, column=3)

        self.server_ip_label = Label(main_win, text="Server IP", padx=10, pady=10, font=("Tahoma", 15))
        self.server_ip_label.grid(row=2, column=0)
        self.server_ip_entry = Entry(main_win, font=("Tahoma", 13))
        self.server_ip_entry.grid(row=2, column=1)

        self.server_port_num = Label(main_win, text="Port", padx=10, pady=10, font=("Tahoma", 15))
        self.server_port_num.grid(row=2, column=2)
        self.server_port_entry = Entry(main_win, font=("Tahoma", 11))
        self.server_port_entry.grid(row=2, column=3)
        self.default_port = StringVar()
        self.default_port_check_button = Checkbutton(main_win,font = ("Tahoma",15),text = "Default port (54321)",offvalue = "off",onvalue = "on" ,variable = self.default_port , command = self.change_port_entry)
        self.default_port_check_button.config(fg="Green")
        self.default_port_check_button.grid(row=3 , column = 1)

        self.connect_button = Button(main_win, text="Connect", font=("Tahoma", 17), command = self.create_chat_gui)
        self.connect_button.config(activeforeground="Blue",activebackground="White")
        self.connect_button.grid(row=3, column=3)

    #create a function for connect button
    def create_chat_gui(self):
        try_to_connect_or_not = messagebox.askokcancel("Connection", "If the chat window exists ,it will be closed")
        if try_to_connect_or_not == True:
            if (self.chat_win_exist is None) or (self.chat_win_exist is not None) :
                try :
                    self.chat_win_exist.chat_win.destroy()
                except :
                    self.chat_win_exist = ChatGui(self)
                else :
                    self.chat_win_exist = ChatGui(self)

    #create a function for change default port checkbox
    def change_port_entry(self):
        self.server_port_entry.delete(0, END)
        if self.default_port.get() == "on":
            self.server_port_entry.insert(0, "54321")
            self.server_port_entry.config(state = "disabled")
            self.default_port_check_button.config(fg="Green")

        elif self.default_port.get() == "off" :
            self.server_port_entry.delete(0, END)
            self.server_port_entry.config(state="normal")
            self.default_port_check_button.config(fg="Orange")

#class for chat room window(second window)
class ChatGui():
    def __init__(self,info):
        global username, password, port_num ,server_ip ,server_status
        username_in_func = info.lbl_user_entry.get()
        # password_in_func = info.lbl_pass_entry.get()
        password_in_func = "nothing"
        server_ip_in_func = info.server_ip_entry.get()
        port_num_in_func = info.server_port_entry.get()
        if len(username_in_func) < 1:
            messagebox.showerror("Error", "Enter your name e.g. : (Amin) !")
        elif len(password_in_func) < 1:
            messagebox.showerror("Error", "Enter password !")
        elif len(server_ip_in_func) < 1:
            messagebox.showerror("Error", "Enter server ip address !")
        elif len(port_num_in_func) < 1:
            messagebox.showerror("Error", "Enter port number e.g. (6969) !")

        if port_num_in_func :
            try:
                port_num = int(port_num_in_func)
            except ValueError:
                messagebox.showerror("Error", "port number must be integer e.g. (6969)")
                return
            else:
                if (password_in_func) and (username_in_func) and (port_num_in_func) and (server_ip_in_func):
                    port_num = int(port_num_in_func)
                    password = password_in_func
                    username = username_in_func
                    server_ip = server_ip_in_func

        if server_ip_in_func:
            server_ip = server_ip_in_func

        if (len(str(port_num)) >= 1) and (len(username) >= 1) and (len(password) >= 1) and (len(server_ip) >= 1) :

            try_to_connect_or_not = messagebox.askokcancel("Connection", "Connect ?")
            if try_to_connect_or_not == True:
                self.chat_win = Tk()
                self.chat_win.title("Chat Room")
                self.chat_win.geometry("610x700")
                self.chat_win.resizable(0,0)
                chat_win_user_label = Label(self.chat_win, text=("Your name : " + username), font=("Tahoma", "15"))
                chat_win_user_label.pack()

                self.chat_server_connection_status = Label(self.chat_win)
                self.chat_server_connection_status.pack()
                self.chat_server_connection_status.config(text=("Server status :"), font=("Tahoma", "15"),fg="Blue")
                if server_status is None:
                    self.chat_server_connection_status.config(text=("Server status : Not connected"), font=("Tahoma", "15"),fg="Red")

                self.try_button = Button(self.chat_win, text="Try", font=("Tahoma", 15),command = self.connect_to_server)
                self.try_button.pack()

                self.chat_room_text_box = Text(self.chat_win)
                self.chat_room_text_box.pack()
                self.chat_room_text_box.config(width="70", height="28", bg="#FFEFDF",state = "disabled")
                chat_rooms_separate_text_box = Text(self.chat_win)
                chat_rooms_separate_text_box.pack()
                chat_rooms_separate_text_box.config(width = 70 ,height = "0",bg = "#E6E6E6",state="disabled")
                self.send_message_text_box = Text(self.chat_win)
                self.send_message_text_box.pack()
                self.send_message_text_box.config(width = "70" , height = "3",padx=5,pady=5,state= "disabled")

                self.send_message_button = Button(self.chat_win)
                self.send_message_button.pack()
                self.send_message_button.config(text="   Send   ",font=("Tahoma", 18),state = "disabled",command=self.send_msg)
                self.chat_win.mainloop()

    # define a function for Try button
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client_socket.connect((server_ip,port_num))
            self.client_socket.sendall(username.encode())
        except :
            messagebox.showerror("Error", "Connection failed")
        else:
            self.try_button.config(state = "disabled")
            self.send_message_text_box.config(state="normal")
            self.send_message_button.config(state="normal")
            self.chat_server_connection_status.config(text=("Server status : Connected"), font=("Tahoma", "15"),fg="Green")
            Thread(target=self.receive_msg).start()

    # define a function for receive clients messages
    def receive_msg(self):
        while True :
            try:
                self.clients_message_from_server = self.client_socket.recv(4096)
                if not self.clients_message_from_server : break
                if self.clients_message_from_server :
                    Thread(target=self.update_text_display,args=(self.clients_message_from_server,)).start()

            except ConnectionResetError :
                messagebox.showerror("Error","Connection closed !")
                self.chat_server_connection_status.config(text=("Server status : Not connected"), font=("Tahoma", "15"),fg="Red")
                self.try_button.config(state="normal")
                break

    # send mesage function
    def send_msg(self):
        new_message = self.send_message_text_box.get("1.0",END)
        if (len(new_message.strip()) >= 1) and (len(new_message.strip()) <= 100) :

            local_message = "You->" + new_message
            final_message = username + "->" + new_message
            self.chat_room_text_box.config(state="normal")
            self.chat_room_text_box.insert(END,local_message + "\n")
            self.chat_room_text_box.config(state="disabled")
            try:
                self.client_socket.sendall(final_message.encode())
            except ConnectionResetError :
                messagebox.showerror("Connection error","Connection is closed !")
                self.try_button.config(state="normal")
                self.chat_server_connection_status.config(text=("Server status : Not connected"), font=("Tahoma", "15"),fg="Red")
            else:
                self.send_message_text_box.delete("1.0", END)
        elif (len(new_message.strip()) <1) :
            messagebox.showerror("Error","Your message must be at least 1 character !")
        elif (len(new_message.strip()) > 100) :
            messagebox.showerror("Error", "Your can't send more that 100 character !")
        else:
            messagebox.showerror("Error", "Message can't be sent !")

    # update function for updating the chat room text box
    def update_text_display(self,msg):
        msg_new = msg.decode()
        msg_new = msg_new.strip() + "\n"
        self.chat_room_text_box.config(state="normal")
        self.chat_room_text_box.insert(END, msg_new)
        self.chat_room_text_box.config(state="disabled")

root = tk.Tk()
Gui = LoginGui(root)
root.mainloop()
