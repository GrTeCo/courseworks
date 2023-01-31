"""The main window class is written in this module"""
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import pyodbc
from tkinter.messagebox import showerror, showwarning, askyesno, showinfo


class MainWindow:
    def __init__(self, user_status):
        """Main window."""
        self.user = user_status
        self.rework_textbox = None  # TextBox for reworking method

        self.m_win = tk.Tk()
        self.m_win.title('Game Ranking')
        self.m_win.geometry('250x220+640+230')

        for i in range(3):
            self.m_win.columnconfigure(index=i, weight=1)
        for i in range(7):
            self.m_win.rowconfigure(index=i, weight=1)

        lbl1 = tk.Label(self.m_win, text='What would you like?')
        lbl1.grid(column=1, row=1)

        if self.user['role'] == 'game_admin':
            btn3 = tk.Button(self.m_win, text='Rework tables.', command=self.reworking)
            btn3.grid(column=1, row=2)
        elif self.user['role'] == 'gamer':
            btn1 = tk.Button(self.m_win, text='Show statistics.', command=self.statistics)
            btn1.grid(column=1, row=2)

        btn2 = tk.Button(self.m_win, text='Show leaderboard.', command=self.leaderboard)
        btn2.grid(column=1, row=3)

        self.m_win.mainloop()

    def statistics(self):
        window = tk.Tk()
        window.title('Game Ranking')
        window.geometry('500x320')

        for i in range(5):
            window.columnconfigure(index=i, weight=1)
        for i in range(10):
            window.rowconfigure(index=i, weight=1)

        textbox = tk.scrolledtext.ScrolledText(window, wrap='word', width=43, height=15)
        textbox.grid(column=0, row=2, columnspan=3, rowspan=5)

        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'SERVER=DESKTOP-F7F7D3J;'
                              'DATABASE=GameRank;'
                              f"UID={self.user['login']};"
                              f"PWD={self.user['password']};")
        cur = conn.cursor()

        cur.execute("select nickname from Accounts where acc_id = ?", (self.user['acc_id'],))
        nickname = cur.fetchone()
        cur.execute("select * from Game_members where acc_id = ? and points = 100", (self.user['acc_id'],))
        wins = cur.fetchall()
        cur.execute("select * from Game_members where acc_id = ? and points = 10 or points = NULL",
                    (self.user['acc_id'],))
        loses = cur.fetchall()
        cur.execute('''select Games.name, Games.date, Game_members.points 
        from Game_members inner join Games on match_id = game_id
        where acc_id = ?''', (self.user['acc_id'],))
        games = cur.fetchall()

        conn.commit()

        points = 0
        for i in range(len(games)):
            points += games[i][2]
            message = f'{games[i][0]} {str(games[i][1])} {str(games[i][2])}\n'
            textbox.insert(tk.END, message)

        nickname = nickname[0]
        wins = len(wins)
        loses = len(loses)

        lbl1 = tk.Label(window, text=f'Statistics of the {nickname}')
        lbl1.grid(column=1, row=0)
        lbl2 = tk.Label(window, text=f'Wins: {wins}')
        lbl2.grid(column=3, row=2)
        lbl3 = tk.Label(window, text=f'Loses: {loses}')
        lbl3.grid(column=3, row=3)
        lbl4 = tk.Label(window, text=f'Points: {points}')
        lbl4.grid(column=3, row=4)

        window.mainloop()

    @staticmethod
    def leaderboard():
        """This method collects information about players and displays a leaderboard"""

        lead_win = tk.Tk()
        lead_win.title('Game Ranking')
        lead_win.geometry('284x280+640+200')

        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'SERVER=DESKTOP-F7F7D3J;'
                              'DATABASE=GameRank;'
                              'Trusted_connection=yes;')
        cur = conn.cursor()
        cur.execute('''select Accounts.acc_id, Accounts.nickname,  sum(points) as points
        from Accounts join  Game_members on Accounts.acc_id = Game_members.acc_id
        group by Accounts.nickname, Accounts.acc_id  order by points desc, Accounts.acc_id asc''')
        res = cur.fetchall()
        conn.commit()

        textbox = tk.scrolledtext.ScrolledText(lead_win, wrap='word', width=33, height=17)
        textbox.grid(column=0, row=0)

        for i in range(len(res)):
            message = f'{i+1} place: {res[i][1]}, points: {str(res[i][2])}\n'
            textbox.insert(tk.END, message)

        lead_win.mainloop()

    def reworking(self):
        rework_win = tk.Tk()
        rework_win.title('Game Ranking')
        rework_win.geometry('580x270+450+230')

        # Connection for the rework
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'SERVER=DESKTOP-F7F7D3J;'
                              'DATABASE=GameRank;'
                              f"UID={self.user['login']};"
                              f"PWD={self.user['password']};")

        for i in range(15):
            rework_win.columnconfigure(index=i, weight=1)
        for i in range(10):
            rework_win.rowconfigure(index=i, weight=1)

        lbl = tk.Label(rework_win, text='Reworking Tables')
        lbl.grid(column=2, row=0)
        lbl0 = tk.Label(rework_win, text='table name:')
        lbl0.grid(column=0, row=1)
        lbl1 = tk.Label(rework_win, text='value 1:')
        lbl1.grid(column=0, row=2)
        lbl2 = tk.Label(rework_win, text='value 2:')
        lbl2.grid(column=0, row=3)
        lbl3 = tk.Label(rework_win, text='value 3:')
        lbl3.grid(column=0, row=4)

        ent0 = tk.Entry(rework_win, width=20)
        ent0.grid(column=1, row=1)
        ent1 = tk.Entry(rework_win, width=20)
        ent1.grid(column=1, row=2)
        ent2 = tk.Entry(rework_win, width=20)
        ent2.grid(column=1, row=3)
        ent3 = tk.Entry(rework_win, width=20)
        ent3.grid(column=1, row=4)

        btn1 = tk.Button(rework_win, text='Insert', command=lambda: self.insert_info((ent0.get(), ent1.get(),
                                                                                      ent2.get(), ent3.get()), conn))
        btn1.grid(column=0, row=7)
        btn2 = tk.Button(rework_win, text='Delete', command=lambda: self.delete_info((ent0.get(), ent1.get(),
                                                                                      ent2.get(), ent3.get()), conn))
        btn2.grid(column=1, row=7)
        btn3 = tk.Button(rework_win, text='Update', command=lambda: self.update_info((ent0.get(), ent1.get(),
                                                                                      ent2.get(), ent3.get()), conn))
        btn3.grid(column=0, row=8)
        btn4 = tk.Button(rework_win, text='Show table', command=lambda: self.select_info(ent0.get(), conn))
        btn4.grid(column=1, row=8)

        self.rework_textbox = tk.scrolledtext.ScrolledText(rework_win, wrap='word', width=43, height=10)
        self.rework_textbox.grid(column=2, row=1, columnspan=14, rowspan=7)

        rework_win.mainloop()
        conn.commit()

    @staticmethod
    def insert_info(config, connection):
        conf = config
        conn = connection

        if conf[0] == 'Accounts':
            request = f'insert into Accounts (user_id, nickname) values({conf[2]}, \'{conf[3]}\')'
        elif conf[0] == 'Game_members':
            request = f'insert into Game_members (acc_id, game_id, points) values({conf[1]}, {conf[2]}, {conf[3]})'
        elif conf[0] == 'Games':
            showinfo(title='Information',
                     message='The date must be specified in the format YYYY-MM-DD HH:MinMin:SecSec')

            request = f"insert into Games (date, name) values (\'{(conf[2])}\', \'{conf[3]}\')"
        else:
            showerror(title='Error!', message='Please enter the correct table name.')
            return

        res = askyesno(title='Information', message='Are you sure you want to continue?')
        if not res:
            return

        try:
            cur = conn.cursor()
            cur.execute(request)
        except Exception as e:
            showerror(title='Error',
                      message=f'Error {e.args[0]}.\nSome values are incorrect or not specified.')
            print(e)

    @staticmethod
    def delete_info(config, connection):
        conf = config
        conn = connection
        cur = conn.cursor()

        if conf[0] == 'Accounts':
            request = 'delete Accounts where acc_id = ' + conf[1]
        elif conf[0] == 'Game_members':
            request = 'delete Game_members where acc_id = ' + conf[1] + 'and game_id = ' + conf[2]
        elif conf[0] == 'Games':
            request = 'delete Games where match_id = ' + conf[1]
        else:
            showerror(title='Error!', message='Please enter the correct table name.')
            return

        try:
            cur.execute(f'{request}')
        except Exception as e:
            showerror(title='Error',
                      message=f'Error {e.args[0]}.\n'
                              f'To delete it, you need to specify the value of the primary key of the table.')

    @staticmethod
    def update_info(config, connection):
        showwarning(title='Warning!', message="All values must be specified!\n"
                                              "If you don't want to change the value, leave it the same")
        res = askyesno(title='Warning!', message='Are you sure you want to continue?')
        if not res:
            return

        conf = config
        conn = connection
        cur = conn.cursor()

        if conf[0] == 'Accounts':
            request = f'update Accounts set user_id = {conf[2]}, nickname = \'{conf[3]}\' where acc_id = {conf[1]}'
        elif conf[0] == 'Game_members':
            request = f'update Game_members set points = {conf[3]} where acc_id = {conf[1]} and game_id = {conf[2]}'
        elif conf[0] == 'Games':
            request = f'update Games set date = \'{conf[2]}\', name = \'{conf[3]}\' where match_id = {conf[1]}'
        else:
            showerror(title='Error!', message='Please enter the correct table name.')
            return

        try:
            cur.execute(f'{request}')
        except Exception as e:
            showerror(title='Error',
                      message=f'Error {e.args[0]}.\nSome values are incorrect or not specified.')
        finally:
            showwarning(title='Warning!', message='After updating the tables, you need to restart the program.'
                                                  'Otherwise, the program may not work correctly')

    def select_info(self, config, connection):
        self.rework_textbox.delete('1.0', tk.END)
        conf = config
        conn = connection
        cur = conn.cursor()

        if conf == 'Accounts':
            message = 'Table Accounts \nwith columns: acc_id, user_id, nickname.\n\n'
            self.rework_textbox.insert(tk.END, message)
        elif conf == 'Game_members':
            message = 'Table Game_members \nwith columns: acc_id, game_id, points.\n\n'
            self.rework_textbox.insert(tk.END, message)
        elif conf == 'Games':
            message = 'Table Games \nwith columns: match_id, date, name.\n\n'
            self.rework_textbox.insert(tk.END, message)
        else:
            showerror(title='Error!', message='Please enter the correct table name.')
            return

        cur.execute(f'select * from {conf}')
        res = cur.fetchall()
        for i in range(len(res)):
            message = f'{res[i][0]} | {str(res[i][1])} | {str(res[i][2])}\n\n'
            self.rework_textbox.insert(tk.END, message)
