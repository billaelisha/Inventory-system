from tkinter import *
from PIL import Image, ImageTk
import sqlite3 
from tkinter import ttk,messagebox
class productClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventor Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        #  variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()
        
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        
        product_frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_frame.place(x=10,y=10,width=450,height=480)
        
        # ======== title ========
        title = Label(product_frame,text=" Manage Product Details", font=("goudy old style",15),bd=2,relief=RIDGE,bg="#FF9900",fg="white")
        title.pack(side=TOP,fill=X)
        #  =====column1 =====
        lbl_category = Label(product_frame,text="Category", font=("goudy old style",15),bd=2,bg="white")
        lbl_category.place(x=30,y=60)
        lbl_supplier = Label(product_frame,text="Supplier", font=("goudy old style",15),bd=2,bg="white")
        lbl_supplier.place(x=30,y=110)
        lbl_product_name = Label(product_frame,text="Name", font=("goudy old style",15),bd=2,bg="white")
        lbl_product_name.place(x=30,y=160)
        lbl_price = Label(product_frame,text="Price", font=("goudy old style",15),bd=2,bg="white")
        lbl_price.place(x=30,y=210)
        lbl_quantity = Label(product_frame,text="Quantity", font=("goudy old style",15),bd=2,bg="white")
        lbl_quantity.place(x=30,y=260)
        lbl_status = Label(product_frame,text="Status", font=("goudy old style",15),bd=2,bg="white")
        lbl_status.place(x=30,y=310)
        
        #  =====column2 =====
        cmb_cat = ttk.Combobox(product_frame,textvariable=self.var_cat,values=self.cat_list,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)
        
        cmb_sup = ttk.Combobox(product_frame,textvariable=self.var_sup,values=self.sup_list,state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)
        
        txt_name = Entry(product_frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow")
        txt_name.place(x=150,y=160,width=200)
        txt_price = Entry(product_frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow")
        txt_price.place(x=150,y=210,width=200)
        txt_qty = Entry(product_frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow")
        txt_qty.place(x=150,y=260,width=200)
        
        cmb_status = ttk.Combobox(product_frame,textvariable=self.var_status,values=("Active","Inactive"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)
        
        #  ===== buttons======
        btn_add=Button(product_frame,text="Save",command=self.add,cursor="hand2",font=("goudy old style",15),bg="#66FF00",fg="black")
        btn_add.place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_frame,text="Update",command=self.update,cursor="hand2",font=("goudy old style",15),bg="#9900ff",fg="black")
        btn_update.place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_frame,text="Delete",command=self.delete,cursor="hand2",font=("goudy old style",15),bg="#FF0000",fg="black")
        btn_delete.place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_frame,text="Clear",command=self.clear,cursor="hand2",font=("goudy old style",15),bg="#FFFF00",fg="black")
        btn_clear.place(x=340,y=400,width=100,height=40)
        
        # ===== search frame =====
        search_frame = LabelFrame(self.root, text="Search Employee",bg="white",font=("goudy old style",12,"bold"))
        search_frame.place(x=480,y=10,width=600,height=80)
        
        # -----options --------------------------------
        cmb_search = ttk.Combobox(search_frame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        
        txt_search=Entry(search_frame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow")
        txt_search.place(x=200,y=10)
        btn_search=Button(search_frame,text="search",command=self.search,cursor="hand2",font=("goudy old style",15),bg="black",fg="gold")
        btn_search.place(x=410,y=9,width=150,height=30)
        
        
         # =======Products Details =================================================================
        p_frame = Frame(self.root,bd=5,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)
        
        scrolly = Scrollbar(p_frame,orient=VERTICAL)
        scrollx = Scrollbar(p_frame,orient=HORIZONTAL)
        
        self.ProductTable = ttk.Treeview(p_frame,columns=("pid", "Supplier", "Category", "name", "price", "qty", "status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set )
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid",text="P ID")
        self.ProductTable.heading("Category",text="Category")
        self.ProductTable.heading("Supplier",text="Supplier")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Qty")
        self.ProductTable.heading("status",text="Status")
        self.ProductTable["show"]="headings"
        
        
        self.ProductTable.column("pid",width=100)
        self.ProductTable.column("Category",width=100)
        self.ProductTable.column("Supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=100)
        self.ProductTable.column("status",width=100)
        
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
   
        # =================================================================
        
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            cur.execute("select name from category")
            cat = cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute("select name from supplier")
            sup = cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
                
            
            
            
            
                
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
        
        
    def add(self):
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","All fields are required",parent =self.root)
            else:
                cur.execute("select * from product where name=?",(self.var_name.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already present try different one",parent =self.root)
                else:
                    cur.execute("INSERT INTO product( Category, Supplier, name, price, qty, status) values(?,?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Product added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
        
    def show(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
               
        
    def get_data(self,ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content["values"]
        self.var_pid.set(row[0]),
        self.var_sup.set(row[1]),
        self.var_cat.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6]),
        
        
    def update(self):
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from the list",parent =self.root)
            else:
                cur.execute("select * from product where pid=?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product id",parent =self.root)
                else:
                    cur.execute("UPDATE product SET Category=?, Supplier=?, name=?, price=?,qty=?, status=? WHERE pid=?",(
                        
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get(),
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Product updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
            
            
            
    def delete(self):
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            if self.var_pid.get()=="":
               messagebox.showerror("Error","Select product from the list",parent =self.root)
            else:
                cur.execute("select * from product where pid=?",(self.var_pid.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product ",parent =self.root)
                else: 
                    op = messagebox.askyesno("Comfirm","Do you really want to delete?")
                    if op ==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete","Product deleted successfully",parent =self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
            
        
    def clear(self):
        self.var_cat.set("Select"),
        self.var_sup.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set(""),                
        self.var_searchtxt.set(""),
        self.var_searchby.set("Select"),
        self.show()
        
    def search(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        
        try:
            if self.var_searchby.get()=="Select":
               messagebox.showerror("Error","Select searchby option",parent =self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input is required",parent =self.root) 
            else:
                cur.execute("SELECT * FROM product WHERE "+self.var_searchby.get()+" LIKE '%"+ self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.EmployeeTable.get_children()) 
                    for row in rows:
                        self.ProductTable.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent =self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
               
        
        
if __name__ == "__main__":       
    root = Tk()
    obj = productClass(root)
    root.mainloop()