#   Created by Nabeel Nayyar (@n43ee7)
#   This script will generate a set of random test data and train a DL-NN (Deep Learning Neural Network) on the random
#   test data.
#
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
import string
from skimage.io import imread
from TFANN import ANNC

MAX_CHAR = 64
ImageSize = (14, 640, 3)                                                                            # Image size for CNN
A, Y, T, FN = [], [], [], []

def ComposeImg(t, f, fn, s = (100, 100), o=(16, 8)):
    """
    Generate an image of text
    t:      The text to display in the image
    f:      The font to use
    fn:     The file name
    s:      The image size
    o:      The offset of the text in the image
    """
    img = Image.new('RGB', s, "black")
    draw = ImageDraw.Draw(img)
    draw.text(OFS, t, (255, 255, 255), font=f)
    img.save(fn)


def LoadData(FP):
    '''
    Loads the OCR dataset. A is matrix of images (NIMG, Height, Width, Channel).
    Y is matrix of characters (NIMG, MAX_CHAR)
    FP:     Path to OCR data folder
    return: Data Matrix, Target Matrix, Target Strings
    Scripts/DL CR method/TrainData.csv
    '''
    TFP = os.path.join(FP, 'TrainData.csv')
    Aa, Yy, Tt, FNn = [], [], [], []
    with open(TFP) as F:
        for Li in F:
            FNi, Yi = Li.strip().split(',')                     #filename,string
            Tt.append(Yi)
            Aa.append(imread(os.path.join(FP, 'TrainingData', FNi)))
            Yy.append(list(Yi) + [' '] * (MAX_CHAR - len(Yi)))   #Pad strings with spaces
            FNn.append(FNi)
    return np.stack(Aa), np.stack(Yy), np.stack(Tt), np.stack(FNn)


scriptpath = os.getcwd()
CS = list(string.ascii_letters) + list(string.digits)
RTS = list(np.random.randint(10, 64, size=300)) + [64]                                   # Size = The amount of data files produced for learning Default file limit 8300
S = [''.join(np.random.choice(CS, i)) for i in RTS]                                      # Generating the random strings
fontpath = os.path.join(scriptpath, 'Fonts', 'arial.ttf')
font = ImageFont.truetype(fontpath, 16)                               # Setting Text properties for Generating test data
# The largest size needed
MS = max(font.getsize(Si) for Si in S)
# Computed offset
OFS = ((640 - MS[0]) // 2, (32 - MS[1]) // 2)
MS = (640, 32)
Y = []

os.chdir(os.path.join(scriptpath, 'TrainingData'))                                  # Moving to an appropriate Directory
for i, Si in enumerate(S):
    ComposeImg(Si, font, str(i) + '.png', MS, OFS)
    Y.append(str(i) + '.png,' + Si)
    print("[!] Random Training Text File Composed: ", str(i), ".png")
    with open(os.path.join(scriptpath, 'TrainData.csv'), 'w') as file:                  # Write the file CSV
        file.write('\n'.join(Y))
# ======================================================================================================================
# Architecture of the neural network

NC = len(string.ascii_letters + string.digits + ' ')
ws = [('C', [4, 4,  3, NC // 2], [1, 2, 2, 1]), ('AF', 'relu'),
      ('C', [4, 4, NC // 2, NC], [1, 2, 1, 1]), ('AF', 'relu'),
      ('C', [8, 5, NC, NC], [1, 8, 5, 1]), ('AF', 'relu'),
      ('R', [-1, 64, NC])]
A, Y, T, FN = LoadData(scriptpath)
cnnc = ANNC(ImageSize, ws, batchSize=64, learnRate=5e-5, maxIter=32, reg=1e-5, tol=1e-2, verbose=True)                  # Creating the neural network with TensorFlow
cnnc.fit(A, Y)                                                                                                          # Fit the network
YH = np.zeros((Y.shape[0], Y.shape[1]), dtype=np.int)                                                                  # The predictions as sequences of character indices
for i in np.array_split(np.arange(A.shape[0]), 32):
    YH[i] = np.argmax(cnnc.predict(A[i]), axis=2)
PS = [''.join(CS[j] for j in YHi) for YHi in YH]                                                                        # Convert from sequence of char indices to strings
for PSi, Ti in zip(PS, T):
    print(Ti + '\t->\t' + PSi)
cnnc.SaveModel(scriptpath)
print("[!] Model Saved on disk")
