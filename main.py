from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import inspect
import os
import time
import tkinter as tk
from tkinter import messagebox
import pyautogui
import csv
from tkinter import filedialog
global lines
lines=[]
logo=''' __        ___           _                           ____        _ _         _       _     _           \n \ \      / / |__   __ _| |_ ___  __ _ _ __  _ __   | __ ) _   _| | | __    / \   __| | __| | ___ _ __ \n  \ \ /\ / /| '_ \ / _` | __/ __|/ _` | '_ \| '_ \  |  _ \| | | | | |/ /   / _ \ / _` |/ _` |/ _ \ '__|\n   \ V  V / | | | | (_| | |_\__ \ (_| | |_) | |_) | | |_) | |_| | |   <   / ___ \ (_| | (_| |  __/ |   \n    \_/\_/  |_| |_|\__,_|\__|___/\__,_| .__/| .__/  |____/ \__,_|_|_|\_\ /_/   \_\__,_|\__,_|\___|_|   \n                                      |_|   |_|                                                        '''

def random(file_path):
    with open(file_path, 'r') as f:
        nums=[]
        fr=csv.reader(f)
        for line in fr:
            nums.append(line[1])
    numbers = [n.replace(' ', '').replace('-', '') for n in nums]
    nums_f = [f"+92 {n[-10:-7]} {n[-7:-3]}{n[-3:]}" for n in numbers]
    contacts=[[f'baka{n}', phone] for n, phone in enumerate(nums_f)]
    lines = [format_contact(f'baka{n}', phone) for n, phone in enumerate(nums_f)]

    with open('contacts.vcf', 'w') as f:
        for line in lines:
            f.write(line)
    return contacts
    


def specific(file_path):
    with open(file_path, 'r') as f:
        nums=[]
        fr=csv.reader(f)
        for line in fr:
            nums.append(line)
    numbers = [[n[0],n[1].replace(' ', '').replace('-', '')] for n in nums]
    nums_f = [[n[0],f"+92 {n[1][-10:-7]} {n[1][-7:-3]}{n[1][-3:]}"] for n in numbers]
    contacts=nums_f
    lines=[format_contact(n[0],n[1]) for n in nums_f]
    with open('contacts.vcf', 'w') as f:
        for line in lines:
            f.write(line)
    return contacts

def format_contact(name, phone):
    return f"BEGIN:VCARD\nVERSION:3.0\nN:  ;{name};;;\nFN:{name}\nTEL;type=Mobile;waid={phone.replace('+','').replace(' ','')}:{phone}\nEND:VCARD\n"


def select_file():
    time.sleep(1.5)
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        None
    else:
        print('No file is selected.')
        select_file()


def display_menu():
    print(logo,'\n\n')
    select_file()
    print("1. Use Random Names")
    print("2. Use Specified Names")
    print("3. Exit")



def main():
    global contacts
    while True:
        os.system('cls')
        display_menu()

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            contacts=random(file_path)
            break
        elif choice == "2":
            contacts=specific(file_path)
            break
        elif choice == "3":
            print("Exiting the CLI menu.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
            time.sleep(1.5)

main()

def initializar():
    global driver
    driver=webdriver.Chrome()
    driver.get('https://web.whatsapp.com/')

    try:
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, '_2vDPL')))
    except:
        print('Try again')


def clicker(t):
    time.sleep(1.5)
    button=driver.find_element(By.XPATH,t)
    button.click()


def locate_dm_by_name(name):
    time.sleep(1.5)
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
    search_box.clear()
    search_box.send_keys(name)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//span[@title="{name}"]')))
    contact = driver.find_element(By.XPATH, f'//span[@title="{name}"]')
    contact.click()

name=input('Enter exact name of the group you want to add members to:\n')

initializar()
clicker('//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[3]/div') #New Chat
clicker('//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div[5]/div/div/div[11]') #You
clicker('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div') #Attach
clicker('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[4]') #Document

time.sleep(1.5)
current_file = inspect.getframeinfo(inspect.currentframe()).filename
folder_path = os.path.abspath(os.path.dirname(current_file)) + '\\contacts.vcf'
pyautogui.typewrite(folder_path, interval=0.01)
pyautogui.press('enter')
time.sleep(4)
pyautogui.press('enter')

def confirm_prompt():
    response = messagebox.askyesno("Followed Guidelines?", "Are you sure you want to proceed?")
    root.destroy()
root = tk.Tk()
root.attributes("-topmost", True)
root.title('Follow the Guidelines.')
confirm_button = tk.Button(root, text="After Done Click here!!!", command=confirm_prompt)
textbox = tk.Label(root, text="1. Go to Whatsapp on your Mobile Device.\n2. Go to your personal message.\n3. Open the Vcf file sent and save all contacts.\n4. After it's done, refresh your Whatsapp contacts manually.", wraplength=500, justify='left')
textbox.pack(pady=10)
confirm_button.pack(pady=20)
root.mainloop()

locate_dm_by_name(name)

clicker('//*[@id="main"]/header/div[3]/div/div[2]/div/div') # Dots
clicker('//*[@id="app"]/div/span[4]/div/ul/div/div/li[1]/div') # Group_info
clicker('//*[@id="app"]/div/div/div[6]/span/div/span/div/div/div/section/div[7]/div[2]/div[1]') # Add_Participants

time.sleep(5)
for line in contacts:
    pyautogui.typewrite(line[0])
    clicker('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div/div[2]/button/div[2]') #Selecting

clicker('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/span[2]/div/div/div') #Confirm
clicker('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button[2]') #confirmation

time.sleep(5)
driver.quit()
print('''  _____ _                 _                        _ _ _ \n |_   _| |__   __ _ _ __ | | __  _   _  ___  _   _| | | |\n   | | | '_ \ / _` | '_ \| |/ / | | | |/ _ \| | | | | | |\n   | | | | | | (_| | | | |   <  | |_| | (_) | |_| |_|_|_|\n   |_| |_| |_|\__,_|_| |_|_|\_\  \__, |\___/ \__,_(_|_|_)\n                                 |___/                   ''')