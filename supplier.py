from tkinter import *
from PIL import Image, ImageTk
import sqlite3 
from tkinter import ttk,messagebox
class supplierClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventor Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        # =====================================-----
        #  all variables=========
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        
        
        
        
        
        
        # ===== search frame =====
        # search_frame = LabelFrame(self.root, text="Search Supplier",bg="white",font=("goudy old style",12,"bold"))
        # search_frame.place(x=250,y=20,width=600,height=70)
        
        # -----options --------------------------------
        lbl_search = Label(self.root,text="Invoice No. ",bg="white",font=("goudy old style",15))
        lbl_search.place(x=700,y=80)
        
        
        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow")
        txt_search.place(x=800,y=80,width=160)
        btn_search=Button(self.root,text="search",command=self.search,cursor="hand2",font=("goudy old style",15),bg="black",fg="gold")
        btn_search.place(x=980,y=79,width=100,height=28)
        
        # =======title===========
        title = Label(self.root,text="Supplier Details",font=("goudy old style",20,'bold'),bg="#FF0000",fg="gold")
        title.place(x=50,y=10,width=1000,height=40)
        
        # =======content===========
        
        #===row one======
        lbl_supplier_invoice = Label(self.root,text="Invoice No:",font=("goudy old style",15,'bold'),bg="white",fg="black")
        lbl_supplier_invoice.place(x=50,y=80)
        txt_supplier_invoice = Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15,'bold'),bg="lightyellow",fg="black")
        txt_supplier_invoice.place(x=180,y=80,width=180)
        
        
        # ====== ROW TWO =================================
        lbl_name = Label(self.root,text="Name:",font=("goudy old style",15,'bold'),bg="white",fg="black")
        lbl_name.place(x=50,y=120)
        txt_name = Entry(self.root,textvariable=self.var_name,font=("goudy old style",15,'bold'),bg="lightyellow",fg="black")
        txt_name.place(x=180,y=120,width=180)
        
        #====third row====
        lbl_contact = Label(self.root,text="Contact:",font=("goudy old style",15,'bold'),bg="white",fg="black")
        lbl_contact.place(x=50,y=160)
        txt_contact = Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15,'bold'),bg="lightyellow",fg="black")
        txt_contact.place(x=180,y=160,width=180)
        
        
        
         #====row 4====
        lbl_desc = Label(self.root,text="Description:",font=("goudy old style",15,'bold'),bg="white",fg="black")
        lbl_desc.place(x=50,y=200)
        self.txt_desc = Text(self.root,font=("goudy old style",15,'bold'),bg="lightyellow",fg="black")
        self.txt_desc.place(x=180,y=200,width=470,height=120)
       
        
        #====== buttons =================================
        btn_add=Button(self.root,text="Save",command=self.add,cursor="hand2",font=("goudy old style",15),bg="#66FF00",fg="black")
        btn_add.place(x=180,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,cursor="hand2",font=("goudy old style",15),bg="#9900ff",fg="black")
        btn_update.place(x=300,y=370,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,cursor="hand2",font=("goudy old style",15),bg="#FF0000",fg="black")
        btn_delete.place(x=420,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,cursor="hand2",font=("goudy old style",15),bg="#FFFF00",fg="black")
        btn_clear.place(x=540,y=370,width=110,height=35)
        
        
        
        # =======Employee Details =================================================================
        emp_frame = Frame(self.root,bd=5,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=350)
        
        scrolly = Scrollbar(emp_frame,orient=VERTICAL)
        scrollx = Scrollbar(emp_frame,orient=HORIZONTAL)
        
        self.supplierTable = ttk.Treeview(emp_frame,columns=("invoice", "name", "contact", "desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set )
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        self.supplierTable.heading("invoice",text="Invoice NO.")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")
        self.supplierTable["show"]="headings"
        self.supplierTable.column("invoice",width=100)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
        
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
# =================================================================
    def add(self):
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice is required",parent =self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This  invoice no. is already asigned try different one",parent =self.root)
                else:
                    cur.execute("INSERT INTO supplier(invoice, name, contact, desc) values(?,?,?,?)",(
                        self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get("1.0",END),
                        
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Supplier added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
        
    def show(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
               
        
    def get_data(self,ev):
        f = self.supplierTable.focus()
        content = (self.supplierTable.item(f))
        row = content["values"]
        # print(row)
        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete("1.0",END),
        self.txt_desc.insert(END,row[3]),
        
        
    def update(self):
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Supplier invoice no. is required",parent =self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid invoice no.",parent =self.root)
                else:
                    cur.execute("UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?",(
                        
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get("1.0",END),
                        self.var_sup_invoice.get(),
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Supplier updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
            
            
            
    def delete(self):
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            if self.var_sup_invoice.get()=="":
               messagebox.showerror("Error","Supplier invoice is required",parent =self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Supplier no.",parent =self.root)
                else: 
                    op = messagebox.askyesno("Comfirm","Do you really want to delete?")
                    if op ==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete","Supplier deleted successfully",parent =self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
            
        
    def clear(self):
        self.var_sup_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),
        self.txt_desc.delete("1.0",END),
        self.var_searchtxt.set(""),
        self.show()
        
    def search(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice no. is required",parent =self.root) 
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?",(self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children()) 
                    self.supplierTable.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent =self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
               
               
        
    
         
if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
      