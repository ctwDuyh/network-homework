from socket import*
from _thread import*

from tkinter import *
from time import *
def createqipan():
    global qipan
    # 生成棋盘
    qipan = Canvas(window, height=600, width=600, bg='white')
    # 生成棋盘框架
    for i in range(9, 12):
        qipan.create_line(10, i, 590, i)  # 生成
        qipan.create_line(i, 10, i, 590)  # 棋盘
        qipan.create_line(10, 580 + i, 590, 580 + i)  # 外围
        qipan.create_line(580 + i, 10, 580 + i, 590)  # 边框
    # 生成棋盘细节
    x = 55;
    y = 55;
    i = 1
    while (x < 550):
        qipan.create_line(x, 55, x, 545)  # 利用循
        qipan.create_line(55, y, 545, y)  # 环生成
        qipan.create_text(x, 565, text=str(i))  # 整个棋
        qipan.create_text(35, y, text=str(16 - i))  # 盘布局
        x += 35;
        y += 35;
        i += 1
        if i in [4, 12, 8]:
            qipan.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')  # 生成棋盘
            qipan.create_oval(x - 5, 595 - y, x + 5, 605 - y, fill='black')  # 上的‘星’
    qipan.pack(side='left')
def createguangbiao():
        # 初始化
        global gb1, gb2, gb3, gb4, gb5, gb6, gb7, gb8, x0, y0
        x0 = 300;
        y0 = 300
        gb1 = qipan.create_line(x0 - 5, y0 - 5, x0 - 5, y0 - 18, fill='purple')  # 生
        gb2 = qipan.create_line(x0 - 5, y0 - 5, x0 - 19, y0 - 5, fill='purple')
        gb3 = qipan.create_line(x0 + 5, y0 + 5, x0 + 5, y0 + 19, fill='purple')  # 成
        gb4 = qipan.create_line(x0 + 5, y0 + 5, x0 + 19, y0 + 5, fill='purple')
        gb5 = qipan.create_line(x0 - 5, y0 + 5, x0 - 5, y0 + 19, fill='purple')  # 光
        gb6 = qipan.create_line(x0 - 5, y0 + 5, x0 - 19, y0 + 5, fill='purple')
        gb7 = qipan.create_line(x0 + 5, y0 - 5, x0 + 5, y0 - 19, fill='purple')  # 标
        gb8 = qipan.create_line(x0 + 5, y0 - 5, x0 + 19, y0 - 5, fill='purple')
def judgekey(event):
    global x0,y0,p,pd
    if pd==0:
     if event.keycode==13:
        x_=int((x0-55)/35); y_=int((y0-55)/35)
        if p==1:
            if player_[x_][y_]==0 and player[x_][y_]==0:
                player[x_][y_]=1#改变玩家1的对局信息
                placeqizi(x0,y0,'white')
                p = 0
                sendinformation()
                show.set("当前轮到对方下子")

        if checkwin(int((x0-55)/35),int((y0-55)/35),p):#判断是否有人胜利
            x0=-1;y0=-1;p=-1
            sleep(0.1)
            sendinformation()
            client_.close()
            show.set("您取得胜利!")
            pd=1
            message=Tk()
            message.geometry('100x100')
            message.maxsize(100,100)
            Label(message,text='您获得胜利').pack()
            Button(message,text='退出程序',command=exit).pack()
     elif event.keycode==37:#键盘按键如果为Left
        if (x0-35<55):#判断光标移动是否要超出棋盘界限
            moveguangbiao(490,0)#如果要超出则移动至对侧
            x0+=490
        else:
            moveguangbiao(-35,0)#否则正常移动
            x0 -= 35
     elif event.keycode==38:#键盘按键如果为Up
        if y0-35<55:#判断光标移动是否要超出棋盘界限
            moveguangbiao(0,490)#如果要超出则移动至对侧
            y0+=490
        else:
            moveguangbiao(0,-35)#否则正常移动
            y0-=35
     elif event.keycode==39:#键盘按键如果为Right
        if x0+35>545:#判断光标移动是否要超出棋盘界限
            moveguangbiao(-490,0)#如果要超出则移动至对侧
            x0-=490
        else:
            moveguangbiao(35,0)#否则正常移动
            x0+=35
     elif event.keycode==40:#键盘按键如果为Down
        if y0+35>545:#判断光标移动是否要超出棋盘界限
            moveguangbiao(0,-490)#如果要超出则移动至对侧
            y0-=490
        else:
            moveguangbiao(0,35)#否则正常移动
            y0+=35
