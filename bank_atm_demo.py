from tkinter import *
from datetime import datetime

class Data:
    def __init__(self):
        self.activities = {"user_1": [0, []],  # 0, ilk basta hesaptaki para, [], hesap hareketini tutacak.
                           "user_2": [0, []]}

        self.members = {"user_1": "1234",
                        "user_2": "4321"}

    def request_data(self):
        return self.activities, self.members

    def add_activities(self, money, user, operation, transfer_user):

        if operation == "deposit":
            self.activities[user][0] = self.activities[user][0] + int(money)
            self.activities[user][1].append(
                f"deposit\t\t\t: €{str(money):<10} {datetime.today().strftime('%d-%m-%y  %H:%M:%S')}")

        elif operation == "withdraw":
            self.activities[user][0] = self.activities[user][0] - int(money)
            self.activities[user][1].append(
                f"withdrawed\t\t\t: €{str(money):<10} {datetime.today().strftime('%d-%m-%y  %H:%M:%S')}")

        elif operation == "transfer":
            self.activities[user][0] = self.activities[user][0] - int(money)
            self.activities[user][1].append(
                f"transferred to {transfer_user}   : €{str(money):<10} {datetime.today().strftime('%d-%m-%y  %H:%M:%S')}")

            self.activities[transfer_user][0] = self.activities[transfer_user][0] + int(money)
            self.activities[transfer_user][1].append(
                f"transferred from {user}\t: €{str(money):<10} {datetime.today().strftime('%d-%m-%y  %H:%M:%S')}")


