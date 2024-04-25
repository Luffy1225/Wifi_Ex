"""
版本: 1.0.0 

缺點 : 無法解決 list 包含list 的問題
格式化到txt檔格式會跑掉
"""
version = "1.0.0"

import subprocess  #執行cmd
import chardet     #cmd output 是 big5需要解碼
import openpyxl    #excel

#cmd取得 曾經登錄過的wifi的名稱 再取得密碼 並記錄到EXCEL 或 .txt

file = open("record_computer_wifipwd_in_excel/WIFI_PWD.txt",mode="a")

cmd = subprocess.Popen("netsh wlan show profile" , shell=True, stdout=subprocess.PIPE)
cmd_output = cmd.stdout.read()  #BIG5編碼
converted_SSID = cmd_output.decode('big5')  #把BIG5 解碼

unconvert_SSID_LIST=converted_SSID.split("所有使用者設定檔 : ")

del unconvert_SSID_LIST[0]

print(unconvert_SSID_LIST)

SSID_LIST=[]

for i in unconvert_SSID_LIST:
    
    if (i != unconvert_SSID_LIST[-1]):

        i=i.split("\r\n")
        del i[-1]
        SSID_LIST.append(i)
        print(i)

    elif(i == unconvert_SSID_LIST[-1]):

        i=i.split("\r\n\r\n")
        del i[-1]
        SSID_LIST.append(i)
        print(i)



print (SSID_LIST)



#########################################################
# WIFI : NKSH-STU 不能用 先刪掉 
del SSID_LIST[0]
###################################################
print(SSID_LIST)


Final_ssid = SSID_LIST

#!!!!!!!!!!! SSID_LIST 目前是 list 包住list  呼叫的話要用    SSID[?][0]







#以下為取得密碼


Final_pwd=[]


for i in SSID_LIST:

    request_PWD = ('netsh wlan show profile name = "%s" key = clear  ' % (i[0]))
    #request_PWD = ('netsh wlan show profile name = "不給你連啦" key = clear  ')
    #request_PWD = ('netsh wlan show profile name = "%s" key = clear  '%  (SSID_LIST[1]))
    cmd = subprocess.Popen( request_PWD , shell=True, stdout=subprocess.PIPE)
    cmd_output = cmd.stdout.read()  #BIG5編碼
    converted_PWD = cmd_output.decode('big5')  #把BIG5 解碼

    WIFI_PWD=converted_PWD.split("金鑰內容               : ")
    WIFI_PWD=WIFI_PWD[-1].split("成本設定")

    del WIFI_PWD[-1]
    print(WIFI_PWD)

    for i in WIFI_PWD:
        
        if (i != WIFI_PWD[-1]):

            i=i.split("\r\n")
            del i[-1]
            print(i)
            Final_pwd.append(i)

        elif(i == WIFI_PWD[-1]):

            i=i.split("\r\n\r\n")
            del i[-1]
            print(i)
            Final_pwd.append(i)

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


#最後帳密

print(Final_ssid)#!!!!!!!!!!! Final_ssid 目前是 list 包住list  呼叫的話要用    Final_ssid[?][0]
print(Final_pwd)#!!!!!!!!!!! Final_pwd 目前是 list 包住list  呼叫的話要用    Final_pwd[?][0]







#印至 WIFI_PWD.txt

'''for PRINT_ssid in Final_ssid:
    print("%.32s" % PRINT_ssid[0] , file =file , end="")
    print("%.32s" % PRINT_ssid[0] , file =file , end="")
    for PRINT_pwd in Final_pwd:
        print("%.32s" % PRINT_pwd[0] , )
        print("%.32s" % PRINT_pwd[0] , file =file )'''


#土法煉鋼

length = len(Final_ssid)
print(length)



#標題
print("Wifi 名稱(SSID)             ",file=file ,end="" )
print("密碼",file=file ,)
print("" ,file=file)
#標題


#內文
for i in range(0,length):
    print("%-32s" % Final_ssid[i][0] , end="")
    print("%-32s" % Final_ssid[i][0] , file =file , end="")#txt
    print("%32s" % Final_pwd[i][0] )
    print("%32s" % Final_pwd[i][0] , file =file)#txt

print("------------------------------------------" ,file=file)
