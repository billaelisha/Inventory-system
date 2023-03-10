from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import time
import sqlite3
import os
import tempfile


class billing:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventor Management System")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print =0
        #  === THE TITLE SECTION==============
        self.icon_image = Image.open("images\R.jpg")
        self.icon_image=self.icon_image.resize((70,69),Image.ANTIALIAS)
        self.icon_image = ImageTk.PhotoImage(self.icon_image)
        title = Label(self.root,text="Inventor Management System",image= self.icon_image,compound=LEFT,font=("times new roman",40,"bold"),bg="#FF9900",fg="#FFFFFF",anchor="w")
        
        title.place(x=0,y=0,relwidth=1,height=70)
        
        # =====logout button =====
        log_out_Button= Button(self.root,command=self.logout, text="logout",font=("arial",15,"bold"),bg="black",fg="gold",cursor="hand2")
        log_out_Button.place(x=1210,y=13,width=100)
        # ===clocks =====
        self.lbl_clock = Label(self.root,text="Wellcome To Inventor Management System\t\tDate:DD-MM-YYYY\t\tTime: HH-MM-SS",font=("times new roman",15,"bold"),bg="#FF0000",fg="#FFFFFF")
        self.lbl_clock.place(x=0,relwidth=1,y=70,height=30)
        
        # ======PRODUCT FRAMES ======
            #variables
        
        ProductFrame1 = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,height=550,width=410)
        
        # =======product title ======
        pTitle = Label(ProductFrame1,text="All products",font=("goudy old style",20,'bold'),bg="#262626",fg="white")
        pTitle.pack(side=TOP,fill=X)
        
        # ===========product search frame================
        self.var_search = StringVar()
        ProductFrame2 = Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,height=90,width=398)
        
        lbl_search = Label(ProductFrame2,text="Search product | by name",font=("times new roman",15,'bold'),bg="white",fg="green")
        lbl_search.place(x=2,y=5)
        lbl_name = Label(ProductFrame2,text="Product name",font=("times new roman",15,'bold'),bg="white",fg="green")
        lbl_name.place(x=2,y=45)
        
        txt_search = Entry(ProductFrame2,textvariable= self.var_search,font=("times new roman",15,),bg="lightyellow")
        txt_search.place(x=128,y=47,width=150,height=22)
        
        # ======== the search button ========
        btn_search = Button(ProductFrame2,command=self.search,text="Search",font=("times new roman",15),bg="black",fg="gold",cursor="hand2")
        btn_search.place(x=290,y=45,width=100,height=25)
        btn_show_all = Button(ProductFrame2,text="Show All",command=self.show,font=("times new roman",15),bg="blue",fg="white",cursor="hand2")
        btn_show_all.place(x=290,y=10,width=100,height=25)
        
        # ===========product details frame================
        ProductFrame3 = Frame(ProductFrame1,bd=5,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)
        
        scrolly = Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3,orient=HORIZONTAL)
        
        self.ProductTable = ttk.Treeview(ProductFrame3,columns=("pid", "name", "price", "qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set )
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview) 
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid",text="PID")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Qty")
        self.ProductTable.heading("status",text="Status")
        self.ProductTable["show"]="headings"
        self.ProductTable.column("pid",width=40)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=60)
        self.ProductTable.column("status",width=90)
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        
        lbl_note = Label(ProductFrame1,text="Note: 'Enter 0 Qty to remove the product from the Cart",anchor='w',font=('goudy old style',12),fg="red",bg="white")
        lbl_note.pack(side=BOTTOM,fill=X)
        
        # ======= customerframe =============================
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        
        CustomerFrame = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)
        
        cTitle = Label(CustomerFrame,text='Customer Details',font=('goudy old style',15),bg="lightgrey",)
        cTitle.pack(side=TOP,fill=X)
        
        lbl_name = Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white")
        lbl_name.place(x=5,y=35)
        txt_name = Entry(CustomerFrame,textvariable= self.var_cname,font=("times new roman",13,),bg="lightyellow")
        txt_name.place(x=75,y=35,width=180)
        
        lbl_contact = Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white")
        lbl_contact.place(x=265,y=35)
        txt_contact = Entry(CustomerFrame,textvariable= self.var_contact,font=("times new roman",13,),bg="lightyellow")
        txt_contact.place(x=370,y=35,width=150)
        # ===========cal_cart frame================
        Cal_cart_Frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_cart_Frame.place(x=420,y=190,width=530,height=360)
        
        # ===========calculator frame================
        self.var_cal_input = StringVar()
        
        Cal_Frame = Frame(Cal_cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)
        
        txt_cal_input = Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arail',15,'bold'),width=21,bd=10,relief=GROOVE,state="readonly",justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)
        
        btn_7 = Button(Cal_Frame,text='7',font=('arial ',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2")
        btn_7.grid(row=1,column=0)
        btn_8 = Button(Cal_Frame,text='8',font=('arial ',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2")
        btn_8.grid(row=1,column=1)
        btn_9 = Button(Cal_Frame,text='9',font=('arial ',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2")
        btn_9.grid(row=1,column=2)
        btn_sum = Button(Cal_Frame,text="+",font=('arial ',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2")
        btn_sum.grid(row=1,column=3)
        
        btn_4 = Button(Cal_Frame,text='4',font=('arial ',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2")
        btn_4.grid(row=2,column=0)
        btn_5 = Button(Cal_Frame,text='5',font=('arial ',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2")
        btn_5.grid(row=2,column=1)
        btn_6 = Button(Cal_Frame,text='6',font=('arial ',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2")
        btn_6.grid(row=2,column=2)
        btn_sub = Button(Cal_Frame,text="-",font=('arial ',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2")
        btn_sub.grid(row=2,column=3)
        
        btn_1 = Button(Cal_Frame,text='1',font=('arial ',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor="hand2")
        btn_1.grid(row=3,column=0)
        btn_2 = Button(Cal_Frame,text='2',font=('arial ',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor="hand2")
        btn_2.grid(row=3,column=1)
        btn_3 = Button(Cal_Frame,text='3',font=('arial ',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor="hand2")
        btn_3.grid(row=3,column=2)
        btn_mul = Button(Cal_Frame,text="*",font=('arial ',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor="hand2")
        btn_mul.grid(row=3,column=3)
        
        btn_0 = Button(Cal_Frame,text='0',font=('arial ',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor="hand2")
        btn_0.grid(row=4,column=0)
        btn_c = Button(Cal_Frame,text='c',font=('arial ',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor="hand2")
        btn_c.grid(row=4,column=1)
        btn_eq = Button(Cal_Frame,text='=',font=('arial ',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor="hand2")
        btn_eq.grid(row=4,column=2)
        btn_div = Button(Cal_Frame,text="/",font=('arial ',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor="hand2")
        btn_div.grid(row=4,column=3)
        
        
        
        # ===========cart frame================
        
        Cart_Frame= Frame(Cal_cart_Frame,bd=5,relief=RIDGE)
        Cart_Frame.place(x=280,y=5,width=245,height=342)
        self.CartTitle = Label(Cart_Frame,text="Cart \t Total Product: [0]",font=("goudy old style",15),bg="lightgrey")
        self.CartTitle.pack(side=TOP,fill=X)
        
        
        scrollx = Scrollbar(Cart_Frame,orient=HORIZONTAL)
        scrolly = Scrollbar(Cart_Frame,orient=VERTICAL)
        
        self.CartTable = ttk.Treeview(Cart_Frame, columns=("pid","name","price","qty"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("pid",text="PID") 
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Qty")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        
        # =========== Add cart wigets frame================
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()
        
        Add_CartWigetFrame= Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWigetFrame.place(x=420,y=550,width=530,height=110)
        
        lbl_p_name = Label(Add_CartWigetFrame,text="Product Name",font=('times new roman',15),bg="white")
        lbl_p_name.place(x=5,y=5)
        txt_p_name = Entry(Add_CartWigetFrame,textvariable=self.var_pname,font=('times new roman',15),bg="lightyellow",state="readonly")
        txt_p_name.place(x=5,y=35,width=190,height=22)
        
        lbl_p_price = Label(Add_CartWigetFrame,text="Price per Qty",font=('times new roman',15),bg="white")
        lbl_p_price.place(x=230,y=5)
        txt_p_price = Entry(Add_CartWigetFrame,textvariable=self.var_price,font=('times new roman',15),bg="lightyellow",state="readonly")
        txt_p_price.place(x=230,y=35,width=150,height=22)
        
        lbl_p_qty = Label(Add_CartWigetFrame,text="Quantity",font=('times new roman',15),bg="white")
        lbl_p_qty.place(x=390,y=5)
        txt_p_qty = Entry(Add_CartWigetFrame,textvariable=self.var_qty,font=('times new roman',15),bg="lightyellow")
        txt_p_qty.place(x=390,y=35,width=120,height=22)
        
        self.lbl_instock = Label(Add_CartWigetFrame,text="In Stock",font=('times new roman',15),bg="white")
        self.lbl_instock.place(x=5,y=70)
        
        btn_clear_cart = Button(Add_CartWigetFrame,text="Clear",command=self.clear_cart,font=('times new roman',15,'bold'),bg="lightgray",cursor="hand2")
        btn_clear_cart.place(x=180,y=70,width=150,height=30)
        
        btn_add_cart = Button(Add_CartWigetFrame,command=self.add_update_cart,text="Add | Update Cart",font=('times new roman',15,'bold'),bg="orange",cursor="hand2")
        btn_add_cart.place(x=340,y=70,width=180,height=30)
        
        
        # =============billing area =============================
        billFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=400,height=410)
        
        bTitle = Label(billFrame,text='Customer Bill Area ',font=('goudy old style',20,'bold'),bg="#f44336",fg="white")
        bTitle.pack(side=TOP,fill=X)
        
        scrolly = Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area = Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        
        # =================billing buttons =================
        billMenuFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=400,height=140)
        
        self.lbl_amnt= Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,'bold'),fg="white",bg="#3f51b5")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)
        
        self.lbl_discount= Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",15,'bold'),fg="white",bg="#8bc34a")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)
        
        self.lbl_net_pay= Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,'bold'),fg="white",bg="#607d8b")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)
        
        btn_print= Button(billMenuFrame,text="Print",command=self.print_bill,font=("goudy old style",15,'bold'),fg="white",bg="lightgreen",cursor="hand2")
        btn_print.place(x=2,y=80,width=120,height=50)
        
        btn_clear_all= Button(billMenuFrame,text="Clear All",command=self.clear_all,font=("goudy old style",15,'bold'),fg="white",bg="gray",cursor="hand2")
        btn_clear_all.place(x=124,y=80,width=120,height=50)
        
        btn_generate= Button(billMenuFrame,text="Generate/ Save Bill",command=self.generate_bill,font=("goudy old style",15,'bold'),fg="white",bg="#009688",cursor="hand2")
        btn_generate.place(x=246,y=80,width=160,height=50)
        
        
        #==============footer============
        footer = Label(self.root,text="IMS- Inventory Management System | Developed by Billa\n for more info contact 05489657654",font=("times new roman",15,),bg="#4d636d",fg="white",cursor="hand2")
        footer.pack(side=BOTTOM,fill=X)
        
        self.show()
        # self.bill_top()
        self.update_date_time()
        
        
        
        
# ================================all functions ================================
    def get_input(self,num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)
        
    def clear_cal(self):
        self.var_cal_input.set('')
        
    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))
     
     
    def show(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT pid, name, price, qty,status FROM product where status='Active'")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
                  
        
    def search(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input is required",parent =self.root) 
            else:
                cur.execute("SELECT pid, name, price, qty,status FROM product WHERE name LIKE '%"+ self.var_search.get()+"%' AND  status='Active'")
                rows = cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children()) 
                    for row in rows:
                        self.ProductTable.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent =self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
    
    def get_data(self,ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content["values"]      
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")
        
    def get_data_cart(self,ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content["values"]
        # pid, name, price, qty,stock      
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
     
    
    def add_update_cart(self):
        if self.var_pid.get() =="":
            messagebox.showerror("Error","Please select product from the list",parent=self.root)
        elif self.var_qty.get() =="":
            messagebox.showerror("Error","Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            # price_cal =int(self.var_qty.get())*float(self.var_price.get())
            # price_cal =float(price_cal)
            price_cal =self.var_price.get()
            # pid, name, price, qty,stock
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            
            #---------update  cart----------------
            present ="no"
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present ="Yes"
                    break
                index_+=1
            if present == "Yes":
                op=messagebox.askyesno("Comfirm","Product already present\nDo you want to update|remove from the cart list",parent=self.root)
                if op == True:
                    if self.var_qty.get() =="0":
                        self.cart_list.pop()
                    else:
                        # pid, name, price, qty,status
                        # self.cart_list[index_][2]= price_cal#price
                        self.cart_list[index_][3]=self.var_qty.get()#quantity
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()
    
    
    def bill_update(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            # pid, name, price, qty,stock 
            self.bill_amnt=self.bill_amnt + (float(row[2])* int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt - self.discount
        self.lbl_amnt.config(text=f"Bill Amnt\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net pay\n{str(self.net_pay)}")
        self.CartTitle.config(text=f"Cart \t Total Product: [{len(self.cart_list)}]")
    
    
    def show_cart(self):
        
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
                  
    def generate_bill(self):
        if self.var_cname.get()=="" or self.var_contact.get()=="":
            messagebox.showerror("Error","Customer name and contact is required",parent =self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please add product to cart!!!!",parent =self.root)
        else:
            #====== bill top=======
            self.bill_top()
            #====== bill middle=======
            self.bill_middle()
            #====== bill bottom=======
            self.bill_bottom()
            
            # =======how to send the bill generated to a folder in your pc==
            fp=open(f"bill/{str(self.invoice)}.txt",'w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo("Saved","Bill has been generated and Saved in backend",parent =self.root)
            self.chk_print =1
            
    def bill_top(self):
        self.invoice =int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tM-Ventures Inventory
\tPhone No. 689********, Tongo
{str("="*46)}
 Customer Name: {str(self.var_cname.get())}
 Phone No: {str(self.var_contact.get())}
 Bill No: {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
 Product Name\t\t\tQty\tPrice
{str("="*46)}
        '''
        self.txt_bill_area.delete("1.0",END)
        self.txt_bill_area.insert("1.0",bill_top_temp)
        
        
    def bill_bottom(self):
        bill_bottom_temp = f'''
{str('='*46)}
 Bill Amount\t\t\t\tGh.{str(self.bill_amnt)}
 Discount \t\t\t\tGh.{str(self.discount)}
 Net Pay \t\t\t\tGh.{str(self.net_pay)}
{str('='*46)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
        
    def bill_middle(self):
        conn = sqlite3.connect(database=r"IMS.db") 
        cur = conn.cursor()
        try:
            for row in self.cart_list:
                # pid, name, price, qty,stock 
                
                pid =row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3]) == int(row[4]):
                    status="Inactive"
                if int(row[3]) != int(row[4]):
                    status="Active"
                price=float(row[2])*int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+row[3]+"\tGh."+price)
                # ======update quantity in priduct table==============
                cur.execute("UPDATE product SET qty=?, status=? WHERE pid=?",(
                    qty,
                    status,
                    pid,
                ))
                conn.commit()
            conn.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)},",parent =self.root)
         
            
    def clear_cart(self):
           
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set("")
        self.var_qty.set("")
        
    def clear_all(self):
        self.chk_print==0
        del self.cart_list[:]
        self.var_cname.set("")
        self.var_contact.set("")
        self.txt_bill_area.delete("1.0",END)
        self.CartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set("")
        self.clear_cart()
        self.show()
        self.show_cart()
        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Wellcome To Inventor Management System\t\tDate:{str(date_)}\t\tTime: {str(time_)}",)
        self.lbl_clock.after(200,self.update_date_time)
    
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing",parent =self.root)
            new_file = tempfile.mkdtemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
            
        else:
            messagebox.showerror("Print","Please generate bill, to print th receipt",parent =self.root)
            
    def logout(self):
        self.root.destroy()
        os.system("python login.py"  )
            
    
    
    
if __name__ == "__main__":
    root = Tk()
    obj = billing(root)
    root.mainloop()