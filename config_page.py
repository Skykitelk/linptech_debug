from tkinter import ttk
import tkinter as tk
import constant as CON

class ConfigPage(ttk.Frame):
	def __init__(self, parent,root):
		ttk.Frame.__init__(self, parent)
		self.app=root
		self.create_widgets()

	def create_widgets(self):

		# version 
		version_lf = ttk.LabelFrame(self,text="版本")
		version_lf.grid(row=0,column=0,padx=15,pady=4,sticky="w")
		self.latest_version=tk.StringVar()
		ttk.Label(version_lf,text="当前版本:"+CON.AppConfig.VERSION.value).grid(row=0,column=0)
		ttk.Label(version_lf,text="   最新版本:").grid(row=0,column=1)
		ttk.Label(version_lf,textvariable=self.latest_version).grid(row=0,column=2)
		ttk.Button(version_lf,text="更新",command=self.update,state="disabled").grid(row=0,column=3)
	
	def update(self):
		pass
	
	def get_latest_version(self):
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
	single_table = ConfigPage(table,root)
	table.add(single_table,text="关于")
	def closeWindow():
		root.destroy()
	root.protocol('WM_DELETE_WINDOW', closeWindow) 
	root.mainloop()