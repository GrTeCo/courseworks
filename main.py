import sqlite3
from tkinter import *
from tkinter import scrolledtext
import entrance
import re

class Phone_book():

    def __init__(self):
        #Окно телефонного справочника

        self.book = Tk()
        self.book.title('Phone book')
        self.book.geometry('600x350')

        self.lbl01 = Label(self.book, text = '')
        self.lbl01.grid(column=0, row=0)

        self.lbl1 = Label(self.book, text = 'Фамилия')
        self.lbl1.grid(column = 0, row = 1)
        self.text_box1 = Entry(self.book, width = 30)
        self.text_box1.grid(column = 1, row = 1)

        self.lbl02 = Label(self.book, text = '')
        self.lbl02.grid(column = 2, row = 1)

        self.lbl2 = Label(self.book, text = 'Имя')
        self.lbl2.grid(column = 0, row = 2)
        self.text_box2 = Entry(self.book, width = 30)
        self.text_box2.grid(column = 1, row = 2)

        self.btn1 = Button(self.book, text = 'Поиск в телефонном справочнике', command = self.search_in_base)
        self.btn1.grid(column = 1, row = 3)

        self.text_lbl = Label(self.book, text = 'Результаты поиска')
        self.text_lbl.place(relx = 0.3, rely = 0.4, anchor = 'c')
        self.text = scrolledtext.ScrolledText(self.book, width=40, height=10)
        self.text.place(relx = 0.3, rely = 0.7, anchor = 'c')
        #================================================================
        self.lbl03 = Label(self.book, text = '                     ')
        self.lbl03.grid(column = 3, row = 1)
        
        self.lbl3 = Label(self.book, text = 'Фамилия')
        self.lbl3.grid(column = 4, row = 1)
        self.text_box3 = Entry(self.book, width = 30)
        self.text_box3.grid(column = 5, row = 1)

        self.lbl4 = Label(self.book, text = 'Имя')
        self.lbl4.grid(column = 4, row = 2)
        self.text_box4 = Entry(self.book, width = 30)
        self.text_box4.grid(column = 5, row = 2)

        self.lbl5 = Label(self.book, text = 'Телефон')
        self.lbl5.grid(column = 4, row = 3)
        self.text_box5 = Entry(self.book, width = 30)
        self.text_box5.grid(column = 5, row = 3)

        self.btn2 = Button(self.book, text = 'Добавить в справочник', command = self.add_to_base)
        self.btn2.grid(column = 5, row = 4)
        #==================================================================
        self.exit_btn = Button(self.book, text = 'Выход', command = self.book.destroy)
        self.exit_btn.place(relx = 0.95, rely = 0.93, anchor = 'c', height = 30, width = 50)

        self.book.mainloop()

    def add_to_base(self):
        #Добавление абонента в базу данных

        mask1 = re.compile('\s+')
        mask2 = re.compile('(\+7|8)\D*\d{3}\D*\d{3}\D*\d{2}\D*\d{2}')

        #Проверка ошибок в имени или фамилии
        if mask1.search(self.text_box3.get()) or mask1.search(self.text_box4.get()) or self.text_box3.get()=='' or self.text_box4.get()=='':
            error=Tk()
            error.title('Ошибка!')
            error.geometry('250x200')
            lbl1 = Label(error, text='Некоректное имя или фамилия')
            lbl1.place(relx=0.5, rely=0.2, anchor='c')
            erbtn = Button(error, text='ok', padx="20", pady="5", command=error.destroy)
            erbtn.place(relx=0.5, rely=0.8, anchor='c')
            error.mainloop()

        #Проверка номера телефона на корректность
        elif not mask2.search(self.text_box5.get()):
            error=Tk()
            error.title('Ошибка!')
            error.geometry('250x200')
            lbl1 = Label(error, text='Телефон введен некорректно!')
            lbl1.place(relx=0.5, rely=0.2, anchor='c')
            erbtn = Button(error, text='ok', padx="20", pady="5", command=error.destroy)
            erbtn.place(relx=0.5, rely=0.8, anchor='c')
            error.mainloop()  
        else:
            #Непосредственно добавление абонента в базу
            abonent = (self.text_box3.get(), self.text_box4.get(), self.text_box5.get())

            conn = sqlite3.connect('phone_book.db')
            cur = conn.cursor()

            cur.execute('''CREATE TABLE IF NOT EXISTS abonents(
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL)''')
            cur.execute('INSERT INTO abonents(surname, name, phone) VALUES(?, ?, ?)', abonent)

            conn.commit()

            #Окно успеха
            success=Tk()
            success.title('Phone book')
            success.geometry('250x200')
            lbl1 = Label(success, text='Абонент добавлен!')
            lbl1.place(relx=0.5, rely=0.2, anchor='c')
            subtn = Button(success, text='ok', padx="20", pady="5", command=success.destroy)
            subtn.place(relx=0.5, rely=0.8, anchor='c')
            success.mainloop()

    def search_in_base(self):
        #Поиск абонента в справочнике

        self.text.delete('1.0', END)
        conn = sqlite3.connect('phone_book.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS abonents(
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL)''')

        cur.execute('SELECT * FROM abonents ORDER BY surname')
        res = cur.fetchall()
        conn.commit()
        surn = self.text_box1.get()
        n = self.text_box2.get()
        i = self.bynary_search(res, surn)
        mask = re.compile('\s+')
        if i == None:
            error=Tk()
            error.title('Ошибка!')
            error.geometry('250x200')
            lbl1 = Label(error, text='Абонент не найден!')
            lbl1.place(relx=0.5, rely=0.2, anchor='c')
            erbtn = Button(error, text='ok', padx="20", pady="5", command=error.destroy)
            erbtn.place(relx=0.5, rely=0.8, anchor='c')
            error.mainloop()
        elif n == '' or mask.search(n):
            while res[i-1][1] == surn:
                i -= 1
            self.text.insert(INSERT, f'{res[i][1]} {res[i][2]}: {res[i][3]}\n')
            while res[i+1][1] == surn:
                i += 1            
                self.text.insert(INSERT, f'{res[i][1]} {res[i][2]}: {res[i][3]}\n')
        else:
            while res[i-1][1] == surn:
                i -= 1
            c = False
            while res[i][1] == surn:
                if res[i][2] == n:
                    c = True
                    self.text.insert(INSERT, f'{res[i][1]} {res[i][2]}: {res[i][3]}\n')
                i +=1
            if c == False:
                error=Tk()
                error.title('Ошибка!')
                error.geometry('250x200')
                lbl1 = Label(error, text='Абонент не найден!')
                lbl1.place(relx=0.5, rely=0.2, anchor='c')
                erbtn = Button(error, text='ok', padx="20", pady="5", command=error.destroy)
                erbtn.place(relx=0.5, rely=0.8, anchor='c')
                error.mainloop()

    def bynary_search(self, list, item):
        #Бинарный поиск

        low = 0
        high = len(list)-1
        
        while low <= high:
            mid = (low+high)//2
            guess = list[mid][1]
            if guess == item:
                return mid
            if guess > item:
                high = mid-1
            else:
                low = mid+1
        return None


enter = [False]
autorization = entrance.Autorithation(enter)

if enter[0] is True:
    Book = Phone_book()



#==============================================================================================================
#==============================================================================================================
#ТЕСТЫ
testing = 0 #0 - отключить тестирование 1 - включить тестирование

#ВО ВРЕМЯ РАБОТЫ ТЕСТОВ НЕОБХОДИМО ПРОСТО ЗАКРЫВАТЬ ВСЕ ВСПЛЫВАЮЩИЕ ОКНА

import unittest
class Test_bynary_search(unittest.TestCase):

    def test_1_search_without_data(self):
        test1 = []
        book1 = Phone_book()
        print('TEST 1...')
        self.assertEqual(book1.bynary_search(test1, 'Black'), None)
        
    def test_2_search_with_1_elem(self):
        test2 = [(1, 'Smith', 'Tom')]
        book2 = Phone_book()
        print('\nTEST 2...')
        self.assertEqual(book2.bynary_search(test2, 'Smith'), 0)

    def test_3_search_with_many_elem(self):
        test3 = [(0, 'Black', 'Dan'), (3, 'Roberts', 'Mary'), (1, 'White', 'Kate')]
        book3 = Phone_book()
        print('\nTEST 3...')
        self.assertEqual(book3.bynary_search(test3, 'White'), 2)

    def test_4_search_with_sorting(self):
        test4 = [(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E'), (5, 'F'), (6, 'G'), (7, 'H')]
        book4 = Phone_book()
        print('\nTEST 4...')
        self.assertEqual(book4.bynary_search(test4, 'E'), 4)

    def test_5_search_without_sorting(self):
        book5 = Phone_book()
        test5 = [(1, 'N'), (5, 'W'), (3, 'B'), (4, 'X'), (2, 'M'), (8, 'A')]
        print('\nTEST 5...')
        self.assertNotEqual(book5.bynary_search(test5, 'N'), 0)

    def test_6_search_with_sorting2(self):
        book6 = Phone_book()
        test6 = [(4, 'a'), (3, 'b'), (7, 'c'), (1, 'd'), (0, 'z')]
        print('\nTEST 6...')
        self.assertEqual(book6.bynary_search(test6, 'z'), 4)

    def test_7_sesarch_with_reverse_sorting(self):
        book7 = Phone_book()
        test7 = [(99, 'Z'), (5, 'X'), (16, 'O'), (9, 'H'), (34, 'B'), (111, 'A')]
        print('\nTEST 7...')
        self.assertNotEqual(book7.bynary_search(test7, 'Z'), 0)

if __name__ == '__main__' and testing == 1:
   unittest.main()