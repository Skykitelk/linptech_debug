from tkinter import ttk
import tkinter as tk

class SinglePage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.createWidgets()

	def createWidgets(self):
		single_lf=ttk.Label(self, text='手动输入配对')
		single_lf.grid()

	# 	#串口选择
	# 	serial_lf=ttk.LabelFrame(self, text='串口设置')
	# 	serial_lf.grid(column=0, row=0,padx=15,pady=4,sticky="w")

	# 	# 手动输入ID配对
	# 	single_lf=ttk.LabelFrame(self, text='手动输入ID配对')
	# 	single_lf.grid(column=0, row=1,padx=15,pady=4)
	# 	self.receiver_id=tk.StringVar()
	# 	self.transmit_id=tk.StringVar()

	# 	ttk.Label(single_lf,text="接收器（910）ID：").grid(row=0,column=0)
	# 	ttk.Entry(single_lf,textvariable=self.receiver_id).grid(row=0,column=1)
	# 	ttk.Button(single_lf,text="打开接收器",command=self.receiver_open).grid(row=0,column=2)
	# 	ttk.Button(single_lf,text="关闭接收器",command=self.receiver_close).grid(row=0,column=3)
	# 	ttk.Button(single_lf,text="清除所有ID",command=self.receiver_clear).grid(row=0,column=4)

	# 	ttk.Label(single_lf,text="发射器（k4rw1）ID：").grid(row=1,column=0)
	# 	ttk.Entry(single_lf,textvariable=self.transmit_id).grid(row=1,column=1)
	# 	ttk.Button(single_lf,text="发射打开信号",state=tk.DISABLED,command=self.transmit_open).grid(row=1,column=2)
	# 	ttk.Button(single_lf,text="发射关闭信号",state=tk.DISABLED,command=self.transmit_close).grid(row=1,column=3)
	# 	ttk.Button(single_lf,text="清除当前ID",command=self.receiver_clear_one).grid(row=1,column=4)

	# 	ttk.Button(single_lf,text="配对",command=self.pair_one).grid(row=0,column=5,rowspan=2,sticky="ns")


	# 	# 读取excel文件批量配对，配对前会清除之前所有配对
	# 	self.file_name=tk.StringVar()
	# 	batch_lf=ttk.LabelFrame(self, text="excel文件批量配对，会删除表中接收器之前的配对")
	# 	batch_lf.grid(column=0, row=2,padx=15,pady=4)
	# 	ttk.Label(batch_lf,text="配对EXCEL文件：").grid(row=0,column=0)
	# 	ttk.Entry(batch_lf,textvariable=self.file_name,width=40).grid(row=0,column=1,columnspan=3,sticky="we")
	# 	ttk.Button(batch_lf,text="选取文件",command=self.get_file).grid(row=0,column=4)
	# 	ttk.Button(batch_lf,text="批量配对",command=self.batch_pair).grid(row=0,column=5)

	# 	# log
	# 	log_lf=ttk.LabelFrame(self, text="运行日志")
	# 	log_lf.grid(column=0, row=3,padx=15,pady=4)
	# 	self.log=tk.Text(log_lf,height=30)
	# 	self.log.grid(row=0,column=0,columnspan=6,sticky="we")

	# #获取串口列表，并返回list
	# def getPortList(self):
	# 	portList = list(serial.tools.list_ports.comports())
	# 	portNameList = []
	# 	for port in portList:
	# 		portNameList.append(str(port[0]))
	# 	print("portNameList=",portNameList)
	# 	return portNameList

	# def serial_open(self):
	# 	try:
	# 		self.serial.start()
	# 		self.add_log("打开串口成功！")
	# 	except Exception as e:
	# 		self.add_log(str(e))
	
	# def generate_message(self,m1,m2):
	# 	return "55"+m1+crc8.crc8(m1)+m2+crc8.crc8(m2)
	
	# def add_log(self,log):
	# 	now=time.strftime("%H:%I:%S", time.localtime(time.time()))
	# 	self.log.insert(tk.END,now+"->"+log+"\n")

	# def receiver_open(self):
	# 	if P.match(self.receiver_id.get()):
	# 		self.add_log("操作：打开接收器"+self.receiver_id.get())
	# 		m1="00090701"
	# 		m2="1f"+self.receiver_id.get()+"8102010100000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)
	# 	else:
	# 		tk.messagebox.showerror("错误", "接收器id错误")
		
	# def receiver_close(self):
	# 	if P.match(self.receiver_id.get()):
	# 		self.add_log("操作：关闭接收器"+self.receiver_id.get())
	# 		m1="00090701"
	# 		m2="1f"+self.receiver_id.get()+"8102010000000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)
	# 	else:
	# 		tk.messagebox.showerror("错误", "接收器id错误")
	
	# def receiver_clear(self):
	# 	if P.match(self.receiver_id.get()):
	# 		self.add_log("操作：清除接收器"+self.receiver_id.get()+"上所有配对ID")
	# 		m1="00080701"
	# 		m2="5d"+self.receiver_id.get()+"81090100000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)
	# 	else:
	# 		tk.messagebox.showerror("错误", "接收器id错误")
	
	# def receiver_clear_one(self):
	# 	if P.match(self.receiver_id.get()) and P.match(self.transmit_id.get()):
	# 		self.add_log("操作：清除接收器"+self.receiver_id.get()+"上一个发射器"+self.transmit_id.get())
	# 		m1="000E0701"
	# 		m2="5d"+self.receiver_id.get()+"810e010101"+self.transmit_id.get()+"00000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)
	# 	else:
	# 		tk.messagebox.showerror("错误", "接收器或发射器id错误")

	# def transmit_open(self):
	# 	if P.match(self.transmit_id.get()):
	# 		self.add_log("操作：模拟开关"+self.transmit_id.get()+"发射打开信号")
	# 		m1="00070701"
	# 		m2="7a00"+self.receiver_id.get()+"012000000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)
	# 	else:
	# 		tk.messagebox.showerror("错误", "发射器id错误")
	
	# def transmit_close(self):
	# 	if P.match(self.transmit_id.get()):
	# 		self.add_log("操作：模拟开关"+self.transmit_id.get()+"发射关闭信号")
	# 		m1="00070701"
	# 		m2="7a00"+self.receiver_id.get()+"012100000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)
	# 	else:
	# 		tk.messagebox.showerror("错误", "发射器id错误")

	# def pair_one(self):
	# 	if P.match(self.receiver_id.get()) and P.match(self.transmit_id.get()):
	# 		self.add_log("操作：将发射器"+self.transmit_id.get()+"和接收器"+self.receiver_id.get()+"进行配对")
	# 		m1="000E0701"
	# 		m2="5d"+self.receiver_id.get()+"810d010101"+self.transmit_id.get()+"00000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)
	# 	else:
	# 		tk.messagebox.showerror("错误", "发射器或接收器id错误")

	# def get_file(self):
	# 	print("get file")
	# 	import tkinter.filedialog
	# 	filename=tkinter.filedialog.askopenfilename(filetypes=[("excel格式","xlsx"),("excel格式","xls")])
	# 	self.file_name.set(filename)
	
	# def batch_pair(self):
	# 	filename=self.file_name.get()
	# 	workbook = xlrd.open_workbook(filename)
	# 	sheet = workbook.sheet_by_name(workbook.sheet_names()[0])
	# 	receiver_ids = sheet.col_values(3)[1:]
	# 	transmit_ids=sheet.col_values(1)[1:]

	# 	# 检查id
	# 	rid_row=0
	# 	for rid in receiver_ids:
	# 		rid_row+=1
	# 		if not P.match(rid.strip()):
	# 			tk.messagebox.showerror("错误", "接收器id错误:"+str(rid_row)+"行")
	# 	tid_row=0
	# 	for tid in transmit_ids:
	# 		tid_row+=1
	# 		if not P.match(rid.strip()):
	# 			tk.messagebox.showerror("错误", "发射器id错误:"+str(tid_row)+"行")

	# 	self.add_log("!!!开始批量清除["+filename.split('/')[-1]+"]中接收器已经配对的ID")
	# 	receiver_ids_set=set(receiver_ids)
	# 	clear_num=0
	# 	for rid in receiver_ids_set:
	# 		clear_num += 1
	# 		self.add_log(str(clear_num)+"清除接收器"+rid+"上所有配对发射器")
	# 		m1="00080701"
	# 		m2="5d"+rid+"81090100000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)

	# 	self.add_log("清除完毕！清除接收器数量"+str(clear_num))
		
	# 	self.add_log("!!!开始批量配对["+filename.split('/')[-1]+"]中配对关系")
	# 	pair_num=0
	# 	for i in range(len(receiver_ids)):
	# 		pairs = sheet.row_values(i+1)
	# 		print(pairs)
	# 		pair_num+=1
	# 		self.add_log(str(pair_num)+"：配对发射器"+pairs[0].strip() +"和接收器"+pairs[2].strip())
	# 		m1="000E0701"
	# 		m2="5d"+pairs[3].strip() +"810d010101"+pairs[1].strip() +"00000000000000"
	# 		message=self.generate_message(m1,m2)
	# 		self.send(message)
	# 	self.add_log("批量配对完毕！配对次数"+str(clear_num))

	# def send(self,message):
	# 	self.serial.write(message,isHex=True)
	# 	self.add_log("发送指令："+message)
	# 	time.sleep(0.5)
	
	# #获取串口数据
	# def receive(self):
	# 	while self.signalSerial.alive:
	# 		try:
	# 			number = self.signalSerial.l_serial.inWaiting()
	# 			if number>=8:
	# 				self.signalSerial.receive_data += self.signalSerial.l_serial.read(number)
	# 				self.signalSerial.l_serial.flushInput()
	# 				self.signalSerial.receive_data = str(binascii.b2a_hex(self.signalSerial.receive_data))
	# 				#print self.signalSerial.receive_data
	# 				if self.signalSerial.thresholdValue != len(self.signalSerial.receive_data):
	# 					self.signalSerial.receive_data = ""
						
	# 				else:
	# 					receiveRSSI = int(self.signalSerial.receive_data[12:14],16)
	# 					setRSSI = int(str(self.signalArea.get()))
	# 					if receiveRSSI < setRSSI:
	# 						self.updateUI(self.signalSerial.receive_data)
	# 					self.signalSerial.receive_data = ""

	# 		except Exception as e:
	# 			logging.error(e)
	# 			#串口断线后重启
	# 			while(1):
	# 				time.sleep(0.5)
	# 				self.signalSerial.stop()
	# 				self.signalSerial.start()
	# 				port = self.currentPort.get()
	# 				print(port)
	# 				if self.signalSerial.alive:
	# 					break		
		
	# def blink(self):
	# 	self.signalButton['bg']='green'
	# 	time.sleep(0.1)
	# 	self.signalButton['bg']='grey'
