# -*-coding:utf8-*-
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
import database

__author__ = 'denkus24'
__version__ = '1.0'
__copyright__ = "Copyright 2021-2022 (©), denkus24"

# Creating window
root = Tk()
root.geometry("640x489+640+240")
root.title("PKeep v1.0")
root.resizable(False, False)
root.iconbitmap('icons/icon.ico')

# Creating main frames
f1 = Frame(width=640)
f2 = Frame(width=640)
f3 = Frame(width=640)
f4 = Frame(width=640)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

path = ''
key = ''


def switch_frames(frame):
    frame.tkraise()


def back(frame):
    frame.tkraise()
    tree.update_idletasks()


# Add menu
def about():
    messagebox.showinfo("About", "  PKeep v1.0\n  Copyright (©) 2021-2022, denkus24")


# Menu for file button in menu
def new_file():
    global path, key

    dir = filedialog.asksaveasfilename()

    if dir == '':
        return
    name = dir + '.csv'
    path = dir
    with open(dir, 'w') as file:
        file.write('name,login,password,link')

    create_window = Tk()
    create_window.geometry('320x240')
    create_window.title('Create new file')
    create_window.resizable(False, False)
    create_window.iconbitmap('icons/icon.ico')

    entry_frame_new = Frame(create_window)
    password_entry_frame = LabelFrame(entry_frame_new, text="Password")

    password_entry_var = StringVar()
    password_entry_new = ttk.Entry(password_entry_frame, textvariable=password_entry_var, show="*")

    def submit_button():
        global key
        key = password_entry_new.get()
        database.encrypting_file(dir, key)
        create_window.destroy()
        root.title(name + ' - PKeep v1.0')

    submit_button = ttk.Button(entry_frame_new, text='Submit', command=submit_button)

    password_entry_frame.pack()
    entry_frame_new.pack(pady=70)
    submit_button.pack(pady=5)
    password_entry_new.pack(padx=3, pady=3)

    create_window.mainloop()


def open_file():
    global path, key

    path = filedialog.askopenfilename()
    if path == '':
        return
    # Filling treeview
    open_window = Tk()
    open_window.geometry('320x240')
    open_window.title('Open file')
    open_window.resizable(False, False)
    open_window.iconbitmap('icons/icon.ico')

    entry_frame_open = Frame(open_window)
    password_entry_frame = LabelFrame(entry_frame_open, text="Password")

    password_entry_var = StringVar()
    password_entry_open = ttk.Entry(password_entry_frame, textvariable=password_entry_var, show="*")

    def submit_button():
        global key
        key = password_entry_open.get()
        open_window.destroy()
        try:
            data = database.reading_file(path, key)
            del (data[0])
            for x in data:
                tree.insert(parent='', index='end', values=x)
            root.title(path + ' - PKeep v1.0')
        except:
            messagebox.showerror("Error", "Error by opening file")
            return

    submit_button = ttk.Button(entry_frame_open, text='Submit', command=submit_button)

    password_entry_frame.pack()
    entry_frame_open.pack(pady=70)
    submit_button.pack(pady=5)
    password_entry_open.pack(padx=3, pady=3)

    open_window.mainloop()


def close_file():
    global path
    file = open(path, 'r')
    file.close()
    path = ''
    root.title('PKeep v1.0')
    for i in tree.get_children():
        tree.delete(i)


def exit():
    root.destroy()


file_menu = Menu(tearoff=False)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Close", command=close_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit)

menu = Menu()
menu.add_cascade(label='File', menu=file_menu)
menu.add_command(label='About', command=about)
root.config(menu=menu)

# Filling f1 frame
# Making buttons
button_frame = Frame(f1, pady=5, relief=RIDGE)

add_image = PhotoImage(file="icons/add.png")
add_button = Button(button_frame, text='add', command=lambda: switch_frames(f2), image=add_image, bd=0)


# Function for delete button
def delete_function():
    selected_item = tree.focus()
    delete_item = tree.item(selected_item, "values")
    if selected_item == '':
        messagebox.showerror("Error", "Item not selected")
        return
    else:
        database.delete_element(path, delete_item, key)
        tree.delete(selected_item)


delete_image = PhotoImage(file="icons/delete.png")
delete_button = Button(button_frame, text='delete', image=delete_image, bd=0, command=delete_function)

# Creating special switch function for edit button
old_element = ''


def edit_switch_frames(frame):
    global old_element
    selected_item = tree.focus()
    edit_item = tree.item(selected_item, "values")
    old_element = edit_item
    if selected_item == '':
        messagebox.showerror("Error", "Item not selected")
        return
    else:
        switch_frames(frame)
    name_var_edit.set(edit_item[0])
    login_var_edit.set(edit_item[1])
    password_var_edit.set(edit_item[2])
    link_var_edit.set(edit_item[3])


edit_image = PhotoImage(file="icons/edit.png")
edit_button = Button(button_frame, text='edit', image=edit_image, bd=0, command=lambda: edit_switch_frames(f3))


# Function for follow site button
def follow_link():
    selected_item = tree.focus()
    link = tree.item(selected_item, "values")

    if selected_item == '':
        messagebox.showerror("Error", "Item not selected")
        return
    else:
        webbrowser.open(link[3])


browser_image = PhotoImage(file="icons/browser.png")
browser_button = Button(button_frame, text='browser', image=browser_image, bd=0, command=follow_link)

