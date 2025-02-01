from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import time
import json
import os
from tkinter import *
from tkinter import ttk, messagebox
import threading

class MouseApp:
    def __init__(self):
        import os
        os.environ['TK_SILENCE_DEPRECATION'] = '1'
        
        self.root = Tk()
        self.root.title("XCC的鼠小侠")
        self.root.geometry("500x600")
        
        # 设置窗口图标
        try:
            self.root.iconbitmap('mouse.ico')  # 添加这行来设置窗口图标
        except:
            pass  # 如果图标文件不存在，就使用默认图标
        
        # 初始化全局变量
        self.is_clicking = False
        self.click_thread = None
        self.keyboard_listener = None  # 移到前面来初始化
        
        # 创建标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # 创建三个页面
        self.auto_click_frame = ttk.Frame(self.notebook)
        self.recorder_frame = ttk.Frame(self.notebook)
        self.macro_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.auto_click_frame, text="鼠标连点")
        self.notebook.add(self.recorder_frame, text="鼠标录制")
        self.notebook.add(self.macro_frame, text="鼠标宏")
        
        # 初始化各个模块
        self.setup_auto_clicker()
        self.recorder = MouseRecorder(self.recorder_frame)
        self.macro = MouseMacro(self.macro_frame)
        
    def setup_auto_clicker(self):
        frame = self.auto_click_frame
        
        # 点击类型选择
        click_type_frame = ttk.LabelFrame(frame, text="点击类型", padding=10)
        click_type_frame.pack(fill=X, padx=10, pady=5)
        
        self.click_type = StringVar(value="left")
        ttk.Radiobutton(click_type_frame, text="鼠标左键", value="left", 
                       variable=self.click_type).pack(side=LEFT, padx=10)
        ttk.Radiobutton(click_type_frame, text="鼠标中键", value="middle", 
                       variable=self.click_type).pack(side=LEFT, padx=10)
        ttk.Radiobutton(click_type_frame, text="鼠标右键", value="right", 
                       variable=self.click_type).pack(side=LEFT, padx=10)
        
        # 点击间隔选择
        interval_frame = ttk.LabelFrame(frame, text="点击间隔", padding=10)
        interval_frame.pack(fill=X, padx=10, pady=5)
        
        self.interval_type = StringVar(value="normal")
        self.custom_interval = StringVar(value="0.1")
        
        def on_interval_change(*args):
            if self.interval_type.get() == "custom":
                custom_entry.config(state='normal')
            else:
                custom_entry.config(state='disabled')
        
        ttk.Radiobutton(interval_frame, text="高效模式 (每秒10次)", value="normal", 
                       variable=self.interval_type, command=on_interval_change).pack(anchor=W)
        ttk.Radiobutton(interval_frame, text="极速模式 (每秒100次)", value="fast", 
                       variable=self.interval_type, command=on_interval_change).pack(anchor=W)
        
        custom_frame = ttk.Frame(interval_frame)
        custom_frame.pack(fill=X, pady=5)
        ttk.Radiobutton(custom_frame, text="自定义间隔 (秒):", value="custom", 
                       variable=self.interval_type, command=on_interval_change).pack(side=LEFT)
        custom_entry = ttk.Entry(custom_frame, textvariable=self.custom_interval, width=10)
        custom_entry.pack(side=LEFT, padx=5)
        custom_entry.config(state='disabled')
        
        # 热键设置
        hotkey_frame = ttk.LabelFrame(frame, text="热键设置", padding=10)
        hotkey_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(hotkey_frame, text="启动/停止热键:").pack(side=LEFT, padx=5)
        self.hotkey = StringVar(value="F8")
        hotkey_combo = ttk.Combobox(hotkey_frame, textvariable=self.hotkey, width=10)
        hotkey_combo['values'] = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 
                                 'F9', 'F10', 'F11', 'F12']
        hotkey_combo.pack(side=LEFT, padx=5)
        
        # 状态显示
        self.status_label = ttk.Label(frame, text="当前状态: 已停止", font=('Arial', 10, 'bold'))
        self.status_label.pack(pady=20)
        
        # 设置键盘监听
        self.setup_keyboard_listener()
        
    def setup_keyboard_listener(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            
        def on_press(key):
            try:
                key_str = key.char.upper() if hasattr(key, 'char') else key.name.upper()
                if key_str == self.hotkey.get():
                    self.toggle_clicking()
            except: pass
            
        self.keyboard_listener = keyboard.Listener(on_press=on_press)
        self.keyboard_listener.start()
        
    def get_click_interval(self):
        interval_type = self.interval_type.get()
        if interval_type == "normal":
            return 0.1  # 每秒10次
        elif interval_type == "fast":
            return 0.01  # 每秒100次
        else:
            try:
                return float(self.custom_interval.get())
            except:
                return 0.1
                
    def toggle_clicking(self):
        if not self.is_clicking:
            self.start_clicking()
        else:
            self.stop_clicking()
            
    def start_clicking(self):
        if self.is_clicking:
            return
            
        self.is_clicking = True
        self.status_label.config(text="当前状态: 运行中")
        
        def clicking():
            mouse_controller = Controller()
            button_map = {
                'left': mouse.Button.left,
                'right': mouse.Button.right,
                'middle': mouse.Button.middle
            }
            button = button_map[self.click_type.get()]
            interval = self.get_click_interval()
            
            while self.is_clicking:
                mouse_controller.click(button)
                time.sleep(interval)
        
        self.click_thread = threading.Thread(target=clicking)
        self.click_thread.daemon = True
        self.click_thread.start()
        
    def stop_clicking(self):
        self.is_clicking = False
        self.status_label.config(text="当前状态: 已停止")
        if self.click_thread:
            self.click_thread.join(timeout=1.0)
            
    def run(self):
        try:
            self.root.mainloop()
        finally:
            # 清理资源
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            if self.click_thread and self.click_thread.is_alive():
                self.is_clicking = False
                self.click_thread.join(timeout=1.0)

class MouseRecorder:
    def __init__(self, parent_frame):
        self.recorded_events = []
        self.mouse_controller = Controller()
        self.recording = False
        self.start_time = 0
        self.listener = None
        self.keyboard_listener = None
        self.recording_start_datetime = None
        self.is_replaying = False
        self.setup_gui(parent_frame)
        
    def setup_gui(self, parent_frame):
        self.root = parent_frame
        
        # 录制按钮
        self.record_btn = ttk.Button(self.root, text="开始录制 (F8)", command=self.toggle_recording)
        self.record_btn.pack(pady=10)
        
        # 录制列表框架
        list_frame = ttk.LabelFrame(self.root, text="录制列表", padding=10)
        list_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # 创建带滚动条的列表
        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side=RIGHT, fill=Y)
        
        # 修改列定义，移除操作列
        columns = ("名称", "录制时间", "时长")
        self.recording_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                         yscrollcommand=list_scroll.set, selectmode='extended')
        
        # 设置列
        self.recording_tree.heading("名称", text="名称")
        self.recording_tree.heading("录制时间", text="录制时间")
        self.recording_tree.heading("时长", text="时长")
        
        self.recording_tree.column("名称", width=200)
        self.recording_tree.column("录制时间", width=120)
        self.recording_tree.column("时长", width=80)
        
        self.recording_tree.pack(fill=BOTH, expand=True)
        list_scroll.config(command=self.recording_tree.yview)
        
        # 右键菜单
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="重命名", command=self.rename_recording)
        self.context_menu.add_command(label="回放", command=self.replay_selected)
        self.context_menu.add_command(label="删除", command=self.delete_selected)
        
        self.recording_tree.bind("<Button-3>", self.show_context_menu)
        
        # 修改操作按钮区域，移除重命名按钮
        btn_frame = Frame(self.root)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="回放(F9)", command=self.replay_selected).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=self.delete_selected).pack(side=LEFT, padx=5)
        
        # 添加全选/取消全选按钮
        select_frame = Frame(self.root)
        select_frame.pack(pady=5)
        ttk.Button(select_frame, text="全选", command=self.select_all).pack(side=LEFT, padx=5)
        ttk.Button(select_frame, text="取消全选", command=self.deselect_all).pack(side=LEFT, padx=5)
        
        # 加载现有录制
        self.load_recordings_list()
        
        # 设置键盘监听
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
    def show_context_menu(self, event):
        item = self.recording_tree.identify_row(event.y)
        if item:
            self.recording_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def rename_recording(self):
        selected = self.recording_tree.selection()
        if not selected:
            return
            
        item = selected[0]
        old_name = self.recording_tree.item(item)['values'][0]
        
        # 创建重命名对话框
        dialog = Toplevel(self.root)
        dialog.title("重命名")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="新名称:").pack(pady=5)
        entry = ttk.Entry(dialog, width=40)
        entry.pack(pady=5)
        entry.insert(0, old_name)
        
        def do_rename():
            new_name = entry.get()
            if new_name and new_name != old_name:
                old_path = f"recordings/{old_name}.json"
                new_path = f"recordings/{new_name}.json"
                try:
                    os.rename(old_path, new_path)
                    self.load_recordings_list()
                except Exception as e:
                    messagebox.showerror("错误", f"重命名失败: {str(e)}")
            dialog.destroy()
            
        ttk.Button(dialog, text="确定", command=do_rename).pack(pady=5)
        
        # 居中显示对话框
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
    
    def format_duration(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}分{seconds}秒"
    
    def load_recordings_list(self):
        # 清除现有项目
        for item in self.recording_tree.get_children():
            self.recording_tree.delete(item)
            
        if not os.path.exists("recordings"):
            return
            
        for file in os.listdir("recordings"):
            if file.endswith(".json"):
                filepath = os.path.join("recordings", file)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        # 计算录制时长
                        if data:
                            duration = data[-1]['time']
                            # 获取文件修改时间
                            mod_time = os.path.getmtime(filepath)
                            record_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(mod_time))
                            
                            self.recording_tree.insert("", END, values=(
                                file[:-5],  # 名称（去除.json后缀）
                                record_time,  # 录制时间
                                self.format_duration(duration)  # 时长
                            ))
                except:
                    continue
                    
    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f8:
                self.toggle_recording()
            elif key == keyboard.Key.f9:
                self.toggle_replay()
        except: pass
    
    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
            self.record_btn.config(text="停止录制 (F8)")
        else:
            self.stop_recording()
            self.record_btn.config(text="开始录制 (F8)")
    
    def start_recording(self):
        self.recording = True
        self.recorded_events = []
        self.start_time = time.time()
        self.recording_start_datetime = time.localtime()
        self.last_event_time = self.start_time  # 添加这行，记录最后一个事件的时间
        
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click)
        self.listener.start()
    
    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.listener:
                self.listener.stop()
                
            # 创建recordings文件夹（如果不存在）
            os.makedirs("recordings", exist_ok=True)
            
            # 生成文件名：鼠标录制-时间戳
            timestamp = time.strftime("%Y%m%d-%H%M%S", self.recording_start_datetime)
            filename = f"recordings/鼠标录制-{timestamp}.json"
            
            self.save_recording(filename)
            self.load_recordings_list()
    
    def replay_selected(self):
        """开始回放选中的录制"""
        self.toggle_replay()  # 使用新的回放控制机制
    
    def delete_selected(self):
        """删除选中的录制（支持单个和批量）"""
        selected = self.recording_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要删除的录制")
            return
            
        # 获取选中的所有录制名称
        selected_names = []
        for item in selected:
            values = self.recording_tree.item(item)['values']
            if values:  # 确保有值
                selected_names.append(str(values[0]))  # 转换为字符串
        
        if not selected_names:  # 如果没有有效的名称
            return
            
        # 确认消息根据选中数量调整
        if len(selected_names) == 1:
            confirm_msg = f"确定要删除 {selected_names[0]} 吗？"
        else:
            confirm_msg = f"确定要删除选中的 {len(selected_names)} 个录制吗？\n\n" + \
                         "\n".join(str(name) for name in selected_names[:5]) + \
                         ("\n..." if len(selected_names) > 5 else "")
        
        # 确认删除
        if messagebox.askyesno("确认", confirm_msg):
            # 执行删除
            for name in selected_names:
                try:
                    os.remove(f"recordings/{name}.json")
                except Exception as e:
                    messagebox.showerror("错误", f"删除 {name} 失败: {str(e)}")
                    
            # 刷新列表
            self.load_recordings_list()
            if len(selected_names) > 1:
                messagebox.showinfo("成功", f"成功删除 {len(selected_names)} 个录制")

    def on_click(self, x, y, button, pressed):
        """记录鼠标点击事件"""
        if not self.recording:
            return
        
        current_time = time.time() - self.start_time
        event = {
            'type': 'click',
            'x': x,
            'y': y,
            'button': str(button),
            'pressed': pressed,
            'delay': int(current_time * 1000) if not self.recorded_events else int((current_time - self.last_event_time) * 1000)
        }
        self.last_event_time = current_time  # 记录这个动作的时间
        self.recorded_events.append(event)

    def on_move(self, x, y):
        """记录鼠标移动事件"""
        if not self.recording:
            return
            
        current_time = time.time() - self.start_time
        event = {
            'type': 'move',
            'x': x,
            'y': y,
            'delay': int(current_time * 1000) if not self.recorded_events else int((current_time - self.last_event_time) * 1000)
        }
        self.last_event_time = current_time  # 记录这个动作的时间
        self.recorded_events.append(event)

    def save_recording(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.recorded_events, f)
            
    def load_recording(self, filename):
        with open(filename, 'r') as f:
            self.recorded_events = json.load(f)
            
    def toggle_replay(self):
        """切换回放状态"""
        if not hasattr(self, 'is_replaying'):
            self.is_replaying = False
            
        if not self.is_replaying:
            self.start_replay()
        else:
            self.stop_replay()
            
    def start_replay(self):
        selected = self.recording_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要回放的录制")
            return
            
        self.is_replaying = True
        # 支持多个录制同时回放
        for item in selected:
            recording_name = self.recording_tree.item(item)['values'][0]
            self.load_recording(f"recordings/{recording_name}.json")
            # 为每个录制创建独立的回放线程
            replay_thread = threading.Thread(target=self.replay)
            replay_thread.daemon = True
            replay_thread.start()
            
    def stop_replay(self):
        self.is_replaying = False
        
    def replay(self):
        if not self.recorded_events:
            return
            
        last_time = 0
        button_map = {
            'button.left': mouse.Button.left,
            'button.right': mouse.Button.right,
            'button.middle': mouse.Button.middle
        }
        
        # 创建独立的鼠标控制器
        mouse_controller = Controller()
        
        for event in self.recorded_events:
            if not self.is_replaying:  # 检查是否需要停止回放
                break
                
            time.sleep(event['time'] - last_time)
            last_time = event['time']
            
            if 'type' in event and event['type'] == 'move':
                mouse_controller.position = (event['x'], event['y'])
            else:
                mouse_controller.position = (event['x'], event['y'])
                button_str = event['button'].lower()
                
                button = None
                for key, value in button_map.items():
                    if key.lower() in button_str:
                        button = value
                        break
                
                if button is None:
                    print(f"未知按钮类型: {button_str}")
                    continue
                    
                try:
                    if event['pressed']:
                        mouse_controller.press(button)
                    else:
                        mouse_controller.release(button)
                except Exception as e:
                    print(f"按钮操作失败: {str(e)}")
                    continue

    def select_all(self):
        """全选所有录制"""
        for item in self.recording_tree.get_children():
            self.recording_tree.selection_add(item)
            
    def deselect_all(self):
        """取消全选"""
        self.recording_tree.selection_remove(self.recording_tree.selection()) 

