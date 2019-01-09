# coding=utf-8
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import tkinter.messagebox
import datetime
import os
import time
import serial.tools.list_ports
from list_page import ListPage
import config as cfg
from linptech.constant import (SerialConfig,ReceiverChannel,ReceiverType,
TransmitType,TransmitChannel,PacketType,CmdType,State,BackState,SerialConfig)
from linptech.linptech_protocol import LinptechProtocol
import platform
import logging

logging.getLogger().setLevel(logging.DEBUG)
class App(tk.Tk):

	def __init__(self):
		super().__init__()
		self.geometry(cfg.WINDOWS_SZIE)
		self.wm_title(cfg.TITLE)
		default_font = tkFont.nametofont("TkDefaultFont")
		default_font.configure(family="Helvetica",size=14)
		self.option_add("*Font", default_font)

		table = ttk.Notebook(self)
		table.pack(expand=1, fill="both",side="top")
		self.list_page = ListPage(table,self)
		table.add(self.list_page,text="列表调试")

		# 串口设置
		if platform.system()=="Darwin":
			port=self.get_port()[-1]
		else:
			port=self.get_port()[0]
		self.lp=LinptechProtocol(port,receive=self.list_page.receive)

	def get_port(self):
		portList = list(serial.tools.list_ports.comports())
		portNameList = []
		for port in portList:
			portNameList.append(str(port[0]))
		logging.debug("portNameList=%s",portNameList)
		return portNameList

if __name__ == '__main__':
	app = App()
	def closeWindow():
		app.destroy()
	app.protocol('WM_DELETE_WINDOW', closeWindow) 
	app.mainloop()