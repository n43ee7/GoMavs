# GoMavs  🐎 💻
 
### Be a Maverick
_______________________________________________________________________________________________
___Overview of files and contents___

## 1) Machine Learning typetext character recognition method 
__(File name: \Scripts\DL CR method\CR_Method.py)__

This script is a method partially moving towards Machine learning where LTSM Type Text Recognition network __Google Tessract__ takes over the final process of accepting your offer with OpenCV preview of the predictions of the network. 

## 2) Training Script

This script is the optional training script which you would need to retrain __Tessract__. Eventhough you __need not__ to Train Tessract, a trainging script is still present if in case the webmasters of the website change to a font not detecteable by the network. 
__Note:__ Enter the .ttf (be sure to name it 'font.ttf') file of the new font used on the website if you are to train Tesract in case it fails. 

_______________________________________________________________________________________________
# Installation and Running 

## Installing project folder
Clone this repository, unzip the files and move the this directory on the terminal (Scripts/DL CR method/) 

## Installing Python dependencies using requirements.txt
Move to virtual enviorment (if any) and use the following command to install the project dependencies and packages.
(Make sure you have pip and Python3.x installed on your machine)

``` pip3 install -r Requirements.txt```

## (OPTIONAL) Training the Neural Network
Ensure the relevant font.ttf file is present in the ```Font``` directory and run the following command

```python3 Training.py```

After the succesful execution of the script you will get newer files of the network which you will have to intigrate to the main script 'CR_Method.py' to replace the previous Tessract.

## Running The script
Run the script by a terminal

``` python3 'CR_Method.py' ```

## Enjoy!
If all the steps are sucessfull the script should take over to accept your offer in style :)
Just be sure to follow up with the prompts where it asks you password and where you need to enter the SMS OTP since these measures will need to be done manually for security purposes.
