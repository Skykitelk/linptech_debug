from tkinter import ttk
import tkinter as tk

class BatchPage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.createWidgets()

	def createWidgets(self):
		single_lf=ttk.Label(self, text='手动配对')
		single_lf.pack()