add_button.pack(padx=2, side=LEFT)
delete_button.pack(padx=2, side=LEFT)
edit_button.pack(padx=2, side=LEFT)
browser_button.pack(padx=2, side=LEFT)
button_frame.pack(fill=X)

# Creating table(treeview)
tree = ttk.Treeview(f1, height=20)

tree["columns"] = ("Name", "Login", "Password", "Link")

tree.column("#0", width=0, stretch=NO)
tree.column("Name", width=120, anchor=W)
tree.column("Login", width=120, anchor=W)
tree.column("Password", width=120, anchor=W)
tree.column("Link", width=120, anchor=W)

tree.heading("#0", text="", anchor=W)
tree.heading("Name", text="Name", anchor=W)
tree.heading("Login", text="Login", anchor=W)
tree.heading("Password", text="Password", anchor=W)
tree.heading("Link", text="Link", anchor=W)

tree.pack(fill=BOTH, expand=1, padx=5)


def treeview_update():
    """Function for updating database"""
    for i in tree.get_children():
        tree.delete(i)
    data = database.reading_file(path, key)
    del (data[0])
    for x in data:
        tree.insert(parent='', index='end', values=x)


# Filling f2 frame (Add)
back_image = PhotoImage(file="icons/back.png")
back_button = Button(f2, command=lambda: switch_frames(f1), image=back_image, bd=0)
back_button.pack(anchor=NW, padx=3, pady=5)

enter_frame_add = Frame(f2)

name_frame_add = LabelFrame(enter_frame_add, text="Name")
name_var_add = StringVar()
name_entry_add = ttk.Entry(name_frame_add, textvariable=name_var_add)
name_entry_add.pack(pady=3, padx=3)
name_frame_add.pack(pady=5)

login_frame_add = LabelFrame(enter_frame_add, text="Login")
login_var_add = StringVar()
login_entry_add = ttk.Entry(login_frame_add, textvariable=login_var_add)
login_entry_add.pack(pady=3, padx=3)
login_frame_add.pack()

password_frame_add = LabelFrame(enter_frame_add, text="Password")
password_var_add = StringVar()
password_entry_add = ttk.Entry(password_frame_add, textvariable=password_var_add)
password_entry_add.pack(pady=3, padx=3, side=LEFT)
password_frame_add.pack(pady=5, side=TOP)

link_frame_add = LabelFrame(enter_frame_add, text="Link")
link_var_add = StringVar()
link_entry_add = ttk.Entry(link_frame_add, textvariable=link_var_add)
link_entry_add.pack(pady=3, padx=3)
link_frame_add.pack(pady=5)


# Function for "accept" button
def accept_function_add():
    if login_var_add.get() == '' and \
            password_var_add.get() == '' and \
            link_var_add.get() == '' or \
            name_var_add.get() == '' or \
            path == '':
        messagebox.showerror("Error", "Unable to create entry")
        return

    database.add_element(path, name_var_add.get(), login_var_add.get(), password_var_add.get(), link_var_add.get(), key)
    treeview_update()


accept_image = PhotoImage(file='icons/accept.png')
accept_button_add = ttk.Button(enter_frame_add, width=5, command=accept_function_add, image=accept_image, compound=LEFT,
                               text='OK')
accept_button_add.pack(pady=5)

enter_frame_add.pack(pady=70)

# Filling f3 frame (Edit)

back_button_edit = Button(f3, command=lambda: switch_frames(f1), image=back_image, bd=0)
back_button_edit.pack(anchor=NW, padx=3, pady=5)

enter_frame_edit = Frame(f3)

name_frame_edit = LabelFrame(enter_frame_edit, text="Name")
name_var_edit = StringVar()
name_entry_edit = ttk.Entry(name_frame_edit, textvariable=name_var_edit)
name_entry_edit.pack(pady=3, padx=3)
name_frame_edit.pack(pady=5)

login_frame_edit = LabelFrame(enter_frame_edit, text="Login")
login_var_edit = StringVar()
login_entry_edit = ttk.Entry(login_frame_edit, textvariable=login_var_edit)
login_entry_edit.pack(pady=3, padx=3)
login_frame_edit.pack(pady=5)

password_frame_edit = LabelFrame(enter_frame_edit, text="Password")
password_var_edit = StringVar()
password_entry_edit = ttk.Entry(password_frame_edit, textvariable=password_var_edit)
password_entry_edit.pack(pady=3, padx=3)
password_frame_edit.pack(pady=5)

link_frame_edit = LabelFrame(enter_frame_edit, text="Link")
link_var_edit = StringVar()
link_entry_edit = ttk.Entry(link_frame_edit, textvariable=link_var_edit)
link_entry_edit.pack(pady=3, padx=3)
link_frame_edit.pack(pady=5)


def accept_function_edit():
    # доделать здесь
    global old_element
    new_element = (name_var_edit.get(), login_var_edit.get(), password_var_edit.get(), link_var_edit.get())
    database.edit_element(old_element, new_element, path, key)
    treeview_update()


accept_button_edit = ttk.Button(enter_frame_edit, text='OK', width=5, command=accept_function_edit, image=accept_image,
                                compound=LEFT)
accept_button_edit.pack(pady=5)

enter_frame_edit.pack(pady=70)


def key_release(event):
    """Function for copy, paste and cut key combinations"""
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")


# Starting a GUI
switch_frames(f1)
root.bind_all('<Key>', key_release, '+')
root.mainloop()