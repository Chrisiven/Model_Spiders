


# url过滤中间件~
import requests
#用于存放下载的url地址的,以便进行二次下载~
class CLpath:#这就是类装饰器啊~~太简单了吧...

    def __init__(self,func):
        self.func = func

    def __call__(self,*args,**kwargs):

        kwargs["folder_path"]=kwargs["folder_path"].replace("\\","/")
        return self.func(self,*args,**kwargs)



class UrlMiddleware:
    """链接中间件"""

    def __init__(self):
        self.local_items = {}
        self.headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"
        }

    def storage_items(self,items):
        # 该功能就是将你传递进来的dict 信息存储在内存中
        """
        items : {序列号:链接}
        """
        self.local_items = items
        print(self.local_items)


    def download_middleware(self,*,fail_file:list,folder_path:str):
        #根据文件失败序列进行下载
        """
        fail_file :失败文件名称
        folder_path :文件夹地址(本地)
        """
        if fail_file:
            for fname in fail_file:

                print("失败序号:",self.local_items[str(fname)])
                self.download(fname, self.local_items[str(fname)], folder_path, proxy=True)

        else:
            print("失败序列号为空~")
            return
    def download(self,name,url,folder_path,proxy=False):
        try:
            if proxy:
                response = requests.get(url,headers=self.headers,proxies={"http":"http:127.0.0.1:1080"})
                if response.status_code == 200:
                    with open(folder_path + "/" + str(name) + ".jpg", "wb") as f:
                        f.write(response.content)
                    print("{} 下载成功".format(name))
            else:
                response = requests.get(url,headers=self.headers)
                if response.status_code == 200:
                    with open(folder_path + "/" + name + ".jpg", "wb") as f:
                        f.write(response.content)
                    print("{} 下载成功".format(name))
        except requests.RequestException as e:
            print("出错~",e)



if __name__ == '__main__':
    c = UrlMiddleware()
    c.storage_items({"1":"我是1","2":"我是2","3":"我是3"})
    c.download_middleware(fail_file=[1,3],folder_path="c")

    """
    如何使用UrlMiddleware()
    1.将您的dict格式的数据使用storage()方法存储
    2.调用download_middleware即可,它会自动调用download()方法下载
    """




