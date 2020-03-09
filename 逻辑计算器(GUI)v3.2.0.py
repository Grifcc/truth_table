from tkinter import messagebox, ttk,Tk,Label,StringVar,Entry,Button,Checkbutton,IntVar,Radiobutton


#全局变量区
# win_Karnaugh_win = Tk()  # 卡诺图计算器主窗口
# win_Truth=Tk()   # 真值表计算器主窗口
# win_tab = Tk()   # 真值表结果窗口
# win_kar=Tk()     # 卡诺图结果窗口
right='copyright@Grifcc  V3.2.0'
# content = StringVar(win_Karnaugh_win, '数字与数字逗号隔开（半角）')    #卡诺图计算器公式输入框
# variate=StringVar(win_Karnaugh_win, '')
# CheckVar_fill_fill_kar= IntVar()

#生成格雷码
class GrayCode:
  def getGray(self, n):
    # write code here
    global maxn
    maxn = n
    return GrayCode.getGrace(self, ['0', '1'], 1)
  def getGrace(self, list_grace, n):
    global maxn
    if n >= maxn:
      return list_grace
    list_befor, list_after = [], []
    for i in range(len(list_grace)):
      list_befor.append('0' + list_grace[i])
      list_after.append('1' + list_grace[-(i + 1)])
    return GrayCode.getGrace(self, list_befor + list_after, n + 1)


#生成BOOL列表
class compute:
    def creat_bin(self,n,x):
        '''

        :param n: 需要变成二进制的数
        :param x: 位数
        :return:  二进制列表
        '''
        bin_list=[]
        for i in (bin(n)[2:]).rjust(x,'0'):
            bin_list.append(i)
        return bin_list
    def creat_bool(self,n):
        '''

        :param n:   变量个数
        :return:    变量列表
        '''
        bool_list=[]
        for i in range(2**n):
            bool_list.append(compute().creat_bin(i,n))
        return bool_list

#根据输入字符串生成真值表列表
class truth_list:
    def ope_str(self,string:str): #字符串操作
        '''

        :param string:需要操作的字符串
        :return:      操作字符串
        '''
        tem=list(string)
        i=0
        while i<=len(tem)-2:
            if tem[i]==')' and tem[i+1]=='(':
                tem.insert(i+1,'*')
            if tem[i].isalpha() and tem[i+1].isalpha():
                tem.insert(i+1, '*')
            i=i+1
        del i
        tem_str=' '.join(tem)
        tem_str=tem_str.replace('+','or').replace('*','and').replace('!','not').replace('@', '^')
        return tem_str

    def creat_truth_tab(self,string:str):
        '''

        :param string: 逻辑函数
        :return:   真值表结果
        '''
        num=[]
        for i in string:
            if i.isalpha():
                num.append(i)
        num=set(num)
        lists=compute().creat_bool(len(num))
        string=truth_list().ope_str(string)
        truth_tab=[]
        for i in lists:
            tem_list = []
            tem = string
            tem_list=i[:]
            for j in range(len(i)):
                tem=tem.replace(chr(65+j),i[j])
            tem_list.append(str(eval(tem)))
            truth_tab.append(tem_list)
        return truth_tab

#生成真值表
class Tab:
    def __init__(self):
        self.win_tab=Tk()
    def tab_show(self,res:list,creat_flag=0,select_flag=1,fill_flag:int=0):
        '''

        :param res: 真值表结果
        :param creat_flag : 选择是否创建卡诺图，默认不创建
        :param select_flag:   选择类别 默认最小项
        :param fill_flag:    选择是否填充  默认不填充
        :return:   无
        '''
        global K_T
        try:
            K_T.win_kar.destroy()
        except:
            pass
        lab=[]
        num=len(res[2])-1
        for i in range(num):
            lab.append(chr(65+i))
        lab.append('F')   #真值表结果表头标签
        self.win_tab.title("真值表结果")  # #窗口标题
        self.win_tab.geometry(f"{100 + 100 * (num + 2)}x{100 + 20 * 2 ** num}+800+300")  # #窗口位置500后面是字母x
        tree = ttk.Treeview(self.win_tab, height=f'{2 ** num}', show="headings")  # #创建表格对象，隐藏首列
        tree["columns"] = tuple(lab)  # #定义列
        for i in tree["columns"]:
            tree.column(i, width=100, anchor='center')  # #设置列
            tree.heading(i, text=i)  # #设置显示的表头名
        for j in range(2 ** num):
            value = res[j]
            tree.insert("", j, values=tuple(value))  # #给第0行添加数据，索引值可重复
        tree.pack()
        if creat_flag==1:
            num, equ = creat_kar_equation(res, fill_flag)
            K_T = Kar()
            K_T.kar_show(num, select_flag, fill_flag, equ)
        self.win_tab.mainloop()   #窗口持久化


