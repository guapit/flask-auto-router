# Flask Auto Routers(自动注册路由)

<p align="center">
<a href="#"><img src="https://img.shields.io/badge/Module-flask_auto_router-critical.svg"/></a>
<a href="#"><img src="https://img.shields.io/badge/Language-Python-blue"/></a>
    <a href="#"><img src="https://img.shields.io/badge/Version-0.1.2-f1c232"/></a>
<img src="https://img.shields.io/badge/Author-guapit-ff69b4"/>
<a href="https://www.github.com/guapit"><img src="https://img.shields.io/badge/Github-guapit-success"/></a>
<a href="https://www.gitee.com/guapit"><img src="https://img.shields.io/badge/Gitee-guapit-yellowgreen"/></a>
<a href="#"><img src="https://img.shields.io/badge/E--mail-guapit%40qq.com-yellowgreen"/></a>
</p><br>

 This is an auto-register routing plugin based on the 'Flask' framework, developed according to the 'flask_restful' specification, you only need to configure the view file, you can automatically register the routing system, if you encounter Debug or problems, please contact me through the above contact information



这是一个基于 `Flask`框架的自动注册路由插件,根据`flask_restful `规范开发的,你只需要配置视图文件,就可以自动注册路由系统,如果你在使用中遇到Debug或者问题,请通过上面的联系方式联系我

Required plugins 必要的插件

```pthon
pip install -U flask
pip install -U flask-restful
```

## pip安装

```bash
pip install flask-auto-routers
```



## settings(配置)

`BASE_DIR`: Sets the root path for the search

设置搜索的根路径

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
```



`AUTO_ROUTER_DIR`: A file filter that allows AutoRouter to search only a specified range of directories

文件过滤器,可以使AutoRouter 只搜索指定范围的目录

```python
AUTO_ROUTER_DIR = ['view', 'view2'] 
```

Simple configuration is all that's needed, and you never have to configure a cumbersome routing system again

只需要简单的配置,从此再也不用配置繁琐的路由系统 ^.^

```python
from flask import Flask
from flask_auto_router import AutoRouter


# 1.flask restful view object Auto register router plugins
# 1.flask restful 自动注册视图类路由插件
auto_router = AutoRouter()

# 2. File filter, which allows searching only a specified range of file directories
#  Add this configuration to app.config
# 2.文件过滤器,只允许搜索指定范围的文件目录
#  将此配置加入到 app.config中即可
# Configuration is only allowed to specify the directory view class
# 只允许配置指定目录视图类
#   AUTO_ROUTER_DIR = ['view', 'view2'] 

# 3. 配置需要自动路由的.py文件(注意带有相对路径)
auto_router.add_routers("home","/","view.home")
auto_router.add_routers("user","/user","view.user")

app = Flask(__name__)
auto_router.init_app(app)

if __name__ in "__main__":
    app.run()
```

## View Object(视图类)

`__url__`: Custom Router 自定义子路由

`__endpoint__`: Jinja2 template reflection names Jinja2 模板反射名称

**view.home**

```python
from flask_restful import Resource

class Home(Resource):
    __url__ = '/'
    __endpoint__ = 'home'

    def get(self, **kwargs):
        return "Hello World!"
```

访问地址: http://localhost:5000

**view.user**

```python
from flask_restful import Resource

class User(Resource):
    __url__ = '/'
    __endpoint__ = 'user'

    def get(self, **kwargs):
        return "Hello User!"
    
# If the route method is not stated, the class name will be used as the route  
# 如果没有申明路由方式,将会以类名作为路由
class Login(Resource):

    def get(self, **kwargs):
        return "Login in!"
```

访问地址:

user:  http://localhost:5000/user

user:  http://localhost:5000/login