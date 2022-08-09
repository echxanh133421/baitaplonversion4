
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Label

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Mô hình phân loại sản phẩm theo màu sắc')
        self.geometry('1200x670')
        self.resizable(False,False)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=2)
        self.columnconfigure(2,weight=1)



class frame(ttk.Frame):
    def __init__(self,container,c,r,rspan=1):
        super().__init__(container)
        self.grid(column=c,row=r,rowspan=rspan)
        

class button(tk.Button):
    def __init__(self,container,C,R,TXT,padx,pady,h,w):
        super().__init__(container)
        self['text']=TXT
        self['height']=h
        self['width']=w
        self.grid(column=C,row=R,padx=padx,pady=pady)

