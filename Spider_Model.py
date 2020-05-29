

import requests,asyncio,aiohttp,aiofiles
from fake_useragent import UserAgent

from requests.exceptions import  RequestException,Timeout,ConnectionError
import os,time
from QueueMiddleware import LoopQueue
from threading import Thread


# 请遵守 PEP8 规范

class Model_Spider:
    name = "Model Spider"
    def __call__(self, *args, **kwargs):
        print("这个模块是为了对付下载多个ts,jpg,png,mp3,mp4这样的情况而开发的,")

    def __init__(self,*,
                    thread_num:int=None, # 设置线程数量
                    proxy:dict=None, # 代理
                    Semaphore_value:int=100, # 一次下载的数目
                    timeout:int=60): #超时时间

        super(Model_Spider, self).__init__()
        if thread_num == None:
            self._thread_num = 5 # 如果不设置,则为 5
        else:
            self._thread_num = thread_num
        self._headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":UserAgent().Chrome
        }
        self.link_data = {
            "title":"",
            "links":[]
        }
        self._proxy = proxy  #代理
        self._timeout = timeout #超时
        self._QueueSize = 1000 #todo  默认队列的长度
        self._title = 'Model_Spider' #标题名称
        self._DateQueue = LoopQueue(self._QueueSize)
        self._queue = self._DateQueue._queue
        self._url_list = ''
        self._loop = asyncio.get_event_loop()
        self._Semaphore = asyncio.Semaphore(Semaphore_value)
        self._file_path = os.getcwd() #当前文件
        self._folder_path = '' # 当前文件夹
        self._file_success = 0 #文件下载成功数
        self._file_fail = 0 #文件下载失败数量
        self.session = requests.Session() #todo 默认开启session功能
    def put_urls(self,urls:list): #todo 传递url
        self._DateQueue.make(urls)
        print("传入成功,数量:{}".format(self._DateQueue._queue.qsize()))
        self.run() # todo 启动整个程序


    def set_headers(self,header_items)->None: #todo 给用户调用,用于设置爬虫的headers
        for key,value in header_items.items():
            self._headers.setdefault(key,value)
            print("{} 设置成功!".format(key))
        print(self._headers)


    def set_QueueSize(self,value): #todo 设置队列的大小
        self._QueueSize = value

    def __Queueloop(self): #todo 队列 不用管
        if self._queue.qsize() <= 0:
            print("队列空间不足,请使用 set_QueueSize() 设置队列大小")
            return False
        elif self._queue.qsize() > 5: #如果任务总数大于5,那么就开启多线程.
            print("正在开启多线程模式:")
            while self._queue.qsize() > 0:
                thread_list = []
                print("当前线程数:",self._thread_num)
                print("当前任务数:",self._queue.qsize())
                for i in range(0,self._thread_num):
                    if self._queue.qsize() == 0:
                        break
                    url = self._queue.get()
                    thread = Thread(target=self.__get,args=(url,))
                    thread_list.append(thread)
                    thread.start()
                for thread_join in thread_list:
                    thread_join.join()
                time.sleep(self._DateQueue._time)
        else:
            while self._queue.qsize() > 0 :
                url = self._queue.get()
                self.__get(url)



    def __get(self,url): #TODO get访问

            print("正在访问 : {}".format(url))
            try:
                response = self.session.get(url,headers=self._headers, proxies=self._proxy)
                if response.status_code == 200:
                    print("{} 访问成功! ".format(url))
                    self.parse(response)
            except Timeout as e:
                print("超时 ...", e)
                return False
            except ConnectionError as e:
                print("连接错误 ...", e)
                return False
            except RequestException as e:
                print("未知错误 ...", e)
                return False

    def __post(self,*,url:str,Data:dict): #todo post访问 需要传递参数
        data = {}
        for key,value in Data.items():
            data[key] = value
        print("{} 正在请求".format(url))
        try:
            response = self.session.post(url, headers=self._headers,data=data, proxies=self._proxy)
            if response.status_code == 200:
                print("{} 访问成功!".format(url))
                self.parse(response)
        except Timeout as e:
                print("超时 ...", e)
                return False
        except ConnectionError as e:
            print("连接错误 ...", e)
            return False
        except RequestException as e:
            print("未知错误 ...", e)
            return False


    def parse(self,response): #todo 用户解析方法 必须写! 继承之后直接调用即可  然后里面是哟个 downLoad_middleware 方法
        #这里自己写解析规则

        pass


    def download_middleware(self,*,title,items:dict,file_model):#todo 下载中间件!

        """
        :param title:  解析的标题
        :param items:  解析出来的数据
        :param file_model: 文件模式 .jpg .jpeg .mp3 .mp4
        """

        task_list = []
        try:
            self._folder_path = self.__mkdir(title)
            # self._DateQueue.make(items)#传入数据
            for name,url in items.items():
                # name,url = self._queue.get_nowait()
                print("正在获取:{}  {}".format(name,url))
                task = self.__async_download(url,name,file_model)
                task_list.append(task)
            self._loop.run_until_complete(asyncio.wait(task_list))
            self.__show_info()
        except Exception as e:
            print("错误 {}".format(e))
            raise e

    async def __async_download(self,url,name,file_model:str): #todo  协程下载
        """
        :param url: 下载地址
        :param num:  下载的名称
        :param file_model: 下载文件的模式 : 一般是 .mp3 .mp4 .ts .jpg .avi .jpeg 等等
        :return:
        """
        async with self._Semaphore:
            try:
                async with aiohttp.ClientSession(headers=self._headers) as session:
                    print("正在访问 {}".format(url))
                    async with session.get(url,proxy=self._proxy) as response:
                        if response.status == 200:
                            content = await response.read()
                            async with aiofiles.open(self._folder_path+"/"+name+file_model,"wb") as f:
                                await f.write(content)
                                self._file_success += 1
                                print("{} 下载成功!".format(name))
            except aiohttp.ClientConnectionError as e:
                print("客户端连接错误",e)
                self._file_fail += 1
            except aiohttp.ClientHttpProxyError as e:
                print("http代理错误!",e)
                self._file_fail += 1
            except aiohttp.ClientError as e:
                print("客户端错误!",e)
                self._file_fail += 1
            except Exception as e:
                print("未知错误!",e,url)
                self._file_fail += 1
    def __mkdir(self,path):  #创建文件夹
        file_path = os.path.join(os.getcwd().replace("\\","/")+ "/", path)
        print(file_path)
        try:
            os.mkdir(file_path)

        except FileExistsError as e:
            print("文件已经存在,无法继续创建")
        finally:
            return file_path

    def __show_info(self):# 最后计算下载的文件数量 和 成功失败数量!
        print("所有链接: {},成功链接: {} ,失败链接: {}".format((self._file_success+self._file_fail),
                                                                    self._file_success,
                                                                    self._file_fail))

    def run(self):#run!
        self.__Queueloop()

if __name__ == '__main__':
    my = Model_Spider()
    # my.put_urls(['https://www.simply-hentai.com/original-work/nyotaika-cheat-ga-souzou-ijou-ni-bannou-sugita-sono-1-aa034/all-pages'])
    # my.run()

"""

    使用方法:
        class mySpider(Model_Spider):
            def __init__(self):
                super(mySpider, self).__init__()
            def parse(self):
                pass 写你的parse函数
                self.downLoad_middleware() #直接调用,注意传参!
    
        model = Model_Spider()
        model.put_urls(["url","url2"])
        model.run() #即可!


"""



