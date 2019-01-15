import os
from git import Repo

# 获取当前文件路径
url = os.getcwd()

class UpDataCode():
	def __init__(self):
		# 创建当前文件版本库对象
		self.repo = Repo(url)
		# 获取默认版本库 origin
		self.remote = self.repo.remote()

	def start_updata(self):
		print(self.repo.bare, self.repo.is_dirty(), self.repo.untracked_files)
		print(self.remote.pull())

if __name__ == '__main__':
	ud = UpDataCode()
	ud.start_updata()