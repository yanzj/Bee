# 本项目的使用办法

## 需要的运行环境
**python3.x** 和 **pycharm**

（建议使用**专业版**，如果使用社区版的话，很多配置就需要自己设置了，本方法只说明在专业版下的使用），
不过，目前本项目是在window平台开发的，当然也能够直接放到mac或linux上运行，但如果是mac或Linux上运行的话，
目前只能用Django自带的数据库`sqlite3`，如果是windows下则可以使用您的`mysql`

## 项目的一些特殊文件夹和文件介绍
1.venv
: 这个是本项目的虚拟环境，所有的依赖库都在里面，项目运行前会提示安装

2.spider
: 这是本项目的爬虫程序，简易的搜索引擎


3.templates/users-window
: 这是用户交互界面的HTML文件存放地点


4.templates/manage-window
: 这是管理员交互界面的HTML文件存放地点


5.db.sqlite3
: 这是Django自带的数据库，本项目目前也可以直接采用这个数据库进行测试

## 开始使用

### 1.克隆项目
在自己电脑找一个合适的位置开始git clone
```
git clone https://github.com/AmanKingdom/Bee.git
```

### 2.识别项目
用pycharm直接打开这个项目，专业版的pycharm会直接识别这是一个Django项目，或许它会询问您使用哪个python解释器，
选择python3.x后，如果不出意外，将会出现安装依赖库的提示，选择安装即可，它会自动识别venv这个虚拟环境自动装好给您

### 3.您想用自带的数据库吗
如果您电脑还没安装MySQL，没关系，您可以直接用项目自带的数据库，请您在`bee/settings.py`中，找到`DATABASES`这项，
注释掉下方的mysql连接代码，取消上方sqlite3连接代码的注释即可启用

### 4.也可以用MySQL
用如果您电脑已安装mysql，那么您需要在您的数据库创建一个名为`bee_database`的数据库，不需要手动一个一个地创建表，
只需进入pycharm底部栏目上的`Terminal`，cd到`Bee`目录，输入下方语句启用虚拟环境：
```
venv\Scripts\activate
```

即可进入虚拟环境，这时候，终端上显示的路径多了个`(venv)`

### 5.给MySQL的bee_database数据库创建表
在上述虚拟环境中、`Bee`路径下，输入：
```
python manage.py makemigrations
# 稍等片刻，完成初始化
python manage.py migrate
# 稍等片刻，完成创建
```
这时候，您会发现mysql数据库中已经创建了好多表，当然，这些操作都需要您在`Bee\bee\setings.py`中的`DATABASES`选项填写正确的密码。

### 6.启动服务器
点击pycharm的`run`，选择`bee`即可启动服务器，在浏览器输入`localhost:8000`即可查看本站

### 7.搜索引擎
上述的操作都是对Django项目环境进行搭建而已，虽然能运行起来，但搜索引擎却什么都都不出来，这是因为`spider`这个文件夹中的搜索引擎还没开始工作，
您需要找到spider2.0.py，把其中有关数据库的SQL语句的一些参数设置为对应自己本地mysql的，并且点击运行spider2.0.py，等待其爬取了文章后，
再次前往`localhost:8000`，这时候您会发现主页上的推荐栏目多了一些文章

## 功能及项目进展介绍
1.搜索：本项目的搜索引擎目前只能对爬取到数据库的文章的标题进行关键字检索


2.登录与注册：目前还是个幌子，虽然能够注册和登录，但安全性和用户信息的完整性还没开始动手


3.写博客：博客文章需要登录后才可编辑，使用kindeditor富文本编辑器，可上传图片、视频



谢谢阅读~

2018.11.06



