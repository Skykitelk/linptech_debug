from tkinter import ttk
import tkinter as tk
import constant as CON
import tkinter.messagebox
import xlwt

class RecordPage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.ids=[]
		self.create_widgets()

	def create_widgets(self):
		# 设备
		device_lf=ttk.LabelFrame(self, text='设备')
		device_lf.grid(column=0, row=0,padx=15,pady=4,sticky='w')

		self.device_id=tk.StringVar()
		self.device_type=tk.StringVar()
		self.device_channel=tk.StringVar()
		self.is_listen= tk.IntVar()
		self.rssi_threshold = tk.IntVar()
		self.device_sn=tk.StringVar()

		listen_check = ttk.Checkbutton(device_lf, text="监听设备",variable=self.is_listen)
		listen_check.grid(row=0,column=0)
		ttk.Label(device_lf,text="RSSI阈值:").grid(row=0,column=1,sticky='e')
		spin = tk.Spinbox(device_lf, from_=40,to=120,textvariable=self.rssi_threshold) 
		spin.grid(row=0,column=2)

		ttk.Label(device_lf,text="设备ID").grid(row=1,column=0)
		ttk.Entry(device_lf,textvariable=self.device_id).grid(row=1,column=1)

		ttk.Label(device_lf,text="设备类型值").grid(row=1,column=2,sticky='e')
		
		ttk.Combobox(device_lf,values=list(CON.transmit_type.values())+list(CON.receiver_type.values()),textvariable=self.device_type).grid(row=1,column=3)

		ttk.Label(device_lf,text="设备通道值").grid(row=1,column=4,sticky='e')
		ttk.Combobox(device_lf,values=list(CON.receiver_channel.values()),textvariable=self.device_channel).grid(row=1,column=5)

		ttk.Label(device_lf,text="设备编号").grid(row=2,column=0)
		ttk.Entry(device_lf,textvariable=self.device_sn).grid(row=2,column=1)
		ttk.Button(device_lf,text="保存记录",command=self.save_device).grid(row=2,column=2)

		# treeview
		record_lf = ttk.LabelFrame(self, text='记录')
		record_lf.grid(column=0, row=1, padx=15,pady=4,sticky='w')

		self.record_table=ttk.Treeview(record_lf, show="headings",height=18, \
					columns=("sn","id","type","channel"))
		self.vbar = ttk.Scrollbar(self.record_table, orient=tk.VERTICAL, command=self.record_table.yview)
		# 定义树形结构与滚动条
		self.record_table.configure(yscrollcommand=self.vbar.set)
		self.record_table.grid(row=0,column=0,columnspan=10)
		self.record_table.column("sn",  anchor="center")
		self.record_table.heading("sn", text="标签名")
		self.record_table.column("id", anchor="center")
		self.record_table.heading("id", text="设备ID")
		self.record_table.column("type", anchor="center")
		self.record_table.heading("type", text="设备类型值")
		self.record_table.column("channel", anchor="center")
		self.record_table.heading("channel", text="设备通道值/键值")

		self.record_numbers=tk.StringVar()
		ttk.Label(record_lf,textvariable=self.record_numbers).grid(row=1,column=0)
		ttk.Button(record_lf,text="删除行",command=self.remove_record).grid(row=1,column=1)
		ttk.Button(record_lf,text="保存为Excel",command=self.save_excel).grid(row=1,column=2)

	
	def listen(self,data,optional):
		if data[10:12] in list(CON.transmit_type.values())+list(CON.receiver_type.values()):
			if int(optional[0:2],16) < int(self.rssi_threshold.get()):
				self.device_id.set(data[2:10])
				self.device_type.set(data[10:12])
				self.device_channel.set(data[12:14])

	def save_device(self):
		if self.device_sn.get() and self.device_id.get() and self.device_type.get() and self.device_channel.get():
			if self.device_id.get() in self.ids:
				tk.messagebox.showerror("错误", "id重复")
			else:
				self.ids.append(self.device_id.get())
				values=(self.device_sn.get(),self.device_id.get(),self.device_type.get(),self.device_channel.get())
				print(values)
				self.record_table.insert("" ,"end",values=values)
				self.record_numbers.set(len(self.record_table.get_children()))
		else:
			tk.messagebox.showerror("错误","信息不全")
	
	def remove_record(self):
		try:
			select_item = self.record_table.focus()
			select_item_id=self.record_table.item(select_item)["values"][1]
			self.record_table.delete(select_item)
			self.ids.remove(select_item_id)
			self.record_numbers.set(len(self.record_table.get_children()))
		except:
			pass
	def save_excel(self):
		import tkinter.filedialog
		filename=tkinter.filedialog.asksaveasfilename(filetypes=[("excel格式","xlsx"),("excel格式","xls")])
		wbk = xlwt.Workbook()
		sheet = wbk.add_sheet('sheet 1')
		# indexing is zero based, row then column
		items=self.record_table.get_children()
		for i in range(len(items)):
			values=self.record_table.item(items[i])['values']
			values[1]="{0:>08}".format(values[1])
			values[2]="{0:>02}".format(values[2])
			values[3]="{0:>02}".format(values[3])
			print(values)
			for j in range(len(values)):
				sheet.write(i,j,values[j])
		if filename.endswith('.xls'):
			wbk.save(filename)
		else:
			wbk.save(filename+'.xls')

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