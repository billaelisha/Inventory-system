from tkinter import *
from PIL import Image, ImageTk
import sqlite3 
from tkinter import ttk,messagebox
class categoryClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventor Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        # ==== variables =================================
        self.var_cat_id = StringVar()
        self.var_name = StringVar()
        
        # ======= title============
        lbl_title = Label(self.root,text="Manage Product Category", font=("goudy old style",30),bd=3,relief=RIDGE,bg="#FF9900",fg="white")
        lbl_title.pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_name = Label(self.root,text="Enter Product Name", font=("goudy old style",30),bg="white")
        lbl_name.place(x=50,y=100)

        text_name = Entry(self.root,textvariable=self.var_name ,font=("goudy old style",18), bg="lightyellow")
        text_name.place(x=50,y=170,width=300)
        
        btn_add = Button(self.root,text="ADD",command=self.add,font=("goudy old style",15), bg="black",fg="gold",cursor="hand2")
        btn_add.place(x=360,y=170,width=150,height=30)
        
        btn_delete = Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15), bg="red",fg="gold",cursor="hand2")
        btn_delete.place(x=520,y=170,width=150,height=30)
        
        # =======Category Details =================================================================
        cat_frame = Frame(self.root,bd=5,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)
        
        scrolly = Scrollbar(cat_frame,orient=VERTICAL)
        scrollx = Scrollbar(cat_frame,orient=HORIZONTAL)
        
        self.categoryTable = ttk.Treeview(cat_frame,columns=("cid", "name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set )
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)
        self.categoryTable.heading("cid",text=" C ID")
        self.categoryTable.heading("name",text="Name")
        self.categoryTable["show"]="headings"
        self.categoryTable.column("cid",width=100)
        self.categoryTable.column("name",width=100)
        self.categoryTable.pack(fill=BOTH,expand=1)
        self.categoryTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        # =====images===============
        self.img1 = Image.open(r"images\beans1.png")
        self.img1 = self.img1.resize((500,250),Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.lbl_img1 = Label(self.root,image=self.img1,bd=2,relief= RAISED)
        self.lbl_img1.place(x=50,y=220)
        
        self.img2 = Image.open(r"images\war2.png")
        self.img2 = self.img2.resize((500,250),Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        self.lbl_img2 = Label(self.root,image=self.img2,bd=2,relief= RAISED)
        self.lbl_img2.place(x=580,y=220)
        # =============functions =================
    def add(self):
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category name is required",parent =self.root)
            else:
                cur.execute("select * from category where name=?",(self.var_name.get(),))
                row = cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This  Category name is already present try different one",parent =self.root)
                else:
                    cur.execute("INSERT INTO category(name) values(?)",(self.var_name.get(),))
                    conn.commit()
                    messagebox.showinfo("Success","Category name is added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
            
    def show(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchone()
            print(rows)
            
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
                  
        
    def get_data(self,ev):
        f = self.categoryTable.focus()
        content = (self.categoryTable.item(f))
        row = content["values"]
        # print(row)
        self.var_cat_id.set(row[0]),
        self.var_name.set(row[1]),    
     
    def delete(self):
        conn = sqlite3.connect(database=r"IMS.db")
        cur = conn.cursor()
        try:
            if self.var_cat_id.get()=="":
               messagebox.showerror("Error","Please select Category from the list",parent =self.root)
            else:
                cur.execute("select * from category where cid=?",(self.var_cat_id.get(),))
                row = cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, please try again.",parent =self.root)
                else: 
                    op = messagebox.askyesno("Comfirm","Do you really want to delete?")
                    if op ==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete","Category deleted successfully",parent =self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
                
if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()