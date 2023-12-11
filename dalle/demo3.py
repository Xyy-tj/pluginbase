# 插件示例
class Plugin:
    def __init__(self, name):
        self.name = name
        
    def run(self):
        print(f"Running plugin {self.name}")
        
# 插件管理器示例
class PluginManager:
    def __init__(self):
        self.plugins = []
        
    def load_plugins(self, *plugins):
        for plugin in plugins:
            self.plugins.append(plugin)
        
    def unload_plugins(self, *plugins):
        for plugin in plugins:
            self.plugins.remove(plugin)
        
    def run_plugins(self):
        for plugin in self.plugins:
            plugin.run()
            
pm = PluginManager()
plugin1 = Plugin('plugin1')
plugin2 = Plugin('plugin2')
pm.load_plugins(plugin1, plugin2)
pm.run_plugins()