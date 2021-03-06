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




# 2018.11.26 大改动

## 更新的地方：
1、完成了和搜索引擎端的爬虫模块的对接，使得文章的显示更丰富了。但还未进行更多功能的引进（比如计划中的：根据检索条件筛选文章）。

2、整个web页面风格全变，前端框架不再使用之前的模板，目前只是简单的套用bootstrap的部分基本用法，但加载速度和显示效果较之前稳定了好多。

3、其次，添加了轮播图功能，但目前轮播图是在数据库管理端手动输入参数，还不能实现点选输入参数的快捷，待改进。

## 轮播图的添加方法：

1、在开启服务器后，在地址栏输入：
```angular2html
localhost:8000/admin
```
2、弹出管理员账号登录界面，输入管理账号

（如何创建管理员账号？只需要在终端输入：
```
python manage.py crearesuperuser
```
然后根据提示输入账号和密码即可）

3、点击carousel项，可以看到可以输入`img_url`之类的信息，然后再另外打开一个管理界面，
点击wechat_article项，打开某一篇你想要放到轮播图上的文章，复制其中的内容到`carousel`的对应
栏中即可，最后保存，刷新主页即可看到轮播图了。


# 2018.11.29前端后台可视化调用爬虫模块
新增的数据管理平台在BEE主页最底部，目前只有爬虫栏的爬取公众号功能开放。

### 爬虫程序被修改部分：

1、由于Django运行后，项目里所有程序访问其他文件的路径都是从Django根目录出发，
所以原来爬虫程序的日志文件路径变化如下：
```python
    # 爬取文章日志部分
    # f = open('../LogFile/article_log.log', 'a+')
    f = open('engine/LogFile/article_log.log', 'a+')
```
```python
    # 爬取公众号日志部分
    # f = open('../LogFile/account_log.log', 'a+')
    f = open('engine/LogFile/account_log.log', 'a+')
```

2、理由同上，原来爬虫程序的访问数据库路径变化如下(目前只修改了爬取公众号函数内的部分)：
```python
    # 连接数据库
    # self.db = sqlite3.connect('../../bee-database.db')
    self.db = sqlite3.connect('bee-database.db')
```

3、理由同上，原来爬虫程序爬取公众号头像和二维码的保存路径修改为：
```python
    # path_head_portrait = '../../static/head_portraits/'
    path_head_portrait = 'static/head_portraits/'
    # path_qr_code = '../../static/qr_codes/'
    path_qr_code = 'static/qr_codes/'
```

4、由于公众号信息保存的头像信息应该为完整路径，加上为了前端显示的方便、统一，
现将头像入库信息由原来的头像文件名称修改为完整路径：
```python
    self.cursor.execute(sql, (wechat_id, wechat_name, '/'+path_head_portrait+head_portrait_name, '/'+path_qr_code+qr_code_name))
```

5、为了在前端能够接受到爬虫程序爬取成功后的信息，现对原程序添加了信息返回：
```python
    Log.account_log(u'入库成功')
    wechat_accounts_list.append({'wechat_id': wechat_id, 'wechat_name': wechat_name})
    
    Log.account_log('爬虫已完成任务 ')
    return wechat_accounts_list
```

### 爬取公众号的功能介绍：
1、多个公众号用逗号隔开输入即可；

2、目前仅支持微信号搜索；

3、删除公众号会连着头像、二维码文件也删除。
