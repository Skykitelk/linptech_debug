import re


WINDOWS_SZIE='1366x768'
# FONT = ("Verdana", 12)
VERSION = "0.3.0"
TITLE = "领普科技部署调试软件"+VERSION
hex8_pattern = re.compile("^[0-9a-fA-F]{8}$")
SEND_INTERVAL=0.1 #发送时间间隔
