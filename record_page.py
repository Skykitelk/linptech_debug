from tkinter import ttk
import tkinter as tk
import constant as CON

class RecordPage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.create_widgets()

	def create_widgets(self):
		# 接收器
		receiver_lf=ttk.LabelFrame(self, text='接收器')
		receiver_lf.grid(column=0, row=0,padx=15,pady=4,sticky="w")

		self.receiver_id=tk.StringVar()
		self.receiver_type=tk.StringVar()
		self.receiver_channel=tk.StringVar()
		self.is_listen_receiver = tk.IntVar()
		self.rssi_threshold = tk.IntVar()
		self.receiver_sn=tk.StringVar()

		listen_check = ttk.Checkbutton(receiver_lf, text="监听接收器",width=10,variable=self.is_listen_receiver)
		listen_check.grid(row=0,column=0,)
		ttk.Label(receiver_lf,text="RSSI阈值：").grid(row=0,column=1)
		spin = tk.Spinbox(receiver_lf, from_=40,to=120,width=3,textvariable=self.rssi_threshold,wrap=True) 
		spin.grid(row=0,column=2)
		ttk.Label(receiver_lf,text="接收器ID").grid(row=0,column=3,sticky='e')
		ttk.Entry(receiver_lf,textvariable=self.receiver_id,width=8).grid(row=0,column=4)
		ttk.Label(receiver_lf,text="接收器类型值").grid(row=0,column=5,sticky='e')
		ttk.Combobox(receiver_lf,values=list(CON.receiver_type.values()),textvariable=self.receiver_type,width=3).grid(row=0,column=6)
		ttk.Label(receiver_lf,text="接收器通道值").grid(row=0,column=7,sticky='e')
		ttk.Combobox(receiver_lf,values=list(CON.receiver_channel.values()),textvariable=self.receiver_channel,width=3).grid(row=0,column=8)
		ttk.Label(receiver_lf,text="输入接收器编号").grid(row=0,column=9,sticky='e')
		ttk.Entry(receiver_lf,textvariable=self.receiver_sn).grid(row=0,column=10)
		ttk.Button(receiver_lf,text="保存记录",command=self.save_receiver).grid(row=0,column=11,sticky='we')

		# 开关
		transmit_lf=ttk.LabelFrame(self, text='开关')
		transmit_lf.grid(column=0, row=1,padx=15,pady=4,sticky="w")

		self.transmit_id=tk.StringVar()
		self.transmit_type=tk.StringVar()
		self.transmit_channel=tk.StringVar()
		self.is_listen_transmit = tk.IntVar()
		self.rssi_threshold = tk.IntVar()
		self.transmit_sn=tk.StringVar()

		listen_check = ttk.Checkbutton(transmit_lf, text="监听开关",width=10,variable=self.is_listen_transmit)
		listen_check.grid(row=0,column=0,)
		ttk.Label(transmit_lf,text="RSSI阈值：").grid(row=0,column=1)
		spin = tk.Spinbox(transmit_lf, from_=40,to=120,width=3,textvariable=self.rssi_threshold,wrap=True) 
		spin.grid(row=0,column=2)
		ttk.Label(transmit_lf,text="开关ID").grid(row=0,column=3,sticky='e')
		ttk.Entry(transmit_lf,textvariable=self.transmit_id,width=8).grid(row=0,column=4)
		ttk.Label(transmit_lf,text="开关类型值").grid(row=0,column=5,sticky='e')
		ttk.Combobox(transmit_lf,values=list(CON.transmit_type.values()),textvariable=self.transmit_type,width=3).grid(row=0,column=6)
		ttk.Label(transmit_lf,text="开关通道值").grid(row=0,column=7,sticky='e')
		ttk.Combobox(transmit_lf,values=list(CON.transmit_channel.values()),textvariable=self.transmit_channel,width=3).grid(row=0,column=8)
		ttk.Label(transmit_lf,text="输入开关编号").grid(row=0,column=9,sticky='e')
		ttk.Entry(transmit_lf,textvariable=self.transmit_sn).grid(row=0,column=10)
		ttk.Button(transmit_lf,text="保存记录",command=self.save_transmit).grid(row=0,column=11,sticky='we')
	
	def save_receiver(self):
		pass
	
	def save_transmit(self):
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
	record_table = RecordPage(table,root)
	table.add(record_table,text="生产记录")
	def closeWindow():
		root.destroy()
	root.protocol('WM_DELETE_WINDOW', closeWindow) 
	root.mainloop()