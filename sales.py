from tkinter import *
from PIL import Image, ImageTk
import sqlite3 
from tkinter import ttk,messagebox
import os
class salesClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventor Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        # ===variable =========
        self.bill_list = []
        self.var_invoice = StringVar()
        
         # ======== title ========
        lbl_title = Label(self.root,text="View Customer Bills", font=("goudy old style",30),bd=3,relief=RIDGE,bg="#FF9900",fg="white")
        lbl_title.pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_invoice = Label(self.root,text="Invoice No. ", font=("times new roman",15),bg="white")
        lbl_invoice.place(x=50,y=100)
        txt_invoice = Entry(self.root,textvariable = self.var_invoice,font=("times new roman",15),bg="lightyellow")
        txt_invoice.place(x=160,y=100,width=180)
        
        btn_search = Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg='black',fg="gold",cursor="hand2")
        btn_search.place(x=360,y=100,width=120,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="#FFFF00",fg="black",cursor="hand2")
        btn_clear.place(x=490,y=100,width=120,height=28)
        
        # ==== BILL LIST =================================
        sales_frame = Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=140,width=200,height=330)
        
        scrolly =Scrollbar(sales_frame,orient=VERTICAL)
        self.sales_list = Listbox(sales_frame, font=("guody old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH,expand= 1)
        self.sales_list.bind("<ButtonRelease-1>",self.get_data)
        
        # ==== BILL AREA =================================
        bill_frame = Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=280,y=140,width=410,height=330)
        
        lbl_title2 = Label(bill_frame,text=" Customer Bills Area", font=("goudy old style",20),bg="orange")
        lbl_title2.pack(side=TOP,fill=X)
        
        
        scrolly2 =Scrollbar(bill_frame,orient=VERTICAL)
        self.bill_area = Text(bill_frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand= 1)
        
        #  =====image =====
        self.bill_photo = Image.open(r"images\bill.jpeg")
        self.bill_photo = self.bill_photo.resize((450,360),Image.ANTIALIAS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
        lbl_image =Label(self.root, image=self.bill_photo,bd=0)
        lbl_image.place(x=700,y=110)
        self.show()
    # ==========================================================
    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0,END)
        # print(os.listdir("bill"))
        for i in os.listdir("bill"):
            # print(i.split('.'),i.split(".")[-1])
            if i.split('.')[-1] =="txt":
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])
                
    def get_data(self,ev):
        index_ = self.sales_list.curselection()
        file_name = self.sales_list.get(index_)
        self.bill_area.delete("1.0",END)
        fp = open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
            
        fp.close()
        
    def search(self,):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. is required",parent = self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f'bill/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
            else:
                messagebox.showerror("Error","Invalid Invoice No.",parent = self.root)
                    
        fp.close()
    
    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)
        
        
        
            
if __name__ == "__main__":       
    root = Tk()
    obj = salesClass(root)
    root.mainloop()