import re
from enum import Enum

class AppConfig(Enum):
    WINDOWS_SZIE='1024x720'
    FONT = ("Verdana", 12)
    TITLE = "领普科技部署调试软件V0.2.0"

# Enum没有dict方便：keys() values()
receiver_type={
    "R3AC":"81",
    "RX_4":"84"
}
receiver_channel={
    "通道1":"01",
    "通道2":"02",
    "通道3":"04",
    "通道4":"08",
    "通道1234":"0f",
    "通道12":"03",
}
transmit_type={
    "K5":"01",
    "K4R":"02"
}
transmit_channel={
    "通道1":"01",
    "通道2":"02",
    "通道3":"04",
}
# 报文类型
packet_type={
    "switch":"00",
    "operate_state":"5f", #控制报文
    "show_state":"5e",#状态报文
    "operate_id":"5d",
    "show_id":"5c"
}

# 控制字节
cmd_type={
    "control_state":"02", #控制指令
    "inquire_state":"01",#状态报文
    "write_id":"0d",
    "delete_id":"0e",
    "delete_all_id":"09",
}
# 接收器状态
receiver_state={
    "ON":"01",
    "OFF":"00",
}

# 操作id状态
id_state={
    "OK":"00",
    "FAIL":"01",
    "FULL":"02",
    "UNSUPPORT":"03",
}



hex8_pattern = re.compile("^[0-9a-fA-F]{8}$")
