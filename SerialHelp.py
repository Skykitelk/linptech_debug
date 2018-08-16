# coding=utf-8

'''
Serial设备通讯帮助类
'''

import sys
import threading
import time
import serial
import binascii
import logging

class SerialHelper(object):
	data = ''
	def __init__(self, Port, BaudRate="57600", ByteSize="8", Parity="N", Stopbits="1"):
		'''
		初始化一些参数
		'''
		self.l_serial = None
		self.alive = False
		self.port = Port
		self.baudrate = BaudRate
		self.bytesize = ByteSize
		self.parity = Parity
		self.stopbits = Stopbits
		
		
		self.thresholdValue = 16
		self.receive_data = ""
		
	def start(self):
		'''
		开始，打开串口
		'''
		self.l_serial = serial.Serial()
		self.l_serial.port = self.port
		self.l_serial.baudrate = self.baudrate
		self.l_serial.bytesize = int(self.bytesize)
		self.l_serial.parity = self.parity
		self.l_serial.stopbits = int(self.stopbits)
		self.l_serial.timeout = 1
		self.l_serial.interCharTimeout = 0.3

		try:
			self.l_serial.open()
			if self.l_serial.isOpen():
				self.alive = True
		except Exception as e:
			self.alive = False
			logging.error(e)

	def stop(self):
		'''
		结束，关闭串口
		'''
		self.alive = False
		if self.l_serial.isOpen():
			self.l_serial.close()

	def read(self):
		'''
		循环读取串口发送的数据
		'''
		while self.alive:
			try:
				number = self.l_serial.inWaiting()
				if number:
					self.receive_data += self.l_serial.read(number)
					if self.thresholdValue < len(self.receive_data):
						self.receive_data = ""
					else:                        
						self.receive_data = str(binascii.b2a_hex(self.receive_data))
						self.__class__.data = self.receive_data
						print(self.__class__)
						print(self.receive_data)
			except Exception as e:
				logging.error(e)

	def write(self, data, isHex=False):
		'''
		发送数据给串口设备
		'''
		if self.alive:
			if self.l_serial.isOpen():
				if isHex:
					# data = data.replace(" ", "").replace("\n", "")
					data = binascii.unhexlify(data)
				self.l_serial.write(data)
				
if __name__ == '__main__':
	import threading
	#ser = SerialHelper("COM5")
	ser = SerialHelper("/dev/ttyUSB0")
	ser.start()
	#重写read方法
	def read():
		while ser.alive:
			try:
				number = ser.l_serial.inWaiting()
				if number:
					ser.receive_data += ser.l_serial.read(number)
					print(ser.receive_data)
					if ser.thresholdValue < len(ser.receive_data):
						ser.receive_data = ""
					else:                        
						ser.receive_data = str(binascii.b2a_hex(ser.receive_data))
						print(ser.receive_data)
			except Exception as e:
				logging.error(e) 
	thread_read = threading.Thread(target=read)
	thread_read.setDaemon(False)
	thread_read.start()
	while 1:
		pass
