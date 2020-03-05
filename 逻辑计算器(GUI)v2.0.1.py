from tkinter import messagebox, ttk,Tk,Label,StringVar,Entry,Button,Checkbutton,IntVar,Radiobutton
from copy import deepcopy
def Karnaugh():
    flag=2  #最小项为0

    Karnaugh =Tk()  # 生成主窗口，用Karnaugh表示，后面就在Karnaugh操作
    # 设置窗口大小和位置
    Karnaugh.geometry('550x400+100+100')  # 指定主框体大小
    # 不允许改变窗口大小
    Karnaugh.resizable(False, False)  # 框体大小可调性，分别表示x,y方向的可变性；
    # 设置窗口标题
    Karnaugh.title('卡诺图计算器')
    Karnaugh.configure(background = 'Gainsboro')

    right_text =Label(Karnaugh,fg='black',text="copyright@CGC\nver  2.0.1",font=('Arial', 12), justify="left",bg="Gainsboro" )
    right_text.place(x=400, y=350, width=180, height=60)

    content = StringVar(Karnaugh, '数字与数字逗号隔开（半角）')
    contentEntry=Entry(Karnaugh, text=content,fg='Chocolate',font=('楷体', 18))  # 括号里面，可见第一个都是Karnaugh,即表示都是以Karnaugh为主界面的，将文本框中的内容存在contentVar中
    contentEntry.place(x=10, y=250, width=530, height=60)  # 文本框在Karnaugh主界面的xy坐标位置，以及文本框自生的宽和高

    variate=StringVar(Karnaugh, '')
    variateEntry=Entry(Karnaugh, text=variate,fg='Chocolate',font=('Arial', 18))  # 括号里面，可见第一个都是Karnaugh,即表示都是以Karnaugh为主界面的，将文本框中的内容存在contentVar中
    variateEntry.place(x=120, y=60, width=80, height=50)  # 文本框在Karnaugh主界面的xy坐标位置，以及文本框自生的宽和高

    select_text=Label(Karnaugh,fg='red',text="变量个数:",font=('楷体',18),bg="Gainsboro")
    select_text.place(x=10, y=50, width=100, height=60)

    CheckVar = IntVar()

    def Max():
        global flag
        flag=0
        contentEntry.select_clear()
        content.set('∏ M()')

    def Min():
        global flag
        flag =1
        contentEntry.select_clear()
        content.set('∑ m()')

    def clear():
        variate.set('')
        content.set('数字与数字逗号隔开（半角）')

    def creat():
        global flag
        try:
            con =content.get()
            con=con[4:-1].split(',')
            con=list(map(int,con))
            con.sort()
        except:
            messagebox.showerror('错误', '表达式有误,请重新输入')
            clear()
        try:
            var=int(variate.get())
            s=CheckVar.get()
            kar_show(var, con, flag,s)
        except:
            messagebox.showerror('错误', '变量个数输入有误,请重新输入')


    C1 = Checkbutton(Karnaugh, text="是否填充", bg='Gainsboro',variable=CheckVar,onvalue=1, offvalue=0, height=5, width=20)
    C1.place(x=430,y=100,width=120,height=30)


    btn_Max=Button(Karnaugh, text='最大项', font=('楷体', 16),bg='orange',command=Max)  # 创建的过程和上面类似
    btn_Max.place(x=350, y=30, width=70, height=40)

    btn_min=Button(Karnaugh, text='最小项', font=('楷体', 16),bg='orange',command=Min)  # 创建的过程和上面类似
    btn_min.place(x=350, y=100, width=70, height=40)

    btn_clear=Button(Karnaugh, text='Clear', font=('Arial', 16),bg='red',command=clear)  # 创建的过程和上面类似
    btn_clear.place(x=350, y=170, width=70, height=40)

    btn_creat=Button(Karnaugh, text='生  成', fg='blue',font=('楷体', 22),bg='red',command=creat)  # 创建的过程和上面类似
    btn_creat.place(x=120, y=150, width=120, height=70)

    def another():
        Karnaugh.destroy()
        Truth_tab()

    btn_truth=Button(Karnaugh, text='真值表计算器', fg='black',font=('楷体', 18),bg='darkcyan',command=another)  # 创建的过程和上面类似
    btn_truth.place(x=50, y=330, width=160, height=50)

    Karnaugh.mainloop()  # 进入消息循环（必需组件）

