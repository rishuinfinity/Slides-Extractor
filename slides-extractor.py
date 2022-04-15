#!/usr/bin/env python
# coding: utf-8


### Necessary imports
import cv2
import os
import math
import subprocess as sp
import numpy as np
import sys
from time import sleep
from PIL import Image

### Listing variables
global videoFile
global threshold
global time_interval
videoFiles = []
threshold = 25
time_interval = 3

### Reading arguments

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hm"

# Long options
long_options = ["help", "multiple"]


try:

    if len(argumentList) == 1 and (argumentList[0] not in ["-h","--help"]):
        videoFiles.append(argumentList[0])
    elif argumentList[0] in ["-m","--multiple"]:
        for i in range(1,len(argumentList)):
            videoFiles.append(argumentList[i])
    else:
        print(
            " Usage1: slides_extractor.py {filename}\n",
            "Usage2: slides_extractor.py [OPTION] [VALUE(s)]\n\n",
            "-h, --help : show this help\n",
            "-m, --multiple: multiple files, write names of all the files separated by space\n",
            "Note: The filename should not contain any spaces. So, either use inverted-commas or put ' \ ' before space"
            )
        quit()
			
except:
	# output error, and return with an error code
    # print("Oops", sys.exc_info()[0])
    # print ("Invalid command: use ' slides_extractor.py -h ' to get help")
    quit()

def ImgCmp(img1,img2):
    if(img1.shape != img2.shape):
        print("Exception: images' shapes inconsistent")
    # both images are numpy array with shape (1080,1920,3)
    shape = img1.shape
    split1 = []
    split2 = []
    # I have to make 4 sections of the image
    split1.append(img1[:shape[0]//2, :shape[1]//2])
    split1.append(img1[:shape[0]//2, shape[1]//2:])
    split1.append(img1[shape[0]//2:, :shape[1]//2])
    split1.append(img1[shape[0]//2:, shape[1]//2:])
    split2.append(img2[:shape[0]//2, :shape[1]//2])
    split2.append(img2[:shape[0]//2, shape[1]//2:])
    split2.append(img2[shape[0]//2:, :shape[1]//2])
    split2.append(img2[shape[0]//2:, shape[1]//2:])

    # just taking the whole image
    # split1.append(img1)
    # split2.append(img2)

    outs = []
    for i in range(len(split1)):
        sqsum = (split1[i]-split2[i])**2
        sqsum_mean = np.sum(sqsum)/(split1[i].shape[0] * split1[i].shape[1]);
        outs.append(sqsum_mean)
    decider = np.array(outs)
    return decider
    
### Bothway Comparision
def Compare(lastframe,frame,newframe):
    pcmp = ImgCmp(lastframe,frame)
    ncmp = ImgCmp(frame,newframe )
    diff = abs(pcmp-ncmp) # new change: added abs
    # attempt to ignore mouse motion
    # marker = np.sum(diff < 4)
    # if marker >= 2:
    #     return False
    diff = np.sum(diff)/diff.size
    if(diff > threshold):
        return True
    return False

### Extractor
# Create a cache directory
cache_dir = "cache"
while os.path.isdir(cache_dir):
    cache_dir+="1"
os.mkdir(cache_dir)

for videoFile in videoFiles:
    print("Starting processing for ",videoFile)
    #cache is expected to be empty
    count = 0
    frame=np.zeros((1080,1920,3))
    lastframe=np.zeros((1080,1920,3))
    cap = cv2.VideoCapture(videoFile)
    frameRate = cap.get(5) #frame rate
    total_frames=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print("Frame Rate ", frameRate)
    img_gap = math.floor(frameRate * time_interval) # ive set image interval to 10sec
    if(img_gap == 0): # exception handling
        img_gap = 1
        print("Warning: img_gap has become 0, changing it appropriately")
        
        
        
    ## To figure out the threshold value
    # mean_storage = []
    ##
    visited_frames = 0
    image_list=[]
    while(cap.isOpened()):
        visited_frames+=1
        frameId = cap.get(1) #current frame number
        ret, newframe = cap.read()
        if (ret != True):
            break
        if (frameId % img_gap == 0):
            # We got the frame we wanted
            if(Compare(lastframe,frame,newframe)):
                cv2.imwrite("./"+cache_dir+"/"+str(count) + ".jpg",lastframe)
                image_list.append(str(count) + ".jpg")
                count+=1

            lastframe = frame
            frame = newframe
            print(" ",round(visited_frames*100/total_frames,2),"%",end='\r')
    cv2.imwrite("./"+cache_dir+"/"+str(count) + ".jpg",lastframe)
    image_list.append(str(count) + ".jpg")
    count+=1
    cv2.imwrite("./"+cache_dir+"/"+str(count) + ".jpg",frame)
    image_list.append(str(count) + ".jpg")
    cap.release()
    print("Total image count ", count)
    print ("Images are extracted in cache, proceeding to create a pdf!")
    # print(image_list)
    image_list = [Image.open('./'+cache_dir+"/"+f).convert('RGB') for f in image_list]
    if os.path.isfile(videoFile+".pdf"):
        os.remove(videoFile+".pdf")
    image_list[0].save(videoFile+".pdf", save_all=True, append_images=image_list)
    for f in os.listdir(cache_dir):
        os.remove(cache_dir+"/"+f)
    os.rmdir(cache_dir)


