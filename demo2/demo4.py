import os
import sys
import importlib
# # 获取当前文件所在目录的父目录
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
# 将父目录添加到sys路径中
sys.path.append(parent_dir)
# 遍历plugins文件夹
plugin_folder = os.path.join(parent_dir, 'plugins')
sys.path.append(plugin_folder)


# 插件示例
class Plugin:
    def __init__(self, name):
        self.name = name
        
    def run(self):
        print(f"Running plugin {self.name}")


class Platform:
    def __init__(self):
        self.loadPlugins()
        
    def sayHello(self,from_):
        print('hello from', from_)
        
    def loadPlugins(self):
        for filename in os.listdir("plugins"):
            if not filename.endswith(".py")or filename.startswith("_"):
                continue
            self.runPlugin(filename)
            
    def runPlugin(self, pluginname):
        try:
            pluginName=os.path.splitext(pluginname)[0]
            print(pluginName)
            plugin = importlib.import_module(pluginName, package=None)
            #Errors may be occured.Handle it yourself.
            plugin.run()
            a = plugin.Plugin("112312")
        except Exception as e:
            print(e)
            print("Error loading plugin %s" % pluginname)
            return False
        
        
if __name__=="__main__":
    platform=Platform()