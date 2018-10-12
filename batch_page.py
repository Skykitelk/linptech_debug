from tkinter import ttk
import tkinter as tk
import xlrd
import constant as CON
import tkinter.messagebox
import logging


class BatchPage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.createWidgets()

	def createWidgets(self):

		self.file_name=tk.StringVar()
		batch_lf=ttk.LabelFrame(self, text="批量配对调试")
		batch_lf.grid(column=0, row=0,padx=15,pady=4)
		ttk.Label(batch_lf,text="配对EXCEL文件：").grid(row=0,column=0)
		ttk.Entry(batch_lf,textvariable=self.file_name,width=40).grid(row=0,column=1,columnspan=3,sticky="we")
		ttk.Button(batch_lf,text="选取文件",command=self.get_file).grid(row=0,column=4)
		

		# treeview
		self.pair_table=ttk.Treeview(batch_lf, show="headings", height=18, \
					columns=("receiver_sn","receiver_id","receiver_type","receiver_channel",\
					 "transmit_sn","transmit_id","transmit_type", "transmit_channel","pair_state","rssi"))
		self.vbar = ttk.Scrollbar(batch_lf, orient=tk.VERTICAL, command=self.pair_table.yview)
		# 定义树形结构与滚动条
		self.pair_table.configure(yscrollcommand=self.vbar.set)
 
		self.pair_table.grid(row=1,column=0,columnspan=5)
		self.pair_table.column("receiver_sn", width=80, anchor="center")
		self.pair_table.heading("receiver_sn", text="接收器标签")
		self.pair_table.column("receiver_id", width=80, anchor="center")
		self.pair_table.heading("receiver_id", text="接收器ID")
		self.pair_table.column("receiver_type", width=80, anchor="center")
		self.pair_table.heading("receiver_type", text="接收器类型")
		self.pair_table.column("receiver_channel", width=80, anchor="center")
		self.pair_table.heading("receiver_channel", text="接收器通道")
		self.pair_table.column("transmit_sn", width=80, anchor="center")
		self.pair_table.heading("transmit_sn", text="开关标签")
		self.pair_table.column("transmit_id", width=80, anchor="center")
		self.pair_table.heading("transmit_id", text="开关ID")
		self.pair_table.column("transmit_type", width=80, anchor="center")
		self.pair_table.heading("transmit_type", text="开关类型")
		self.pair_table.column("transmit_channel", width=80, anchor="center")
		self.pair_table.heading("transmit_channel", text="开关通道")
		self.pair_table.column("pair_state", width=80, anchor="center")
		self.pair_table.heading("pair_state", text="配对状态")
		self.pair_table.column("rssi", width=80, anchor="center")
		self.pair_table.heading("rssi", text="信号强度")

		ttk.Button(batch_lf,text="批量配对",state="disabled",command=self.batch_pair).grid(row=2,column=0)


		# log
		self.log=tk.StringVar()
		ttk.Label(self,textvariable=self.log).grid(column=0,row=3,columnspan=5,sticky='s')
	
	def get_file(self):

		import tkinter.filedialog
		filename=tkinter.filedialog.askopenfilename(filetypes=[("excel格式","xlsx"),("excel格式","xls")])
		self.file_name.set(filename)
		self.read_xls(filename)

	def read_xls(self,filename):
		self.log.set("读取"+filename.split('/')[-1])
		workbook = xlrd.open_workbook(filename)
		sheet = workbook.sheet_by_name(workbook.sheet_names()[0])
		receiver_ids = sheet.col_values(1)[1:]
		transmit_ids=sheet.col_values(5)[1:]
		# 检查id
		rid_row=0
		for rid in receiver_ids:
			rid_row+=1
			if not CON.hex8_pattern.match(rid.strip()):
				logging.error(rid.strip())
				tk.messagebox.showerror("错误", "接收器id错误:"+str(rid_row)+"行")
				break
		tid_row=0
		for tid in transmit_ids:
			tid_row+=1
			if not CON.hex8_pattern.match(tid.strip()):
				tk.messagebox.showerror("错误", "发射器id错误:"+str(tid_row)+"行")
				break
		for i in range(len(receiver_ids)):
			item = sheet.row_values(i+1)
			values=(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],"未配对","")
			self.pair_table.insert("" ,"end",values=values)
	def batch_pair(self):
		"""
		批量配对tree_view中的行
		并获取返回状态及返回的信号强度
		"""
		pass
		# receiver_ids_set=set(receiver_ids)
		# clear_num=0
		# for rid in receiver_ids_set:
		# 	clear_num += 1
		# 	self.add_log(str(clear_num)+"清除接收器"+rid+"上所有配对发射器")
		# 	m1="00080701"
		# 	m2="5d"+rid+"81090100000000000000"
		# 	message=self.generate_message(m1,m2)
		# 	self.send(message)

		# self.add_log("清除完毕！清除接收器数量"+str(clear_num))
		
		# self.add_log("!!!开始批量配对["+filename.split('/')[-1]+"]中配对关系")
		# pair_num=0
		# for i in range(len(receiver_ids)):
		# 	pairs = sheet.row_values(i+1)
		# 	print(pairs)
		# 	pair_num+=1
		# 	self.add_log(str(pair_num)+"：配对发射器"+pairs[0].strip() +"和接收器"+pairs[2].strip())
		# 	m1="000E0701"
		# 	m2="5d"+pairs[3].strip() +"810d010101"+pairs[1].strip() +"00000000000000"
		# 	message=self.generate_message(m1,m2)
		# 	self.send(message)
		# self.add_log("批量配对完毕！配对次数"+str(clear_num))

	
	
if __name__ == '__main__':
	root=tk.Tk()

	# default_font = tkFont.nametofont("TkDefaultFont")
	# default_font.configure(size=18)
	# self.option_add("*Font", default_font)

	# 多页面table设置
	table = ttk.Notebook(root)
	table.pack(expand=1, fill="both",side="top")
	single_table = BatchPage(table,root)
	table.add(single_table,text="批量调试")
	def closeWindow():
		root.destroy()
	root.protocol('WM_DELETE_WINDOW', closeWindow) 
	root.mainloop()
