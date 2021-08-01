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
import gc

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
        if len(cv2.split(cv2.imread(img, cv2.IMREAD_UNCHANGED))) == 4: # Image has alpha channel
            try:
                oldtime = time.time()
                alpha = cv2.split(cv2.imread(img, cv2.IMREAD_UNCHANGED))[-1] # Get the alpha channel
                image = cv2.imread(img)
                newimg = sr.upsample(image)
                newalpha = cv2.resize(alpha, (alpha.shape[0]*scalefactor, alpha.shape[1]*scalefactor), interpolation=cv2.INTER_CUBIC)
                r,g,b = cv2.split(newimg)
                newimg = cv2.merge([r,g,b,newalpha]) # Put together all the channels
                cv2.imwrite(img, newimg)
                print(f"Spent {time.time() - oldtime} seconds upscaling 4ch {img}")
            except Exception as e:
                print(f"Error {e} with {img}. Skipping.")
                continue # Skip and continue to next image
        elif len(cv2.split(cv2.imread(img, cv2.IMREAD_UNCHANGED))) == 3: # Image does not have alpha, just RGB
            try:
                oldtime = time.time()
                image = cv2.imread(img)
                newimg = sr.upsample(image)
                cv2.imwrite(img, newimg)
                print(f"Spent {time.time() - oldtime} seconds upscaling 3ch {img}")
            except Exception as e:
                print(f"Error {e} with {img}. Skipping.")
                continue
        else:
            print(f"Error. Image {img} does not have 3 or 4 channels.")
        
        # Delete old images since they will not be used anymore
        del newimg
        del image
        gc.collect()


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
    print(f"\nExtracted {folder} in {time.time() - oldtime} seconds \n")

    oldtime = time.time()
    upscale(scalefactor=scalefactor,algo=model)
    print(f"\nUpscaled images {folder} in {time.time() - oldtime} seconds \n")

    oldtime = time.time()
    finalize(scalefactor=scalefactor, name=folder)
    print(f"\nSaved upscaled (x{scalefactor}) texturepack in {time.time() - oldtime} seconds \n")

if __name__ == "__main__":
    main()
