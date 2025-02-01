from PIL import Image, ImageDraw

# 创建一个 256x256 的透明背景图像
size = 256
image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# 绘制鼠标形状
# 主体
draw.ellipse((78, 78, 178, 178), fill='black', outline='white', width=3)
# 左键
draw.rectangle((88, 98, 128, 138), fill='gray')
# 右键
draw.rectangle((128, 98, 168, 138), fill='gray')
# 滚轮
draw.ellipse((118, 88, 138, 108), fill='white')
# 连接线
draw.line((128, 138, 128, 168), fill='black', width=3)

# 保存为 ICO 文件
image.save('mouse.ico', format='ICO') 