# Created by Nabeel Nayyar (@n43ee7)
#
#   ================================================Disclaimer [!]======================================================
#   This script is purely designed for educational purposes and there is no other intent. The user advised to exercise
#   caution during the run-time of this program as any malfunctions could caused by the script may lead to any action
#   that could lead to unknown conclusions. Please use at your own risk and ensure all parameters before running.
#               ======================================================================================
#
#
import os
import win32api, win32con, pywintypes
import tkinter as tk
from win32con import *
from tkinter import *
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import datetime, time

os.chdir('../..')                                                                                                       # Moving to the top of the project directory
print("[!] System Directory Shifted to ", os.getcwd())

url = "https://www.uta.edu/mymav/"                                                                                      # UTA WebPage URL
service = Service(os.path.join('Chromedriver', 'chromedriver_80.exe'))                                                  # Root path to Chromedriver.exe
service.start()
driver = webdriver.Remote(service.service_url)
uname = ''                                                                                                              # Global Var for Username
pswrd = ''                                                                                                              # Global Var for Password
xit = False


def webrequesthandler(path, arg, parram):
    action = webdriver.common.action_chains.ActionChains(driver)

    if arg == 1:
        button = driver.find_elements_by_xpath(path)[0]  # Click To XPath Location function
        action.move_to_element_with_offset(button, 5, 5)
        action.click()
        action.perform()
    elif arg == 0:  # Click To ID location Function
        button = driver.find_element_by_id(path)
        action.move_to_element_with_offset(button, 5, 5)
        action.click()
        action.perform()
    elif arg == 2:
        entry = driver.find_elements_by_xpath(path)[0]  # Special Argument for data entry
        entry.send_keys(parram)
        time.sleep(0.01)
        entry.send_keys(Keys.RETURN)
        entry.send_keys(Keys.RETURN)


def webscroll(param):
    for xe in range(0, param):
        win32api.mouse_event(MOUSEEVENTF_WHEEL, 0, param, -1, 0)
        time.sleep(0.01)


class uiApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Class of 2024")
        self.iconbitmap('uta.ico')
        self.geometry('300x150')
        self.label = Label(self, text="UTA ID")  # UTA ID label
        self.label.pack()

        self.entry = tk.Entry(self)  # UTA ID Entry
        self.entry.pack()

        self.label2 = Label(self, text="Password")  # Password label
        self.label2.pack()

        self.entry2 = tk.Entry(self)  # password entry
        self.entry2 = Entry(self, show="*", width=15)  # Security of the content entry
        self.entry2.pack()

        self.button = tk.Button(self, text="Submit", command=self.on_button)  # Button
        self.button.pack()

    def on_button(self):
        global uname, pswrd
        uname = self.entry.get()
        pswrd = self.entry2.get()
        self.destroy()  # exit windows

    def screenoverlay(self, parram):
        overlay = tk.Label(text=parram, font=('Ariel', '15'), fg='white', bg='blue')
        overlay.master.overrideredirect(True)
        overlay.master.geometry("+20+120")
        overlay.master.lift()
        overlay.master.wm_attributes("-topmost", True)
        overlay.master.wm_attributes("-disabled", True)

        hWindow = pywintypes.HANDLE(int(overlay.master.frame(), 16))
        # Click Exception
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
        overlay.pack()


visuals = uiApp()
visuals.mainloop()
driver.get(url)
driver.maximize_window()
time.sleep(0.01)
webscroll(400)
time.sleep(3)

# For the automation to occur I decided to use X-Paths and sometimes element ID from the Website for navigation

webrequesthandler('studentBtn', 0, "")  # (click) Student login button ID
webrequesthandler("/html/body/div/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[3]/a/button", 1, "")            # (click) Student Login button Xpath
time.sleep(0.1)
webrequesthandler('//*[@id="i0116"]', 2, uname)  # (sending keys) Email
webrequesthandler('//*[@id="i0118"]', 2, pswrd)  # (sending keys) Password

while driver.title == 'Sign in to your account':
    win32api.keybd_event(0x0D, 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)
    driver.implicitly_wait(0.5)
    if len(driver.find_elements_by_id('idTxtBx_SAOTCC_OTC')) != 0:
        time.sleep(30)
        break

while xit == False:
    if driver.title == 'Homepage':                                                                                      # Making sure we have reached the UTA main page
        if len(driver.find_elements_by_xpath('//*[@id="win5divPTGP_APP_WRK_PTGP_TILE_HTM_AREA"]/div/div/div/img')) != 0:
            break
    driver.implicitly_wait(5)

webscroll(200)
webrequesthandler('PTNUI_LAND_REC14$0_row_7', 0, "")                                                                    # (click) Admissions tab in the portal

while xit == False:
    if driver.title == 'Fluid TSI Status':
        if len(driver.find_elements_by_xpath('//*[@id="PT_WORK_PT_BUTTON_BACK"]/span')) != 0:
            break
    driver.implicitly_wait(5)
time.sleep(10)
webrequesthandler('win6div$ICField10$2', 0, "")                                                                         # (click) Admissions status in the portal

while xit == False:                                                                                                     # Making sure we are in the admissions tab
    if driver.title == 'Admissions':
        if len(driver.find_elements_by_xpath('//*[@id="DERIVED_SAD_FL_SAD_ADM_APP_FL_LBL"]')) != 0:
            break
    driver.implicitly_wait(5)

# OpenCV Integration with temp image collection

while xit == False:
    capture = driver.get_screenshot_as_png()
    cv2.imshow('OpenCV Output', capture)
    time.sleep(0.000001)                                                                                                # Delay
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break                                                                                                           # Exiting iteration upon press of Q key


time.sleep(30)
driver.minimize_window()
driver.quit()
cv2.destroyAllWindows()
gradyear = int(datetime.datetime.today().year) + 4
visuals.screenoverlay("Congratulations, Welcome to the Maverick class of " + str(gradyear))
visuals.mainloop()
