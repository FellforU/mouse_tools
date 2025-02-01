XCC的鼠小侠
版本：1.0
作者：XCC

功能说明：
1. 鼠标连点
   - 支持左键、中键、右键
   - 支持自定义间隔
   - F8 开始/停止

2. 鼠标录制
   - 记录鼠标操作
   - F8 开始/停止录制
   - F9 开始/停止回放

3. 鼠标宏
   - 支持录制宏
   - 支持编辑延迟
   - 支持循环执行
   - F7 开始/停止录制
   - F6 开始/停止执行

注意事项：
1. 首次运行会自动创建recordings和macros文件夹
2. 建议仅用于测试和学习用途
3. 在某些游戏中使用可能违反规则 

打包：
pip install pyinstaller
然后执行 build_exe.py
或者
pyinstaller example_usage.py --name="XCC的鼠小侠" --windowed --onefile --clean --noconfirm