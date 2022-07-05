import glob
import cv2
import numpy as np
import random
import string
import tqdm
import math

dic = {}

# 調整する平均輝度を設定
averageBrightness = 150

files = glob.glob("./images/*/*g")

def sigmoid(a):
    s = 1 / (1 + math.e**-a)
    return s

for file in tqdm.tqdm(files):
    img=cv2.imread(str(file))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h,s,v = cv2.split(hsv)
    
    mean = np.mean(v)
    std = np.std(v)
    
    for i in range(1000):
        gamma = 1.0
        if mean > averageBrightness:
            gamma = 1.05
        else:
            gamma = 0.95
        
        x = np.arange(256)
        y = (x / 255) ** gamma * 255
        v = cv2.LUT(v.astype(np.uint8), y)
        mean = v.mean()
        std = v.std()
        print("mean:", mean, "std:", std)
        
        if averageBrightness - 1 < mean < averageBrightness + 1:
            
            result = np.array(v, dtype=np.uint8)
            hsv = cv2.merge((h,s,result))
            rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            cv2.imwrite(file, rgb)
            mean = result.mean()
            std = result.std()
            print("mean:", mean, "std:", std)
            break
    