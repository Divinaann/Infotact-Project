import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

def display(uname):   
    def tab2():
        def table(): 
            root = tk.Tk() 
            root.title("Display Details") 
            root.geometry("500x300")
    
            mysqldb = mysql.connector.connect(host='localhost', username='root', password='*', database='internship_project')
            my_cursor = mysqldb.cursor()

            my_cursor.execute("SELECT * FROM password WHERE username = %s", (uname,))

            tree = ttk.Treeview(root)

            tree["columns"] = ("id", "username", "password_for", "password")

            tree.column("id", width=1, minwidth=20, anchor=tk.CENTER)
            tree.column("username", width=10, minwidth=100, anchor=tk.CENTER)
            tree.column("password_for", width=100, minwidth=115, anchor=tk.CENTER)
            tree.column("password", width=150, minwidth=125, anchor=tk.CENTER)

            tree.heading("id", text="ID", anchor=tk.CENTER)
            tree.heading("username", text="User Name", anchor=tk.CENTER)
            tree.heading("password_for", text="Password Purpose", anchor=tk.CENTER)
            tree.heading("password", text="Password", anchor=tk.CENTER)

            i = 0
            for r in my_cursor:
                tree.insert('', i, text="", values=(r[0], r[1], r[2], r[3]))
                i += 1

            tree.pack()

        table()
    tab2()

def Ok():
    mysqldb = mysql.connector.connect(host='localhost', username='root', password='*', database='internship_project')
    my_cursor = mysqldb.cursor()
    uname = e1.get()
    password = e2.get()
    
    sql = "SELECT * FROM login WHERE username = %s AND password = %s"
    my_cursor.execute(sql, (uname, password))
    res = my_cursor.fetchall()
    if res:
        def tab1():
            main_window = Toplevel(root)  
            main_window.title("Password Generator")
            main_window.geometry('300x250')
            padd = 50
            main_window['padx'] = padd
            
            def password_generate(leng):
                valid_char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                password = "".join(random.sample(valid_char, leng))
                display_result.delete(0, tk.END)
                display_result.insert(0, password)
                return password  

            def generate_password():
                try:
                    length = int(length_entry.get())
                    if length < 4:
                        display_result.delete(0, tk.END)
                        display_result.insert(0, "Length must be at least 4")
                    else:
                        generated_password = password_generate(length)
                        return generated_password  
                except ValueError:
                    display_result.delete(0, tk.END)
                    display_result.insert(0, "Enter a valid number")

            def save_password(password):
                try:
                    mysqldb = mysql.connector.connect(host='localhost', username='root', password='*', database='internship_project')
                    my_cursor = mysqldb.cursor()
                    sql = "INSERT INTO password (username, password_for, password) VALUES (%s, %s, %s)"
                    password_for_value = password_for_entry.get()
                    my_cursor.execute(sql, (uname, password_for_value, password))
                    mysqldb.commit()
                    messagebox.showinfo("Success", "Password saved successfully!")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
                finally:
                    mysqldb.close()

            def on_generate_and_save():
                generated_password = generate_password()
                if generated_password:
                    save_password(generated_password)

            title_text = tk.Label(main_window, text='Password Generator')
            title_text.grid(row=0, column=0)

            length_label = tk.Label(main_window, text='Enter Password Length:')
            length_label.grid(row=1, column=0)

            length_entry = tk.Entry(main_window)
            length_entry.grid(row=2, column=0)
            
            password_for = tk.Label(main_window, text="Enter the password's purpose:")
            password_for.grid(row=3, column=0)
            
            password_for_entry = tk.Entry(main_window)
            password_for_entry.grid(row=4, column=0)

            display_result = tk.Entry(main_window)
            display_result.grid(row=5, column=0)

            pass_generate = tk.Button(main_window, text='Generate', command=on_generate_and_save)
            pass_generate.grid(row=6, column=0)
            
            pass_display = tk.Button(main_window, text='Display', command=lambda: display(uname))
            pass_display.grid(row=7, column=0)

            main_window.grab_set()  

        tab1()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def cancel():
    root.destroy()

root = Tk()
root.title("Login")
root.geometry("360x200")
global e1
global e2

Label(root, text="Username").place(x=10, y=10)
Label(root, text="Password").place(x=10, y=40)

e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=40)
e2.config(show="*")

Button(root, text="Login", command=Ok, height=1, width=6).place(x=100, y=100)
Button(root, text="Cancel", command=cancel, height=1, width=6).place(x=200, y=100)

root.mainloop()