#生成卡诺图
class Kar:
    def __init__(self):
        self.win_kar=Tk()
    def kar_show(self,num: int, select_flag: int, fill_flag: int, res: list):
        '''

        :param num: 变量个数
        :param select_flag:  选择生成卡诺图类别
        :param fill_flag:    选择是否填充
        :param res:    标准式
        :return:  无
        '''
        # 计算横竖行变量个数
        if num % 2 == 0:
            row = num // 2
            col = num // 2
        else:
            row = num // 2 + 1
            col = num // 2

        # 判断最小项\最大项
        if select_flag == 0:
            M = '0'
            m = '1'
        elif select_flag == 1:
            M = '1'
            m = '0'
        else:
            messagebox.showerror('错误', '请选择计算类别')

        # 判断是否填充
        if fill_flag == 0:
            m = ' '

        row_gray = GrayCode().getGray(row)  # 卡诺图横行标签
        col_gray = GrayCode().getGray(col)  # 卡诺图竖行标签
        Labs = [' ']
        for i in row_gray:
            Labs.append(i)
        self.win_kar.title("卡诺图结果")  # #窗口标题
        self.win_kar.geometry(f"{105 + 35 * 2 ** row}x{70 + 20 * 2 ** col}+800+40")  # #窗口位置500后面是字母x
        tree = ttk.Treeview(self.win_kar, height=f'{2 ** col + 1}', show="headings")  # #创建表格对象，隐藏首列
        tree["columns"] = tuple(Labs)  # #定义列

        for i in tree["columns"]:
            tree.column(i, width=35, anchor='center')  # #设置列
            tree.heading(i, text=i)  # #设置显示的表头名

        for j in range(2 ** col):
            value = []
            value.append(col_gray[j])
            for k in range(2 ** row):
                tem = int(row_gray[k] + col_gray[j], 2)
                if tem in res:
                    res.remove(tem)
                    value.append(M)
                else:
                    value.append(m)
            tree.insert("", j, values=tuple(value))  # #给第j行添加数据，索引值可重复

        tree.pack()
        self.win_kar.mainloop()  # #窗口持久化


#根据真值表创建标准与或式  或与式
def creat_kar_equation(res:list,select:int):
    '''

    :param res: 真值表
    :param select: 选择是否填充
    :return: 变量个数  标准式
    '''

    kar=[]
    num=len(res[0])-1
    for i in res:
        if i[-1] == str(select):
            value = i[:-1]
            tem = ''.join(map(str, value))
            kar.append(int(tem, 2))
    return  num,kar

