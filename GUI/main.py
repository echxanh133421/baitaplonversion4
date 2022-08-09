

from modul1 import *
import serial
import serial.tools.list_ports
import threading
import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv

#biến

list_excel=[]

red=0
green=0
blue=0
bien_bat_tat=0
# sum=0

#các hàm xử lí

# def draw(red,green,blue):
#     x=np.array(['RED','GREEN','BLUE'])
#     y=np.array([red,green,blue])
#     plt.bar(x,y)
#     plt.show()

def tinh_giay(list_time):
    time= int(list_time[0])*3600+int(list_time[1])*60+int(list_time[2])
    return time


def xu_li_nang_xuat(list_excel):
    list_a=list_excel[0].split(':')
    list_b=list_excel[1].split(':')

    time=(tinh_giay(list_b)-tinh_giay(list_a))
    nang_xuat=int(list_excel[5]/time*3600)
    return nang_xuat


#bật tắt động cơ arduino
def dc_on():
    global bien_bat_tat,arduino,red,blue,green,sum
    if bien_bat_tat==0:
      arduino.write(get_current_value().encode())
      bien_bat_tat = 1

    sum=red+blue+green
    if sum==0 and list_excel==[]:
        now=datetime.datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        list_excel.append(dt_string)


#truyền giá trị 0 cho arduino
def dc_off():
    global bien_bat_tat,arduino
    bien_bat_tat=0
    # current_value.set(0)
    arduino.write(b'0')
    # current_value.set(127)
    # value_label.configure(text=get_current_value())

#truyền giá trị hiện tại thanh slider cho arduino
def button_speed_click():
    global bien_bat_tat,arduino
    if bien_bat_tat==1:
     arduino.write(get_current_value().encode())


def update_text_count_color(color,color_label):
   # Configuring the text in Label widget
   color_label.configure(text=str(color))

def update_text_count_sum(red,green,blue):
    global sum_label
    sum_label.configure(text=str(red + green + blue))

def button_reset_click():
    global red,green,blue,list_excel
    current_value.set(127)
    value_label.configure(text=get_current_value())
    # button_speed_click()

    #ghi data lại file excel
    #bao gồm ghi các giá trị số lượng
    #tính sản lượng

    '''
    1:điều kiện mong muốn: khi bấm nút reset thì sẽ cập nhật và tính toán giá trị sản lượng vào file excel
    2: cụ thể:
    -khí nhấn nút start và đồng thời các label đếm số lượng sản phảm bằng 0 thì ghi thời gian vào thời gian bắt đầu của file excel
    +hàm trong nút start tức hàm dc-on()
    -khi nhất nút reset và đồng thời các label đếm số lượng sản phẩm khác 0 thì:
    +ghi vào thời gian hiện tại vào list_excel, red,green,blue,sum
    
    tính tổng sản lượng, tính thời gian, tính năng xuất
    #
    '''
    now = datetime.datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    list_excel.append(dt_string)
    list_excel.append(red)
    list_excel.append(blue)
    list_excel.append(green)
    list_excel.append(red+blue+green)

    nang_xuat=xu_li_nang_xuat(list_excel)
    list_excel.append(nang_xuat)


    #viết vào file excel
    print(list_excel)
    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(list_excel)
    list_excel=[]

    red=0
    green=0
    blue=0
    # sum=0
    update_text_count_color(red, red_label)
    update_text_count_color(green, green_label)
    update_text_count_color(blue, blue_label)
    update_text_count_sum(red,green,blue)
    dc_off()




def get_current_value():
    return '{0}'.format(current_value.get())

def slider_changed(event):
    value_label.configure(text=get_current_value())

