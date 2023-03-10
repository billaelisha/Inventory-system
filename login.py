from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
conn = sqlite3.connect(database=r"IMS.db")
curr = conn.cursor()
class Login_System:

    def __init__(self,root):
        self.root = root
        self.root.title('Login System | Developed by Billa')
        self.root.geometry('1350x700+0+0')
        self.root.config(bg="#fafafa")
        
        self.otp = ""
        
        # ============== images ============
        self.phone_image = Image.open(r'images\phone1.jpg')
        self.phone_image = self.phone_image.resize((400,600),Image.ANTIALIAS)
        self.phone_image = ImageTk.PhotoImage(self.phone_image)
        self.lbl_phone_image = Label(self.root,image=self.phone_image,bd=0).place(x=150,y=70)
        
        
        #===========login frame================
        #-----user variables --------------------------------
        self.employee_id = StringVar()
        self.password = StringVar()
        login_frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=620,y=70,width=350,height=460)
        
        title = Label(login_frame,text="Login System",font=('Elephant',30,"bold"),bg='white')
        title.place(x=0,y=30,relwidth=1)
        
        lbl_username = Label(login_frame,text="Employee ID",font=('Amdalus',15),bg='white',fg='#767171')
        lbl_username.place(x=50,y=100)
        
        
        txt_username = Entry(login_frame,textvariable=self.employee_id,font=('times new roman',15),bg='#ECECEC')
        txt_username.place(x=50,y=140,width=250 )
        
        lbl_password = Label(login_frame,text="Password",font=('Amdalus',15),bg='white',fg='#767171')
        lbl_password.place(x=50,y=180)
        txt_password = Entry(login_frame,textvariable=self.password,show="*",font=('times new roman',15),bg='#ECECEC')
        txt_password.place(x=50,y=220,width=250 )
        
        
        btn_login = Button(login_frame,command=self.login,text = "Log In",font=('times new roman',15),bg='#00B0F0',activebackground="#00B0F0",fg="white",activeforeground="white",cursor='hand2')
        btn_login.place(x=50,y=280,width=240,height=35)
        
        hr = Label(login_frame,bg="lightgrey").place(x=50,y=340,width=240,height=2)
        or_ = Label(login_frame,text='OR',fg='lightgrey',bg="White",font=("times new roman",15,"bold")).place(x=150,y=325,)
        
        btn_forgetpass = Button(login_frame,text = "Forgt Passwor?",command=self.forget_window,font=('times new roman',13),bg='white',bd=0,activebackground="white",activeforeground="#00759E",fg = "#00759E",cursor='hand2')
        btn_forgetpass.place(x=50,y=380,width=240,height=35)
        
        #=======frame 2 =========
        register_frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=620,y=550,width=350,height=60)
        
        lbl_dont_have = Label(register_frame,text="Don't have an acount?",font=('times new roman',15),bg='white')
        lbl_dont_have.place(x=40,y=15)
        btn_signup = Button(register_frame,text = "SignUp",font=('times new roman',13,'bold'),bg='white',bd=0,activebackground="white",activeforeground="#00759E",fg = "#00759E",cursor='hand2')
        btn_signup.place(x=220,y=15)
        
        
        #===============animation images =============================
        self.im1 = Image.open(r'images\animation1.jpeg')
        self.im2 = Image.open(r'images\animation2.jpg')
        self.im3 = Image.open(r'images\animation3.jpg')
        self.im1 = ImageTk.PhotoImage(self.im1)
        
        self.im2 = ImageTk.PhotoImage(self.im2)
        self.im3 = ImageTk.PhotoImage(self.im3)
        
        self.lbl_change_image = Label(self.root,bd=0,bg='white')
        self.lbl_change_image.place(x=239,y=161,width=222,height=418)
        
        self.animate()
        
    
    # a=================== all functions =================
    def animate(self):
        self.im =self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)
    
    
    def login(self):
        conn = sqlite3.connect(database=r"IMS.db")
        curr = conn.cursor()
        try:
            if self.employee_id.get()=='' or self.password=='':
                messagebox.showerror("Error","Please all fields are required",parent=self.root)
            else:
                curr.execute("select utype from employee where eid=? and pass = ?",(self.employee_id.get(),self.password.get(),))
                user = curr.fetchone()
                if user == None:
                     messagebox.showerror("Error","Invalid employee ID | Password ",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("Python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("Python billing.py")
                   
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
    
    def forget_window(self):
        conn = sqlite3.connect(database=r"IMS.db")
        curr = conn.cursor()
        try:
            if self.employee_id.get() == "" :
                messagebox.showerror("Error"," Employee ID is required ")
            else :
                curr.execute("SELECT email FROM employee WHERE eid=?",(self.employee_id.get(),))
                email =curr.fetchone()
                if email == None:
                    messagebox.showerror("Error","Invalid Employee ID try again",parent =self.root)
                else:
                    # ========forget window=========
                    # variables
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()
                    # call send email function()
                    chk = self.send_email(email[0])
                    if chk == "f":
                        messagebox.showerror("Error","Connection error try again",parent=self.root)
                    else:
                        self.forget_win = Toplevel(self.root)
                        self.forget_win.title("RESET PASSWORD")
                        self.forget_win.geometry("400x350+500+100")
                        self.forget_win.focus_force()
                    
                        title = Label(self.forget_win, text="Reset Password",font=("times new roman",15,"bold"),bg="#3f51b5",fg="white")
                        title.pack(side=TOP,fill=X)
                    
                        lbl_reset = Label(self.forget_win, text="Enter the OTP sent to your Registered Email",font=("times new roman",15,))
                        lbl_reset.place(x=20,y=60)
                        txt_reset = Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15 ), bg="lightyellow")
                        txt_reset.place(x=20,y=100,width=250,height=30)
                    
                        self.btn_reset = Button(self.forget_win,text="Confirm",command=self.validate_otp,font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)
                    
                        lbl_new_pass = Label(self.forget_win, text="New Password ",font=("times new roman",15,))
                        lbl_new_pass.place(x=20,y=160)
                        txt_new_pass = Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15 ), bg="lightyellow")
                        txt_new_pass.place(x=20,y=190,width=250,height=30)
                    
                        lbl_conf_pass = Label(self.forget_win, text="Confirm Password",font=("times new roman",15,))
                        lbl_conf_pass.place(x=20,y=225)
                        txt_conf_pass = Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15 ), bg="lightyellow")
                        txt_conf_pass.place(x=20,y=255,width=250,height=30)
                    
                        self.btn_update = Button(self.forget_win,text="Submit",command=self.update_password,state=DISABLED,font=("times new roman",15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)
                    
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent = self.root)
            
    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent = self.forget_win)
        elif self.var_new_pass.get()!= self.var_conf_pass.get():
            messagebox.ABORT("Error","New Password and confirmed password should be the same",parent = self.forget_win)
        else:
            conn = sqlite3.connect(database=r"IMS.db")
            curr = conn.cursor()
            try:
                curr.execute("UPDATE employee SET pass=? where eid = ?",(self.var_new_pass.get(),self.employee_id.get(),))
                conn.commit()
                messagebox.showinfo("Success","Passwords updated successfully",parent =self.forget_win)
                self.forget_win.destroy()
            
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
    
            
    def validate_otp(self):
        if int(self.otp)== int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP try again",parent=self.forget_win)
        
    def send_email(self,to_):
        s =smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        email_ = email_pass.email_
        pass_ = email_pass.pass_
        
        s.login(email_,pass_)
        
        self.otp =int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        subj = "IMS Reset Password OTP"
        msg =f"Dir Sir/Madam,\n\nYour reset OTP is {self.otp}\n\n With regards\nIMS Team"
        msg ="Subject :{}\n\n{}".format(subj,msg)
    
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return "f"
    
    
root = Tk()
ob = Login_System(root)
root.mainloop()