class MouseMacro:
    def __init__(self, parent_frame):
        self.root = parent_frame
        self.recording = False
        self.is_running = False
        self.macro_events = []
        self.current_macro = None
        self.mouse_listener = None
        self.start_time = 0
        self.setup_gui()
        
    def setup_gui(self):
        # 左侧：宏列表和操作按钮
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        
        # 宏列表
        list_frame = ttk.LabelFrame(left_frame, text="宏列表", padding=10)
        list_frame.pack(fill=BOTH, expand=True)
        
        # 创建带滚动条的列表
        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side=RIGHT, fill=Y)
        
        columns = ("名称", "动作数", "循环次数")
        self.macro_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                     yscrollcommand=list_scroll.set)
        
        self.macro_tree.heading("名称", text="名称")
        self.macro_tree.heading("动作数", text="动作数")
        self.macro_tree.heading("循环次数", text="循环次数")
        
        self.macro_tree.column("名称", width=150)
        self.macro_tree.column("动作数", width=70)
        self.macro_tree.column("循环次数", width=70)
        
        self.macro_tree.pack(fill=BOTH, expand=True)
        list_scroll.config(command=self.macro_tree.yview)
        
        # 宏操作按钮
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=X, pady=5)
        
        ttk.Button(btn_frame, text="新建", command=self.create_macro).pack(side=LEFT, padx=2)
        ttk.Button(btn_frame, text="删除", command=self.delete_macro).pack(side=LEFT, padx=2)
        ttk.Button(btn_frame, text="重命名", command=self.rename_macro).pack(side=LEFT, padx=2)
        
        # 右侧：动作列表和设置
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        
        # 动作列表
        action_frame = ttk.LabelFrame(right_frame, text="动作列表", padding=10)
        action_frame.pack(fill=BOTH, expand=True)
        
        action_scroll = ttk.Scrollbar(action_frame)
        action_scroll.pack(side=RIGHT, fill=Y)
        
        columns = ("序号", "类型", "位置", "延迟(ms)")
        self.action_tree = ttk.Treeview(action_frame, columns=columns, show="headings",
                                      yscrollcommand=action_scroll.set)
        
        self.action_tree.heading("序号", text="序号")
        self.action_tree.heading("类型", text="类型")
        self.action_tree.heading("位置", text="位置")
        self.action_tree.heading("延迟(ms)", text="延迟(ms)")
        
        self.action_tree.column("序号", width=50)
        self.action_tree.column("类型", width=100)
        self.action_tree.column("位置", width=150)
        self.action_tree.column("延迟(ms)", width=80)
        
        self.action_tree.pack(fill=BOTH, expand=True)
        action_scroll.config(command=self.action_tree.yview)
        
        # 动作操作按钮
        action_btn_frame = ttk.Frame(right_frame)
        action_btn_frame.pack(fill=X, pady=5)
        
        ttk.Button(action_btn_frame, text="录制(F7)", command=self.toggle_recording).pack(side=LEFT, padx=2)
        ttk.Button(action_btn_frame, text="删除动作", command=self.delete_action).pack(side=LEFT, padx=2)
        ttk.Button(action_btn_frame, text="编辑延迟", command=self.edit_delay).pack(side=LEFT, padx=2)
        
        # 添加动作全选/取消全选按钮
        select_frame = ttk.Frame(right_frame)
        select_frame.pack(fill=X, pady=5)
        ttk.Button(select_frame, text="全选动作", command=self.select_all_actions).pack(side=LEFT, padx=2)
        ttk.Button(select_frame, text="取消全选", command=self.deselect_all_actions).pack(side=LEFT, padx=2)
        
        # 执行设置
        settings_frame = ttk.LabelFrame(right_frame, text="执行设置", padding=10)
        settings_frame.pack(fill=X)
        
        # 循环次数设置
        loop_frame = ttk.Frame(settings_frame)
        loop_frame.pack(fill=X, pady=5)
        
        ttk.Label(loop_frame, text="循环次数:").pack(side=LEFT)
        self.loop_count = StringVar(value="1")
        loop_entry = ttk.Entry(loop_frame, textvariable=self.loop_count, width=10)
        loop_entry.pack(side=LEFT, padx=5)
        ttk.Label(loop_frame, text="(0表示无限循环)").pack(side=LEFT)
        
        # 热键设置
        hotkey_frame = ttk.Frame(settings_frame)
        hotkey_frame.pack(fill=X, pady=5)
        
        ttk.Label(hotkey_frame, text="执行热键:").pack(side=LEFT)
        self.hotkey = StringVar(value="F6")
        hotkey_combo = ttk.Combobox(hotkey_frame, textvariable=self.hotkey, width=10)
        hotkey_combo['values'] = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
        hotkey_combo.pack(side=LEFT, padx=5)
        
        # 执行按钮
        ttk.Button(settings_frame, text="执行宏(F6)", command=self.toggle_macro).pack(pady=5)
        
        # 设置键盘监听
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
        # 加载现有宏
        self.load_macros()
        
        # 在创建宏列表树之后，添加选择事件绑定
        self.macro_tree.bind('<<TreeviewSelect>>', self.on_macro_select)

    def create_macro(self):
        """创建新宏"""
        dialog = Toplevel(self.root)
        dialog.title("新建宏")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="宏名称:").pack(pady=5)
        entry = ttk.Entry(dialog, width=40)
        entry.pack(pady=5)
        entry.focus()
        
        def do_create():
            name = entry.get()
            if not name:
                messagebox.showwarning("警告", "请输入宏名称")
                return
                
            # 创建新宏
            macro_data = {
                'name': name,
                'actions': [],
                'loop_count': 1
            }
            
            # 确保macros文件夹存在
            os.makedirs("macros", exist_ok=True)
            
            # 保存宏
            filename = f"macros/{name}.json"
            if os.path.exists(filename):
                if not messagebox.askyesno("确认", f"宏 {name} 已存在，是否覆盖？"):
                    return
                    
            with open(filename, 'w') as f:
                json.dump(macro_data, f)
                
            self.load_macros()  # 刷新列表
            self.select_macro(name)  # 选中新建的宏
            dialog.destroy()
            
        ttk.Button(dialog, text="确定", command=do_create).pack(pady=5)
        dialog.bind('<Return>', lambda e: do_create())

    def select_macro(self, name):
        """选中指定名称的宏"""
        for item in self.macro_tree.get_children():
            if self.macro_tree.item(item)['values'][0] == name:
                self.macro_tree.selection_set(item)
                self.load_macro_actions(name)
                break

    def load_macros(self):
        """加载所有宏"""
        # 清空列表
        for item in self.macro_tree.get_children():
            self.macro_tree.delete(item)
            
        if not os.path.exists("macros"):
            return
            
        for file in os.listdir("macros"):
            if file.endswith(".json"):
                try:
                    with open(f"macros/{file}", 'r') as f:
                        macro_data = json.load(f)
                        name = macro_data['name']
                        actions = macro_data['actions']
                        loop_count = macro_data.get('loop_count', 1)
                        
                        self.macro_tree.insert("", END, values=(
                            name,
                            len(actions),
                            loop_count
                        ))
                except:
                    continue

    def load_macro_actions(self, macro_name):
        """加载指定宏的动作列表"""
        # 清空动作列表
        for item in self.action_tree.get_children():
            self.action_tree.delete(item)
            
        try:
            with open(f"macros/{macro_name}.json", 'r') as f:
                macro_data = json.load(f)
                self.current_macro = macro_name
                self.loop_count.set(str(macro_data.get('loop_count', 1)))
                
                # 显示动作列表
                for i, action in enumerate(macro_data['actions'], 1):
                    self.action_tree.insert("", END, values=(
                        i,
                        action['type'],
                        f"({action['x']}, {action['y']})",
                        action['delay']
                    ))
        except:
            self.current_macro = None

    def toggle_recording(self):
        """开始/停止录制宏动作"""
        if not self.current_macro:
            messagebox.showinfo("提示", "请先选择或创建一个宏")
            return
            
        if not hasattr(self, 'recording'):
            self.recording = False
            
        if not self.recording:
            self.start_recording()
            # 修改按钮文本以显示当前状态
            for widget in self.action_btn_frame.winfo_children():
                if widget['text'] == "录制(F7)":
                    widget.config(text="停止录制(F7)")
                    break
        else:
            self.stop_recording()
            # 恢复按钮文本
            for widget in self.action_btn_frame.winfo_children():
                if widget['text'] == "停止录制(F7)":
                    widget.config(text="录制(F7)")
                    break

    def start_recording(self):
        """开始录制宏动作"""
        self.recording = True
        self.macro_events = []
        self.start_time = time.time()
        self.last_event_time = self.start_time  # 添加这行，记录最后一个事件的时间
        
        # 修改鼠标监听器，添加移动轨迹的记录
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click,
            on_move=self.on_move
        )
        self.mouse_listener.start()

    def on_click(self, x, y, button, pressed):
        """记录鼠标点击事件"""
        if not self.recording:
            return
            
        current_time = time.time() - self.start_time
        event = {
            'type': 'click',
            'x': x,
            'y': y,
            'button': str(button),
            'pressed': pressed,
            'delay': int(current_time * 1000) if not self.macro_events else int((current_time - self.last_event_time) * 1000)
        }
        self.last_event_time = current_time  # 记录这个动作的时间
        self.macro_events.append(event)

    def on_move(self, x, y):
        """记录鼠标移动事件"""
        if not self.recording:
            return
            
        current_time = time.time() - self.start_time
        event = {
            'type': 'move',
            'x': x,
            'y': y,
            'delay': int(current_time * 1000) if not self.macro_events else int((current_time - self.last_event_time) * 1000)
        }
        self.last_event_time = current_time  # 记录这个动作的时间
        self.macro_events.append(event)

    def stop_recording(self):
        """停止录制并保存动作"""
        if not self.recording:
            return
            
        self.recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
            
        # 读取现有宏数据
        with open(f"macros/{self.current_macro}.json", 'r') as f:
            macro_data = json.load(f)
            
        # 添加新录制的动作
        macro_data['actions'].extend(self.macro_events)
        
        # 保存更新后的宏
        with open(f"macros/{self.current_macro}.json", 'w') as f:
            json.dump(macro_data, f)
            
        # 刷新显示
        self.load_macro_actions(self.current_macro)

    def delete_macro(self):
        """删除选中的宏"""
        selected = self.macro_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要删除的宏")
            return
            
        macro_name = self.macro_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("确认", f"确定要删除宏 {macro_name} 吗？"):
            try:
                os.remove(f"macros/{macro_name}.json")
                self.load_macros()
                if self.current_macro == macro_name:
                    self.current_macro = None
                    # 清空动作列表
                    for item in self.action_tree.get_children():
                        self.action_tree.delete(item)
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def rename_macro(self):
        """重命名选中的宏"""
        selected = self.macro_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要重命名的宏")
            return
            
        old_name = self.macro_tree.item(selected[0])['values'][0]
        
        dialog = Toplevel(self.root)
        dialog.title("重命名宏")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="新名称:").pack(pady=5)
        entry = ttk.Entry(dialog, width=40)
        entry.pack(pady=5)
        entry.insert(0, old_name)
        entry.select_range(0, END)
        entry.focus()
        
        def do_rename():
            new_name = entry.get()
            if new_name and new_name != old_name:
                try:
                    # 读取原宏数据
                    with open(f"macros/{old_name}.json", 'r') as f:
                        macro_data = json.load(f)
                    
                    # 更新宏名称
                    macro_data['name'] = new_name
                    
                    # 保存为新文件
                    with open(f"macros/{new_name}.json", 'w') as f:
                        json.dump(macro_data, f)
                    
                    # 删除旧文件
                    os.remove(f"macros/{old_name}.json")
                    
                    # 更新界面
                    self.load_macros()
                    if self.current_macro == old_name:
                        self.current_macro = new_name
                        self.load_macro_actions(new_name)
                except Exception as e:
                    messagebox.showerror("错误", f"重命名失败: {str(e)}")
            dialog.destroy()
            
        ttk.Button(dialog, text="确定", command=do_rename).pack(pady=5)
        dialog.bind('<Return>', lambda e: do_rename())

    def delete_action(self):
        """删除选中的动作"""
        if not self.current_macro:
            return
            
        selected = self.action_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要删除的动作")
            return
            
        if not messagebox.askyesno("确认", "确定要删除选中的动作吗？"):
            return
            
        # 读取宏数据
        with open(f"macros/{self.current_macro}.json", 'r') as f:
            macro_data = json.load(f)
            
        # 获取选中的索引并删除对应动作
        indices = [self.action_tree.index(item) for item in selected]
        indices.sort(reverse=True)  # 从后往前删除
        
        for index in indices:
            del macro_data['actions'][index]
            
        # 保存更新后的宏
        with open(f"macros/{self.current_macro}.json", 'w') as f:
            json.dump(macro_data, f)
            
        # 刷新显示
        self.load_macro_actions(self.current_macro)

    def edit_delay(self):
        """编辑选中动作的延迟时间"""
        if not self.current_macro:
            return
            
        selected = self.action_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要编辑的动作")
            return
            
        # 只编辑第一个选中的动作
        item = selected[0]
        index = self.action_tree.index(item)
        current_delay = self.action_tree.item(item)['values'][3]
        
        dialog = Toplevel(self.root)
        dialog.title("编辑延迟")
        dialog.geometry("250x100")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="延迟时间(毫秒):").pack(pady=5)
        entry = ttk.Entry(dialog, width=20)
        entry.pack(pady=5)
        entry.insert(0, str(current_delay))
        entry.select_range(0, END)
        entry.focus()
        
        def do_edit():
            try:
                new_delay = int(entry.get())
                if new_delay < 0:
                    raise ValueError("延迟时间不能为负数")
                    
                # 更新宏数据
                with open(f"macros/{self.current_macro}.json", 'r') as f:
                    macro_data = json.load(f)
                    
                macro_data['actions'][index]['delay'] = new_delay
                
                with open(f"macros/{self.current_macro}.json", 'w') as f:
                    json.dump(macro_data, f)
                    
                # 刷新显示
                self.load_macro_actions(self.current_macro)
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("错误", "请输入有效的延迟时间")
                
        ttk.Button(dialog, text="确定", command=do_edit).pack(pady=5)
        dialog.bind('<Return>', lambda e: do_edit())

    def toggle_macro(self):
        """开始/停止执行宏"""
        if not hasattr(self, 'is_running'):
            self.is_running = False
            
        if not self.is_running:
            self.start_macro()
        else:
            self.stop_macro()
            
    def start_macro(self):
        """开始执行宏"""
        selected = self.macro_tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请选择要执行的宏")
            return
            
        macro_name = self.macro_tree.item(selected[0])['values'][0]
        
        try:
            with open(f"macros/{macro_name}.json", 'r') as f:
                macro_data = json.load(f)
                
            if not macro_data['actions']:
                messagebox.showinfo("提示", "该宏没有任何动作")
                return
                
            self.is_running = True
            
            # 创建执行线程
            self.macro_thread = threading.Thread(target=self.run_macro, args=(macro_data,))
            self.macro_thread.daemon = True
            self.macro_thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"执行宏失败: {str(e)}")
            
    def stop_macro(self):
        """停止执行宏"""
        self.is_running = False
        
    def run_macro(self, macro_data):
        """执行宏的具体逻辑"""
        mouse_controller = Controller()
        button_map = {
            'button.left': mouse.Button.left,
            'button.right': mouse.Button.right,
            'button.middle': mouse.Button.middle
        }
        
        try:
            loop_count = int(self.loop_count.get())
        except ValueError:
            loop_count = 1
            
        current_loop = 0
        
        while self.is_running and (loop_count == 0 or current_loop < loop_count):
            for action in macro_data['actions']:
                if not self.is_running:
                    break
                    
                # 移动鼠标到指定位置
                if action['type'] == 'move':
                    mouse_controller.position = (action['x'], action['y'])
                elif action['type'] == 'click':
                    mouse_controller.position = (action['x'], action['y'])
                    button_str = action['button'].lower()
                    button = None
                    for key, value in button_map.items():
                        if key.lower() in button_str:
                            button = value
                            break
                            
                    if button:
                        if action['pressed']:
                            mouse_controller.press(button)
                        else:
                            mouse_controller.release(button)
                            
                # 等待指定的延迟时间
                time.sleep(action['delay'] / 1000.0)  # 转换为秒
                
            current_loop += 1
            
    def on_key_press(self, key):
        """处理键盘事件"""
        try:
            # 获取按键名称
            key_str = key.char.upper() if hasattr(key, 'char') else key.name.upper()
            
            # 检查是否是执行热键
            if key_str == self.hotkey.get():
                self.toggle_macro()
            # 添加录制热键
            elif key_str == 'F7':
                self.toggle_recording()
                
        except AttributeError:
            pass

    def on_macro_select(self, event):
        """当选择宏时自动加载其动作列表"""
        selected = self.macro_tree.selection()
        if selected:
            macro_name = self.macro_tree.item(selected[0])['values'][0]
            self.load_macro_actions(macro_name)

    def select_all_actions(self):
        """全选所有动作"""
        for item in self.action_tree.get_children():
            self.action_tree.selection_add(item)
            
    def deselect_all_actions(self):
        """取消全选动作"""
        self.action_tree.selection_remove(self.action_tree.selection()) 