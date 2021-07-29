# Minecraft Texture Upscaler

## Usage
Minecraft Texture Upscaler is built on Python and OpenCV's **contrib** module. 
1. Install Python 3.7 or later. 
2. Install OpenCV with `pip install opencv`
3. Install OpenCV Contrib Modules with `pip install opencv-contrib-python`
4. Install Pillow: `pip install pillow`
5. Put the code where your textures are stored.
6. Download the Super Resolution models [here](https://1drv.ms/u/s!AqCfKwE9L_nAgZYzRBuM8rTIHD2DrA?e=dyT3yp) and put it in the same folder. 
7. Run texturepack.py, put in the data, and enjoy! 

Notes:
* Type in the model to use in ALL CAPS.
* The EDSR model supports x2, x3, and x4 upscaling.
* The ESPCN model supports x2, x3, and x4 upscaling.
* The FSRCNN model also supports x2, x3 and x4 upscaling.
* The LapSRN model supports x2, x4, x8 upscaling.