class Bank_ATM_GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry('600x325+500+150')

        # Frames
        # Kullanilacak her frame in objesini olustururuz.
        self.loginPage = Frame(self.parent)
        self.userLoginPage = Frame(self.parent)
        self.loginUser = Frame(self.parent)
        self.userOperations = Frame(self.parent)

        # StringVar
        self.clock = StringVar()  # A StringVar() is used to edit a widget's text

        # variables
        self.update_permission = True  # ekranda saatin gosterilgi ekranlarda True, digerlerinde False tutulur.

        # Classes
        self.data = Data()

        self.defines()
        self.login_page()

    def login_page(self):
        self.update_permission = True
        self.loginPage.grid(row=0, column=0)
        self.text_1.grid(row=0, column=2, rowspan=2, columnspan=3, pady=5, padx=125)
        self.text_2.grid(row=2, column=2, rowspan=2, columnspan=3, pady=5, padx=125)
        self.buttonUser.grid(row=4, column=2, rowspan=2, columnspan=3, padx=125, pady=20)
        self.button_login_exit.grid(row=6, column=2, rowspan=2, columnspan=3, padx=125, pady=20)

    def user_login_page(self):
        self.update_permission = False
        self.loginPage.grid_remove()
        self.userLoginPage.grid(row=0, column=0)

        self.loginUsername.grid(row=0, column=1, columnspan=3, rowspan=2, padx=130, pady=7)
        self.usernameLoginEntry.grid(row=2, column=1, columnspan=3, rowspan=2, padx=130, pady=10)
        self.loginPassword.grid(row=4, column=1, columnspan=3, rowspan=2, padx=130, pady=7)
        self.passwordLoginEntry.grid(row=6, column=1, columnspan=3, rowspan=2, padx=130, pady=10)
        self.button_user.grid(row=8, column=1, columnspan=3, rowspan=2, padx=130, pady=10)

    def checking_data(self):
        username = self.usernameLoginEntry.get()
        password = self.passwordLoginEntry.get()
        activities, members = self.data.request_data()
        if username in members:
            if members[username] == password:
                self.login_user()
            else:
                messagebox.showinfo("Warning", "Username or password incorrect.")
        else:
            messagebox.showinfo("Warning", "Username or password incorrect.")

    def login_user(self):
        self.userLoginPage.grid_remove()
        self.loginUser.grid(row=0, column=0)
        self.button1.grid(row=0, column=0, pady=7, padx=2)
        self.button2.grid(row=1, column=0, pady=7, padx=2)
        self.button3.grid(row=2, column=0, pady=7, padx=2)
        self.button4.grid(row=3, column=0, pady=7, padx=2)
        self.button5.grid(row=4, column=0, pady=7, padx=2)

    def defines(self):
        ######################################################################
        # login_page

        self.text_1 = Label(self.loginPage,
                            text="Demo ATM v.01",
                            font="Ariel 15 bold italic")

        self.text_2 = Label(self.loginPage,
                            textvariable=self.clock,
                            font="Ariel 15 bold italic")

        self.clock.set("PyCoders " + datetime.today().strftime('%d-%m-%y  %H:%M:%S'))

        self.buttonUser = Button(self.loginPage,
                                 text="Login",
                                 anchor="center",
                                 height=4, width=30,
                                 command=self.user_login_page)


        self.button_login_exit = Button(self.loginPage,
                                        text="Exit",
                                        anchor="center",
                                        height=4, width=30,
                                        command=self.parent.destroy)
        ############################################################################

        # user_login_page

        self.loginUsername = Label(self.userLoginPage,
                                   text="Username",
                                   font="Ariel 24 bold italic")

        self.usernameLoginEntry = Entry(self.userLoginPage,
                                        font="Ariel 22 bold italic")

        self.loginPassword = Label(self.userLoginPage,
                                   text="Password",
                                   font="Ariel 24 bold italic")

        self.passwordLoginEntry = Entry(self.userLoginPage,
                                        font="Ariel 22 bold italic")

        self.button_user = Button(self.userLoginPage,
                                  text="Login",
                                  wraplength=750, anchor="center",
                                  height=3, width=30,
                                  command=self.checking_data)
        ######################################################################

        # login_user
        self.button1 = Button(self.loginUser,
                              text="Withdraw Money",
                              anchor="center", height=2, width=57,
                              command=lambda: self.user_operations("withdraw"))
        self.button2 = Button(self.loginUser,
                              text="Deposit Money",
                              anchor="center", height=2, width=57,
                              command=lambda: self.user_operations("deposit"))

        self.button3 = Button(self.loginUser,
                              text="Transfer Money",
                              anchor="center", height=2, width=57,
                              command=lambda: self.user_operations("tranfer_money"))

        self.button4 = Button(self.loginUser,
                              text="Account Info",
                              anchor="center", height=2, width=57,
                              command=lambda: self.user_operations("info"))

        self.button5 = Button(self.loginUser,
                              text="Logout",
                              anchor="center", height=2, width=57,
                              command=lambda: [self.loginUser.grid_remove(), self.login_page()])

        ######################################################################

        # user_operations

        ###########  withdraw ###########
        self.withdrawLabel = Label(self.userOperations,
                                   text="How much would you like to withdraw?",
                                   font="Ariel 14 bold italic")
        self.withdrawEntry = Entry(self.userOperations, font="Ariel 22 bold italic")

        self.withdrawButton = Button(self.userOperations,
                                     text="Withdraw Money",
                                     anchor="center", height=3, width=30,
                                     command=lambda: [self.operation_control("withdraw",
                                                                             self.withdrawEntry.get()),
                                                      self.withdrawEntry.delete(0, 'end')])

        self.withdrawExit = Button(self.userOperations,
                                   text="Close Panel",
                                   anchor="center", height=3, width=30,
                                   command=lambda: [self.userOperations.grid_remove(),
                                                    self.withdrawEntry.delete(0, 'end'),
                                                    self.login_user()])
        ###########  deposit ###########
        self.depositLabel = Label(self.userOperations,
                                  text="How much would you like to deposit?",
                                  font="Ariel 14 bold italic")

        self.depositEntry = Entry(self.userOperations, font="Ariel 22 bold italic")

        self.depositButton = Button(self.userOperations,
                                    text="Deposit Money",
                                    anchor="center", height=3, width=30,
                                    command=lambda: [self.operation_control("deposit",
                                                                            self.depositEntry.get()),
                                                     self.depositEntry.delete(0, 'end')])

        self.depositExit = Button(self.userOperations,
                                  text="Close Panel",
                                  anchor="center", height=3, width=30,
                                  command=lambda: [self.userOperations.grid_remove(),
                                                   self.depositEntry.delete(0, 'end'),
                                                   self.login_user()])
        ###########  transfer ###########
        self.transferLabel_1 = Label(self.userOperations,
                                     text="To whom would you like to transfer?",
                                     font="Ariel 14 bold italic")

        self.transferEntry_1 = Entry(self.userOperations,
                                     font="Ariel 22 bold italic")

        self.transferLabel_2 = Label(self.userOperations,
                                     text="How much would you like to transfer?",
                                     font="Ariel 14 bold italic")

        self.transferEntry_2 = Entry(self.userOperations,
                                     font="Ariel 22 bold italic")

        self.transferButton = Button(self.userOperations,
                                     text="Transfer Money",
                                     anchor="center", height=3, width=30,
                                     command=lambda: [self.operation_control("transfer_money",
                                                                             self.transferEntry_2.get(),
                                                                             self.transferEntry_1.get()),
                                                      self.transferEntry_1.delete(0, 'end'),
                                                      self.transferEntry_2.delete(0, 'end')])

        self.transferExit = Button(self.userOperations,
                                   text="Close Panel",
                                   anchor="center", height=3, width=30,
                                   command=lambda: [self.userOperations.grid_remove(),
                                                    self.transferEntry_1.delete(0, 'end'),
                                                    self.transferEntry_2.delete(0, 'end'),
                                                    self.login_user()])

    def user_operations(self, process):
        self.userOperations.grid(row=0, column=0)

        list = [self.loginUser,
                self.withdrawLabel, self.withdrawEntry, self.withdrawButton, self.withdrawExit,
                self.depositLabel, self.depositEntry, self.depositButton, self.depositExit,
                self.transferLabel_1, self.transferEntry_1, self.transferLabel_2, self.transferEntry_2,
                self.transferButton, self.transferExit]
        for i in list: i.grid_remove()

        if process == "withdraw":
            self.withdrawLabel.grid(row=0, column=0, padx=135, pady=15)
            self.withdrawEntry.grid(row=1, column=0, padx=135, pady=15)
            self.withdrawButton.grid(row=4, column=0, padx=135, pady=15)
            self.withdrawExit.grid(row=5, column=0, padx=135, pady=15)
        elif process == "deposit":
            self.depositLabel.grid(row=0, column=0, padx=135, pady=15)
            self.depositEntry.grid(row=1, column=0, padx=135, pady=15)
            self.depositButton.grid(row=2, column=0, padx=135, pady=15)
            self.depositExit.grid(row=3, column=0, padx=135, pady=15)
        elif process == "tranfer_money":
            self.transferLabel_1.grid(row=0, column=0, padx=135, pady=5)
            self.transferEntry_1.grid(row=1, column=0, padx=135, pady=5)
            self.transferLabel_2.grid(row=2, column=0, padx=135, pady=5)
            self.transferEntry_2.grid(row=3, column=0, padx=135, pady=5)
            self.transferButton.grid(row=4, column=0, padx=135, pady=5)
            self.transferExit.grid(row=5, column=0, padx=135, pady=5)
        else:
            self.operation_control("info")

    def update_clock(self):
        if self.update_permission:
            self.clock.set("PyCoders " + datetime.today().strftime('%d-%m-%y  %H:%M:%S'))
        root.after(1000, run.update_clock)

    def operation_control(self, operation, money=None, transfer_user=None):
        if operation == "withdraw":
            if (not money.isdigit()) or (int(money) <= 0):
                messagebox.showinfo("Warning", "Wrong money entry")

            elif int(money) > 0:
                activities, users = self.data.request_data()  # activities: self.activities,
                # users:self.members
                # self.data: data classindan olusturulmus data objesi
                for i in activities:
                    if i == self.usernameLoginEntry.get():
                        balance = activities[i][0]

                if int(money) < balance:
                    self.data.add_activities(money,
                                             self.usernameLoginEntry.get(),
                                             operation, transfer_user)

                    messagebox.showinfo(title="Warning",
                                        message=f"Withdraw €{money}")

                    # islem basarili olunca herzaman mevcut arayuz temizlenip, bir ust menuye gecilir.
                    self.userOperations.grid_remove()
                    self.login_user()
                else:
                    messagebox.showinfo("Warning", "Not enough balance")

        elif operation == "deposit":
            if (not money.isdigit()) or (int(money) <= 0):
                messagebox.showinfo("Warning", "Wrong money entry")
            else:
                if int(money) > 0:
                    self.data.add_activities(money,
                                             self.usernameLoginEntry.get(),
                                             operation, transfer_user)

                    messagebox.showinfo(title="Warning",
                                        message=f"Deposit €{money}")

                    self.userOperations.grid_remove()
                    self.login_user()

                else:
                    messagebox.showinfo("Warning", "Wrong money entry")


        elif operation == "transfer_money":
            activities, users = self.data.request_data()
            control = False
            for i in users:
                if (i == transfer_user):
                    control = True
            if control:
                if (not money.isdigit()) or (int(money) <= 0):
                    messagebox.showinfo("Warning", "Wrong money entry")
                else:
                    if int(money) > 0:
                        for i in activities:
                            if i == self.usernameLoginEntry.get():
                                if activities[i][0] >= int(money):
                                    self.data.add_activities(int(money),
                                                             self.usernameLoginEntry.get(),
                                                             "transfer",
                                                             transfer_user)

                                    messagebox.showinfo(title="Warning",
                                                        message=f"Transferring €{money} to {transfer_user} succeeded.")

                                    self.userOperations.grid_remove()
                                    self.login_user()
                                else:
                                    messagebox.showinfo("Warning", "Not enough balance")
            else:
                messagebox.showinfo("Warning", "Not found transfer user")


        # show user information
        else:
            self.userOperations.grid_remove()

            showInfo = Frame(self.parent, bg='grey')
            showInfo.grid(row=0, column=0)

            textInfo = Text(showInfo, height=15, width=60)
            textInfo.grid(row=0, column=0,
                          padx=10, pady=10)  # text objesinin cerceve margin ini belirledik.

            activities, users = self.data.request_data()
            textInfo.insert(INSERT, "| _____________________ User Data _____________________ |\n")

            for name in activities:
                if (name == self.usernameLoginEntry.get()):
                    textInfo.insert(INSERT, f"Date: {datetime.today().strftime('%d-%m-%y')}\n" +
                                    f"Time: {datetime.today().strftime('%H:%M:%S')}\n" +
                                    f"Your: {name}\n" +
                                    f"Password: {users[name]}\n" +
                                    f"Balance : {str(activities[name][0])}\n" +
                                    f"| ____________________ Transactions ___________________ |\n")

                    for message in activities[name][1]:
                        textInfo.insert(INSERT, message + '\n')

            textButton = Button(showInfo, text="Exit",
                                anchor="center", height=1, width=20,
                                command=lambda: [showInfo.destroy(),
                                                 self.login_user()])
            textButton.grid(row=2, column=0)


if __name__ == "__main__":
    root = Tk()
    run = Bank_ATM_GUI(root)
    root.after(1000, func=run.update_clock)  # her 1 sn de bir function i calistirir)
    root.mainloop()
