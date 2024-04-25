"""
Wi-Fi Information Extraction Tool
(Network Credentials Logger)

Version: 2.1.0

Features:
    Retrieve Wi-Fi information from the cmd command "netsh wlan show profile"
    Obtain SSID and passwords of all previously connected Wi-Fi networks
    Write the information into a txt file

Updates:
    Modularization of functions
    Code simplification
    Update of the name to Wi-Fi Information Extraction Tool
    OOP
    translation to English

"""
#import
from datetime import datetime
import subprocess #執行cmd
from socket import gethostname
import re

#Setup

class Wifi_Info_Extractor:

    def __init__(self, output_file):
        self.version = "2.1.0"
        self.output_file = output_file
        self.PC_Name = self.get_PC_name()
        self.current_time = self.get_current_time()
        
    #function
    def get_PC_name(self):
        return gethostname()

    def get_current_time(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
        return formatted_datetime

    def get_WIFI_Dict(self):
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

    def write_to_file(self,file_path: str, wifiinfo: dict):

        file = open(file_path,mode="a" )  #開啟wifi 密碼紀錄的txt

        file.write("===================================================\n")

        file.write("WiFi Information:\n")
        file.write("-----------------\n")
        file.write("Version : %s\n" % self.version)
        file.write("Computer from : %s\n" % self.PC_Name)
        file.write("Current time : %s\n" % self.current_time)
        file.write("-----------------\n")

        if wifiinfo is not None:
            for ssid, password in wifiinfo.items():
                file.write(f"SSID: {ssid.ljust(20)} Password: {password}\n")
                have_wifi = True
        else:
            file.write(f"{self.PC_Name} has No WiFi information available.")


        file.write("===================================================\n\n")

        file.close()

    def display_WIFI_info(self, wifi_info: dict):
        print("===================================================")
        print("""  
    ╭─────────────────────────────────────────────╮
    │                  WIFI-Ex                    │
    │    ──────────────────────────────────────   │
    │     (Wi-Fi Information Extraction Tool)     │
    │               Version: 2.1.0                │
    ╰─────────────────────────────────────────────╯
              """)
        print("WiFi Information:")
        
        print("-----------------")
        print("Version : %s" % self.version)
        print("Computer from : %s" % self.PC_Name)
        print("Current time : %s" % self.current_time)
        print("-----------------")

        if wifi_info is not None:
            for ssid, password in wifi_info.items():
                print(f"SSID: {ssid.ljust(20)} Password: {password}")
                have_wifi = True
        else:
            print(f"{self.PC_Name} has No WiFi information available.")

        print("===================================================")

    def Run(self):
        wifi_info = self.get_WIFI_Dict()
        self.display_WIFI_info(wifi_info)

        choice = input('If to save the information, press "Y" or "y" to continue...')

        if choice == "Y" or "y": 
            file = "WIFI-Ex_Information.txt"
            self.write_to_file(file,wifi_info)
            print(f'Saved to {file}')
        else:
            print("Information not saved.")
            exit()

if __name__ == "__main__":
    wifi_info_extractor = Wifi_Info_Extractor("WIFI-Ex_Information.txt")
    print("""
        
    ╭─────────────────────────────────────────────╮
    │                  WIFI-Ex                    │
    │    ──────────────────────────────────────   │
    │     (Wi-Fi Information Extraction Tool)     │
    │               Version: 2.1.0                │
    ╰─────────────────────────────────────────────╯

    ✦ Welcome to NetCred Logger! ✦
    Securely manage and log network credentials
    for various purposes.
          
    "Enter" to continue...

    """)
    wifi_info_extractor.Run()
