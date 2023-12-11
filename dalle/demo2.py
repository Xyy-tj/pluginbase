import importlib
import os
import sys


class Car:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def drive(self):
        print('Driving', self.name, self.color, 'car')


if __name__ == '__main__':
    
    # 获取当前文件所在目录的父目录
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)

    # 将父目录添加到sys路径中
    sys.path.append(parent_dir)
    # 遍历plugins文件夹
    plugin_folder = os.path.join(parent_dir, 'plugins')
    sys.path.append(plugin_folder)
    for root, dirs, files in os.walk(plugin_folder):
        for file in files:
            if file.endswith('.py'):
                module_name = file[:-3]  # 去掉文件后缀名
                try:
                    module = importlib.import_module(module_name, package=None)
                    print(f"Successed to import {module_name}")
                except ImportError as e:
                    print(f"Failed to import {module_name}: {e}")
    # module = importlib.import_module(module_name, package=None)
    
    car = Car('BMW', 'red')