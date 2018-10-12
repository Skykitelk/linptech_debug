from tkinter import ttk
import tkinter as tk
import xlrd
import constant as CON
import tkinter.messagebox
import logging
import xlwt
import tkinter.filedialog

class StickyEntry(tk.Entry):
	def __init__(self, parent, id, **kw):
		''' If relwidth is set, then width is ignored '''
		#fa = super(self,StickyEntry)
		#fa.__init__(parent, **kw)
		tk.Entry.__init__(self, parent,kw)
		self.parent=parent
		self.item_id=id
		self.insert(0, self.parent.item(id)["values"][0])
		self['readonlybackground'] = 'white'
		self['selectbackground'] = '#1BA1E2'
		self['exportselection'] = False
		self.focus_force()
		self.bind("<Escape>", lambda *ignore: self.destroy())
		self.bind("<Return>",self.confirm)
		self.bind("<Button-1>",self.confirm)
		self.bind("<Button-3>",self.confirm)

	def confirm(self,event):
		self.parent.set(self.item_id,0,self.get())
		self.destroy()

class ListPage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.app=root
		self.createWidgets()

	def createWidgets(self):
		
		# receiver_lf
		self.file_name=tk.StringVar()
		receiver_lf=ttk.LabelFrame(self, text="接收器（支持R3AC和RX-4）")
		receiver_lf.grid(column=0, row=0,padx=15,pady=4)
		
		self.is_listen_receiver = tk.IntVar()
		self.receiver_rssi_threshold = tk.IntVar()
		self.receiver_rssi_threshold.set("100")

		listen_check = ttk.Checkbutton(receiver_lf, text="监听新接收器",width=10,variable=self.is_listen_receiver)
		listen_check.grid(row=0,column=0)
		ttk.Label(receiver_lf,text="监听RSSI阈值：").grid(row=0,column=1)
		spin = tk.Spinbox(receiver_lf, from_=40,to=100,width=3,textvariable=self.receiver_rssi_threshold,wrap=True) 
		spin.grid(row=0,column=2)

		ttk.Button(receiver_lf,text="删除行",command=self.delete_receiver).grid(row=2,column=0,)
		ttk.Button(receiver_lf,text="清除配对",command=self.clear_receiver).grid(row=2,column=1)
		ttk.Button(receiver_lf,text="打开",command=self.open_receiver).grid(row=2,column=2)
		ttk.Button(receiver_lf,text="关闭",command=self.close_receiver).grid(row=2,column=3)
		ttk.Button(receiver_lf,text="打开中继",command=self.open_relay).grid(row=3,column=0)
		ttk.Button(receiver_lf,text="关闭中继",command=self.close_relay).grid(row=3,column=1)
		ttk.Button(receiver_lf,text="查询中继",command=self.inquire_relay).grid(row=3,column=2)

		self.receiver_table=ttk.Treeview(receiver_lf, show="headings", height=25, \
					columns=("receiver_name","receiver_id","receiver_type","receiver_channel",\
					"transmit_names","rssi"))
		vbar = ttk.Scrollbar(receiver_lf, orient=tk.VERTICAL, command=self.receiver_table.yview)
		# 定义树形结构与滚动条
		self.receiver_table.configure(yscrollcommand=vbar.set)
		vbar.grid(row=4,column=4,sticky="ns")
		self.receiver_table.grid(row=4,column=0,columnspan=4)
		self.receiver_table.column("receiver_name", width=80, anchor="center")
		self.receiver_table.heading("receiver_name", text="接收器标签")
		self.receiver_table.column("receiver_id", width=100, anchor="center")
		self.receiver_table.heading("receiver_id", text="接收器ID")
		self.receiver_table.column("receiver_type", width=80, anchor="center")
		self.receiver_table.heading("receiver_type", text="接收器类型")
		self.receiver_table.column("receiver_channel", width=80, anchor="center")
		self.receiver_table.heading("receiver_channel", text="接收器通道")
		self.receiver_table.column("transmit_names", width=150, anchor="center")
		self.receiver_table.heading("transmit_names", text="配对开关")
		self.receiver_table.column("rssi", width=80, anchor="center")
		self.receiver_table.heading("rssi", text="信号强度")
		self.receiver_table.bind('<Double-Button-1>',self.double_click)

		# transmit_lf
		transmit_lf=ttk.LabelFrame(self, text="发射器（支持K4R和单按键开关）")
		transmit_lf.grid(column=2, row=0,padx=15,pady=4)

		self.is_listen_transmit = tk.IntVar()
		self.transmit_rssi_threshold = tk.IntVar()
		self.transmit_rssi_threshold.set("70")

		listen_check = ttk.Checkbutton(transmit_lf, text="监听新发射器",width=10,variable=self.is_listen_transmit)
		listen_check.grid(row=0,column=0)
		ttk.Label(transmit_lf,text="监听RSSI阈值：").grid(row=0,column=1)
		spin = tk.Spinbox(transmit_lf, from_=40,to=100,width=3,textvariable=self.transmit_rssi_threshold,wrap=True) 
		spin.grid(row=0,column=2)

		ttk.Button(transmit_lf,text="发射开",command=self.transmit_open).grid(row=2,column=0)
		ttk.Button(transmit_lf,text="发射关",command=self.transmit_close).grid(row=2,column=1)
		ttk.Button(transmit_lf,text="删除行",command=self.delete_transmit).grid(row=2,column=2)

		self.transmit_table=ttk.Treeview(transmit_lf, show="headings", height=25, \
					columns=("transmit_name","transmit_id","transmit_type","transmit_channel",\
					"receiver_names","rssi"))
		vbar = ttk.Scrollbar(transmit_lf, orient=tk.VERTICAL, command=self.transmit_table.yview)
		vbar.grid(row=3,column=4,sticky="ns")

		# 定义树形结构与滚动条

		self.transmit_table.configure(yscrollcommand=vbar.set)
		self.transmit_table.grid(row=3,column=0,columnspan=4)
		self.transmit_table.column("transmit_name", width=80, anchor="center")
		self.transmit_table.heading("transmit_name", text="发射器标签")
		self.transmit_table.column("transmit_id", width=100, anchor="center")
		self.transmit_table.heading("transmit_id", text="发射器ID")
		self.transmit_table.column("transmit_type", width=80, anchor="center")
		self.transmit_table.heading("transmit_type", text="发射器类型")
		self.transmit_table.column("transmit_channel", width=80, anchor="center")
		self.transmit_table.heading("transmit_channel", text="发射器通道")
		self.transmit_table.column("receiver_names", width=150, anchor="center")
		self.transmit_table.heading("receiver_names", text="配对接收器")
		self.transmit_table.column("rssi", width=80, anchor="center")
		self.transmit_table.heading("rssi", text="信号强度")
		self.transmit_table.bind('<Double-Button-1>',self.double_click)
		
		# 配对按钮
		pair_lf=ttk.LabelFrame(self, text="配对")
		pair_lf.grid(column=1, row=0,padx=1,pady=4,sticky="we")
		tk.Button(pair_lf,text="配对",command=self.pair,width=10,height=4).grid(row=0,column=0,sticky="ns")
		ttk.Button(pair_lf,text="查配对",command=self.inquire_pair).grid(row=1,column=0,sticky="ns")
		ttk.Button(pair_lf,text="清除配对",command=self.clear_pair).grid(row=2,column=0,sticky="ns")
		ttk.Button(pair_lf,text="保存配置",command=self.save_xls).grid(row=3,column=0,sticky="ns")
		ttk.Button(pair_lf,text="导入excel",command=self.import_xls).grid(row=4,column=0,sticky="ns")
		ttk.Button(pair_lf,text="导出hass",command=self.save_hass).grid(row=5,column=0,sticky="ns")

		# log
		self.log=tk.StringVar()
		ttk.Label(self,textvariable=self.log).grid(column=0,row=4,columnspan=5,sticky='w')

		# dev_name
		self.receiver_order=1
		self.transmit_order=1

		self.entryPopup=None
	
	# 监听信号，rssi和其他一直监听
	def listen(self,data,optional):
		# 始终处理中继和配对
		print("-----------------------"+data[10:12])
		if data[10:12] in list(CON.receiver_type.values()):
			if data[12:14] == CON.cmd_type["inquire_relay"]:
				print("#################中继")
				receiver_id = data[2:10]
				receiver_type = data[10:12]
				relay_state = data[14:16]
				receiver_rssi = str(int(optional[0:2],16))
				self.show_relay(receiver_id,receiver_type,relay_state,receiver_rssi)
			elif data[12:14] == CON.cmd_type["inquire_id"]:
				print("#########查询配对id")
				self.update_pairs(data)
		
		# 勾选处理，插入新的接收器
		if self.is_listen_receiver.get() and (data[10:12] in list(CON.receiver_type.values()))\
			 and (int(optional[0:2],16) < int(self.receiver_rssi_threshold.get())) and data[14:16]!="00":
			receiver_id = data[2:10]
			receiver_type = data[10:12]
			receiver_channel = data[14:16]
			receiver_rssi = str(int(optional[0:2],16))
			self.insert_receiver(receiver_id,receiver_type,receiver_channel,receiver_rssi)

		# 勾选处理，插入新的发射器
		if self.is_listen_transmit.get() and (int(optional[0:2],16) < int(self.transmit_rssi_threshold.get())):
			if (data[10:12] in list(CON.transmit_type.values()))and data[12:14]!="00":
				transmit_id = data[2:10]
				transmit_type = data[10:12]
				transmit_channel = "0"+data[13:14]
				transmit_rssi = str(int(optional[0:2],16))
				self.insert_transmit(transmit_id,transmit_type,transmit_channel,transmit_rssi)

	# 查重复 id 和 channel，更新rssi和状态
	def is_repeat(self,id,type,channel,rssi,treeview):
		repeat=False
		for item in treeview.get_children():
			values=treeview.item(item)['values']
			values[1]="{0:>08}".format(values[1])
			values[2]="{0:>02}".format(values[2])
			values[3]="{0:>02}".format(values[3])
			if id+type+channel == values[1]+values[2]+values[3]:
				repeat=True
				# update rssi
				treeview.set(item,5,rssi)
				break
		return repeat

	# 插入一行接收器
	def insert_receiver(self,id,type,channel,rssi):
		if type == "81":
			values=(self.receiver_order,id,type,channel,"",rssi)
			if not self.is_repeat(id,type,channel,rssi,self.receiver_table):
				self.receiver_table.insert("","0",values=values)
				self.receiver_order += 1
		if type == "84":
			for channel in ["01","02","04","08"]:
				values=(self.receiver_order,id,type,channel,"",rssi)
				if not self.is_repeat(id,type,channel,rssi,self.receiver_table):
					self.receiver_table.insert("","0",values=values)
					self.receiver_order += 1
	# 插入一行发射器
	def insert_transmit(self,id,type,channel,rssi):
		values=(self.transmit_order,id,type,channel,"",rssi)
		if not self.is_repeat(id,type,channel,rssi,self.transmit_table):
			self.transmit_table.insert("","0",values=values)
			self.transmit_order += 1

	def double_click(self, event):
		''' 双击编辑name '''
		# close previous popups
		if self.entryPopup:
			# self.entryPopup.confirm(event)
			self.entryPopup.destroy()
		# what row and column was clicked on
		tv=event.widget
		rowid = tv.identify_row(event.y)
		column = 0 #只修改名字		
		# get column position info
		try:
			x,y,_,height = tv.bbox(rowid, column)
			pady = height // 2
			self.entryPopup = StickyEntry(tv, rowid, width=5)
			self.entryPopup.place( x=x, y=y+pady, anchor=tk.W)
		except :
			pass
	
	def delete_receiver(self):
		for item in self.receiver_table.selection():
			self.receiver_table.delete(item)
	
	def clear_receiver(self):
		for item in self.receiver_table.selection():
			values=self.receiver_table.item(item)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			receiver_channel="{0:>02}".format(values[3])
			data=CON.packet_type["operate_id"]+receiver_id+receiver_type+\
				CON.cmd_type["delete_all_id"]+receiver_channel
			self.app.send(data)
			self.log.set("清除接收器%s（id=%s）的配对" % (receiver_name,receiver_id))
	
	def open_receiver(self):
		for item in self.receiver_table.selection():
			values=self.receiver_table.item(item)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			receiver_channel="{0:>02}".format(values[3])
			data=CON.packet_type["operate_state"]+receiver_id+receiver_type+\
				CON.cmd_type["control_state"]+receiver_channel+receiver_channel
			self.app.send(data)
			self.log.set("打开接收器%s（id=%s）" % (receiver_name,receiver_id))

	def close_receiver(self):
		for item in self.receiver_table.selection():
			values=self.receiver_table.item(item)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			receiver_channel="{0:>02}".format(values[3])
			data=CON.packet_type["operate_state"]+receiver_id+receiver_type+\
				CON.cmd_type["control_state"]+receiver_channel+CON.receiver_state["off"]
			self.app.send(data)
			self.log.set("关闭接收器%s（id=%s）" % (receiver_name,receiver_id))
	
	def inquire_relay(self):
		for item in self.receiver_table.selection():
			values=self.receiver_table.item(item)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			data=CON.packet_type["operate_id"]+receiver_id+receiver_type+\
				CON.cmd_type["inquire_relay"]
			self.app.send(data)
			self.log.set("查询中继：接收器%s（id=%s）" % (receiver_name,receiver_id))	
		self.receiver_table.selection_remove(self.receiver_table.selection())
	def open_relay(self):
		for item in self.receiver_table.selection():
			values=self.receiver_table.item(item)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			data=CON.packet_type["operate_id"]+receiver_id+receiver_type+\
				CON.cmd_type["control_relay"]+CON.receiver_state["on"]
			self.app.send(data)
			self.log.set("打开中继接收器%s（id=%s）" % (receiver_name,receiver_id))
	
	def close_relay(self):
		for item in self.receiver_table.selection():
			values=self.receiver_table.item(item)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			data=CON.packet_type["operate_id"]+receiver_id+receiver_type+\
				CON.cmd_type["control_relay"]+CON.receiver_state["off"]
			self.app.send(data)
			self.log.set("打开中继接收器%s（id=%s）" % (receiver_name,receiver_id))
	
	def show_relay(self,id,type,state,rssi):
		for item in self.receiver_table.get_children():
			values=self.receiver_table.item(item)['values']
			values[1]="{0:>08}".format(values[1])
			values[2]="{0:>02}".format(values[2])
			if id+type == values[1]+values[2]:
				# update rssi
				self.receiver_table.set(item,5,rssi)
				if int(state[-1]):
					print("relay_on")
					self.receiver_table.item(item, tags=('relay_on'))
				else:
					print("relay_off")
					self.receiver_table.item(item, tags=('relay_off'))
				break
		self.receiver_table.tag_configure('relay_on', foreground='#00ffff')
		self.receiver_table.tag_configure('relay_off', foreground='#000000')

	# 移除选择
	def remove_selection(self):
		self.receiver_table.selection_remove(self.receiver_table.selection())
		self.transmit_table.selection_remove(self.transmit_table.selection())

	def transmit_open(self):
		for item in self.transmit_table.selection():
			values=self.transmit_table.item(item)['values']
			transmit_name=str(values[0])
			transmit_id="{0:>08}".format(values[1])
			transmit_type="{0:>02}".format(values[2])
			transmit_channel="{0:>02}".format(values[3])
			data=CON.packet_type["switch"]+transmit_id+transmit_type+"3"+transmit_channel[-1]
			self.app.send(data)
			self.log.set("模拟发射器开：%s(ID=%s)" % (transmit_name,transmit_id))
	def transmit_close(self):
		for item in self.transmit_table.selection():
			values=self.transmit_table.item(item)['values']
			transmit_name=str(values[0])
			transmit_id="{0:>08}".format(values[1])
			transmit_type="{0:>02}".format(values[2])
			transmit_channel="{0:>02}".format(values[3])
			data=CON.packet_type["switch"]+transmit_id+transmit_type+"2"+transmit_channel[-1]
			self.app.send(data)
			self.log.set("模拟发射器关：%s(ID=%s)" % (transmit_name,transmit_id))
	def delete_transmit(self):
		for item in self.transmit_table.selection():
			self.transmit_table.delete(item)
	
	def update_pairs(self,data):
		r_id = data[2:10]
		r_type = data[10:12]
		r_channel = data[14:16]
		t_type=data[18:20]
		t_channel=data[20:22]
		t_id=data[22:30]
		t_name=None
		t_item=None

		for receiver in self.receiver_table.get_children():
			values=self.receiver_table.item(receiver)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			receiver_channel="{0:>02}".format(values[3])
			if receiver_id+receiver_type+receiver_channel == r_id+r_type+r_channel:
				r_name = receiver_name
				r_item = receiver
				break

		for transmit in self.transmit_table.get_children():
			values=self.transmit_table.item(transmit)['values']
			transmit_name=str(values[0])
			transmit_id="{0:>08}".format(values[1])
			transmit_type="{0:>02}".format(values[2])
			transmit_channel="{0:>02}".format(values[3])
			if transmit_id+transmit_type+transmit_channel == t_id + t_type + t_channel:
				t_name = transmit_name
				t_item=transmit
				break
		if t_name and t_name not in self.receiver_table.item(r_item)['values'][4]:
			t_names = self.receiver_table.item(r_item)['values'][4]
			t_names += "["+t_name+"]"
			self.receiver_table.set(r_item,4,t_names)
		
		if t_item and r_name not in self.transmit_table.item(t_item)['values'][4]:
			r_names = self.transmit_table.item(t_item)['values'][4]
			r_names += "["+r_name+"]"
			self.transmit_table.set(t_item,4,r_names)

	def pair(self):
		for receiver in self.receiver_table.selection():
			values=self.receiver_table.item(receiver)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			receiver_channel="{0:>02}".format(values[3])
			for transmit in self.transmit_table.selection():
				values=self.transmit_table.item(transmit)['values']
				transmit_name=str(values[0])
				transmit_id="{0:>08}".format(values[1])
				transmit_type="{0:>02}".format(values[2])
				transmit_channel="{0:>02}".format(values[3])
				data=CON.packet_type["operate_id"]+receiver_id+receiver_type+CON.cmd_type["write_id"]\
						+receiver_channel+transmit_type+transmit_channel+transmit_id
				self.app.send(data)
				self.log.set("配对接收器%s和开关%s" % (receiver_name,transmit_name))

	def clear_pair(self):
		for receiver in self.receiver_table.selection():
			values=self.receiver_table.item(receiver)['values']
			receiver_name=str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			receiver_channel="{0:>02}".format(values[3])
			for transmit in self.transmit_table.selection():
				values=self.transmit_table.item(transmit)['values']
				transmit_name=str(values[0])
				transmit_id="{0:>08}".format(values[1])
				transmit_type="{0:>02}".format(values[2])
				transmit_channel="{0:>02}".format(values[3])
				data=CON.packet_type["operate_id"]+receiver_id+receiver_type+CON.cmd_type["delete_id"]\
						+receiver_channel+transmit_type+transmit_channel+transmit_id
				self.app.send(data)
				self.log.set("解除接收器%s和开关%s的配对" % (receiver_name,transmit_name))

	def inquire_pair(self):
		# 清空显示
		for transmit in self.transmit_table.get_children():
			values=self.transmit_table.item(transmit)['values']
			self.transmit_table.set(transmit,4,"")
		for receiver in self.receiver_table.selection():
			values=self.receiver_table.item(receiver)['values']
			self.receiver_table.set(receiver,4,"")
			receiver_name = str(values[0])
			receiver_id="{0:>08}".format(values[1])
			receiver_type="{0:>02}".format(values[2])
			receiver_channel="{0:>02}".format(values[3])
			data=CON.packet_type["operate_id"]+receiver_id+receiver_type+CON.cmd_type["inquire_id"]+receiver_channel
			self.app.send(data)
			self.log.set("查询接收器%s的配对" % (receiver_name))

	def save_xls(self):
		"""
		最后状态保存为xls文件,可以导入导出
		"""
		filename=tkinter.filedialog.asksaveasfilename(filetypes=[("excel格式","xlsx"),("excel格式","xls")])
		wbk = xlwt.Workbook()
		sheet1 = wbk.add_sheet('接收器')
		sheet2 = wbk.add_sheet('发射器')
		# indexing is zero based, row then column
		receivers=self.receiver_table.get_children()
		for  i in range(len(receivers)):
			values=self.receiver_table.item(receivers[i])['values']
			values[0]=str(values[0]) # name
			values[1]="{0:>08}".format(values[1]) # id
			values[2]="{0:>02}".format(values[2]) # type
			values[3]="{0:>02}".format(values[3]) # channel
			values[4]=str(values[4]) # pair_names
			values[5]=str(values[5]) # rsis
			for j in range(len(values)):
				sheet1.write(i,j,values[j])
		transmits=self.transmit_table.get_children()
		for  i in range(len(transmits)):
			values=self.transmit_table.item(transmits[i])['values']
			values[0]=str(values[0]) # name
			values[1]="{0:>08}".format(values[1]) # id
			values[2]="{0:>02}".format(values[2]) # type
			values[3]="{0:>02}".format(values[3]) # channel
			values[4]=str(values[4]) # pair_names
			values[5]=str(values[5]) # rsis
			for j in range(len(values)):
				sheet2.write(i,j,values[j])
		if filename.endswith('.xls'):
			wbk.save(filename)
		else:
			wbk.save(filename+'.xls')
	
	def import_xls(self):
		"""
		最后状态保存为xls文件,可以导入导出
		"""
		filename=tkinter.filedialog.askopenfilename(filetypes=[("excel格式","xlsx"),("excel格式","xls")])
		workbook = xlrd.open_workbook(filename)
		sheet1 = workbook.sheet_by_name(workbook.sheet_names()[0])
		sheet2 = workbook.sheet_by_name(workbook.sheet_names()[1])

		receiver_ids = sheet1.col_values(1)[1:]
		transmit_ids=sheet2.col_values(1)[1:]
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
		for i in range(len(receiver_ids)+1):
			item = sheet1.row_values(i)
			values=(item[0],item[1],item[2],item[3],item[4],item[5])
			self.receiver_table.insert("" ,"end",values=values)
		for i in range(len(transmit_ids)+1):
			item = sheet2.row_values(i)
			values=(item[0],item[1],item[2],item[3],item[4],item[5])
			self.transmit_table.insert("" ,"end",values=values)
	
	def save_hass(self):
		"""
		保存为hass配置文件，linptech.yaml
		"""
		filename=tkinter.filedialog.asksaveasfilename(filetypes=[("yaml格式","yaml")])
		if not filename.endswith('.yaml'):
			filename += '.yaml'
		with open(filename,'w') as f:
				conf="linptech_dongle:\n"
				conf += "  "+"device:/dev/ttyS0\n"
				# indexing is zero based, row then column
				conf += "light:\n"
				receivers=self.receiver_table.get_children()
				for  i in range(len(receivers)):
					values=self.receiver_table.item(receivers[i])['values']
					values[0]=str(values[0]) # name
					values[1]="{0:>08}".format(values[1]) # id
					values[2]="{0:>02}".format(values[2]) # type
					values[3]="{0:>02}".format(values[3]) # channel
					if values[3]=="01":
						if values[2]=="84":
							conf += "  "+"- platform: linptech_RX-4\n"
						if values[2]=="81":
							conf += "  "+"- platform: linptech_R3AC\n"
						conf += "    "+"id: "+values[1]+"\n"
						conf += "    "+"name: "+values[0]+"\n"
				f.writelines(conf)
		
	
if __name__ == '__main__':
	root=tk.Tk()

	# default_font = tkFont.nametofont("TkDefaultFont")
	# default_font.configure(size=18)
	# self.option_add("*Font", default_font)

	# 多页面table设置
	table = ttk.Notebook(root)
	table.pack(expand=1, fill="both",side="top")
	single_table = ListPage(table,root)
	table.add(single_table,text="批量调试")
	def closeWindow():
		root.destroy()
	root.protocol('WM_DELETE_WINDOW', closeWindow) 
	root.mainloop()
