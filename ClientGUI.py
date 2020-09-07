#!/usr/bin/python3

'''
Python multi user GUI messenger (Client V2)
author = xenon-xenon(Mohammad Amin Nasiri)
email = Khodexenon@gmail.com
'''

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import socket
from threading import Thread
from time import sleep

server_status = None # connection status with the server

#class for login GUI
class LoginGui():
    def __init__(self, main_win): # main_win = tk.Tk()
        # define GUI options
        self.chat_win_exist = None # If chat window exists it won't be None
        self.main_win = main_win # main window for login
        self.main_win.title('Messenger (Client) V2')
        self.main_win.geometry('750x200')
        self.main_win.resizable(1, 1)
        # setting user options
        self.lbl_user = Label(main_win, text='Name', padx=10, pady=10, font=('Tahoma', 15))
        self.lbl_user.grid(row=0, column=0)
        self.lbl_user_entry = Entry(main_win, font=('Tahoma', 11))
        self.lbl_user_entry.grid(row=0, column=1)
        # setting password options
        self.lbl_pass = Label(main_win, text='Password', padx=10, pady=10, font=('Tahoma', 15))
        self.lbl_pass.grid(row=0, column=2)
        self.lbl_pass_entry = Entry(main_win, show='*', font=('Tahoma', 11))
        self.lbl_pass_entry.grid(row=0, column=3)
        # setting server ip options
        self.server_ip_label = Label(main_win, text='Server IP', padx=10, pady=10, font=('Tahoma', 15))
        self.server_ip_label.grid(row=2, column=0)
        self.server_ip_entry = Entry(main_win, font=('Tahoma', 13))
        self.server_ip_entry.grid(row=2, column=1)
        # setting server connecting port options
        self.server_port_num = Label(main_win, text='Port', padx=10, pady=10, font=('Tahoma', 15))
        self.server_port_num.grid(row=2, column=2)
        self.server_port_entry = Entry(main_win, font=('Tahoma', 11))
        self.server_port_entry.grid(row=2, column=3)
        # setting default port check box
        self.default_port = StringVar()
        self.default_port_check_button = Checkbutton(main_win, font=('Tahoma', 15), text='Default port (54321)',offvalue='off', onvalue='on', variable=self.default_port, command=self.change_port_entry)
        self.change_port_entry()
        self.default_port_check_button.config(fg='Black')
        self.default_port_check_button.grid(row=3, column=1)
        self.default_port.set('off')

        # setting the authentication status check box if it is enabled user must use password
        self.auth_status = StringVar()
        self.auth_status_check_button = Checkbutton(main_win, font=('Tahoma', 15), text='Authentication enabled', offvalue='off', onvalue='on', variable=self.auth_status, command=self.change_authentication_status_entry)
        self.auth_status_check_button.config(fg='Black')
        self.auth_status_check_button.grid(row=3, column=2)
        self.lbl_pass_entry.insert(0, 'public') # set default password to public when authentication is disabled
        self.auth_status.set('off') # set check box to disabled mode by default
        self.lbl_pass_entry.config(state='disabled') # disable password box bcs authentication is not enabled by default

        # setting set button for connection info
        self.set_button = Button(main_win, text='   Set   ', font=('Tahoma', 17), command=self.create_chat_gui)
        self.set_button.config(activeforeground='Blue', activebackground='White')
        self.set_button.grid(row=4, column=3)


    def change_port_entry(self):
        '''function for changing default port checkbox'''
        self.server_port_entry.delete(0, END)
        # if it's on ,set value to 54321 and disable the port entry box
        if self.default_port.get() == 'on':
            self.server_port_entry.insert(0, '54321')
            self.server_port_entry.config(state='disabled')
        # if it's off ,clear the value and enable the port entry box
        elif self.default_port.get() == 'off':
            self.server_port_entry.delete(0, END)
            self.server_port_entry.config(state='normal')

    def change_authentication_status_entry(self):
        '''function for changing authentication mode'''
        # if it's on ,enable the password entry
        if self.auth_status.get() == 'on' :
            self.lbl_pass_entry.config(state='normal')
            self.lbl_pass_entry.delete(0,END)

        # if it's off ,disable the password entry
        if self.auth_status.get() == 'off':
            self.lbl_pass_entry.delete(0, END)
            self.lbl_pass_entry.insert(0,'public')
            self.lbl_pass_entry.config(state='disabled')

    def create_chat_gui(self):
        '''function for connect button'''

        try_to_connect_or_not = messagebox.askokcancel('Connection', 'If the chat window exists ,it will be closed')
        if try_to_connect_or_not == True:
             if (self.chat_win_exist is None) or (self.chat_win_exist is not None): # This condition is true anyway
                try:
                    self.chat_win_exist.chat_win.destroy() # try to close chat window
                except:
                    self.chat_win_exist = ChatGui(self) # create chat window
                else:
                    self.chat_win_exist = ChatGui(self) # create chat window


