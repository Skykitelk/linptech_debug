# coding=utf-8
import tkinter as tk
import datetime
import os
import tkinter.messagebox
import time
import serial.tools.list_ports
from tkinter import ttk
import time
import re
import xlrd
from batch_page import BatchPage
from single_page import SinglePage
from graphic_page import GraphicPage

class App(tk.Tk):

	def __init__(self):
		super().__init__()
		self.geometry('600x700')  
		# self.iconbitmap(default="kankan_01.ico")
		self.wm_title("多页面测试程序")

		table = ttk.Notebook(self)
		table.pack(expand=1, fill="both",side="top")
		single_table = SinglePage(table,self)
		table.add(single_table,text="单个调试")
		batch_table = BatchPage(table,self)
		table.add(batch_table,text="批量调试")
		graphic_table=GraphicPage(table,self)
		table.add(graphic_table,text="图形操作")



if __name__ == '__main__':
	app = App()
	def closeWindow():
		app.destroy()
	app.protocol('WM_DELETE_WINDOW', closeWindow) 
	app.mainloop()