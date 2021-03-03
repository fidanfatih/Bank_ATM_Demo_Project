__auther__ = "Fatih Fidan"
__version__ = "0.02"
__email__ = "fatihfidan52@gmail.com"

from tkinter import *
from tkinter import messagebox
from datetime import datetime

class Data:
    users = []
    passwords = []

    def __init__(self):
        pass

    @classmethod
    def users_cls(cls):
        with open('user_info.txt', 'r', encoding = "utf-8") as f:
            f.seek(0)
            for line in f:
                cls.users.append(line.replace('\n', '').split('|')[0])

    @classmethod
    def passwords_cls(cls):
        with open('user_info.txt', 'r', encoding = "utf-8") as f:
            f.seek(0)
            for line in f:
                cls.passwords.append(line.replace('\n', '').split('|')[1])

    def read_attr(self, username=None, password=None):
        with open('user_info.txt', 'r', encoding = "utf-8") as f:
            f.seek(0)
            for line in f:
                self.attributes = line.replace('\n', '').split('|')
                if username == self.attributes[0]:
                    self.user_name = self.attributes[0]
                    self.password = self.attributes[1]
                    self.name = self.attributes[2]
                    self.surname = self.attributes[3]
                    self.phone_num = self.attributes[4]
                    self.email = self.attributes[5]
                    self.balance = int(self.attributes[6])
                    self.transactions = self.attributes[7].split(',')

    def write_attr(self, user_name=None):
        list = [self.user_name,
                self.password,
                self.name,
                self.surname,
                self.phone_num,
                self.email,
                str(self.balance),
                ",".join(self.transactions)]
        updated_line = "|".join(list) + "\n"

        with open('user_info.txt', 'a+', encoding = "utf-8") as file:
            file.seek(0)
            new_text = file.read()

            file.seek(0)
            for line in file:
                customer_info = line.replace('\n', '').split('|')
                if customer_info[0] == user_name:
                    file.seek(0)
                    new_text = new_text.replace(line, updated_line)

                    file.seek(0)
                    file.truncate(0)  # delete all contents of the file
                    file.write(new_text)
                    break

    def add_activities(self, money, user_name, operation, transfer_user_name):
        if operation == "deposit":
            self.balance = self.balance + int(money)
            self.transactions.append(
                f"deposit\t\t\t: €{str(money):<10} {datetime.today().strftime('%d-%m-%y  %H:%M:%S')}")
            self.write_attr(user_name)

        elif operation == "withdraw":
            self.balance = self.balance - int(money)
            self.transactions.append(
                f"withdrawed\t\t\t: €{str(money):<10} {datetime.today().strftime('%d-%m-%y  %H:%M:%S')}")
            self.write_attr(user_name)

        elif operation == "transfer":
            self.balance = self.balance - int(money)
            self.transactions.append(
                f"transferred to {transfer_user_name}   : €{str(money):<10} {datetime.today().strftime('%d-%m-%y  %H:%M:%S')}")
            self.write_attr(user_name)

            self.read_attr(transfer_user_name)
            self.balance = self.balance + int(money)
            self.transactions.append(
                f"transferred from {user_name}\t: €{str(money):<10} {datetime.today().strftime('%d-%m-%y  %H:%M:%S')}")
            self.write_attr(transfer_user_name)
            self.read_attr(user_name)


