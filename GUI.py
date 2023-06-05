import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import user

# Global variables
database_name = 'DBVC'
db_connect = None
db_cursor = None
current_version = None
current_branch = None


class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)
        self.config(menu=menu)

        command_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Pages", menu=command_menu)
        command_menu.add_command(
            label="Init", command=lambda: self.show_frame(InitPage)
        )
        command_menu.add_command(
            label="Register", command=lambda: self.show_frame(RegisterPage)
        )
        command_menu.add_command(
            label="Login", command=lambda: self.show_frame(LoginPage)
        )

        for F in (StartPage, InitPage, RegisterPage, LoginPage, DashboardPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to DBVC system")
        label.pack(pady=10, padx=10)


class InitPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Init")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        user_var = tk.StringVar()
        pwd_var = tk.StringVar()
        host_var = tk.StringVar()
        port_var = tk.StringVar()

        user_label = tk.Label(self, text='User:')
        user_label.grid(row=1, column=0, sticky='e')
        user_entry = tk.Entry(self, textvariable=user_var)
        user_entry.insert(0, 'root')
        user_entry.grid(row=1, column=1)

        pwd_label = tk.Label(self, text='Password:')
        pwd_label.grid(row=2, column=0, sticky='e')
        pwd_entry = tk.Entry(self, textvariable=pwd_var)
        pwd_entry.insert(0, 'secure1234')
        pwd_entry.grid(row=2, column=1)

        host_label = tk.Label(self, text='Host:')
        host_label.grid(row=3, column=0, sticky='e')
        host_entry = tk.Entry(self, textvariable=host_var)
        host_entry.insert(0, '127.0.0.1')
        host_entry.grid(row=3, column=1)

        port_label = tk.Label(self, text='Port:')
        port_label.grid(row=4, column=0, sticky='e')
        port_entry = tk.Entry(self, textvariable=port_var)
        port_entry.insert(0, '3306')
        port_entry.grid(row=4, column=1)

        parse_button = tk.Button(
            self,
            text='Parse',
            command=lambda: self.init_database(
                user_var.get(), pwd_var.get(), host_var.get(), port_var.get()
            ),
        )
        parse_button.grid(row=5, column=0, columnspan=2, pady=10)

    def init_database(self, db_user, pwd, host, port):
        global db_connect, db_cursor
        db_connect, db_cursor = user.init(
            db_user, pwd, host, port, database_name
        )
        print(db_connect, db_cursor)
        messagebox.showinfo('Init', 'Database initialized successfully.')


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Register")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        name_var = tk.StringVar()
        email_var = tk.StringVar()

        name_label = tk.Label(self, text='User Name:')
        name_label.grid(row=1, column=0, sticky='e')
        name_entry = tk.Entry(self, textvariable=name_var)
        name_entry.grid(row=1, column=1)

        email_label = tk.Label(self, text='User Email:')
        email_label.grid(row=2, column=0, sticky='e')
        email_entry = tk.Entry(self, textvariable=email_var)
        email_entry.grid(row=2, column=1)

        parse_button = tk.Button(
            self,
            text='Parse',
            command=lambda: self.register_user(
                name_var.get(), email_var.get()
            ),
        )
        parse_button.grid(row=5, column=0, columnspan=2, pady=10)

    def register_user(self, name, email):
        global db_connect, db_cursor, database_name
        if db_connect is None:
            print("Error: Database connection is not initialized. Run 'init' command first.")
            messagebox.showinfo('Register', "Error: Database connection is not initialized. Run 'init' command first.")
        else:
            user.register(db_connect, db_cursor, database_name, name, email)

            messagebox.showinfo('Register', 'User registered successfully.')


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frames = {}

        label = tk.Label(self, text="Login")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        name_var = tk.StringVar()
        email_var = tk.StringVar()

        name_label = tk.Label(self, text='User Name:')
        name_label.grid(row=1, column=0, sticky='e')
        name_entry = tk.Entry(self, textvariable=name_var)
        name_entry.insert(0, 'Leo')
        name_entry.grid(row=1, column=1)

        email_label = tk.Label(self, text='User Email:')
        email_label.grid(row=2, column=0, sticky='e')
        email_entry = tk.Entry(self, textvariable=email_var)
        email_entry.insert(0, 'Leo@gmail.com')
        email_entry.grid(row=2, column=1)

        parse_button = tk.Button(
            self,
            text='Parse',
            command=lambda: self.login_user(
                name_var.get(), email_var.get()
            ),
        )
        parse_button.grid(row=5, column=0, columnspan=2, pady=10)

    def login_user(self, name, email):
        global current_version
        global current_branch
        try:
            current_version, current_branch = user.login(db_cursor, database_name, name, email)
            messagebox.showinfo('Login', "Login successfully.")
            print(current_version, current_branch)
            self.controller.show_frame(DashboardPage)
        except Exception as e:
            print(e)
            messagebox.showinfo('Login', e)

# After login show the page below

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Dashboard")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        commit_button = tk.Button(
            self,
            text='Commit',
            command=self.commit_changes
        )
        commit_button.grid(row=1, column=0, pady=10)

        log_button = tk.Button(
            self,
            text='Log',
            command=self.view_log
        )
        log_button.grid(row=1, column=1, pady=10)

        merge_button = tk.Button(
            self,
            text='Merge',
            command=self.merge_branches
        )
        merge_button.grid(row=1, column=2, columnspan=2, pady=10)

    def commit_changes(self):
        # Add your commit logic here
        messagebox.showinfo('Commit', 'Changes committed successfully.')

    def view_log(self):
        # Add your log viewing logic here
        messagebox.showinfo('Log', 'Log viewed successfully.')

    def merge_branches(self):
        # Add your merge logic here
        messagebox.showinfo('Merge', 'Branches merged successfully.')


app = MyApp()
app.geometry("800x600")
app.mainloop()
