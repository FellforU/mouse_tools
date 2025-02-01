from PIL import Image
import os

def convert_to_ico(png_path, ico_path):
    # 打开PNG图片
    img = Image.open(png_path)
    
    # 确保图片是RGBA模式
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 调整大小为标准图标尺寸（可以是16x16, 32x32, 48x48, 256x256等）
    sizes = [(16,16), (32,32), (48,48), (256,256)]
    img.save(ico_path, format='ICO', sizes=sizes)

# 转换图片
if os.path.exists('mouse.png'):
    convert_to_ico('mouse.png', 'mouse.ico')
    print("转换完成!")
else:
    print("找不到 mouse.png 文件") 