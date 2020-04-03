import win32api, win32con, win32gui
import tkinter as tk
from tkinter import *
import cv2
import tensorflow as tf
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
from PIL import ImageGrab
from win32api import GetSystemMetrics

S_Width = GetSystemMetrics(0)
S_Height = GetSystemMetrics(1)  # Creating the TK instance
url = "https://www.uta.edu/mymav/"  # UTA WebPage URL
service = Service(
    'Chromedriver/chromedriver_80.exe')  # Root path to Chromedriver.exe (Be sure to verify your chrome version before altering)
service.start()
driver = webdriver.Remote(service.service_url)
uname = ''
pswrd = ''


def mouse_del(x, y):
    xcurrent, ycurrent = win32gui.GetCursorPos()
    xcurrent = int(xcurrent)
    ycurrent = int(ycurrent)
    for xi in range(xcurrent, x, -10):
        for yi in range(ycurrent, y, -10):
            time.sleep(0.0000000000000005)
            win32api.SetCursorPos((xi, yi))
    time.sleep(0.00000000000005)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)  # Hope nobody notices
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    print("[!] Manual click at", x, y)


def screencapture():
    # Saving engine replace to output for now
    print(S_Width)
    print(S_Height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = "output" + str(time.time()) + ".avi"
    out = cv2.VideoWriter(filename, fourcc, 15.0, (GetSystemMetrics(0), GetSystemMetrics(1)))
    time.sleep(3)
    # Recoding engine
    while True:
        img = ImageGrab.grab()
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        out.write(frame)
        classifier(frame)
        if cv2.waitKey(1) == 37:
            break
    out.release()
    cv2.destroyAllWindows()


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
        entry.send_keys(Keys.ENTER)
        entry.send_keys(Keys.ENTER)


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
        self.destroy()  # exit windows                                                  #


def prepare(file):
    IMG_SIZE = 416
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


def classifier(image):
    CATEGORIES = ["accept_button", "misc_button"]
    model = tf.keras.models.load_model("Training/CNN.model")            # Location to the trained classifier
    image = prepare(image)
    prediction = model.predict([image])
    prediction = list(prediction[0])
    return CATEGORIES[prediction.index(max(prediction))]


app = uiApp()
app.mainloop()
driver.get(url)
driver.maximize_window()
time.sleep(0.005)
for xe in range(0, 400, 10):
    driver.execute_script("window.scrollTo(0, " + str(xe) + ");")  # Hardcoded scroll parameter (xe)）
    time.sleep(0.0001)

# For the automations to occur I decided to use X-Paths and sometimes element ID from the Website(s) for script to navigate through.

webrequesthandler('studentBtn', 0, "")  # (click) Student login button ID
webrequesthandler("/html/body/div/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[3]/a/button", 1,
                  "")  # (click) Student Login button Xpath
webrequesthandler("/html/body/div/form[1]/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]", 2,
                  uname)  # (sending keys) Email
webrequesthandler('//*[@id="i0118"]', 2, pswrd)  # (sending keys) Password

time.sleep(20)  # Delay for the SMS OTP Manuall (entry)

time.sleep(5)  # change to something sensible at end
driver.minimize_window()
driver.quit()