class ATM(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.root = parent

        # Frames
        # Kullanilacak her frame in objesini olustururuz.
        self.loginPage = Frame(self.root)
        self.userPasswordPage = Frame(self.root)
        self.mainMenu = Frame(self.root)
        self.withdrawMoney = Frame(self.root)
        self.depositMoney = Frame(self.root)
        self.transferMoney = Frame(self.root)
        self.accountInfo = Frame(self.root, bg = 'grey')
        self.editInfo = Frame(self.root, bg = 'grey')

        # StringVar
        self.clock = StringVar()  # A StringVar() is used to edit a widget's text

        # variables
        self.update_permission = True  # ekranda saatin gosterilgi ekranlarda True, digerlerinde False tutulur.

        # Classes
        self.data = Data()

        # Methods
        Data.users_cls()
        Data.passwords_cls()
        self.defines()
        self.login_page()

    def defines(self):
        ######################################################################
        # login_page

        self.header_1 = Label(self.loginPage,
                              text = "Demo ATM v.01",
                              font = "Ariel 15 bold italic")

        self.header_2 = Label(self.loginPage,
                              textvariable = self.clock,
                              font = "Ariel 15 bold italic")

        self.clock.set("PyCoders " + datetime.today().strftime('%d-%m-%y  %H:%M:%S'))

        self.buttonUser = Button(self.loginPage,
                                 text = "Login",
                                 anchor = "center",
                                 height = 4, width = 30,
                                 command = self.user_password_page)

        self.button_login_exit = Button(self.loginPage,
                                        text = "Exit",
                                        anchor = "center",
                                        height = 4, width = 30,
                                        command = self.root.destroy)
        ############################################################################

        # user_password_page

        self.loginUsername = Label(self.userPasswordPage,
                                   text = "Username",
                                   font = "Ariel 24 bold italic")

        self.usernameLoginEntry = Entry(self.userPasswordPage,
                                        font = "Ariel 22 bold italic")

        self.loginPassword = Label(self.userPasswordPage,
                                   text = "Password",
                                   font = "Ariel 24 bold italic")

        self.passwordLoginEntry = Entry(self.userPasswordPage,
                                        font = "Ariel 22 bold italic")

        self.button_user = Button(self.userPasswordPage,
                                  text = "Login",
                                  wraplength = 750, anchor = "center",
                                  height = 3, width = 30,
                                  command = self.checking_data)
        ######################################################################

        # main_menu
        self.button1 = Button(self.mainMenu,
                              text = "Withdraw Money",
                              anchor = "center", height = 2, width = 57,
                              command = self.withdraw_money)
        self.button2 = Button(self.mainMenu,
                              text = "Deposit Money",
                              anchor = "center", height = 2, width = 57,
                              command = self.deposit_money)

        self.button3 = Button(self.mainMenu,
                              text = "Transfer Money",
                              anchor = "center", height = 2, width = 57,
                              command = self.transfer_money)

        self.button4 = Button(self.mainMenu,
                              text = "Account Info",
                              anchor = "center", height = 2, width = 57,
                              command = self.account_info)

        self.button5 = Button(self.mainMenu,
                              text = "Edit Info",
                              anchor = "center", height = 2, width = 57,
                              command = self.edit_info)

        self.button6 = Button(self.mainMenu,
                              text = "Logout",
                              anchor = "center", height = 2, width = 57,
                              command = lambda: [self.mainMenu.grid_remove(), self.login_page()])

        ###########  withdraw ###########
        self.withdrawLabel = Label(self.withdrawMoney,
                                   text = "How much would you like to withdraw?",
                                   font = "Ariel 14 bold italic")
        self.withdrawEntry = Entry(self.withdrawMoney, font = "Ariel 22 bold italic")

        self.withdrawButton = Button(self.withdrawMoney,
                                     text = "Withdraw Money",
                                     anchor = "center", height = 3, width = 30,
                                     command = lambda: [self.operation_control("withdraw",
                                                                               self.withdrawEntry.get()),
                                                        self.withdrawEntry.delete(0, 'end')])

        self.withdrawExit = Button(self.withdrawMoney,
                                   text = "Close Panel",
                                   anchor = "center", height = 3, width = 30,
                                   command = lambda: [self.withdrawMoney.grid_remove(),
                                                      self.withdrawEntry.delete(0, 'end'),
                                                      self.main_menu()])
        ###########  deposit ###########
        self.depositLabel = Label(self.depositMoney,
                                  text = "How much would you like to deposit?",
                                  font = "Ariel 14 bold italic")

        self.depositEntry = Entry(self.depositMoney, font = "Ariel 22 bold italic")

        self.depositButton = Button(self.depositMoney,
                                    text = "Deposit Money",
                                    anchor = "center", height = 3, width = 30,
                                    command = lambda: [self.operation_control("deposit", self.depositEntry.get()),
                                                       self.depositEntry.delete(0, 'end')])

        self.depositExit = Button(self.depositMoney,
                                  text = "Close Panel",
                                  anchor = "center", height = 3, width = 30,
                                  command = lambda: [self.depositMoney.grid_remove(),
                                                     self.depositEntry.delete(0, 'end'),
                                                     self.main_menu()])
        ###########  transfer ###########
        self.transferLabel_1 = Label(self.transferMoney,
                                     text = "To whom would you like to transfer?",
                                     font = "Ariel 14 bold italic")

        self.transferEntry_1 = Entry(self.transferMoney,
                                     font = "Ariel 22 bold italic")

        self.transferLabel_2 = Label(self.transferMoney,
                                     text = "How much would you like to transfer?",
                                     font = "Ariel 14 bold italic")

        self.transferEntry_2 = Entry(self.transferMoney,
                                     font = "Ariel 22 bold italic")

        self.transferButton = Button(self.transferMoney,
                                     text = "Transfer Money",
                                     anchor = "center", height = 3, width = 30,
                                     command = lambda: [self.operation_control("transfer_money",
                                                                               self.transferEntry_2.get(),
                                                                               self.transferEntry_1.get()),
                                                        self.transferEntry_1.delete(0, 'end'),
                                                        self.transferEntry_2.delete(0, 'end')])

        self.transferExit = Button(self.transferMoney,
                                   text = "Close Panel",
                                   anchor = "center", height = 3, width = 30,
                                   command = lambda: [self.transferMoney.grid_remove(),
                                                      self.transferEntry_1.delete(0, 'end'),
                                                      self.transferEntry_2.delete(0, 'end'),
                                                      self.main_menu()])

    def login_page(self):
        self.update_permission = True
        self.loginPage.grid(row = 0, column = 0)
        self.header_1.grid(row = 0, column = 2, rowspan = 2, columnspan = 3, pady = 5, padx = 125)
        self.header_2.grid(row = 2, column = 2, rowspan = 2, columnspan = 3, pady = 5, padx = 125)
        self.buttonUser.grid(row = 4, column = 2, rowspan = 2, columnspan = 3, padx = 125, pady = 20)
        self.button_login_exit.grid(row = 6, column = 2, rowspan = 2, columnspan = 3, padx = 125, pady = 20)

    def user_password_page(self):
        self.update_permission = False
        self.loginPage.grid_remove()
        self.userPasswordPage.grid(row = 0, column = 0)
        self.loginUsername.grid(row = 0, column = 1, columnspan = 3, rowspan = 2, padx = 130, pady = 7)
        self.usernameLoginEntry.grid(row = 2, column = 1, columnspan = 3, rowspan = 2, padx = 130, pady = 10)
        self.loginPassword.grid(row = 4, column = 1, columnspan = 3, rowspan = 2, padx = 130, pady = 7)
        self.passwordLoginEntry.grid(row = 6, column = 1, columnspan = 3, rowspan = 2, padx = 130, pady = 10)
        self.button_user.grid(row = 8, column = 1, columnspan = 3, rowspan = 2, padx = 130, pady = 10)

    def main_menu(self):
        self.userPasswordPage.grid_remove()
        self.data.read_attr(self.usernameLoginEntry.get())
        self.mainMenu.grid(row = 0, column = 0)
        self.button1.grid(row = 0, column = 0, pady = 7, padx = 2)
        self.button2.grid(row = 1, column = 0, pady = 7, padx = 2)
        self.button3.grid(row = 2, column = 0, pady = 7, padx = 2)
        self.button4.grid(row = 3, column = 0, pady = 7, padx = 2)
        self.button5.grid(row = 4, column = 0, pady = 7, padx = 2)
        self.button6.grid(row = 5, column = 0, pady = 7, padx = 2)

    def checking_data(self):
        username = self.usernameLoginEntry.get()
        password = self.passwordLoginEntry.get()
        if (username in self.data.users) and (password in self.data.passwords):
            self.main_menu()
        else:
            messagebox.showinfo("Warning", "Username or password incorrect.")

    def withdraw_money(self):
        self.withdrawMoney.grid(row = 0, column = 0)
        self.withdrawLabel.grid(row = 0, column = 0, padx = 135, pady = 15)
        self.withdrawEntry.grid(row = 1, column = 0, padx = 135, pady = 15)
        self.withdrawButton.grid(row = 4, column = 0, padx = 135, pady = 15)
        self.withdrawExit.grid(row = 5, column = 0, padx = 135, pady = 15)

    def deposit_money(self):
        self.depositMoney.grid(row = 0, column = 0)
        self.depositLabel.grid(row = 0, column = 0, padx = 135, pady = 15)
        self.depositEntry.grid(row = 1, column = 0, padx = 135, pady = 15)
        self.depositButton.grid(row = 2, column = 0, padx = 135, pady = 15)
        self.depositExit.grid(row = 3, column = 0, padx = 135, pady = 15)

    def transfer_money(self):
        self.transferMoney.grid(row = 0, column = 0)
        self.transferLabel_1.grid(row = 0, column = 0, padx = 135, pady = 5)
        self.transferEntry_1.grid(row = 1, column = 0, padx = 135, pady = 5)
        self.transferLabel_2.grid(row = 2, column = 0, padx = 135, pady = 5)
        self.transferEntry_2.grid(row = 3, column = 0, padx = 135, pady = 5)
        self.transferButton.grid(row = 4, column = 0, padx = 135, pady = 5)
        self.transferExit.grid(row = 5, column = 0, padx = 135, pady = 5)

    def account_info(self):
        self.mainMenu.grid_remove()
        self.accountInfo.grid(row = 0, column = 0)
        textInfo = Text(self.accountInfo, height = 15, width = 60)
        textInfo.grid(row = 0, column = 0,
                      padx = 10, pady = 10)
        textInfo.insert(INSERT, "| ___________________ Account Info ___________________ |\n")
        # print(self.data.user_name,self.data.name )
        textInfo.insert(INSERT, f"Date\t\t: {datetime.today().strftime('%d-%m-%y')}\n" +
                        f"Time\t\t: {datetime.today().strftime('%H:%M:%S')}\n" +
                        f"Username\t\t: {self.data.user_name}\n" +
                        f"Name\t\t: {self.data.name}\n"
                        f"Surname\t\t: {self.data.surname}\n" +
                        f"Balance\t\t: {self.data.balance}\n" +
                        f"| ___________________ Transactions __________________ |\n")

        for transaction in self.data.transactions:
            textInfo.insert(INSERT, transaction + '\n')

        exitButton = Button(self.accountInfo, text = "Exit",
                            anchor = "center", height = 1, width = 20,
                            command = lambda: [self.accountInfo.grid_remove(),
                                               self.main_menu()])

        exitButton.grid(row = 2, column = 0)

    def edit_info(self):
        self.mainMenu.grid_remove()
        self.editInfo.grid(row = 0, column = 0)
        textInfo = Text(self.editInfo, height = 8, width = 50)
        textInfo.grid(row = 0, columnspan = 2,
                      padx = 10, pady = 10)
        textInfo.insert(INSERT, "| ______________ Account Details _____________ |\n")
        textInfo.insert(INSERT, f"Username \t\t: {self.data.user_name}\n" +
                        f"Password \t\t: {self.data.password}\n"
                        f"Name \t\t: {self.data.name}\n"
                        f"Surname \t\t: {self.data.surname}\n" +
                        f"Phone Number \t\t: {self.data.phone_num}\n"
                        f"Email \t\t: {self.data.email}\n")

        editButton = Button(self.editInfo, text = "Edit Info",
                            anchor = "center", height = 1, width = 10,
                            command = self.edit)

        editButton.grid(row = 2, column = 0,
                        sticky = E,
                        padx = 10, pady = 10)

        exitButton = Button(self.editInfo, text = "Exit",
                            anchor = "center", height = 1, width = 10,
                            command = lambda: [self.editInfo.grid_remove(),
                                               self.main_menu()])
        exitButton.grid(row = 2, column = 1,
                        sticky = W,
                        padx = 10, pady = 10)

    def edit(self):
        self.edit_user = Label(self.editInfo, text = 'UserName\t\t:')
        self.edit_user.grid(row = 4, column = 0,
                            sticky = E,
                            padx = 10, pady = 2)
        self.edit_user_entry = Entry(self.editInfo)
        self.edit_user_entry.grid(row = 4, column = 1,
                                  sticky = W,
                                  padx = 0, pady = 2)
        self.edit_password = Label(self.editInfo, text = 'Password\t\t:')
        self.edit_password.grid(row = 5, column = 0,
                                sticky = E,
                                padx = 10, pady = 2)
        self.edit_password_entry = Entry(self.editInfo)
        self.edit_password_entry.grid(row = 5, column = 1,
                                      sticky = W,
                                      padx = 0, pady = 2)
        self.edit_name = Label(self.editInfo, text = 'Name\t\t\t:')
        self.edit_name.grid(row = 6, column = 0,
                            sticky = E,
                            padx = 10, pady = 2)
        self.edit_name_entry = Entry(self.editInfo)
        self.edit_name_entry.grid(row = 6, column = 1,
                                  sticky = W,
                                  padx = 0, pady = 2)
        self.edit_surname = Label(self.editInfo, text = 'Surname\t\t\t:')
        self.edit_surname.grid(row = 7, column = 0,
                               sticky = E,
                               padx = 10, pady = 2)
        self.edit_surname_entry = Entry(self.editInfo)
        self.edit_surname_entry.grid(row = 7, column = 1,
                                     sticky = W,
                                     padx = 0, pady = 2)
        self.edit_phone = Label(self.editInfo, text = 'Phone Number\t\t:')
        self.edit_phone.grid(row = 8, column = 0,
                             sticky = E,
                             padx = 10, pady = 2)
        self.edit_phone_entry = Entry(self.editInfo)
        self.edit_phone_entry.grid(row = 8, column = 1,
                                   sticky = W,
                                   padx = 0, pady = 2)

        self.edit_email = Label(self.editInfo, text = 'Email\t\t\t:')
        self.edit_email.grid(row = 9, column = 0,
                             sticky = E,
                             padx = 10, pady = 2)
        self.edit_email_entry = Entry(self.editInfo)
        self.edit_email_entry.grid(row = 9, column = 1,
                                   sticky = W,
                                   padx = 0, pady = 2)

        self.update_button = Button(self.editInfo, text = 'Update',
                                    anchor = "center", height = 1, width = 10,
                                    command = lambda: [self.update_data(),
                                    self.editInfo.grid_remove(),
                                    self.main_menu()])

        self.update_button.grid(row = 10, column = 1,
        sticky = W,
        padx = 10, pady = 10)

    def update_data(self):
        confirmation = messagebox.askyesnocancel(title = 'Warning', message = 'Are you sure?')
        if confirmation == True:
            self.data.user_name = self.edit_user_entry.get()
            self.data.password = self.edit_password_entry.get()
            self.data.name = self.edit_name_entry.get()
            self.data.surname = self.edit_surname_entry.get()
            self.data.phone_num = self.edit_phone_entry.get()
            self.data.email = self.edit_email_entry.get()

            self.data.write_attr(self.data.user_name)
            messagebox.showinfo(title = 'Warning', message = 'Customer Informations were updated!')

    def operation_control(self, operation, money=None, transfer_user=None):
        if operation == "withdraw":
            if (not money.isdigit()) or (int(money) <= 0):
                messagebox.showinfo("Warning", "Wrong money entry")

            elif int(money) > 0:
                balance = self.data.balance
                if int(money) < balance:
                    self.data.add_activities(money,
                                             self.usernameLoginEntry.get(),
                                             operation,
                                             transfer_user)

                    messagebox.showinfo(title = "Warning",
                                        message = f"Withdraw €{money}")

                    # islem basarili olunca herzaman mevcut arayuz temizlenip, bir ust menuye gecilir.
                    self.withdrawMoney.grid_remove()
                    self.main_menu()
                else:
                    messagebox.showinfo("Warning", "Not enough balance")

        elif operation == "deposit":
            if (not money.isdigit()) or (int(money) <= 0):
                messagebox.showinfo("Warning", "Wrong money entry")
            else:
                if int(money) > 0:
                    self.data.add_activities(money,
                                             self.usernameLoginEntry.get(),
                                             operation,
                                             transfer_user)

                    messagebox.showinfo(title = "Warning",
                                        message = f"Deposit €{money}")

                    self.depositMoney.grid_remove()

                else:
                    messagebox.showinfo("Warning", "Wrong money entry")

        elif operation == "transfer_money":
            if transfer_user in self.data.users:
                if (not money.isdigit()) or (int(money) <= 0):
                    messagebox.showinfo("Warning", "Wrong money entry")
                else:
                    if int(money) <= self.data.balance:
                        self.data.add_activities(int(money),
                                                 self.usernameLoginEntry.get(),
                                                 "transfer",
                                                 transfer_user)

                        messagebox.showinfo(title = "Warning",
                                            message = f"Transferring €{money} to {transfer_user} succeeded.")

                        self.transferMoney.grid_remove()
                        self.main_menu()
                    else:
                        messagebox.showinfo("Warning", "Not enough balance")
            else:
                messagebox.showinfo("Warning", "Not found transfer user")

    def update_clock(self):
        if self.update_permission:
            self.clock.set("PyCoders " + datetime.today().strftime('%d-%m-%y  %H:%M:%S'))
        root.after(1000, obj.update_clock)


if __name__ == "__main__":
    root = Tk()
    root.title("Sign In")
    root.geometry("600x420")
    # icon = PhotoImage(file = "icon.png")
    # root.call("wm", 'iconphoto', root._w, icon)
    obj = ATM(root)
    root.after(1000, func = obj.update_clock)
    root.mainloop()
