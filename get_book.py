# encoding:utf-8
import threading
import time
import requests
import json
import re
from lxml import etree
from tkinter import *
from tkinter.ttk import *


requests.packages.urllib3.disable_warnings()
class Spider():
    
    def __init__(self):
        # 保存数据的列表
        self.data_list = []
        # 模拟构造参数
        self.j_time = 'jsonp_'+str(time.time_ns())[0:13]+'_'+str(time.time_ns())[14:]
        # 请求的url
        self.url = 'https://pjapi.jd.com/book/sort'
        # 构建参数
        self.params = {
            'source': 'bookSort',
            'callback': self.j_time
        }
        # 构建请求头
        self.headers = {
            'cookie': 'unpl=V2_ZzNtbRJTRRJwD0BcK05ZVmIGEQ5KBBdGIA5GUC9JXgw1UUVZclRCFnQUR11nGVsUZwMZXEpcRhJFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsbVAdhAxVcQl9zJXI4dmR%2fHVkEYAQiXHJWc1chVEZTch5bACoDEFVAUUMSdAhOZHopXw%3d%3d; __jdu=1393716019; shshshfpb=mFhzJyPywkV5vL0qrmRSnnw%3D%3D; shshshfpa=52c00520-ca15-739c-d9a7-ab5aa24eb21d-1587279821; user-key=f7083f4d-61a5-4ec1-8711-f6ff9b38358a; cn=0; __jdv=76161171|direct|-|none|-|1598858101857; areaId=16; ipLoc-djd=16-1332-1336-0; PCSYCityID=CN_350000_350500_350583; shshshfp=c3983266c29808bcf0fce98a5d7339c3; shshshsID=586902d611a50b76309d9d70d19fdbef_1_1598858105891; __jda=122270672.1393716019.1597547387.1597547389.1598858102.2; __jdc=122270672; 3AB9D23F7A4B3C9B=A22HWYHNRIFP23N4VD3HZIWXQFT7PUSAN4RBBZZ5GLKR42HBJO5SZMXNF4RQTBETFNBGZDINZVDE5PU2PATVOPNAYM; __jdb=122270672.6.1393716019|2.1598858102',
            'referer': 'https://book.jd.com/booksort.html',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
        self.header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }


    def ININ_WIN(self):
        Label(win, text='欢迎使用爬虫软件', font=(None, 14)).pack(padx=10, pady=10)     # 界面标签
        Button(win, text='开始爬取', command=lambda :self.thread_it(self.get_data)).pack(padx=10, pady=10)      # 界面按钮
        Button(win, text='退出爬虫', command=self.shut).pack(padx=10, pady=10)  # 界面按钮

        self.tree = Treeview(height=10, column=('爬取进程'))        # 创建显示界面
        self.tree.pack(side=TOP,padx=10, pady=10)       # 放置显示位置
        Label(win, text='请输入要搜索的内容：').pack(side=LEFT, padx=10, pady=10)     # 创建标签
        self.search = Entry(win, text=StringVar())      # 创建输入框
        self.search.pack(side=LEFT, padx=10, pady=10)
        Button(win, text='搜索', command=lambda :self.thread_it(self.search_)).pack(side=LEFT, padx=10, pady=10)      # 创建按钮
        cols = ('类别', '书名', '价格', '店铺', '活动','链接')
        self.search_tree = Treeview(height=10, column=cols, show='headings')
        for col in cols:
            self.search_tree.heading(col, text=col, anchor=CENTER)
            self.search_tree.column(col, width=100, anchor='center')  # 界面列表
        self.search_tree.pack(padx=10, pady=10, ipadx=300)
        win.mainloop()
    def shut(self):
        """退出程序"""
        exit()

    def search_(self):
        """搜索数据"""

        with open('result.txt', 'r')as f:       # 打开文件
            data = [str(i).replace('\n','') for i in f.readlines()]
        for i in data:
            if self.search.get() in i:
                r1 = re.findall(r"'类别': '(.*?)'", i)[0]
                r2 = re.findall(r"'书名': '(.*?)'", i)[0]
                r3 = re.findall(r"'价格': '(.*?)'", i)[0]
                r4 = re.findall(r"'店铺': '(.*?)'", i)[0]
                r5 = re.findall(r"'活动': \[(.*?)\]", i)[0]
                r6 = re.findall(r"'链接': '(.*?)'", i)[0]
                self.search_tree.insert('',END, text='搜索结果', values=(r1, r2, r3, r4, r5, r6))       # 插入界面数据


    def parse_detail(self, url_detail, title):
        # 发送请求获取响应
        self.tree.heading('爬取进程', text='爬取进程', anchor=CENTER)       # 界面的列表头
        self.tree.column('爬取进程', width=250, anchor='center')        # 界面中的列
        self.tree.insert('', END, text='正在爬取..', values=(url_detail))   # 将数据插入界面
        response = requests.get(url_detail, headers=self.header)        # 发送请求并获取响应
        print(response.text)
        # 解析数据
        tree = etree.HTML(response.content)
        uls = tree.xpath('//ul[@class="gl-warp clearfix"]/li')  # 获取网页数据
        for li in uls:
            item = {}
            try:
                # 若数据格式正确则写入文件
                name = li.xpath('.//div[@class="p-name"]/a/em//text()')[0]  # 书名
                price = li.xpath('.//div[@class="p-price"]//i/text()')[0]   # 价格
                shop = li.xpath('.//div[@class="p-shopnum"]/a/@title')[0]   # 店铺
                activity = li.xpath('.//div[@class="p-icons"]//text()')[1::2]   # 活动
                url_d = 'https:' + li.xpath('.//div[@class="p-img"]/a/@href')[0]    # 详情链接
                # 用字典格式储存数据
                item['类别'] = title
                item['书名'] = name
                item['价格'] = price
                item['店铺'] = shop
                item['活动'] = activity
                item['链接'] = url_d
                with open('result.txt', 'a+')as f:  # 打开文件
                    f.write(str(item) + ',\n')  # 保存文件， 并自动关闭文件
            except:
                # 格式错误则不写入
                self.tree.insert('', END, text='正在爬取' , values=('索引错误...'))

    @staticmethod
    def thread_it(func, *args):
        """开启多线程防止界面卡死"""
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def get_data(self):
        response = requests.get(self.url, params = self.params, headers = self.headers)  # 发送请求获取响应
        str_data = response.text.replace('{}'.format(self.j_time), '').replace('(', '').replace(')', '')  # 获取数据并清洗
        j_data = json.loads(str_data)["data"]  # 转化成json数据
        for data in j_data:
            category_b = data['categoryName']  # 获取分类名称
            categories = data['sonList']
            for category in categories:
                detail_list = []
                title = category['categoryName']  # 获取标题
                id_after = str(category['categoryId']).replace('.0', ',')  # 获取id
                id_fur = str(category['fatherCategoryId']).replace('.0', ',')  # 获取id
                url_detail = 'https://list.jd.com/list.html?cat=' + id_fur + id_after  # 构建url
                all_data = category_b + '--' + title + ':' + url_detail

                detail_list.append(all_data)
                self.parse_detail(url_detail,title)


if __name__ == '__main__':

    win = Tk()  # 创建界面
    app = Spider()  # 创建爬虫对象
    app.ININ_WIN()



