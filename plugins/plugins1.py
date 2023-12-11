# 插件示例
class Plugin:
    def __init__(self, name):
        self.name = name
        
    def run(self):
        print(f"Running plugin {self.name}")
           
        
def run():
    print(f"Running plugin 1")