def Karnaugh():

    flag=2  #最小项为0
    Karnaugh_win =Tk()  # 生成主窗口，用Karnaugh_win表示，后面就在Karnaugh_win操作
    # 设置窗口大小和位置
    Karnaugh_win.geometry('550x400+100+100')  # 指定主框体大小
    # 不允许改变窗口大小
    Karnaugh_win.resizable(False, False)  # 框体大小可调性，分别表示x,y方向的可变性；
    # 设置窗口标题
    Karnaugh_win.title('卡诺图计算器')
    Karnaugh_win.configure(background = 'Gainsboro')

    right_text =Label(Karnaugh_win,fg='black',text=right,font=('Arial', 12), justify="left",bg="Gainsboro" )
    right_text.pack(side='bottom')

    content = StringVar(Karnaugh_win, '数字与数字逗号隔开（半角）')
    contentEntry=Entry(Karnaugh_win, text=content,fg='Chocolate',font=('楷体', 18))  # 括号里面，可见第一个都是Karnaugh_win,即表示都是以Karnaugh_win为主界面的，将文本框中的内容存在contentVar中
    contentEntry.place(x=10, y=250, width=530, height=60)  # 文本框在Karnaugh_win主界面的xy坐标位置，以及文本框自生的宽和高

    variate=StringVar(Karnaugh_win, '')
    variateEntry=Entry(Karnaugh_win, text=variate,fg='Chocolate',font=('Arial', 18))  # 括号里面，可见第一个都是Karnaugh_win,即表示都是以Karnaugh_win为主界面的，将文本框中的内容存在contentVar中
    variateEntry.place(x=120, y=60, width=80, height=50)  # 文本框在Karnaugh_win主界面的xy坐标位置，以及文本框自生的宽和高

    select_text=Label(Karnaugh_win,fg='red',text="变量个数:",font=('楷体',18),bg="Gainsboro")
    select_text.place(x=10, y=50, width=100, height=60)

    CheckVar_fill = IntVar()

    def callback(btn:str):
        '''
        :param btn: Button 值
        :return:
        '''
        global flag
        global K
        if btn =='max':
            flag=0
            contentEntry.select_clear()
            content.set('∏ M()')
        elif btn == 'min':
            flag=1
            contentEntry.select_clear()
            content.set('∑ m()')
        elif btn == 'clear':
            variate.set('')
            content.set('数字与数字逗号隔开（半角）')
            try:
                K.win_kar.destroy()
            except:
                pass
        elif btn == 'switch':
            Karnaugh_win.destroy()
            try:
                K.win_kar.destroy()
            except:
                pass
            Truth_tab()

    def creat():
        global flag
        global K
        try:
            K.win_kar.destroy()
        except:
            pass
        try:
            con =content.get()
            con=con[4:-1].split(',')
            con=list(map(int,con))
            con.sort()
        except:
            messagebox.showerror('错误', '表达式有误,请重新输入')
            callback('clear')
        try:
            var=int(variate.get())
            fill_flag=CheckVar_fill.get()
            K=Kar()
            K.kar_show(var,flag,fill_flag,con)
        except:
            messagebox.showerror('错误', '变量个数输入有误,请重新输入')

    btn_fill = Checkbutton(Karnaugh_win, text="是否填充", bg='Gainsboro',variable=CheckVar_fill,onvalue=1, offvalue=0, height=5, width=20)
    btn_fill.place(x=430,y=100,width=120,height=30)

    btn_Max=Button(Karnaugh_win, text='最大项', font=('楷体', 16),bg='orange',command=lambda x='max':callback(x))  # 创建的过程和上面类似
    btn_Max.place(x=350, y=30, width=70, height=40)

    btn_min=Button(Karnaugh_win, text='最小项', font=('楷体', 16),bg='orange',command=lambda x='min':callback(x))  # 创建的过程和上面类似
    btn_min.place(x=350, y=100, width=70, height=40)

    btn_clear=Button(Karnaugh_win, text='Clear', font=('Arial', 16),bg='red',command=lambda x='clear':callback(x))  # 创建的过程和上面类似
    btn_clear.place(x=350, y=170, width=70, height=40)

    btn_creat=Button(Karnaugh_win, text='生  成', fg='blue',font=('楷体', 22),bg='red',command=creat)  # 创建的过程和上面类似
    btn_creat.place(x=120, y=150, width=120, height=70)


    btn_truth=Button(Karnaugh_win, text='真值表计算器', fg='black',font=('楷体', 18),bg='darkcyan',command=lambda x='switch':callback(x))  # 创建的过程和上面类似
    btn_truth.place(x=175, y=320, width=200, height=40)

    Karnaugh_win.mainloop()  # 进入消息循环（必需组件）

