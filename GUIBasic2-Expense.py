from tkinter import *
from tkinter import ttk, messagebox
from tkinter import messagebox
from datetime import datetime
import csv

GUI = Tk()
GUI.title('โปรแกรมคำนวนค่าใช้จ่าย v.1.1 By FlukeAsL')
GUI.geometry('500x500+500+200')

menubar = Menu(GUI)
GUI.config(menu=menubar)

##file
filemenu = Menu(menubar)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='import CSV')

helpmenu = Menu(menubar)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About')

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1)

icon_t1 = PhotoImage(file='Add.png').subsample(10)
icon_t2 = PhotoImage(file='list.png').subsample(10)

Tab.add(T1, text=f'{"Add":^{30}}',image=icon_t1,compound='top')
Tab.add(T2,text=f'{"List":^{30}}',image=icon_t2,compound='top')

F1 = Frame(T1)
F1.place(x=100,y=50)

F1Photo = PhotoImage(file='coin.png').subsample(5)
F1BG = ttk.Label(F1,image=F1Photo)
F1BG.pack(pady=20)

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thr':'พฤหัส',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}
        
def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('ERROR','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return 
    elif price =='':
        messagebox.showwarning('ERROR','กรุณากรอกข้อมูลจำนวน')
        return
    elif quantity =='':
        messagebox.showwarning('ERROR','กรุณากรอกข้อมูลราคา')
        return    

    try:
        total = float(price) * float(quantity)
        
        print('รายการ: {} ราคา: {}'.format(expense,price))
        print('จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total))
        text = 'รายการ: {} ราคา: {}\n'.format(expense,price) 
        text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total)
        v_result.set(text)

        v_expense.set('')
        v_price.set('')
        v_quantity.set('')
        
        today = datetime.now().strftime('%a')
        print(today)
        dt = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        dt = days[today] + '-' + dt

        with open('savedatav2.csv','a',encoding='utf-8',newline='') as f:

            fw = csv.writer(f)
            data = [expense,price,quantity,total,dt]
            fw.writerow(data)

        E1.focus()    
    except:

        print('ERROR')
        #messagebox.showerror('ERROR','Please try Again')
        messagebox.showwarning('ERROR','Please try Again')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')    

    
GUI.bind('<Return>',Save)

FONT1 = (None,20)

#box1
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()

#box2
L = ttk.Label(F1,text='จำนวน',font=FONT1).pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

#box3
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()

savepic = PhotoImage(file='savepic2.png').subsample(10)
B2 = ttk.Button(F1,text=f'{"Save": >{10}}', image = savepic,compound='left',command=Save)
B2.pack(ipadx=50,ipady=20)

v_result = StringVar()
v_result.set('-----ผลลัพธ์-----')
result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground='red')
result.pack(pady=20)

def read_csv():
    with open('savedatav2.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data

L = ttk.Label(T2,text='ตารางแสดงค่าใช้จ่าย',font=FONT1).pack(pady=20)

header = ['รายการ','จำนวน','ค่าใช้จ่าย','รวม','วัน-เวลา']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10)
resulttable.pack()

for h in header:
    resulttable.heading(h,text=h)

headerwidth = [150,170,80,80,100]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)

resulttable.insert('','end',value=['']) 

def update_table():
    resulttable.delete(*resulttable.get_children())
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

update_table()

print('GET CHILD:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