def kar_show(var,res,flag,s):

    if var % 2 == 0:
        row = var // 2
        col = var // 2
    else:
        row = var // 2 + 1
        col = var // 2
    Labs=[' ']

    if flag==0:
        M='0'
        m='1'
    elif flag==1:
        M='1'
        m='0'
    else:
        messagebox.showerror('错误', '请选择计算类别')

    if s==0:
        m=' '

    for i in range(2**row):
        Labs.append(bin(i)[2:].rjust(row,'0'))
    win =Tk()
    win.title("卡诺图结果")  # #窗口标题
    win.geometry(f"{105+35*2**row}x{70+20*2**col}+800+40")# #窗口位置500后面是字母x
    '''
    表格
    '''
    tree = ttk.Treeview(win, height=f'{2**col+1}',show="headings")  # #创建表格对象，隐藏首列
    tree["columns"] = tuple(Labs)  # #定义列
    for i in tree["columns"]:
        tree.column(i, width=35,anchor='center')  # #设置列
        tree.heading(i, text=i)  # #设置显示的表头名
    for j in range(2**col):
        value = []
        value.append(bin(j)[2:].rjust(col,'0'))
        for k in range(2**row):
            if  len(res)!=0 and  res[0] == j*(2**row)+k:
                value.append(M)
                res=res[1:]
            else:
                value.append(m)
        tree.insert("", j, values=tuple(value))  # #给第j行添加数据，索引值可重复
    tree.pack()
    win.mainloop()  # #窗口持久化