def Truth_tab():

    def buttonClik(btn):
        global T
        content = contentVar.get()  # 获取文本框中的内容
        # 根据不同的按钮作出不同的反应
        if btn in 'ABCDEF()':
            content += btn  # 哪个键按下了，就在content字符串中增添
        elif btn == 'clear':
            content = ''  # 清除文本框
            try:
                T.win_tab.destory()
            except:
                pass

        elif btn == 'Backspace':
            content = content[:-1]  # 文本框退格
        elif btn == '=':
            try:
                T.win_tab.destroy()
            except:
                pass
            try:
                # 对输入的表达式求值
                content=contentVar.get()
                res=truth_list().creat_truth_tab(content)
                creat_flag=CheckVar_select.get()
                select_flag = radio.get()
                fill_flag = CheckVar_fill.get()
                T = Tab()
                if creat_flag==1:
                    T.tab_show(res,creat_flag=creat_flag,select_flag=select_flag,fill_flag=fill_flag)
                else :
                    T.tab_show(res)
            except:
                messagebox.showerror('错误', '表达式有误')
                return
        elif btn in operators:
            if not btn == '!' and content.endswith(operators):  # 如果content中最后出现的+-*/
                messagebox.showerror('错误', '不允许存在连续运算符')
                return
            content += btn
        elif btn == 'info':
            messagebox.askokcancel('温馨提示', '同或运算与异或运算呈反演\n请自行转换')
        elif btn == 'switch':
            try:
                T.win_tab.destroy()
            except:
                pass
            win_Truth.destroy()
            Karnaugh()
        contentVar.set(content)  # 将结果显示到文本框中

    win_Truth =Tk()  # 生成主窗口，用win_Truth表示，后面就在win_Truth操作
    # 设置窗口大小和位置
    win_Truth.geometry('550x500+400+100')  # 指定主框体大小
    # 不允许改变窗口大小
    win_Truth.resizable(False, False)  # 框体大小可调性，分别表示x,y方向的可变性；
    # 设置窗口标题
    win_Truth.title('真值表计算器')
    win_Truth.configure(background='Gainsboro')
    w = Label(win_Truth, fg='black', text=right, font=('Arial', 12), justify="right", bg="Gainsboro")
    w.pack(side='bottom')

    CheckVar_select = IntVar()
    CheckVar_fill = IntVar()
    radio = IntVar()
    # 文本框和按钮都是tkinter中的组件
    # Entry        　　 文本框（单行）；
    # Button        　　按钮；
    # 放置用来显示信息的文本框，设置为只读
    # tkinter.StringVar    能自动刷新的字符串变量，可用set和get方法进行传值和取值

    contentVar = StringVar(win_Truth, '')
    contentEntry = Entry(win_Truth, textvariable=contentVar, fg='Chocolate',font=('Arial', 18))  # 括号里面，可见第一个都是win_Truth,即表示都是以win_Truth为主界面的，将文本框中的内容存在contentVar中
    contentEntry.place(x=10, y=10, width=530, height=60)  # 文本框在win_Truth主界面的xy坐标位置，以及文本框自生的宽和高

    btnClear = Button(win_Truth, text='清除', bg='red', font=('楷体', 16), command=lambda: buttonClik('clear'))
    btnClear.place(x=60, y=100, width=80, height=40)

    btnBackspace = Button(win_Truth, text='退格', bg='red', font=('楷体', 16), command=lambda: buttonClik('Backspace'))
    btnBackspace.place(x=230, y=100, width=80, height=40)

    btnCompute =Button(win_Truth, text='=', bg='yellow', font=('Arial', 16), command=lambda: buttonClik('='))
    btnCompute.place(x=400, y=100, width=80, height=40)

    digits = list('ABCDE')  # 序列list是Python中最基本的数据结构。序列中的每个元素都分配一个数字 - 它的位置，或索引，第一个索引是0，第二个索引是1，依此类推。
    for col in range(5):
        d = digits[col]  # 按索引从list中取值，和c语言中的数组类似
        btnDigit =Button(win_Truth, text=d, font=('Arial', 16), bg='PaleVioletRed',command=lambda x=d: buttonClik(x))  # 和上面的是类似的
        btnDigit.place(x=20 + col * 110, y=170, width=70, height=40)  # 很显然，每次放一个按钮的位置是不一样的，但是它们之间的关系时确定的

    brackets = ['(', ')']
    for col in range(2):
        d = brackets[col]
        btnDigit = Button(win_Truth, text=d, font=('楷体', 16), bg='orange',command=lambda x=d: buttonClik(x))  # 创建的过程和上面类似
        btnDigit.place(x=20 + col * 110, y=330, width=70, height=40)

    # 放置运算符按钮
    operators = ('+', '*', '!', '@')  # Python的元组与列表类似，不同之处在于元组的元素不能修改。
    operators_show = ('或', '与', '非', '异或')
    # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
    for index, operator in enumerate(operators):
        btnOperator =Button(win_Truth, text=operators_show[index], font=('楷体', 16), bg='orange',
                                     command=lambda x=operator: buttonClik(x))  # 创建的过程和上面类似
        btnOperator.place(x=20 + index * 110, y=250, width=70, height=40)

    def callback():

        if CheckVar_select.get()== 1:
            radio1.place(x=160,y=400,width=120,height=30)
            radio2.place(x=160,y=440, width=120, height=30)
            C_fill.place(x=402, y=400, width=120, height=30)
        elif CheckVar_select.get()==0:
            radio1.place_forget()
            radio2.place_forget()
            C_fill.place_forget()

    btnOperator = Button(win_Truth, text='同或', font=('楷体', 16), bg='orange', command=lambda x='info':buttonClik(x))  # 创建的过程和上面类似
    btnOperator.place(x=20 + 4 * 110, y=250, width=70, height=40)


    radio1 = Radiobutton(win_Truth, text='最大项卡诺图', bg='Gainsboro', value=0, variable=radio)
    radio2 = Radiobutton(win_Truth, text='最小项卡诺图', bg='Gainsboro', value=1, variable=radio)
    C_fill = Checkbutton(win_Truth, text="是否填充", bg='Gainsboro', variable=CheckVar_fill, onvalue=1, offvalue=0,
                         height=5,width=20)

    C_select = Checkbutton(win_Truth, text="是否生成卡诺图", bg='Gainsboro', variable=CheckVar_select, onvalue=1, offvalue=0, height=5,
                     width=20,command=callback)
    C_select.place(x=20, y=400, width=120, height=30)

    btn_truth=Button(win_Truth, text='卡诺图计算器', fg='black',font=('楷体', 18),bg='darkcyan',command=lambda x='switch':buttonClik(x))  # 创建的过程和上面类似
    btn_truth.place(x=280, y=330, width=200, height=40)
    win_Truth.mainloop()


Truth_tab()
