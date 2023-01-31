from tkinter import *
import sqlite3
import encryption

class Autorithation():
    def __init__(self, enter):
        #Окно авторизации

        self.enter = enter
        
        self.window = Tk()
        self.window.title('Phone Book')
        self.window.geometry('400x200')

        self.lbl0 = Label(self.window, text=' ')
        self.lbl0.grid(column=0, row=0)

        self.lbl_center = Label(self.window, text='Вход')
        self.lbl_center.grid(column=2, row=0)

        self.lbl1 = Label(self.window, text='Логин')
        self.lbl1.grid(column=0, row=1)

        self.lbl01 = Label(self.window, text=' ')
        self.lbl01.grid(column=0, row=2)

        self.lbl2 = Label(self.window, text='Пароль')
        self.lbl2.grid(column=0, row=3)

        self.text_box1 = Entry(self.window, width=30)  
        self.text_box1.grid(column=2, row=1)

        self.text_box2 = Entry(self.window, width=30, show='*')  
        self.text_box2.grid(column=2, row=3)

        self.btn1 = Button(self.window, text='Войти', command = lambda:self.login(self.text_box1.get(), self.text_box2.get()))
        self.btn1.grid(column=2, row=4)

        self.lbl02 = Label(self.window, text=' ')
        self.lbl02.grid(column=2, row=5)

        self.btn2 = Button(self.window, text='Регистрация', command=self.registration)
        self.btn2.grid(column=1, row=6)

        self.btn3 = Button(self.window, text='Выход', command=self.window.destroy)
        self.btn3.grid(column=3, row=6)

        self.window.mainloop()

    def login(self, log, paswd):
        #Авторизация

        paswd = encryption.MD5(paswd)
        
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS users(
               userid INTEGER PRIMARY KEY AUTOINCREMENT,
               login TEXT NOT NULL,
               password TEXT NOT NULL)''')

        cur.execute('SELECT login FROM users WHERE login = ? AND password = ?', (log, paswd,))
        result = cur.fetchone()
        if result is None:
            error=Tk()
            error.title('Ошибка!')
            error.geometry('250x200')
            lbl1 = Label(error, text='Неверный логин или пароль!')
            lbl1.place(relx=0.5, rely=0.2, anchor='c')
            erbtn = Button(error, text='ok', padx="20", pady="5", command=error.destroy)
            erbtn.place(relx=0.5, rely=0.8, anchor='c')
            error.mainloop()
        else:
            success=Tk()
            success.title('Авторизация')
            success.geometry('250x200')
            lbl1 = Label(success, text='Авторизация прошла успешно!')
            lbl1.place(relx=0.5, rely=0.2, anchor='c')
            subtn = Button(success, text='ok', padx="20", pady="5", command=success.destroy)
            subtn.place(relx=0.5, rely=0.8, anchor='c')
            success.mainloop
            self.enter[0] = True
            self.window.destroy()
        conn.commit()

    def registration(self):
        #Окно регистрации

        r_window = Tk()
        r_window.title('Phone Book')
        r_window.geometry('270x200')

        lbl0 = Label(r_window, text=' ')
        lbl0.grid(column=0, row=0)

        lbl_center = Label(r_window, text='Регистрация')
        lbl_center.grid(column=2, row=0)

        lbl1 = Label(r_window, text='Логин')
        lbl1.grid(column=0, row=1)

        lbl01 = Label(r_window, text=' ')
        lbl01.grid(column=0, row=2)

        lbl2 = Label(r_window, text='Пароль')
        lbl2.grid(column=0, row=3)

        text_box1 = Entry(r_window, width=30)  #Ввод логина
        text_box1.grid(column=2, row=1)

        text_box2 = Entry(r_window, width=30, show='*')  #Ввод пароля
        text_box2.grid(column=2, row=3)

        text_box3 = Entry(r_window, width=30, show='*')  #Повторный ввод пароля
        text_box3.grid(column=2, row=4)

        #Кнопка для регистрации:
        btn1 = Button(r_window, text='Зарегистрироваться', command=lambda:self.add_to_base(text_box1.get(), text_box2.get(), text_box3.get()))
        btn1.grid(column=2, row=5)

        lbl02 = Label(r_window, text=' ')
        lbl02.grid(column=2, row=6)

        btn2 = Button(r_window, text='Вернуться назад', command=r_window.destroy) #Кнопка для выхода
        btn2.grid(column=2, row=7)

        r_window.mainloop()

    def add_to_base(self, log, pas1, pas2):
        #Регистрация

        if log == '' or pas1 == '' or pas2 == '':
            error=Tk()
            error.title('Ошибка!')
            error.geometry('250x200')
            lbl1 = Label(error, text='Логин или пароль введены некорректно!')
            lbl1.place(relx=0.5, rely=0.2, anchor='c')
            erbtn = Button(error, text='ok', padx="20", pady="5", command=error.destroy)
            erbtn.place(relx=0.5, rely=0.8, anchor='c')
            error.mainloop()

        elif pas1 != pas2:
            error=Tk()
            error.title('Ошибка!')
            error.geometry('250x200')
            lbl1 = Label(error, text='Пароли не совпадают!')
            lbl1.place(relx=0.5, rely=0.2, anchor='c')
            erbtn = Button(error, text='ok', padx="20", pady="5", command=error.destroy)
            erbtn.place(relx=0.5, rely=0.8, anchor='c')
            error.mainloop()

        elif pas1 == pas2:
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()

            cur.execute('''CREATE TABLE IF NOT EXISTS users(
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL,
                password TEXT NOT NULL)''')

            cur.execute('SELECT login FROM users WHERE login = ?', (log,))
            result = cur.fetchone()

            if result is not None:
                error=Tk()
                error.title('Ошибка!')
                error.geometry('250x200')
                lbl1 = Label(error, text='Такой логин уже существует!')
                lbl1.place(relx=0.5, rely=0.2, anchor='c')
                erbtn = Button(error, text='ok', padx="20", pady="5", command=error.destroy)
                erbtn.place(relx=0.5, rely=0.8, anchor='c')
                error.mainloop()
            else:
                pas1 = encryption.MD5(pas1)
                user = (log, pas1)
                cur.execute('INSERT INTO users(login, password) VALUES(?, ?)', user)
            
                success=Tk()
                success.title('Регистрация')
                success.geometry('250x200')
                lbl1 = Label(success, text='Регистрация прошла успешно')
                lbl1.place(relx=0.5, rely=0.2, anchor='c')
                subtn = Button(success, text='ok', padx="20", pady="5", command=success.destroy)
                subtn.place(relx=0.5, rely=0.8, anchor='c')
                success.mainloop()
            conn.commit()