# Program to upscale or downscale Minecraft texture packs

import glob
import os
from PIL import Image # pip install pillow 

import cv2 # pip install opencv
from cv2 import dnn_superres # pip install opencv-contrib-python
import time

import zipfile
import json
import shutil

def downscale(path): # Legacy

    imgs = glob.glob(path+ "/**/*.png",recursive=True)

    for i,img in enumerate(imgs):
        # filename = os.path.basename(img)
        print(img)
        # filename=img[:-4] + "_old.png"
        # print(filename)
        # os.replace(img,filename)
        image = Image.open(img)
        width, height = image.size
        w = int(width/2)
        h = int(height/2)
        image = image.resize((w,h))
        image.save(img.replace("_old",""))
        os.remove(img) # this stuff gets commented out in the first stage(renaming everthing)
    
def upscale(scalefactor=4, algo="EDSR", use_cuda=True):
    sr = dnn_superres.DnnSuperResImpl_create()    
    path = f"./models/{algo}_x{scalefactor}.pb"
    sr.readModel(path)

    if use_cuda:# Set CUDA backend and target to enable GPU inference
        sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # Set the desired model and scale to get correct pre- and post-processing
    sr.setModel(algo.lower(), scalefactor)

    path = "./temp/assets/minecraft/"
    imgs = glob.glob(path+ "/**/*.png",recursive=True)

    for i,img in enumerate(imgs):
        oldtime = time.time()
        image = cv2.imread(img, cv2.IMREAD_UNCHANGED)
        newimg = sr.upsample(image)
        cv2.imwrite(img, newimg)
        print(f"Spent {time.time() - oldtime} seconds upscaling {img}")

def extract(filename):
    data_zip = zipfile.ZipFile(f"./{filename}.zip", "r")
    data_zip.extractall(path="temp/")
    
def finalize(scalefactor=4, name="./Upscaled_Textures"):
    # Edit MCMETA file
    meta_str = open("./temp/pack.mcmeta").read()
    meta = json.loads(meta_str)
    meta["pack"]["description"] += f" Upscaled x{scalefactor}"
    with open("./temp/pack.mcmeta","w",encoding="utf-8") as file:
        json.dump(meta, file)

    # Zip file again
    # data = glob.glob("temp/**/*",recursive=True)

    shutil.make_archive(f"{name}_x{scalefactor}","zip","./temp/")
    # Delete temp folder
    shutil.rmtree("./temp/")

def main():
    folder = input("Name of texture pack to upscale: ")
    scalefactor = int(input("Scale Factor(Can be 2,3,4,or 8, depending on model): "))
    model = input("Super Resolution model to use: ")
    
    oldtime = time.time()
    extract(folder)
    print(f"\n Extracted {folder} in {time.time() - oldtime} seconds \n")

    oldtime = time.time()
    upscale(scalefactor=scalefactor,algo=model)
    print(f"\n Upscaled images {folder} in {time.time() - oldtime} seconds \n")

    oldtime = time.time()
    finalize(scalefactor=scalefactor, name=folder)
    print(f"\n Saved upscaled (x{scalefactor}) texturepack in {time.time() - oldtime} seconds \n")

if __name__ == "__main__":
    main()