def main():

    global app, connect_btn ,frame_bd,frame_com,refresh_btn
    global button_start, button_stop, button_reset, button_speed
    global red_label, green_label, blue_label, current_value, value_label,slider,sum_label

    app=App()

    # đầu trang:
    frame_top=frame(app,1,0)
    img=tk.PhotoImage(file='logoEn.png')
    label_logo=ttk.Label(frame_top,image=img)
    label_logo.grid()


    #phần tiêu đề tên GUI
    frame_main=frame(app,1,1)
    label_header=ttk.Label(frame_main,text='MÔ HÌNH PHÂN LOẠI SẢN PHẨM THEO MÀU SẮC')
    label_header.config(font=("Courier", 20))
    label_header.grid(pady=20)

    #label mục của 3 phần chính trong trang
    frame_control=frame(app,0,2)
    label_control=tk.Label(frame_control,text='ĐIỀU KHIỂN',bg='gray',height=3,width=20,fg='white')
    label_control.config(font=("Courier", 11))
    label_control.grid(pady=20)

    frame_count=frame(app,1,2)
    label_count=tk.Label(frame_count,text='PHÂN LOẠI',bg='gray',height=3,width=65,fg='white')
    label_count.config(font=("Courier", 11))
    label_count.grid(pady=20)

    frame_setting=frame(app,2,2)
    label_setting=tk.Label(frame_setting,text='KẾT NỐI',bg='gray',height=3,width=20,fg='white')
    label_setting.config(font=("Courier", 11))
    label_setting.grid(pady=20)

    # ĐIỀU KHIỂN
    frame_button_1 = frame(app, 0, 3)
    # frame_button.columnconfigure(0,weight=1)
    # frame_button.columnconfigure(1,weight=1)
    # frame_button.columnconfigure(2,weight=1)

    button_start = button(frame_button_1, 0, 0, 'START', 10, 7, 3, 20)
    button_start['command'] = dc_on
    frame_button_2 = frame(app, 0, 4)
    button_stop = button(frame_button_2, 0, 0, 'STOP', 10, 7, 3, 20)
    button_stop['command'] = dc_off
    frame_button_3 = frame(app, 0, 5)
    button_reset = button(frame_button_3, 0, 0, 'RESET', 10, 7, 3, 20)
    button_reset['command'] = button_reset_click
    frame_button_4 = frame(app, 0, 6)
    button_speed = button(frame_button_4, 0, 0, 'SPEED', 10, 7, 3, 20)
    button_speed['command'] = button_speed_click

    button_start['state'] = 'disable'
    button_stop['state'] = 'disable'
    button_speed['state'] = 'disable'
    button_reset['state'] = 'disable'

    # slider
    frame_button_5 = frame(app, 0, 7)
    current_value = tk.IntVar()
    current_value.set(127)
    slider = ttk.Scale(frame_button_5, from_=0, to=255, orient='horizontal', command=slider_changed,variable=current_value)
    slider.grid(column=0, row=4, sticky='we', pady=20)
    value_label = ttk.Label(frame_button_5, text=get_current_value())
    value_label.grid(column=0, row=5)

    # PHÂN LOẠI
    frame_color = frame(app, 1, 3, 2)
    frame_color.columnconfigure(0, weight=1)
    frame_color.columnconfigure(1, weight=1)
    frame_color.columnconfigure(2, weight=1)


    label_red = tk.Label(frame_color, bg='red', text='RED', fg='white', height=5, width=25)
    label_red.grid(column=0, row=0, padx=10, pady=7, rowspan=2)
    label_blue = tk.Label(frame_color, bg='blue', text='BLUE', fg='white', height=5, width=25)
    label_blue.grid(column=1, row=0, padx=10, pady=7, rowspan=2)
    label_green = tk.Label(frame_color, bg='green', text='GREEN', fg='white', height=5, width=25)
    label_green.grid(column=2, row=0, padx=10, pady=7, rowspan=2)

    # entry số lượng sản phẩm phân loại
    frame_count_color = frame(app, 1, 5)
    frame_count_color.columnconfigure(0, weight=1)
    frame_count_color.columnconfigure(1, weight=1)
    frame_count_color.columnconfigure(2, weight=1)
    red_label = tk.Label(frame_count_color, text='0', height=1,width=11)
    red_label.config(font=("Courier", 20))
    red_label.grid(column=0, row=0,padx=10, pady=7, rowspan=2)
    blue_label = tk.Label(frame_count_color, text='0', height=1,width=11)
    blue_label.config(font=("Courier", 20))
    blue_label.grid(column=1, row=0,padx=10, pady=7, rowspan=2)
    green_label = tk.Label(frame_count_color, text='0', height=1,width=11)
    green_label.config(font=("Courier", 20))
    green_label.grid(column=2, row=0,padx=10, pady=7, rowspan=2)

    frame_sum=frame(app,1,6)
    label_sum=tk.Label(frame_sum,text='SUM',height=3,width=80,bg='gray',fg='white')
    label_sum.grid()

    #entry label sum
    frame_sum_count=frame(app,1,7)
    sum_label=tk.Label(frame_sum_count,text='0',height=1,width=11)
    sum_label.config(font=("Courier", 20))
    sum_label.grid()

    #phần kết nối
    frame_reset_com=frame(app,2,5)
    refresh_btn = tk.Button(frame_reset_com, text="RESET_COM", height=3, width=20,command=update_coms)
    refresh_btn.grid()

    frame_connect=frame(app,2,6)
    connect_btn = tk.Button(frame_connect, text='CONNECT', height=3, width=20, state='disabled',command=connection)
    connect_btn.grid(padx=10,pady=7)

    #tạo frame chứa các thành phần option baud và option com
    frame_bd=frame(app,2,3)
    frame_com=frame(app,2,4)

    baud_select()
    update_coms()

    # footer:
    label_footer = tk.Label(app, text=str('Designer: Cương, Duy, Tuấn Anh'), bg='gray', fg='white', height=2, width=200)
    label_footer.grid(column=0, columnspan=3, row=8, pady=10)
    label_setting.config(font=("Courier", 10))

    app.mainloop()


