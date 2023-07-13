"""The authorization window class is written in this module"""
import tkinter as tk
import hashlib as hsh
import json
import socket
from tkinter.messagebox import showerror, showinfo


class AuthorizationWindow:

    def __init__(self, usr_status):
        """Authorization window"""

        # Dictionary with user's information
        self.user = usr_status

        # Info for sending data
        self.server_addr = '10.10.1.10'
        self.server_port = 7770

        # Creating window
        self.window = tk.Tk()
        self.window.title('Corp Messanger')
        self.window.geometry('255x120+640+290')

        # Empty labels for markup
        label0 = tk.Label(self.window, text='')
        label0.grid(row=0, column=0)
        label01 = tk.Label(self.window, text='     ')
        label01.grid(row=4, column=0)

        # Creating window elements
        label1 = tk.Label(self.window, text='Login:')
        label1.grid(row=1, column=1)
        self.ent1 = tk.Entry(self.window)
        self.ent1.grid(row=1, column=2)

        label2 = tk.Label(self.window, text='Password:')
        label2.grid(row=2, column=1)
        self.ent2 = tk.Entry(self.window, show='*')
        self.ent2.grid(row=2, column=2)

        btn1 = tk.Button(self.window, text="log in", command=self.authorize)
        btn1.grid(row=3, column=2)

        self.window.mainloop()

    @staticmethod
    def make_hash(passwd):
        """Function that provides hashing the password"""

        enc_pass = hsh.md5(passwd.encode('utf-8'))
        return enc_pass.hexdigest()

    def authorize(self):
        """A function that provides authorization"""

        # Preparing request
        payload = {
            "action": "login",
            "login": self.ent1.get(),
            "password": self.make_hash(self.ent2.get())
        }
        payload = json.dumps(payload)

        # Request sending
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.server_addr, self.server_port))
            sock.sendall(bytes(payload, encoding='utf-8'))
            answer = sock.recv(1024)
            answer = answer.decode('utf-8')
            answer = json.loads(answer)

            if answer['success']:
                self.user['acc_id'] = answer['id']
                self.user['login'] = self.ent1.get()
                self.user['token'] = answer['token']
                self.user['enter'] = True
                sock.close()
                showinfo(title='Success', message='Authorization complete')
                self.window.destroy()
            else:
                showinfo(title='Error', message='Incorrect login or password')

        except Exception as exc:
            showerror(title='Error', message=f'{exc}')
            self.user['enter'] = False
        finally:
            sock.close()
