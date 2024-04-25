"""
版本: 2.0.0


更新:
    修改整體架構
    移除Block_SSID
    字串控制改用re 而非純文字處理
    函數化
    簡化程式碼

"""
#import
from datetime import datetime
import subprocess #執行cmd
from socket import gethostname
import re


#function
def GetPCName():
    return gethostname()

def GetCurrentTime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_datetime

def GetWIFIDict():
    wifi_dict = {}

    try:
        cmd_output = subprocess.check_output(["netsh", "wlan", "show", "profile"], text=True)
    except subprocess.CalledProcessError:
        print("WiFi service not available")
        return None

    ssid_list = re.findall(r"所有使用者設定檔 : (\S+)", cmd_output)

    for ssid in ssid_list:
        command = ['netsh', 'wlan', 'show', 'profile', 'name="%s"' % ssid, 'key=clear']
        try:
            output = subprocess.check_output(command, text=True)
            key_content_match = re.search(r"金鑰內容\s+:\s+(.+)", output)
            if key_content_match:
                key_content = key_content_match.group(1)
                wifi_dict[ssid] = key_content
            else:
                wifi_dict[ssid] = "none"
        except subprocess.CalledProcessError:
            wifi_dict[ssid] = "error"

    return wifi_dict

#setup

WIFI_Info = {}
have_wifi = False
version = "2.0.0"
PC_Name = GetPCName()
current_time = GetCurrentTime()



#file = open("WIFI_PWD.txt",mode="a" )  #開啟wifi 密碼紀錄的txt
file = open("test_wifi.txt",mode="a" )  #開啟wifi 密碼紀錄的txt


#Main
file.write("===================================================\n")

WIFI_Info = GetWIFIDict()
file.write("WiFi Information:\n")
file.write("-----------------\n")
file.write("Version : %s\n" % version)
file.write("Computer from : %s\n" % PC_Name)
file.write("Current time : %s\n" % current_time)
file.write("-----------------\n")

if WIFI_Info is not None:
    for ssid, password in WIFI_Info.items():
        file.write(f"SSID: {ssid.ljust(20)} Password: {password}\n")
        print(f"SSID: {ssid.ljust(20)} Password: {password}")
        have_wifi = True
else:
    print(f"{PC_Name} has No WiFi information available.")
    file.write(f"{PC_Name} has No WiFi information available.")


file.write("===================================================\n\n")

file.close()


    