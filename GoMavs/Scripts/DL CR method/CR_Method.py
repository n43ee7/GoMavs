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
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import datetime, time

os.chdir('../..')  # Moving to the top of the project directory
print("[!] System Directory Shifted to ", os.getcwd())

url = "https://www.uta.edu/mymav/"  # UTA WebPage URL
service = Service(os.path.join('Chromedriver', 'chromedriver_80.exe'))  # Root path to Chromedriver.exe
service.start()
driver = webdriver.Remote(service.service_url)
uname = ''  # Global Var for Username
pswrd = ''  # Global Var for Password
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


def cv_predictions(scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    #
    # Credits to Ardian at PyImageSearch for this function (Check him out for more CV marvels)
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            if scoresData[x] < 0.6:  # Setting Min confidence as 60% for certainty in data
                continue

            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # return a tuple of the bounding boxes and associated confidences
    return rects, confidences


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
webrequesthandler("/html/body/div/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[3]/a/button", 1,
                  "")  # (click) Student Login button Xpath
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
    if driver.title == 'Homepage':  # Making sure we have reached the UTA main page
        if len(driver.find_elements_by_xpath('//*[@id="win5divPTGP_APP_WRK_PTGP_TILE_HTM_AREA"]/div/div/div/img')) != 0:
            break
    driver.implicitly_wait(5)

webscroll(200)
webrequesthandler('PTNUI_LAND_REC14$0_row_7', 0, "")  # (click) Admissions tab in the portal

while xit == False:
    if driver.title == 'Fluid TSI Status':
        if len(driver.find_elements_by_xpath('//*[@id="PT_WORK_PT_BUTTON_BACK"]/span')) != 0:
            break
    driver.implicitly_wait(5)
time.sleep(10)
webrequesthandler('win6div$ICField10$2', 0, "")  # (click) Admissions status in the portal

while xit == False:  # Making sure we are in the admissions tab
    if driver.title == 'Admissions':
        if len(driver.find_elements_by_xpath('//*[@id="DERIVED_SAD_FL_SAD_ADM_APP_FL_LBL"]')) != 0:
            break
    driver.implicitly_wait(5)

# OpenCV Integration with temp image collection
padding = 0.0
eastloc = str(os.path.join(os.getcwd(), 'frozen_east_text_detection.pb'))
width = 320
height = 320
while not xit:
    capture = driver.get_screenshot_as_png()
    cv2.imread(capture)
    orig = capture.copy()
    (origH, origW) = capture.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = origW / float(newW)
    rH = origH / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(capture, (newW, newH))
    (H, W) = image.shape[:2]

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[!] loading EAST text detector...")
    net = cv2.dnn.readNet(eastloc)

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = cv_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * padding)
        dY = int((endY - startY) * padding)

        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + (dX * 2))
        endY = min(origH, endY + (dY * 2))

        # extract the actual padded ROI
        roi = orig[startY:endY, startX:endX]

        # in order to apply Tesseract v4 to OCR text we must supply
        # (1) a language, (2) an OEM flag of 4, indicating that the we
        # wish to use the LSTM neural net model for OCR, and finally
        # (3) an OEM value, in this case, 7 which implies that we are
        # treating the ROI as a single line of text
        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(roi, config=config)

        # add the bounding box coordinates and OCR'd text to the list
        # of results
        results.append(((startX, startY, endX, endY), text))

    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r: r[0][1])

    # loop over the results
    for ((startX, startY, endX, endY), text) in results:
        # display the text OCR'd by Tesseract
        print("=================================")
        print("[!] Detected text")
        print("=================================")
        print("{}\n".format(text))

    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV, then draw the text and a bounding box surrounding
    # the text region of the input image
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        output = orig.copy()
        cv2.rectangle(output, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.putText(output, text, (startX, startY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

         # show the output image
        cv2.imshow("Text Detection", output)
        cv2.waitKey(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[!] Aborted Execution!")
        break  # Exiting iteration upon press of Q key



time.sleep(30)
driver.minimize_window()
driver.quit()
cv2.destroyAllWindows()
gradyear = int(datetime.datetime.today().year) + 4
visuals.screenoverlay("Congratulations, Welcome to the Maverick class of " + str(gradyear))
visuals.mainloop()
