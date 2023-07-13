"""The authorization window class is written in this module"""
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
import pyodbc


class AuthorizationWindow:
    def __init__(self, user_status):
        """Main authorization window"""
        self.user = user_status

        # Attributes for registration window.
        self.ent3 = None
        self.ent4 = None
        self.ent5 = None
        # ===================================

        self.window = tk.Tk()
        self.window.title('Game Ranking')
        self.window.geometry('265x150+630+280')

        # Empty labels for markup
        label0 = tk.Label(self.window, text='')
        label0.grid(row=0, column=0)
        label01 = tk.Label(self.window, text='     ')
        label01.grid(row=4, column=0)
        # =======================

        label1 = tk.Label(self.window, text='Login:')
        label1.grid(row=1, column=1)
        self.ent1 = tk.Entry(self.window)
        self.ent1.grid(row=1, column=2)

        label2 = tk.Label(self.window, text='Password:')
        label2.grid(row=2, column=1)
        self.ent2 = tk.Entry(self.window, show='*')
        self.ent2.grid(row=2, column=2)

        btn1 = tk.Button(self.window, text="log in", command=self.log_in)
        btn1.grid(row=3, column=2)
        btn2 = tk.Button(self.window, text="enter as guest", command=self.guest_enter)
        btn2.grid(row=5, column=2)

        self.window.mainloop()

    def guest_enter(self):
        self.user['enter'] = True
        self.window.destroy()

    def log_in(self):
        """Log in function."""
        log = self.ent1.get()
        passwd = self.ent2.get()

        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'SERVER=DESKTOP-F7F7D3J;'
                              'DATABASE=GameRank;'
                              'Trusted_connection=yes;')
        cur = conn.cursor()
        cur.execute('select user_id from Users where login = ? and password = ?', (log, passwd))
        res = cur.fetchone()

        if res is None:
            showerror(title='Error', message='User not found or password is incorrect.')
            return

        cur.execute('select acc_id from Accounts where user_id = ?', res)
        res = cur.fetchone()
        conn.commit()

        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'SERVER=DESKTOP-F7F7D3J;'
                              'DATABASE=GameRank;'
                              f'UID={log};'
                              f'PWD={passwd};')
        cur = conn.cursor()
        cur.execute("select is_member ('game_admin')")
        res2 = cur.fetchone()
        conn.commit()

        if res2[0] == 0:
            res = res[0]
            res2 = 'gamer'
        else:
            res2 = 'game_admin'

        # Filling in the user_status
        self.user['acc_id'] = res
        self.user['login'] = log
        self.user['password'] = passwd
        self.user['role'] = res2
        self.user['enter'] = True
        # ==========================

        showinfo(title='Success', message='Welcome!')
        self.window.destroy()
