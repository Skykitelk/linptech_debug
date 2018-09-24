from tkinter import ttk
import tkinter as tk
import constant as CON

class SinglePage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.root=root
		self.create_widgets()

	def create_widgets(self):
		# config
		config_lf=ttk.LabelFrame(self,text="设置")
		config_lf.grid(row=0,column=0,padx=15,pady=4,sticky="w")
		self.is_listen = tk.IntVar() 
		listen_check = ttk.Checkbutton(config_lf, text="监听ID",width=10,variable=self.is_listen)
		listen_check.grid(row=0,column=0,)
		ttk.Label(config_lf,text="监听RSSI阈值：").grid(row=0,column=1)
		self.rssi_threshold = tk.IntVar()
		spin = tk.Spinbox(config_lf, from_=40,to=120,width=3,textvariable=self.rssi_threshold,wrap=True) 
		spin.grid(row=0,column=2)

		# 单个配对
		single_lf=ttk.LabelFrame(self, text='单个调试配对')
		single_lf.grid(column=0, row=2,padx=15,pady=4,sticky="w")

		self.receiver_id=tk.StringVar()
		self.receiver_type=tk.StringVar()
		self.receiver_channel=tk.StringVar()
		self.receiver_rssi=tk.StringVar()
		ttk.Label(single_lf,text="接收器ID").grid(row=0,column=0,sticky='e')
		ttk.Entry(single_lf,textvariable=self.receiver_id,width=8).grid(row=0,column=1)
		ttk.Label(single_lf,text="接收器类型值").grid(row=0,column=2,sticky='e')
		ttk.Combobox(single_lf,values=list(CON.receiver_type.values()),textvariable=self.receiver_type,width=3).grid(row=0,column=3)
		ttk.Label(single_lf,text="接收器通道值").grid(row=0,column=4,sticky='e')
		ttk.Combobox(single_lf,values=list(CON.receiver_channel.values()),textvariable=self.receiver_channel,width=3).grid(row=0,column=5)
		ttk.Label(single_lf,text="接收器信号强度").grid(row=0,column=6,sticky='e')
		ttk.Entry(single_lf,textvariable=self.receiver_rssi,width=3).grid(row=0,column=7)
		
		self.transmit_id=tk.StringVar()
		self.transmit_type=tk.StringVar()
		self.transmit_channel=tk.StringVar()
		self.transmit_rssi=tk.StringVar()
		ttk.Label(single_lf,text="发射器ID").grid(row=1,column=0,sticky='e')
		ttk.Entry(single_lf,textvariable=self.transmit_id,width=8).grid(row=1,column=1)
		ttk.Label(single_lf,text="发射器类型值").grid(row=1,column=2,sticky='e')
		ttk.Combobox(single_lf,values=list(CON.transmit_type.values()),textvariable=self.transmit_type,width=3).grid(row=1,column=3)
		ttk.Label(single_lf,text="发射器通道值").grid(row=1,column=4,sticky='e')
		ttk.Combobox(single_lf,values=list(CON.transmit_channel.values()),textvariable=self.transmit_channel,width=3).grid(row=1,column=5)
		ttk.Label(single_lf,text="发射器信号强度").grid(row=1,column=6,sticky='e')
		ttk.Entry(single_lf,textvariable=self.transmit_rssi,width=3).grid(row=1,column=7)

		ttk.Button(single_lf,text="打开接收器",command=self.receiver_open).grid(row=3,column=0,columnspan=2,sticky='we')
		ttk.Button(single_lf,text="关闭接收器",command=self.receiver_close).grid(row=3,column=2,columnspan=2,sticky='we')
		ttk.Button(single_lf,text="清除所有ID",command=self.receiver_clear).grid(row=3,column=4,columnspan=2,sticky='we')

		ttk.Button(single_lf,text="发射打开信号",command=self.transmit_open).grid(row=4,column=0,columnspan=2,sticky='we')
		ttk.Button(single_lf,text="发射关闭信号",command=self.transmit_close).grid(row=4,column=2,columnspan=2,sticky='we')
		ttk.Button(single_lf,text="清除当前ID",command=self.receiver_clear_one).grid(row=4,column=4,columnspan=2,sticky='we')
		ttk.Button(single_lf,text="配对",command=self.pair_one).grid(row=3,column=6,rowspan=2,columnspan=2,sticky="nswe")
		
		# log
		self.log=tk.StringVar()
		ttk.Label(self,textvariable=self.log).grid(column=0,row=4,columnspan=8,sticky='s')

	def receiver_open(self):
		if CON.hex8_pattern.match(self.receiver_id.get()):
			data=CON.packet_type["operate_state"]+\
				self.receiver_id.get()+\
				self.receiver_type.get()+\
				CON.cmd_type["control_state"]+\
				self.receiver_channel.get()+\
				CON.receiver_state["ON"]
			self.root.send(data)
			self.log.set("操作：打开接收器"+self.receiver_id.get())
		else:
			tk.messagebox.showerror("错误", "接收器id错误")
		
	def receiver_close(self):
		pass
	
	def receiver_clear(self):
		pass
	
	def receiver_clear_one(self):
		pass

	def transmit_open(self):
		pass
	
	def transmit_close(self):
		pass

	def pair_one(self):
		pass

	
	def receive(self):
		pass

if __name__ == "__main__":
	root=tk.Tk()
	import tkinter.font as tkFont

	default_font = tkFont.nametofont("TkDefaultFont")
	default_font.configure(size=15)
	root.option_add("*Font", default_font)

	# 多页面table设置
	table = ttk.Notebook(root)
	table.pack(expand=1, fill="both",side="top")
	single_table = SinglePage(table,root)
	table.add(single_table,text="单个调试")
	def closeWindow():
		root.destroy()
	root.protocol('WM_DELETE_WINDOW', closeWindow) 
	root.mainloop()