def Truth_tab():
    # 按钮操作，点击按钮后需要做的处理
    def buttonClik(btn):
        content = contentVar.get()  # 获取文本框中的内容
        # 根据不同的按钮作出不同的反应
        if btn in 'ABCDEF()':
            content += btn  # 哪个键按下了，就在content字符串中增添
        elif btn == 'M':
            content = ''  # 清除文本框
        elif btn == 'Bs':
            content = content[:-1]  # 文本框退格
        elif btn == '=':
            try:
                # 对输入的表达式求值
                a = 0
                b = []
                c = []
                a, b, c = operate(content)  # 调用函数eval，用字符串计算出结果
                tab_show(a, b, c)
            except:
                messagebox.showerror('错误', '表达式有误')
                return
        elif btn in operators:
            if not btn == '!' and content.endswith(operators):  # 如果content中最后出现的+-*/
                messagebox.showerror('错误', '不允许存在连续运算符')
                return
            content += btn
        contentVar.set(content)  # 将结果显示到文本框中

    root = Tk()  # 生成主窗口，用root表示，后面就在root操作
    # 设置窗口大小和位置
    root.geometry('550x500+100+100')  # 指定主框体大小
    # 不允许改变窗口大小
    root.resizable(False, False)  # 框体大小可调性，分别表示x,y方向的可变性；
    # 设置窗口标题
    root.title('真值表计算器')
    root.configure(background='Gainsboro')
    w = Label(root, fg='black', text="copyright@CGC  ver  2.0.1", font=('Arial', 12), justify="right",
                      bg="Gainsboro")
    w.pack(side='bottom')

    # 文本框和按钮都是tkinter中的组件
    # Entry        　　 文本框（单行）；
    # Button        　　按钮；
    # 放置用来显示信息的文本框，设置为只读
    # tkinter.StringVar    能自动刷新的字符串变量，可用set和get方法进行传值和取值
    CheckVar_select = IntVar()
    CheckVar_fill = IntVar()
    radio=IntVar()
    contentVar = StringVar(root, '')
    contentEntry =Entry(root, textvariable=contentVar, fg='Chocolate',
                                 font=('Arial', 18))  # 括号里面，可见第一个都是root,即表示都是以root为主界面的，将文本框中的内容存在contentVar中
    contentEntry['state'] = 'readonly'  # 文本框只能读，不能写
    contentEntry.place(x=10, y=10, width=530, height=60)  # 文本框在root主界面的xy坐标位置，以及文本框自生的宽和高
    # x:        　　　 组件左上角的x坐标；
    # y:        　　   组件右上角的y坐标；
    # 放置清除按钮和等号按钮
    btnClear = Button(root, text='清除', bg='red', font=('楷体', 16), command=lambda: buttonClik('M'))
    btnClear.place(x=60, y=100, width=80, height=40)

    btnBackspace = Button(root, text='退格', bg='red', font=('楷体', 16), command=lambda: buttonClik('Bs'))
    btnBackspace.place(x=230, y=100, width=80, height=40)

    btnCompute =Button(root, text='=', bg='yellow', font=('Arial', 16), command=lambda: buttonClik('='))
    btnCompute.place(x=400, y=100, width=80, height=40)

    radio1=Radiobutton(root,text='最大项卡诺图',bg='Gainsboro',value=0,variable=radio)
    radio2=Radiobutton(root,text='最小项卡诺图',bg='Gainsboro',value=1, variable=radio)
    C_fill = Checkbutton(root, text="是否填充", bg='Gainsboro', variable=CheckVar_fill, onvalue=1, offvalue=0,
                         height=5,
                         width=20)
    def callback():
        if CheckVar_select.get()== 1:
            radio1.place(x=160,y=400,width=120,height=30)
            radio2.place(x=160,y=440, width=120, height=30)
            C_fill.place(x=402, y=400, width=120, height=30)
        elif CheckVar_select.get()==0:
            radio1.place_forget()
            radio2.place_forget()
            C_fill.place_forget()
    C_select = Checkbutton(root, text="是否生成卡诺图", bg='Gainsboro', variable=CheckVar_select, onvalue=1, offvalue=0, height=5,
                     width=20,command=callback)
    C_select.place(x=20, y=400, width=120, height=30)



    # 放置10个数字、小数点和计算平方根的按钮
    digits = list('ABCDE')  # 序列list是Python中最基本的数据结构。序列中的每个元素都分配一个数字 - 它的位置，或索引，第一个索引是0，第二个索引是1，依此类推。
    # 用循环的方式将上面数字、小数点、平方根这12个按钮分成四行三列进行放置
    for col in range(5):
        d = digits[col]  # 按索引从list中取值，和c语言中的数组类似
        btnDigit = Button(root, text=d, font=('Arial', 16), bg='PaleVioletRed',
                                  command=lambda x=d: buttonClik(x))  # 和上面的是类似的
        btnDigit.place(x=20 + col * 110, y=170, width=70, height=40)  # 很显然，每次放一个按钮的位置是不一样的，但是它们之间的关系时确定的

    brackets = ['(', ')']
    for col in range(2):
        d = brackets[col]
        btnDigit = Button(root, text=d, font=('楷体', 16), bg='orange',
                                  command=lambda x=d: buttonClik(x))  # 创建的过程和上面类似
        btnDigit.place(x=20 + col * 110, y=330, width=70, height=40)

    # 放置运算符按钮
    operators = ('+', '*', '!', '@')  # Python的元组与列表类似，不同之处在于元组的元素不能修改。
    operators_show = ('或', '与', '非', '异或')
    # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
    for index, operator in enumerate(operators):
        btnOperator = Button(root, text=operators_show[index], font=('楷体', 16), bg='orange',
                                     command=lambda x=operator: buttonClik(x))  # 创建的过程和上面类似
        btnOperator.place(x=20 + index * 110, y=250, width=70, height=40)

    def info():
        messagebox.askokcancel('温馨提示', '同或运算与异或运算呈反演\n请自行转换')

    def kra():
        root.destroy()
        Karnaugh()

    btnOperator = Button(root, text='同或', font=('楷体', 16), bg='orange', command=info)  # 创建的过程和上面类似
    btnOperator.place(x=20 + 4 * 110, y=250, width=70, height=40)

    btn_kra=Button(root, text='卡诺图计算器', fg='black', font=('楷体', 18), bg='darkcyan',command=kra)  # 创建的过程和上面类似
    btn_kra.place(x=290, y=330, width=180, height=40)


    def boo(x, leng, listboo, array):  # 递归实现布尔真值全排列
        if x == leng:
            for i in range(0, leng):
                array.append(listboo[i])
            return (listboo)
        else:
            listboo[x] = 1
            boo(x + 1, leng, listboo, array)
            listboo[x] = 0
            boo(x + 1, leng, listboo, array)

    def operate(x):
        listch = []
        listnum = []
        listok = []
        array = []
        listcom = []
        res = []
        l = list(x)

        for i in range(0, len(l)):
            char = l[i]
            if (ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122):
                if char not in listch:
                    listch.append(l[i])
                    listnum.append(0)
            else:
                listcom.append(l[i])
        boo(0, len(listch), listnum, array)
        i = 0
        while i < len(array):
            listok.append(array[i:i + len(listch):])
            i += len(list(listch))
        for i in range(0, len(listok)):
            newl =deepcopy(l)
            for o in range(0, len(listch)):
                for j in range(0, len(l)):
                    char = l[j]
                    if char == listch[o]:
                        newl[j] = int(listok[i][o])
                o += 1
            tem = ' '.join(map(str, newl))
            tem = tem.replace('+', 'or')
            tem = tem.replace('*', 'and')
            tem = tem.replace('!', 'not')
            tem = tem.replace('@', '^')
            res.append(int(eval(tem)))
        return len(listch), listok[::-1], res[::-1]

    def tab_show(x, listok, res):
        LABS = ['A', 'B', 'C', 'D', 'E']
        kar=[]
        win = Tk()
        win.title("真值表结果")  # #窗口标题
        win.geometry(f"{100 + 100 * (x + 2)}x{100 + 20 * 2 ** x}+800+300")  # #窗口位置500后面是字母x
        '''
        表格
        '''
        tree = ttk.Treeview(win, height=f'{2 ** x}', show="headings")  # #创建表格对象，隐藏首列
        lab = LABS[:x]
        lab.append('F')
        tree["columns"] = tuple(lab)  # #定义列
        for i in tree["columns"]:
            tree.column(i, width=100, anchor='center')  # #设置列
            tree.heading(i, text=i)  # #设置显示的表头名
        for j in range(2 ** x):
            value = []
            value = listok[j]
            value.append(res[j])
            tree.insert("", j, values=tuple(value))  # #给第0行添加数据，索引值可重复
            if CheckVar_select.get() == 1:
                if value[-1] == radio.get():
                    value = value[:-1]
                    tem = ''.join(map(str, value))
                    kar.append(int(tem, 2))

        tree.pack()
        if CheckVar_select.get()== 1:
            kar_show(x, kar, radio.get(), CheckVar_fill.get())
        win.mainloop()  # #窗口持久化

    root.mainloop()  # 进入消息循环（必需组件）

Truth_tab()