def run():
    global prevent,pd,show
    pd=0
    if prevent==0:
        createqipan()#创建棋盘
            # 获得键盘活动
        qipan.bind('<KeyPress>', judgekey)
            # 获得焦点
        qipan.focus_set()
        createguangbiao()
        prevent=1
        start_new_thread(recvinformation, ())
        #Button(window,text='重新开始',command=restart,bg='white',height=8,width=20).place(x=620,y=200)
def sendinformation():
    global x0,y0,p,client_
    x_ = str(x0)
    y_ = str(y0)
    p_ = str(p)
    client_.send(x_.encode())
    sleep(0.3)
    client_.send(y_.encode())
    sleep(0.3)
    client_.send(p_.encode())
def placeqizi(x,y,color):
    global qipan
    qipan.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color)  # 生成棋子
def client():
    global p,client_,input_2
    client_ = socket(AF_INET, SOCK_STREAM)
    host=input_2.get()
    client_.connect((host,9999))

    main()
def recvinformation():
    global p,client_,pd,show
    while True:
        x = int(client_.recv(1024).decode())
        sleep(0.3)
        y = int(client_.recv(1024).decode())
        sleep(0.3)
        p = int(client_.recv(1024).decode())
        if x==0 and y==0 and p==0:
            st.set('游戏已开始')
            show = StringVar()
            show.set('当前轮到对方下子')
            showplayer = Label(window, textvariable=show)
            showplayer.place(x=620, y=100)
            sleep(0.3)
        elif x==-1 and y==-1 and p==-1:
            pd=1
            show.set("对方取得胜利!")
            client_.close()
        else:
            placeqizi(x, y, 'black')
            player_[int((x - 55) / 35)][int((y - 55) / 35)] = 1
            show.set("当前轮到您下子")
            sleep(0.3)
def moveguangbiao(x,y):
    qipan.move(gb1, x, y)
    qipan.move(gb2, x, y)
    qipan.move(gb3, x, y)
    qipan.move(gb4, x, y)
    qipan.move(gb5, x, y)
    qipan.move(gb6, x, y)
    qipan.move(gb7, x, y)
    qipan.move(gb8, x, y)
def checkwin(xPoint,yPoint,p):
    #检查行
        #定义计数变量count
        count=0
        x = xPoint
        y = yPoint
        while player[x][y]!=0:
                count+=1
                if x-1<0:
                    break
                else:
                    x-=1
        x = xPoint
        y = yPoint
        while player[x][y]!=0:
            count+=1
            if x+1>14:
                break
            else:
                x+=1
        if count>5: return True
    #检查列
        count=0
        x = xPoint
        y = yPoint
        while player[x][y] != 0:
                count += 1
                if y-1<0:
                    break
                else:
                    y -= 1
        x = xPoint
        y = yPoint
        while player[x][y] != 0:
                count += 1
                if y+1>14:
                    break
                else:y+=1

        if count>5:return True
    #检查主对角线

        count=0
        x = xPoint
        y = yPoint
        while player[x][y] != 0:
                count += 1
                if y-1<0 or x-1<0:
                    break
                else:
                    y-= 1
                    x-=1
        x = xPoint
        y = yPoint
        while player[x][y] != 0:
                count += 1
                if y+1>14 or x+1>14:
                    break
                else:
                    y += 1
                    x+=1

        if count>5:return True
    #检查次对角线

        count=0
        x = xPoint
        y = yPoint
        while player[x][y] != 0:
                count += 1
                if y-1<0 or x+1>14:
                    break
                else:
                    y-= 1
                    x+=1
        x = xPoint
        y = yPoint
        while player[x][y] != 0:
                count += 1
                if y+1>14 or x-1<0:
                    break
                else:
                    y += 1
                    x-=1
        if count>5:return True
def main():
    global window,p,prevent,player,player_,st
    input_2.destroy()
    input_1.destroy()
    button0.destroy()
    window.geometry("800x600")
    window.maxsize(800, 600)
    player = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    player_ = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    p = 0
    prevent = 0
    Label(window, text='------已连接玩家------\n方向键移动光标，回车键下子').place(x=620,y=10)
    st=StringVar()
    st.set("等待对方开始游戏——")
    Label(window,textvariable=st).place(x=620,y=50)
    run()
def first():
    global window,input_2,input_1,button0
    window = Tk()
    window.geometry("200x100")
    window.title("五子棋联机版客户端----------by 杜宇航")
    input_1 = Label(window, text='请输入您要连接的主机名：')
    input_2 = Entry(window)
    button0 = Button(window, text='输入完毕', command=client)
    input_1.pack()
    input_2.pack()
    button0.pack()
    mainloop()
first()









