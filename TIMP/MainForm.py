"""Module that provides main form and it functions"""

import json
import socket
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showerror


class MainWindow:
    """Class that provides main window"""

    def __init__(self, usr_status):

        # Info for sending data
        self.server_addr = '10.10.1.10'
        self.server_port = 7770

        # dictionary with user's information
        self.user = usr_status

        # Window creation
        self.m_win = tk.Tk()
        self.m_win.title('Corp Messenger')
        self.m_win.geometry('700x450+480+180')

        # Setting the orientation
        for i in range(10):
            self.m_win.columnconfigure(index=i, weight=1)
        for i in range(10):
            self.m_win.rowconfigure(index=i, weight=1)

        # Welcome message
        label1 = tk.Label(self.m_win, text=f"Welcome, {self.user['login']}!")
        label1.grid(column=0, row=0)

        # Users List
        label2 = tk.Label(self.m_win, text='Users list')
        label2.grid(column=0, row=1)
        btn1 = tk.Button(self.m_win, text='Update',
                         command=self.update_users)
        btn1.grid(column=2, row=1)
        self.textbox = tk.scrolledtext.ScrolledText(self.m_win, wrap='word',
                                                    width=30, height=10)
        self.textbox.grid(column=0, row=2, rowspan=2, columnspan=3)

        # User selection
        label3 = tk.Label(self.m_win, text='Select user\'s id:')
        label3.grid(column=0, row=4)
        self.ent1 = tk.Entry(self.m_win, width=5)
        self.ent1.grid(column=1, row=4)

        # Messages list
        label4 = tk.Label(self.m_win, text='Messages list')
        label4.grid(column=5, row=0)
        btn2 = tk.Button(self.m_win, text='Update',
                         command=self.update_messages)
        btn2.grid(column=7, row=0)
        self.textbox2 = tk.scrolledtext.ScrolledText(self.m_win, wrap='word',
                                                     width=40, height=13)
        self.textbox2.grid(column=5, row=1, rowspan=3, columnspan=4,)

        # Write message
        self.textbox3 = tk. scrolledtext.ScrolledText(self.m_win, wrap='word',
                                                      width=65, height=10)
        self.textbox3.grid(column=1, row=7, rowspan=2, columnspan=7)

        btn2 = tk.Button(self.m_win, text='Send', command=self.send_message)
        btn2.grid(column=8, row=8, columnspan=2)

        self.m_win.mainloop()

    def send_message(self):
        """Function for sending messages"""

        # Preparing request
        payload = {
            "action": "send_mess",
            "from": f"{self.user['acc_id']}",
            "to": f"{self.ent1.get()}",
            "message": f"{self.textbox3.get('1.0', tk.END)}",
            "token": self.user['token']
        }
        payload = json.dumps(payload)

        # Sending request
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.server_addr, self.server_port))
            sock.sendall(bytes(payload, encoding='utf-8'))
            answer = sock.recv(1024)
            answer = answer.decode('utf-8')
            answer = json.loads(answer)

            if answer['success']:
                self.textbox3.delete('1.0', tk.END)
                self.update_messages()
            else:
                showerror(title='Error',
                          message='Error when sending the message')

        except Exception as exc:
            showerror(title='Error', message=f'{exc}')
        finally:
            sock.close()

    def update_messages(self):
        """Function for updating messages in window"""

        # Preparing request
        payload = {
            "action": "update_messages",
            "from": f"{self.user['acc_id']}",
            "to": f"{self.ent1.get()}",
            "token": self.user['token']
        }

        payload = json.dumps(payload)

        # Sending request
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.server_addr, self.server_port))
            sock.sendall(bytes(payload, encoding='utf-8'))
            answer = sock.recv(1024)
            answer = answer.decode('utf-8')
            answer = json.loads(answer)

            if answer['success']:
                self.textbox2.delete('1.0', tk.END)
                self.textbox2.insert(tk.END, answer['result'])
                # for mess in answer['result']:
                #     self.textbox2.insert(tk.END, mess + '\n')
            else:
                showerror(title='Error', message='Getting information error')

        except Exception as exc:
            showerror(title='Error', message=f'{exc}')
        finally:
            sock.close()

    def update_users(self):
        """Function for update users list"""

        # Preparing request
        payload = {
            "action": "update_users",
            # "id": f"{self.user['acc_id']}",
            "token": self.user['token']
        }
        payload = json.dumps(payload)

        # Sending request
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.server_addr, self.server_port))
            sock.sendall(bytes(payload, encoding='utf-8'))
            answer = sock.recv(1024)
            answer = answer.decode('utf-8')
            answer = json.loads(answer)

            if answer['success']:
                self.textbox.delete('1.0', tk.END)
                for usr in answer['result']:
                    line = f'{usr[0]} {usr[1]}\n'
                    self.textbox.insert(tk.END, line)
            else:
                showerror(title='Error', message='Getting information error')

        except Exception as exc:
            showerror(title='Error', message=f'{exc}')
        finally:
            sock.close()
