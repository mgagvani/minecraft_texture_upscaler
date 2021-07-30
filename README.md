# Minecraft Texture Upscaler
#### Have you ever wanted to try a cool texture pack you saw on the Net? And then realized that the high-res one they use is stuck behind a paywall? This program can take a lower-res texture pack and scale it up. It produces textures indistinguishable from the originals.
Left | Right
------------ | -------------
32x Texture | 128x Upscaled texture 


![gold_ore](https://user-images.githubusercontent.com/37602685/127584667-112116f4-61b0-437a-9c34-a58afefb8731.png)
![gold_ore](https://user-images.githubusercontent.com/37602685/127584944-916e65a2-423f-4f8b-a042-ea82af74f109.png)

![redstone_ore](https://user-images.githubusercontent.com/37602685/127586238-a34373d3-8e1d-4b22-a948-7579a90b628a.png)
![redstone_ore](https://user-images.githubusercontent.com/37602685/127586172-72b3b1c3-e86e-461c-b4c9-03dc87076835.png)


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




