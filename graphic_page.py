from tkinter import ttk
import tkinter as tk

class GraphicPage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.createWidgets()

	def createWidgets(self):
		single_lf=ttk.Label(self, text='开发中')
		single_lf.pack()