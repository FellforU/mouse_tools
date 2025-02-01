import os
import subprocess

def run_git_config():
    commands = [
        'git config --global core.quotepath false',
        'git config --global gui.encoding utf-8',
        'git config --global i18n.commit.encoding utf-8',
        'git config --global i18n.logoutputencoding utf-8'
    ]
    
    for cmd in commands:
        subprocess.run(cmd, shell=True)
        
    # 设置环境变量
    os.environ['LANG'] = 'zh_CN.UTF-8'
    
    print("Git 中文配置已完成!")

if __name__ == '__main__':
    run_git_config() 