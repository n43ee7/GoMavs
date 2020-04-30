# GoMavs  🐎 💻
 
### Be a Maverick 
Automation scripts that will accept your offer for you while you record it or just chill.
_______________________________________________________________________________________________
___Overview of files and contents___

## 1) Automation method 
__(File name: \Scripts\Automation method\Automation_Method.py)__

This script is indipendent of any machine learning libraries and focuses on direct system automation and web control to do the job. The navigation throughout the script is done in XML XPaths for the elements and entities on the website. _If you recieve any errors please update all xpaths for the website_. 

__Note:__ When installing dependencies and required packages use the 'Requirements.txt' in the installation procedure below.

## 2) Machine Learning typetext character recognition method 
__(File name: \Scripts\DL CR method\CR_Method.py)__

This script is a method partially moving towards Machine learning where Type Text Recognition network __Google Tessract__ takes over the final process of accepting your offer with OpenCV preview of the predictions of the network. 

Eventhough you __need not__ to Train Tessract, a trainging script is still present if in case the webmasters of the website change to a font not detecteable by the network. 

__Note:__ When installing dependencies and required packages use the 'Requirements.txt' along the script in the respective directory in the installation procedure below.

_______________________________________________________________________________________________
## Supported platforms

* Windows 7/8/10 with Chrome version 80 or later,  Python 3.x or later

_______________________________________________________________________________________________
# Installation and Running 

## Installing project folder
Clone this repository and unzip the files

## Installing Python dependencies using requirements.txt
Move to virtual enviorment (if any) and use the following command to install the project dependencies and packages.
(Make sure you have pip and Python3.x installed on your machine)

``` pip3 install -r Requirements.txt```

## Running The script
Run the script by moving to the scripts folder and typing the following in the terminal opened in the relevant directory

``` python3 'script_name'.py ```

__Note:__ The 'script name' is the name of the script in the directory with the names given above

_________________________________________________________________________________________________
## Disclaimer!
The contents of this repository are purely designed for educational purposes with motives for others to learn and seek aid for their projects. Every user advised to exercise caution during the run-time of this program as any malfunctions could caused by the script may lead to any action that could lead to unknown conclusions. You are advised to be very __cautious__ during the code runtime and ensure all X-Path or other parameters used for navigating through the websites before running since there may be changes to the website after the latest commit of this repository. <3
