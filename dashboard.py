from tkinter import *
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3 
from tkinter import messagebox
import os
import time

class IMS:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventor Management System")
        self.root.config(bg="white")
        #  === THE TITLE SECTION==============
        self.icon_image = Image.open("images\R.jpg")
        self.icon_image=self.icon_image.resize((70,69),Image.ANTIALIAS)
        self.icon_image = ImageTk.PhotoImage(self.icon_image)
        title = Label(self.root,text="Inventor Management System",image= self.icon_image,compound=LEFT,font=("times new roman",40,"bold"),bg="#FF9900",fg="#FFFFFF",anchor="w")
        
        title.place(x=0,y=0,relwidth=1,height=70)
        
        # =====logout button =====
        btn_log_out_Button= Button(self.root, text="logout",command=self.logout,font=("arial",15,"bold"),bg="black",fg="gold",cursor="hand2")
        btn_log_out_Button.place(x=1210,y=13,width=100)
        # ===clocks =====
        self.lbl_clock = Label(self.root,text="Wellcome To Inventor Management System\t\tDate:DD-MM-YYYY\t\tTime: HH-MM-SS",font=("times new roman",15,"bold"),bg="#FF0000",fg="#FFFFFF")
        self.lbl_clock.place(x=0,relwidth=1,y=70,height=30)
        # ======lEFT MUNU========
        self.menu_logo_icon= Image.open(r"images\logo2.jpeg" )
        self.menu_logo_icon = self.menu_logo_icon.resize((200,200),Image.ANTIALIAS)
        self.menu_logo_icon = ImageTk.PhotoImage(self.menu_logo_icon)
        left_menu_frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        left_menu_frame.place(x=0,y=100,width=200,height=565)
        lbl_menu_logo =Label(left_menu_frame,image=self.menu_logo_icon)
        lbl_menu_logo.pack(side=TOP,fill=X)
        
        lbl_menu= Label(left_menu_frame, text="Menu",font=("arial",15),bg="#FF9900",fg="black")
        lbl_menu.pack(side=TOP,fill=X)
        
        btn_employee= Button(left_menu_frame,command=self.employee ,text="Employee",font=("arial",15),bg="white",fg="black",cursor="hand2",bd=3)
        btn_employee.pack(side=TOP,fill=X)
        btn_supplier= Button(left_menu_frame, command=self.supplier,text="Supplier",font=("arial",15),bg="white",fg="black",cursor="hand2",bd=3)
        btn_supplier.pack(side=TOP,fill=X)
        btn_category= Button(left_menu_frame, text="Category",command=self.category,font=("arial",15),bg="white",fg="black",cursor="hand2",bd=3)
        btn_category.pack(side=TOP,fill=X)
        btn_product= Button(left_menu_frame, text="Product",command=self.product,font=("arial",15),bg="white",fg="black",cursor="hand2",bd=3)
        btn_product.pack(side=TOP,fill=X)
        btn_sales= Button(left_menu_frame, text="Sales",command=self.sales,font=("arial",15),bg="white",fg="black",cursor="hand2",bd=3)
        btn_sales.pack(side=TOP,fill=X)
        btn_exit= Button(left_menu_frame, text="Exit",font=("arial",15),bg="white",fg="black",cursor="hand2",bd=3)
        btn_exit.pack(side=TOP,fill=X)
        
        # =====content-=========
        self.lbl_employee = Label(self.root, text="Total Employee\n[0]",bd=5,relief=RIDGE,bg="#FF9900",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)
        
        self.lbl_supplier = Label(self.root, text="Total Suppliers\n[0]",bd=5,relief=RIDGE,bg="#FF9900",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)
        
        self.lbl_category = Label(self.root, text="Total Category\n[0]",bd=5,relief=RIDGE,bg="#FF9900",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)
        
        self.lbl_product = Label(self.root, text="Total Product\n[0]",bd=5,relief=RIDGE,bg="#FF9900",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)
        
        self.lbl_sales = Label(self.root, text="Total Sales\n[0]",bd=5,relief=RIDGE,bg="#FF9900",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)
        
        # === footer =====
        self.lbl_footer = Label(self.root,text="IMS Inventory Management System | Develop by Billa\nFor Any Technical Issue Contact 0548947033",font=("times new roman",12,"bold"),bg="#FF0000",fg="#FFFFFF")
        self.lbl_footer.pack(side=BOTTOM,fill=X)
        
        self.update_content()
    # ===================================================================
    def employee(self):
        self.new_window = Toplevel(self.root)
        self.new_obj =employeeClass(self.new_window)
        
    def supplier(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_window)
        
    def category(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_window)
    
    def product(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = productClass(self.new_window)
        
    def sales(self):
        self.new_window = Toplevel(self.root)
        self.new_obj = salesClass(self.new_window)
        
    def update_content(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[{str(len(product))}]")
            
            cur.execute("SELECT * FROM supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n[{str(len(supplier))}]")
            
            cur.execute("SELECT * FROM category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[{str(len(category))}]")
            
            cur.execute("SELECT * FROM employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n\n[{str(len(employee))}]")
            bill =len(os.listdir('bill'))
            self.lbl_sales.config(text=f"Total Sales\n[{str(bill)}]")
            
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Wellcome To Inventor Management System\t\tDate:{str(date_)}\t\tTime: {str(time_)}",)
            self.lbl_clock.after(200,self.update_content)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
         
    def logout(self):
        self.root.destroy() 
        os.system("Python login.py")  
            
            
            
            
if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
      
    
