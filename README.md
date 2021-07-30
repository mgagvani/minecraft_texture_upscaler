# Minecraft Texture Upscaler
#### Have you ever wanted to try a cool texture pack you saw on the Net? And then realized that the high-res one they use is stuck behind a paywall? This program can take a lower-res texture pack and scale it up. It looks virtually the same as the originals. 

## Usage
Minecraft Texture Upscaler is built on **Python** and OpenCV's **contrib** module. 
1. Install Python 3.7 or later. 
2. Install OpenCV with `pip install opencv`
3. Install OpenCV Contrib Modules with `pip install opencv-contrib-python`
4. Install Pillow: `pip install pillow`
5. Put the code where your textures are stored.
6. Download the Super Resolution models [here](https://1drv.ms/u/s!AqCfKwE9L_nAgZYzRBuM8rTIHD2DrA?e=dyT3yp) and put it in the same folder. 
7. Run texturepack.py, put in the required information, and enjoy! 

Notes:
* Type in the model to use in ALL CAPS.
* The EDSR model supports x2, x3, and x4 upscaling. It produces the best results, but takes a lot of time to process images. 
* The ESPCN model supports x2, x3, and x4 upscaling.
* The FSRCNN model also supports x2, x3 and x4 upscaling.
* The LapSRN model supports x2, x4, x8 upscaling.
* By default, the program tries to use CUDA, which will only work with an Nvidia GPU. If you do not have CUDA it will fall back to using the CPU, which is slower.

## References
[Deep Learning based Super Resolution with OpenCV](https://towardsdatascience.com/deep-learning-based-super-resolution-with-opencv-4fd736678066)
[OpenCV - Upscaling images: single-output](https://docs.opencv.org/master/d5/d29/tutorial_dnn_superres_upscale_image_single.html)




