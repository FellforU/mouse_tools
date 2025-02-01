import os
import subprocess

# 确保目录存在
os.makedirs("dist", exist_ok=True)
os.makedirs("build", exist_ok=True)

# 构建命令
cmd = [
    'pyinstaller',
    'example_usage.py',
    '--name=XCC的鼠小侠',
    '--windowed',
    '--onefile',
    '--clean',
    '--noconfirm'
]

# 如果有图标文件，添加图标
if os.path.exists('mouse.ico'):
    cmd.append('--icon=mouse.ico')

# 如果有说明文档，添加文档
if os.path.exists('README.txt'):
    cmd.append('--add-data=README.txt;.')

# 执行打包命令
print("开始打包...")
result = subprocess.run(cmd, capture_output=True, text=True)

# 打印输出
print(result.stdout)
if result.stderr:
    print("错误信息:")
    print(result.stderr)

print("打包完成!") 