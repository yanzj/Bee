# coding: utf-8
import random
import re
import os
import string
import time
import sqlite3
import pymysql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pyquery import PyQuery as pq

class Spider:
    def __init__(self, wechat_ids):
        '''
        构造函数，根据公众号微信号获取对应文章的发布时间、文章标题, 文章链接等信息
        :param
        '''
        self.wechat_ids = wechat_ids

        # 请求头
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

        # 超时时长
        self.timeout = 5

        # 爬虫模拟在一个request.session中完成
        self.session = requests.Session()

        # 连接数据库
        self.db = sqlite3.connect('../../bee-database.db')
        self.cursor = self.db.cursor()


    def log(self,msg):
        '''
        日志函数
        :param msg: 日志信息
        :return:
        '''
        print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))

    def get_infos(self):

        for wechat_id in self.wechat_ids:

            print('\n')
            self.log(u'公众号为：%s' % wechat_id)

            # 搜索url
            search_url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=' + wechat_id
            search_html = self.session.get(search_url,headers=self.headers, timeout=self.timeout).content

            #获取公众号URL
            doc = pq(search_html)
            wechat_url = doc('div[class=txt-box]')('p[class=tit]')('a').attr('href')
            self.log(u'公众号url：%s' % wechat_url)

            # 获取html
            browser = webdriver.Chrome()
            browser.get(wechat_url)
            time.sleep(2)
            wechat_html = browser.execute_script("return document.documentElement.outerHTML")
            browser.close()

            # 检测是否被限制访问
            if pq(wechat_html)('#verify_change').text() != '':
                self.log(u'已限制访问，请稍后再试')

            else:
                # 获取发布时间，标题，首图，URL
                doc = pq(wechat_html)
                articles_list = doc('div[class="weui_media_box appmsg"]')
                articlesLength = len(articles_list)
                self.log(u'抓到文章%s篇' % articlesLength)

                items = []
                for item in articles_list.items():
                    items.append(item)
                items.reverse()

                if articles_list:
                    index = 1

                    for article in items:

                        self.log('')
                        self.log('正在爬取(%s/%s)' % (index, articlesLength))
                        index += 1

                        # 获取标题
                        title = article('h4[class="weui_media_title"]').text().strip()
                        self.log(u'标题： %s' % title)

                        # 获取文章发表时间
                        temp_date = article('p[class="weui_media_extra_info"]').text().strip()
                        if temp_date.endswith("原创"):
                            pdate = temp_date.replace('原创','')
                        else:
                            pdate = temp_date
                        self.log(u'发表时间： %s' % pdate)

                        # 获取标题对应的地址
                        temp_url = article('h4[class="weui_media_title"]').attr('hrefs')
                        # 存在某些推文的临时链接为完整链接，判断是否需要拼接
                        if temp_url.startswith('http://mp.weixin.qq.com'):
                            article_url = temp_url
                        else:
                            article_url = 'http://mp.weixin.qq.com' + temp_url
                        self.log(u'地址： %s' % article_url)

                        # 在获取到标题和发布日期的时候先进行查询数据库是否存在此条记录
                        sql1 = "SELECT article_title, publish_date FROM wechat_article WHERE article_title='" + title + "'"+"AND publish_date='"+pdate+"'"
                        self.cursor.execute(sql1)
                        exits = self.cursor.fetchall()  # 查找所有符合条件的数据
                        if len(exits) >= 1:
                            Spider.log("%s", '数据已存在，忽略此次爬取.')
                            continue

                        # 获取封面图片
                        cover = article('.weui_media_hd').attr('style')

                        pic = re.compile(r'background-image:url(.+)')
                        rs = pic.findall(cover)
                        if len(rs) > 0:
                            pic = rs[0].replace('(', '')
                            pic = pic.replace(')', '')
                            #self.log(u'封面图片：%s ' % pic)

                        # 获取正文内容
                        if title == "分享图片":     # 判断文章是否是为分享图片的类型
                            content = "null"
                        else:
                            content = self.get_atticle_info(article_url)

                        # 获取文章图片
                        imgs = self.get_article_img(article_url)

                        # 获取html代码
                        temp_html = requests.get(article_url)
                        temp_html.encoding = 'utf-8'
                        data = temp_html.text
                        delete = '''<div id="js_pc_qr_code" class="qr_code_pc_outer" style="display:none;">
            <div class="qr_code_pc_inner">
                <div class="qr_code_pc">
                    <img id="js_pc_qr_code_img" class="qr_code_pc_img">
                    <p>微信扫一扫<br>关注该公众号</p>
                </div>
            </div>
        </div>'''

                        html = re.sub(pattern='<head>', repl='<head><meta name="referrer" content="never">', string=data)
                        html = re.sub(pattern=delete, repl=' ', string=html)

                        path_name = '../../static/wechat_imgs/'         # 存储图片的路径

                        for img_name in imgs:                 # 依次将data-src替换为本地路径
                            if img_name == 'video':
                                html = re.sub(pattern='data-src', repl='src', string=html, count=1)
                            else:
                                img = path_name+img_name
                                html = re.sub(pattern='data-src=".*?"', repl='src="%s"' %img, string=html, count=1)


                        # html写入项目当前目录的HTML文件夹，文件名为标题前10个字，需要使用可删除注释
                        # f = open('HTML/'+title[:10]+'.html', 'a+')
                        # f.write(html)
                        # f.close()

                        # 保存数据到数据库
                        sql = 'INSERT INTO wechat_article(publish_date,article_title,wechat_id,article_url,cover_img,article_content,article_img,article_html) values(?, ?, ?, ?, ?, ?, ?, ?)'
                        # 推文为分享其他文章则不入库
                        if content != 'null':
                            try:
                                self.cursor.execute(sql,(pdate, title, wechat_id, article_url, pic, content, imgs[0], html))
                                self.db.commit()
                                self.log(u'入库成功')
                            except:
                                self.db.rollback()
                                self.log(u'入库不成功')

        self.db.close()
        Spider.log("%s",'\n爬虫已完成任务 ')

    def get_atticle_info(self,url):
        '''
        获取文章详细内容
        :param url:
        :return:
        '''
        html = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(html.text,"lxml")
        content = soup.find('div', id='img-content')

        temp_contents = re.findall('此(.*?)无法查看', html.text, re.S)

        if len(temp_contents) > 0:
            if '内容因违规' in temp_contents[0]:
                return 'null'

        p_list = []

        try:
            ps = content.find_all('p')
            for i in ps:
                x = i.get_text()
                p_list.append(x)

            main_content = '\n'.join(p_list)
        except:
            return "null"                   #异常则返回null

        return main_content

    def get_article_img(self,url):
        '''
        获取文章图片
        :param url:
        :return:
        '''

        res = requests.get(url)
        if res.status_code == 200:
            contents = re.findall('data-src="(.*?)"', res.text, re.S)

        imgs = []
        path = '../../static/wechat_imgs/'

        for img in contents:
            # 随机生成一个长度为30的字符串，作为图片的文件名
            ran_str = (''.join(random.sample(string.ascii_letters + string.digits, 30)))
            if img.endswith('jpg'):
                img_name = ran_str + '.jpg'
                imgs.append(img_name)

                data = requests.get(img, headers=self.headers)
                fp = open(path + img_name, 'wb')            # 下载图片到本地
                fp.write(data.content)
                fp.close()
            elif img.endswith('jpeg'):
                img_name = ran_str + '.jpeg'
                imgs.append(img_name)

                data = requests.get(img, headers=self.headers)
                fp = open(path + img_name, 'wb')
                fp.write(data.content)
                fp.close()

            elif img.endswith('png'):
                img_name = ran_str + '.png'
                imgs.append(img_name)

                data = requests.get(img, headers=self.headers)
                fp = open(path + img_name, 'wb')
                fp.write(data.content)
                fp.close()

            elif img.endswith('gif'):
                img_name = ran_str + '.gif'
                imgs.append(img_name)

                data = requests.get(img, headers=self.headers)
                fp = open(path + img_name, 'wb')
                fp.write(data.content)
                fp.close()
            else:
                if img.startswith('https://mmbiz.qpic.cn/mmbiz_jpg'):
                    img_name = ran_str + '.jpg'
                    imgs.append(img_name)

                    data = requests.get(img, headers=self.headers)
                    fp = open(path + img_name, 'wb')  # 下载图片到本地
                    fp.write(data.content)
                    fp.close()

                elif img.startswith('https://mmbiz.qpic.cn/mmbiz_jpeg'):
                    img_name = ran_str + '.jpeg'
                    imgs.append(img_name)

                    data = requests.get(img, headers=self.headers)
                    fp = open(path + img_name, 'wb')
                    fp.write(data.content)
                    fp.close()

                elif img.startswith('https://mmbiz.qpic.cn/mmbiz_png'):
                    img_name = ran_str + '.png'
                    imgs.append(img_name)

                    data = requests.get(img, headers=self.headers)
                    fp = open(path + img_name, 'wb')
                    fp.write(data.content)
                    fp.close()

                elif img.startswith('https://mmbiz.qpic.cn/mmbiz_gif'):
                    img_name = ran_str + '.gif'
                    imgs.append(img_name)

                    data = requests.get(img, headers=self.headers)
                    fp = open(path + img_name, 'wb')
                    fp.write(data.content)
                    fp.close()

                elif img.startswith('https://v.qq.com/iframe'):
                    img_name = 'video'
                    imgs.append(img_name)


        return imgs

if __name__ == '__main__':

    ids = ['莞工青年', 'Appso', '差评', '腾讯科技']

    Spider(ids).get_infos()

