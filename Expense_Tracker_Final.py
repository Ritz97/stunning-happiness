#=====================================EXPENSE TRACKER===================================================================


#=====================================IMPORT PACKAGES===================================================================
from tkinter import *
from tkinter import messagebox
import mysql.connector, sys


#===========================================CLASS DECLARATION===========================================================
class expense:


    #======================================CONSTRUCTOR==================================================================
    def __init__(self):

        try:
            self.conn = mysql.connector.connect(user="root", password="", host="localhost", database="expense")
            self.mycursor = self.conn.cursor()

        except:
            messagebox.showerror("Restricted access", "You are accessing a database which does not exist")
            sys.exit()

        self.is_logged_in = 0
        self.gui_1()


    #============================================================REGISTRATION===========================================
    def register(self, name, email, password, conf):

        if password!="" and password==conf and name!="" and email!="":
            self.mycursor.execute("""SELECT * FROM `details` 
                    WHERE `email` LIKE '%s' AND `password` LIKE '%s'"""
                                  % (email, password))
            user_list = self.mycursor.fetchall()
            counter = 0
            for i in user_list:
                counter += 1

            if counter==1:
                messagebox.showerror("Already registered", "You are already registered")

            else:
                self.mycursor.execute("""INSERT INTO `details` (`name`, `email`, `password`, `balance`)
                VALUES ('%s', '%s', '%s', '%d')"""
                %(name,email,password,0))
                self.conn.commit()
                messagebox.showinfo("Congratulations", "You are successfully registered")

        elif password!="" and password!=conf and name!="" and email!="":
            messagebox.showerror("Invalid details", "Password did not match")

        else:
            messagebox.showerror("Invalid details", "Enter all details")


    #====================================================================LOGIN==========================================
    def login(self, root, email_for_login, password_for_login):

        self.mycursor.execute("""SELECT * FROM `details` 
        WHERE `email` LIKE '%s' AND `password` LIKE '%s'"""
                              %(email_for_login, password_for_login))
        user_list=self.mycursor.fetchall()
        counter=0
        for i in user_list:
            counter+=1

        if counter==1:
            self.is_logged_in=1
            root.destroy()
            self.gui_2(email_for_login, password_for_login)

        else:
            messagebox.showerror("Incorrect credentials", "Incorrect email/password")


    #======================================================================SHOW BALANCE=================================
    def showbalance(self, root2, email_for_login, password_for_login):

        if self.is_logged_in==1:
            self.mycursor.execute("""SELECT * FROM `details` 
            WHERE `email` LIKE '%s' AND `password` LIKE '%s'"""
                              %(email_for_login, password_for_login))
            user_list=self.mycursor.fetchall()
            for i in user_list:
                s=i[0]+', your balance is Rs. '+str(i[3])
            return s

        else:
            messagebox.showerror("Invalid credentials", "You are not logged in")
            root2.destroy()


    #========================================================MAKE TRANSACTION===========================================
    def trans(self, type, amount, remarks, root3, email_for_login, password_for_login):

        if self.is_logged_in==1:
            self.mycursor.execute("""SELECT * FROM `details` 
        WHERE `email` LIKE '%s' AND `password` LIKE '%s'"""
                              %(email_for_login, password_for_login))
            user_list=self.mycursor.fetchall()
            for i in user_list:
                user_id=i[1]
                balance=i[3]

            if type!="" and amount!="":
                if type=='Debit' or type=='Credit':
                    self.mycursor.execute("""INSERT INTO `transactions` (`email`, `transaction_type`, `amount`, `remarks`) 
                                VALUES ('%s', '%s', '%d', '%s')"""
                                          % (user_id, type, int(amount), remarks))
                    self.conn.commit()
                    if type=='Debit':
                        self.mycursor.execute("""UPDATE `details` SET `balance`='%d' WHERE `email` LIKE '%s'"""%(balance-int(amount), user_id))
                        self.conn.commit()

                    elif type=='Credit':
                        self.mycursor.execute("""UPDATE `details` SET `balance`='%d' WHERE `email` LIKE '%s'"""%(balance+int(amount), user_id))
                        self.conn.commit()

                    messagebox.showinfo("Transaction recorded", "Your transaction has been successfully recorded")
                    root3.destroy()
                    self.gui_2(email_for_login, password_for_login)

                else:
                    messagebox.showerror("Invalid credentials", "Please enter proper transaction type (Debit/Credit)")

            else:
                messagebox.showerror("Invalid Credentials", "Enter all details. Remarks are optional.")

        else:
            messagebox.showerror("Invalid credentials", "You are not logged in")
            root3.destroy()


    #=============================================GO BACK TO WELCOME USER SCREEN========================================
    def goback(self, root2, root3or4, email_for_login, password_for_login):

        root3or4.destroy()
        self.gui_2(email_for_login, password_for_login)


    #================================================LOGOUT=============================================================
    def logout(self, root2):

        self.is_logged_in = 0
        messagebox.showinfo("Logged out", "You have successfully logged out")
        root2.destroy()
        self.gui_1()


    #======================================WELCOME SCREEN WITH LOGIN AND REGISTER OPTIONS===============================
    def gui_1(self):

        root=Tk()
        root.minsize("1366", "768")
        root.maxsize("1366", "768")
        root.title("EXPENSE TRACKER")

        f1 = Frame(root)
        l1 = Label(f1, text="EXPENSE TRACKER", font=('arial', 70, 'bold'), bg="Maroon", fg="White", padx=224, pady=10)
        l1.pack()
        f1.pack()

        f2 = Frame(root, pady=35)

        f21 = Frame(f2, pady=10)
        l21 = Label(f21, text="EMAIL ID:", font=('arial', 20), pady=5)
        l22 = Label(f21, text="PASSWORD:", font=('arial', 20), pady=5)
        e21 = Entry(f21)
        e22 = Entry(f21, show="*")
        l21.grid(row=0, column=0)
        e21.grid(row=0, column=1)
        l22.grid(row=1, column=0)
        e22.grid(row=1, column=1)
        f21.pack()

        f22 = Frame(f2)
        b2 = Button(f2, text="LOGIN", pady=5, command=lambda : self.login(root, e21.get(), e22.get()))
        b2.pack()
        f22.pack()

        f2.pack()

        f3 = Frame(root, pady=35)

        f31 = Frame(f3, pady=10)
        l31 = Label(f31, text="NAME:", font=('arial', 20), pady=5)
        l32 = Label(f31, text="EMAIL ID:", font=('arial', 20), pady=5)
        l33 = Label(f31, text="PASSWORD:", font=('arial', 20), pady=5)
        l34 = Label(f31, text="CONFIRM PASSWORD:", font=('arial', 20), pady=5)
        e31 = Entry(f31)
        e32 = Entry(f31)
        e33 = Entry(f31, show="*")
        e34 = Entry(f31, show="*")
        l31.grid(row=0, column=0)
        e31.grid(row=0, column=1)
        l32.grid(row=1, column=0)
        e32.grid(row=1, column=1)
        l33.grid(row=2, column=0)
        e33.grid(row=2, column=1)
        l34.grid(row=3, column=0)
        e34.grid(row=3, column=1)
        f31.pack()

        f32 = Frame(f3)
        b3 = Button(f32, text="REGISTER", pady=5,
                    command=lambda : self.register(e31.get(), e32.get(), e33.get(), e34.get()))
        b3.pack()
        f32.pack()

        f3.pack()

        root.mainloop()


    #===============================================AFTER LOGGED IN SCREEN==============================================
    def gui_2(self, email_for_login, password_for_login):

        root2=Tk()
        root2.minsize("1366", "768")
        root2.maxsize("1366", "768")
        root2.title("WELCOME USER")

        f1 = Frame(root2)
        l1 = Label(f1, text="EXPENSE TRACKER", font=('arial', 70, 'bold'), bg="Maroon", fg="White", padx=224, pady=10)
        l1.pack()
        f1.pack()

        f2 = Frame(root2, pady=35)
        l2=Label(f2, text=self.showbalance(root2, email_for_login, password_for_login), font=('arial', 20), pady=10)
        b21=Button(f2, text="Record a transaction", font=('arial', 20), command=lambda : self.gui_3(root2, email_for_login, password_for_login))
        b22 = Button(f2, text="Show your previous transactions", font=('arial', 20), command=lambda : self.gui_4(root2, email_for_login, password_for_login))
        b23 = Button(f2, text="Logout", font=('arial', 20), command=lambda : self.logout(root2))
        l2.pack()
        b21.pack(pady=10)
        b22.pack(pady=10)
        b23.pack(pady=10)
        f2.pack()

        root2.mainloop()


    #=================================================RECORD TRANSACTION SCREEN=========================================
    def gui_3(self, root2, email_for_login, password_for_login):

        root2.destroy()
        root3=Tk()
        root3.minsize("1366", "768")
        root3.maxsize("1366", "768")
        root3.title("RECORD TRANSACTION")

        f1 = Frame(root3)
        l1 = Label(f1, text="EXPENSE TRACKER", font=('arial', 70, 'bold'), bg="Maroon", fg="White", padx=224, pady=10)
        l1.pack()
        f1.pack()

        f2=Frame(root3, pady=20)
        l2 = Label(f2, text="RECORD A TRANSACTION", font=('arial', 20), pady=5)
        l2.pack()
        f2.pack()

        f3=Frame(root3, pady=35)
        l31 = Label(f3, text="Enter the type of transaction (Debit/Credit):", font=('arial', 20), padx=5, pady=5)
        e31=Entry(f3)
        l32=Label(f3, text="Enter amount:", font=('arial', 20), padx=5, pady=5)
        e32=Entry(f3)
        l33=Label(f3, text="Enter remarks (Optional):", font=('arial', 20), padx=5, pady=5)
        e33=Entry(f3)
        l31.grid(row=0, column=0)
        e31.grid(row=0, column=1)
        l32.grid(row=1, column=0)
        e32.grid(row=1, column=1)
        l33.grid(row=2, column=0)
        e33.grid(row=2, column=1)
        f3.pack()

        f4=Frame(root3, pady=35)
        b41=Button(f4, text="Record this transaction", font=('arial', 20), command=lambda : self.trans(e31.get(), e32.get(), e33.get(), root3, email_for_login, password_for_login))
        b42=Button(f4, text="Go back", font=('arial', 20), command=lambda : self.goback(root2, root3, email_for_login, password_for_login))
        b41.pack(pady=5)
        b42.pack(pady=5)
        f4.pack()

        root3.mainloop()


    #================================================PREVIOUS TRANSACTIONS SCREEN=======================================
    def gui_4(self, root2, email_for_login, password_for_login):

        if self.is_logged_in==1:
            root2.destroy()
            root4 = Tk()
            root4.minsize("1366", "768")
            root4.maxsize("1366", "768")
            root4.title("YOUR PREVIOUS TRANSACTIONS")

            f1 = Frame(root4)
            l1 = Label(f1, text="EXPENSE TRACKER", font=('arial', 70, 'bold'), bg="Maroon", fg="White", padx=224, pady=10)
            l1.pack()
            f1.pack()

            f2 = Frame(root4, pady=20)
            l2 = Label(f2, text="PREVIOUS TRANSACTIONS", font=('arial', 20), pady=5)
            l2.pack()
            f2.pack()

            f3=Frame(root4, pady=20)
            sb1 = Scrollbar(f3)
            sb2 = Scrollbar(f3, orient=HORIZONTAL)
            sb1.pack(side=RIGHT, fill=Y)
            sb2.pack(side=BOTTOM, fill=X)
            lb=Listbox(f3, width=50, font=('arial', 15), bg="gray94", yscrollcommand=sb1.set, xscrollcommand=sb2.set)
            l31=lb.insert(0, "        Type of transaction        Amount            Remarks        ")
            l32=lb.insert(1, "")
            self.mycursor.execute("""SELECT * FROM `transactions` 
                    WHERE `email` LIKE '%s'"""
                                  % (email_for_login))
            user_list = self.mycursor.fetchall()
            counter = 0
            for i in user_list:
                counter += 1

            if counter == 0:
                messagebox.showerror("Not available", "No transactions are available")

            else:
                term=0
                for i in user_list:
                    lb.insert(term+2, "                %s                     %d                 %s"%(i[1], i[2], i[3]))
                    term+=1

            lb.pack()
            sb1.config(command=lb.yview)
            sb2.config(command=lb.xview)
            f3.pack()

            f4=Frame(root4, pady=30)
            b4=Button(f4, text="Go back", font=('arial', 20), command=lambda : self.goback(root2, root4, email_for_login, password_for_login))
            b4.pack()
            f4.pack()

            root4.mainloop()

        else:
            messagebox.showerror("Invalid credentials", "You are not logged in")
            root2.destroy()


obj=expense()