#class for chat room window(second window)
class ChatGui():
    def __init__(self,info):
        self.server_ip = info.server_ip_entry.get()
        self.port_num = info.server_port_entry.get()
        self.username = info.lbl_user_entry.get()
        self.password = info.lbl_pass_entry.get()

        # show message boxes if inputs are not entered
        if len(self.username) < 1:
            messagebox.showerror('Error', 'Enter your name e.g. (Xenon) !')
            return
        elif len(self.password) < 1:
            messagebox.showerror('Error', 'Enter password ! if you don\'t have password *uncheck* authentication enabled check box')
            return
        elif len(self.server_ip) < 1:
            messagebox.showerror('Error', 'Enter server ip address !')
            return
        elif len(self.port_num) < 1:
            messagebox.showerror('Error', 'Enter port number e.g. (54321) !')
            return
        # check if the port number entere is valid(integer)
        if self.port_num :
            try:
                self.port_num = int(self.port_num)
            except ValueError:
                messagebox.showerror('Error', 'port number must be integer e.g. (54321)')
                return

        # check input if they are entered and create the chat window for establishing the connection
        if (len(str(self.port_num)) >= 1) and (len(self.username) >= 1) and (len(self.password) >= 1) and (len(self.username) >= 1) :
            self.create_chat_window()

    def create_chat_window(self):
        '''function for creating chat window'''
        try_to_connect_or_not = messagebox.askokcancel('Connection', 'Connect ?')
        if try_to_connect_or_not == True:
            # chat window properties
            self.chat_win = Tk()
            self.chat_win.title('Chat Room')
            self.chat_win.geometry('610x820')
            self.chat_win.resizable(1, 1)
            # user info on top of the window
            chat_win_user_label = Label(self.chat_win, text=('Your name : ' + self.username), font=('Tahoma', '15'))
            chat_win_user_label.pack()
            # connection status on top of the window
            self.chat_server_connection_status = Label(self.chat_win)
            self.chat_server_connection_status.pack()
            self.chat_server_connection_status.config(text=('Server status :'), font=('Tahoma', '15'), fg='Blue')
            # first red connection status label before establishing the connection
            if server_status is None:
                self.chat_server_connection_status.config(text=('Server status : Not connected'), font=('Tahoma', '15'), fg='Red')
            # set connect button settings
            self.connect_button = Button(self.chat_win, text='Connect', font=('Tahoma', 15), command=self.connect_to_server)
            self.connect_button.pack()
            # setting the text box windows
            self.chat_room_text_box = Text(self.chat_win)
            self.chat_room_text_box.pack()
            self.chat_room_text_box.config(width='70', height='28', bg='#FFEFDF', state='disabled')
            # setting a box for separating the messages text box and send message box
            chat_rooms_separate_text_box = Text(self.chat_win)
            chat_rooms_separate_text_box.pack()
            chat_rooms_separate_text_box.config(width=70, height='0', bg='#E6E6E6', state='disabled')
            # setting the send box for sending messages
            self.send_message_text_box = Text(self.chat_win)
            self.send_message_text_box.pack()
            self.send_message_text_box.config(width='70', height='3', padx=5, pady=5, state='disabled')
            # setting the send message button
            self.send_message_button = Button(self.chat_win)
            self.send_message_button.pack()
            self.send_message_button.config(text='   Send   ', font=('Tahoma', 18), state='disabled', command=self.send_msg)

            self.chat_win.mainloop()

    def connect_to_server(self):
        '''function for initial connection to the server'''
        try:
            self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip,self.port_num))
            # credential format => user:username,pass:password;
            credential = 'user:' + self.username + ',pass:' + self.password + ';'
            self.client_socket.sendall(credential.encode())

        except :
            self.client_socket.close()
            messagebox.showerror('Error', 'Connection failed !')
            return
        else:
            # get ACK if credential is correct or not

            credential_ack = self.client_socket.recv(4096)
            if credential_ack.decode() == 'invalid credentials':
                self.client_socket.close()
                messagebox.showerror('Error','Invalid credential')
                return
            elif credential_ack.decode() == 'valid credentials':
                pass
            else:
                self.client_socket.close()
                messagebox.showerror('Error','An unexpected error occurred !')
                return
            # setting GUI elements
            self.connect_button.config(state = 'disabled') # disable connect button
            self.send_message_text_box.config(state='normal') # enable send message box
            self.send_message_button.config(state='normal') # enable send message button
            self.chat_server_connection_status.config(text=('Server status : Connected'), font=('Tahoma', '15'),fg='Green')

            Thread(target=self.receive_msg).start() # start threading for getting messages
            Thread(target=self.send_client_signal).start() # start threading for sending signal messages

    def receive_msg(self):
        '''function for getting clients messages from server'''
        while True :
            try:
                self.clients_message_from_server = self.client_socket.recv(4096)
                if not self.clients_message_from_server : break
                if (self.clients_message_from_server) and (self.clients_message_from_server.decode() != 'server signal') :
                    # server signal is a message from server to check connection between itself and client
                    Thread(target=self.update_text_display,args=(self.clients_message_from_server,)).start()

            except:
                self.client_socket.close()
                self.connect_button.config(state='normal')  # enable connect button
                self.send_message_text_box.config(state='disabled')  # disable send message box
                self.send_message_button.config(state='disabled')  # disable send message button
                self.chat_server_connection_status.config(text=('Server status : Not connected'), font=('Tahoma', '15'),fg='Red')
                messagebox.showerror('Error','Connection closed !')
                break

    def send_msg(self):
        '''
        function for sending messages
        this function will be called when send button is clicked
        '''

        new_message = self.send_message_text_box.get('1.0',END)
        if (len(new_message.strip()) >= 1) and (len(new_message.strip()) <= 100) :

            local_message = 'You->' + new_message.strip()
            final_message = self.username + '->' + new_message.strip()
            self.chat_room_text_box.config(state='normal',fg='Black') # enable chat box for inserting message
            self.chat_room_text_box.insert(END,local_message + '\n')
            self.chat_room_text_box.config(state='disabled') # disable chat box
            try:
                self.client_socket.sendall(final_message.encode())
            except:
                self.client_socket.close()
                self.connect_button.config(state='normal')
                self.send_message_text_box.config(state='disabled')  # disable send message box
                self.send_message_button.config(state='disabled') # disable send message button
                self.chat_server_connection_status.config(text=('Server status : Not connected'), font=('Tahoma', '15'), fg='Red')
                messagebox.showerror('Connection error','Connection is closed !')

            else:
                self.send_message_text_box.delete('1.0', END)
        elif (len(new_message.strip()) < 1) :
            messagebox.showerror('Error','Your message must be at least 1 character !')
        elif (len(new_message.strip()) > 100) :
            messagebox.showerror('Error', 'Your can\'t send more that 100 character !')
        else:
            messagebox.showerror('Error', 'Message can\'t be sent !')

    def update_text_display(self, msg):
        '''function for displaying messages in the messages text box'''
        msg_new = msg.decode()
        msg_new = msg_new.strip() + '\n'
        self.chat_room_text_box.config(state='normal')
        self.chat_room_text_box.insert(END, msg_new)
        self.chat_room_text_box.config(state='disabled')

    def send_client_signal(self):
        '''function for sending signal to server for checking connection between client and server'''
        while True:
            sleep(5) # sending signal every 5 sec
            try:
                self.client_socket.sendall(b'client signal')
            except:
                self.client_socket.close()
                self.connect_button.config(state='normal')
                self.send_message_text_box.config(state='disabled')  # disable send message box
                self.send_message_button.config(state='disabled')  # disable send message button
                self.chat_server_connection_status.config(text=('Server status : Not connected'), font=('Tahoma', '15'), fg='Red')
                messagebox.showerror('Connection error', 'Connection is closed !')

root = tk.Tk()
Gui = LoginGui(root)
root.mainloop()
