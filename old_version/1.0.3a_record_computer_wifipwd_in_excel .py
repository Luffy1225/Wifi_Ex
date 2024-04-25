"""
版本: 1.0.3.a

缺點 :格式化到txt檔格式會跑掉

更新:優化 1.0.2 (pwd list 包含list 的問題尚未解決)
    增加 顯示 主機名稱、現在時間


"""
version = "1.0.3a"
from datetime import date, datetime
import subprocess #執行cmd
#import openpyxl   #excel

#cmd取得 曾經登錄過的wifi的名稱 再取得密碼 並記錄到EXCEL 或 .txt

file = open("WIFI_PWD.txt",mode="a" )  #開啟wifi 密碼紀錄的txt

now =datetime.now()
current_time = now
print(current_time)


cmd = subprocess.Popen("ipconfig/all" , shell=True, stdout=subprocess.PIPE)
cmd_output = cmd.stdout.read()  #BIG5編碼
unconvert_computer_name = cmd_output.decode('big5')  #把BIG5 解碼

computer_name=unconvert_computer_name.split("主機名稱 . . . . . . . . . . . . .: ")
computer_name=computer_name[-1].split("主要 DNS 尾碼  . . . . . . . . . .:")
del computer_name[-1]

print(computer_name)
computer_name=computer_name[0][:-5]   #刪除 \r\n 
print(computer_name)

cmd = subprocess.Popen("netsh wlan show profile" , shell=True, stdout=subprocess.PIPE)
cmd_output = cmd.stdout.read()  #BIG5編碼
converted_SSID = cmd_output.decode('big5')  #把BIG5 解碼


unconvert_SSID_LIST=converted_SSID.split("所有使用者設定檔 : ")

#test
print(type(unconvert_SSID_LIST))
print(unconvert_SSID_LIST)
################

del unconvert_SSID_LIST[0]  #刪除list 第一個不重要的元素 :(\r\n介面 Wi-Fi 上的設定檔: \r\n\r\n群組原則設定檔 (唯讀)\r\n---------------------------------\r\n    <無>\r\n\r\n使用者設定檔\r\n-------------\r\n   )

print(unconvert_SSID_LIST)

SSID_LIST=[]

for get_ssid in unconvert_SSID_LIST:

    if (get_ssid == unconvert_SSID_LIST[-1] ):
        Delete_rn=get_ssid[:-4]   #刪除 \r\n 
        SSID_LIST.append(Delete_rn)

    else:
        Delete_rn=get_ssid[:-6]   #刪除 \r\n    
        SSID_LIST.append(Delete_rn)

#block ssid

block_ssid = ['NKSH-STU','NKSH-TEA','NKSH-STU_5G',"NKSH  遠傳  10G","連線失敗(； ?`??’)","??????","????????????????"]

#TEST NKSH-STU

for target_block in block_ssid:

    if target_block in SSID_LIST:
        SSID_LIST.remove(target_block)
        print(SSID_LIST)

print(SSID_LIST)
print("test_end")

#以下為取得密碼


PWD_LIST=[]


for pwd in SSID_LIST:
    print("current: id = %s" % pwd )#debug


    request_PWD = ('netsh wlan show profile name = "%s" key = clear  ' % (pwd))
    cmd = subprocess.Popen( request_PWD , shell=True, stdout=subprocess.PIPE)
    cmd_output = cmd.stdout.read()  #BIG5編碼
    converted_PWD = cmd_output.decode('big5')  #把BIG5 解碼

    WIFI_PWD=converted_PWD.split("金鑰內容               : ")
    WIFI_PWD=WIFI_PWD[-1].split("成本設定")

    del WIFI_PWD[-1]
    print(WIFI_PWD)

    if (WIFI_PWD == SSID_LIST[-1] ):
        Delete_rn=WIFI_PWD[0][:-4]   #刪除 \r\n 
        print(Delete_rn) 
        PWD_LIST.append(Delete_rn)

    else:
        Delete_rn=WIFI_PWD[0][:-4]   #刪除 \r\n   
        print(Delete_rn) 
        PWD_LIST.append(Delete_rn)

print(PWD_LIST)


print("-------------------------------------")

print("Final check")
print("Wifi name")
print(SSID_LIST)
print("password")
print(PWD_LIST)
print("-------------------------------------")
#########################txt

length = len(SSID_LIST)


#標題
print("Version : %s" % version ,file = file)
print("Computer from : %s      " %computer_name ,file = file   , end ="")
print("current time : %s" % current_time ,file = file)
print("" ,file=file)
print("Wifi 名稱(SSID)                 ",file=file ,end="" )
print("密碼",file=file )
print("" ,file=file)
#標題


#內文
for i in range(0,length):
    print("%-32s" % SSID_LIST[i] , end="")
    print("%-32s" % SSID_LIST[i] , file =file , end="")#txt
    print("%-32s" % PWD_LIST[i] )
    print("%-32s" % PWD_LIST[i] , file =file)#txt

print("------------------------------------------" ,file=file)

file.close()