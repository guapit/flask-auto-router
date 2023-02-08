from flask import Flask,Blueprint
from flask_restful import Resource, Api
# from pprint import pprint
import inspect, importlib
import sys, os, re
from pathlib import Path

api = Api()


# Flask自动注册路由插件
class AutoRouter:
    def __init__(self, app: Flask = None):
        self.app = app
        self.__base_dir = None
        self.__router_file = None
        self.__module_list = []
        self.__modules = []
        self.root_url = Blueprint('root', __name__, url_prefix="/")
        self.__root_urls = []
        self.__count = 0
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        # 继承 Flask config的配置
        new_dir = Path(__file__).resolve().parent.parent
        app.config.setdefault('BASE_DIR', new_dir)
        app.config.setdefault('AUTO_ROUTER_DIR', None)
        # 获取配置
        self.__base_dir = app.config.get('BASE_DIR')
        self.__router_file = app.config.get('AUTO_ROUTER_DIR')

        self.get_modules()
        self.get_filter_modules()
        if self.__count == 0:
            if self.__root_urls:
                for root_url in self.__root_urls:
                    self.mount_router(root_url['route'],root_url['path'])
                    app.register_blueprint(root_url['route'])
            self.__count = 1
        
    # modules -> filter_modules -> 注册路由
    # 获取当前项目下所有模块
    def get_modules(self):
        # 获取当前路径所有文件包
        _modules = []
        for root, dirs, files in os.walk("."):
            for file in files:
                # 拼接文件路径
                file_name = os.path.join(root, file)
                re_name = re.search(r'.*?(.py)$', file_name)
                if re_name:
                    re_name = re_name.group(0).replace("\\", ".").replace("..", "").replace(".py", "")
                    # 导入相对路径的包
                    modules = importlib.import_module(re_name, package='')
                    _modules.append(modules)
                    
        return _modules

    # 获取需要注册路由的视图类
    def get_filter_modules(self):
        module_list = []
        _modules = self.get_modules()
        base_path = str(self.__base_dir).replace("\\", ".")
        if _modules:
            # 查询所有的模块
            for _module in _modules:
                module_name_path = str(_module).replace("\\\\", ".")
                pattern = re.compile(r'<module \'(.*?)\'')
                module_name = pattern.search(module_name_path)

                # 得到当前目录所有的模块文件名
                if module_name:
                    # 得到当前目录所有模块的文件
                    module_file = module_name.group(1)
                    # 过滤文件目录
                    if not self.filter_file(self.__router_file,module_file):
                        continue

                    inspect_list = inspect.getmembers(sys.modules[module_file])

                    for name, _class in inspect_list:
                        # 找寻所有自建的类
                        
                        pattern2 = re.compile(r'__')
                        if isinstance(_class, object) and not pattern2.search(name):
                            
                            obj_module_name = str(_class).replace("\\\\", ".")

                            obj_pattern = pattern.search(obj_module_name)
                            # 查询所有类带有元类属性 methods的类
                            if hasattr(_class, 'methods') and _class.__name__ != 'Resource':
                                # 根目录创建的视图对象
                                # 
                                if not _module in module_list:
                                    module_list.append(_class)
                                    # print(_module)
            # pprint("-----------过滤模块后----------")
                                
        return module_list

    # 自定义路由蓝图
    def add_routers(self,name:str,url_prefix:str,path_name:str):
        if name and url_prefix and path_name:
            router = {
                "route": Blueprint(name, __name__, url_prefix=url_prefix),
                "path": path_name
            }
            self.__root_urls.append(router)
                

    # 挂载路由
    def mount_router(self,router:Blueprint, file_name:str):
        # pattern = re.compile(r'__')
        pattern = re.compile(r'<class \'(.*?)\'>')
        _filter = self.get_filter_modules()
        _filter_list = []
        # 从模块的名称中过滤出指定范围的视图类
        for fil in _filter:
            is_fil_name = pattern.search(str(fil))
            if pattern.search(str(fil)):
                fil_name = is_fil_name.group(1)
                # 如果 file_name的路径名称包括在目录中
                if self.filter_file(file_name, fil_name):
                    
                    _name = fil.__name__
                    
                    if hasattr(fil, 'methods'):
                            r = {
                                'url': fil.__dict__.get('__url__'.lower(),
                                                                "/" + _name.lower()),
                                'func': fil,
                                'endpoint': fil.__dict__.get('__endpoint__'.lower(),
                                                                    _name.lower())
                            }
                            print(r)
                            
                            router.import_name = file_name
                            api.app = router
                            api.add_resource(r['func'], r['url'], endpoint=r['endpoint'])

                        

     
    # # 注册所有的蓝图
    # def get_blueprint(self):
    #     pattern = re.compile(r'__')
    #     module_list = self.get_filter_modules()

    #     if module_list:
    #         module_list = list(set(module_list))
    #         # pprint(module_list)
    #         for mokuai in module_list:
    #             mokuai_objs = inspect.getmembers(sys.modules[mokuai])

    #             for sub_name, sub_class in mokuai_objs:
    #                 # 文件内自己创建的视图对象
    #                 if not pattern.search(sub_name):
    #                     if isinstance(sub_class, Blueprint):
    #                         # 注册蓝图
    #                         # pprint(sub_name)
    #                         self.app.register_blueprint(sub_class)

    # 过滤文件
    def filter_file(self,filte_path:str|list, file_name):
        if filte_path is None:
            return True
        # 如果有过滤器,只查询过滤器内的对象
        if filte_path:
            if isinstance(filte_path, str):
                filte_path = filte_path.replace("/", '.')
                if filte_path == file_name[0:len(filte_path)]:
                    return True

            elif isinstance(filte_path, list):
                for str_name in filte_path:
                    str_name = str(str_name).replace("/", ".")
                    if str_name == file_name[0:len(str_name)]:
                        # pprint("%s, %s" % (str_name, file_name[0:len(str_name)]))
                        return True
            else:  # 如果有过滤器,并且不在范围内不进行扫描
                return False
        return False