def baud_select():
    global  clicked_bd,drop_bd
    clicked_bd=tk.StringVar()
    bds=['BAUD_SELECT','9600']
    clicked_bd.set(bds[0])
    drop_bd=tk.OptionMenu(frame_bd,clicked_bd,*bds,command=connect_check)
    drop_bd.config(width=18,height=3)
    drop_bd.grid()

def update_coms():
    global clicked_com,drop_com
    ports=serial.tools.list_ports.comports()
    coms=[com[0] for com in ports]
    try:
        drop_com.destroy()
    except:
        pass
    coms.insert(0, 'COM_SELECT')
    clicked_com = tk.StringVar()
    clicked_com.set(coms[0])

    drop_com = tk.OptionMenu(frame_com, clicked_com, *coms,command=connect_check)
    drop_com.config(width=18,height=3)
    drop_com.grid(pady=7)
    connect_check(0)

def connect_check(args):
    if 'COM_SELECT' in clicked_com.get() or 'BAUD_SELECT' in clicked_bd.get():
        connect_btn['state']='disable'
    else:
        connect_btn['state'] = 'active'

def connection():
    global arduino,serialData
    global button_start,button_stop, button_reset,button_speed
    global red,green,blue
    if connect_btn['text']=='DISCONNECT':
        connect_btn['text']='CONNECT'
        refresh_btn['state']='active'
        drop_bd['state']='active'
        drop_com['state']='active'
        dc_off()
        red = 0
        green = 0
        blue = 0
        # sum = 0
        update_text_count_color(red, red_label)
        update_text_count_color(green, green_label)
        update_text_count_color(blue, blue_label)
        update_text_count_sum(red, green, blue)

        current_value.set(127)
        value_label.configure(text=get_current_value())

        button_start['state']='disable'
        button_stop['state'] = 'disable'
        button_speed['state'] = 'disable'
        button_reset['state'] = 'disable'
        serialData=False
    else:
        serialData = True
        connect_btn['text']='DISCONNECT'
        refresh_btn['state'] = 'disable'
        drop_bd['state'] = 'disable'
        drop_com['state'] = 'disable'

        button_start['state']='active'
        button_stop['state'] = 'active'
        button_speed['state'] = 'active'
        button_reset['state'] = 'active'
        port=clicked_com.get()
        baud=clicked_bd.get()
        try:
            arduino = serial.Serial(port,baud,timeout=0)
        except:
            pass
        t1=threading.Thread(target=readSerial)
        t1.daemon=True
        t1.start()

def readSerial():
    global serialData,red,green,blue, arduino
    while serialData:
        data=arduino.readline()
        try:
            if len(data)>0:
                Data=data.decode('utf8')
                print(Data)
                if(Data=='red'):
                    red=red+1
                    update_text_count_color(red,red_label)
                elif(Data=='green'):
                    green=green+1
                    update_text_count_color(green,green_label)
                elif(Data=='blue'):
                    blue=blue+1
                    update_text_count_color(blue,blue_label)
                update_text_count_sum(red, green, blue)
                # draw(red, green, blue)
        except:
            pass

if __name__=="__main__":
    main()