
import requests,os
from lxml import etree
import aiohttp ,asyncio,aiofiles
from aiohttp.client_exceptions import ClientConnectionError
from model.QueryFiles import QueryFiles
from model.UrlMiddleware import UrlMiddleware



class ImHentai_Spider:
    """
    错误 : 下载文件无法找到地址 18:57

    """
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.sem=asyncio.Semaphore(20)
        self.success=0
        self.folder_name = ""
        self.fail=0
        self.query = QueryFiles() #查询本地是否有遗漏的文件
        self.urlmidd = UrlMiddleware()


        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        }
        self.proxy={
            "http":"you proxy"
        }
        self.domain_url='https://imhentai.com'
        self.title = ""
        self.image_dict = {}

    def get_title(self,response):
        html = etree.HTML(response)
        # eng_title=html.xpath('//div[@class="col-md-7 col-sm-7 col-lg-8 right_details"]/h1/text()')[0]
        jap_title=html.xpath('//div[@class="col-md-7 col-sm-7 col-lg-8 right_details"]/h1/text()')[0]

        self.title = jap_title
        print("该动漫的标题是:",self.title)


    def get(self,url):
        self.write_url = url
        print("正在访问: {}".format(url))
        try:
                response =requests.get(url,headers=self.headers,proxies=self.proxy)
                if response.status_code == 200:
                    print("success!")
                    next_url=response.url.replace("gallery","view")
                    self.get_title(response.text)
                    self.second_get(next_url+"1")
        except requests.exceptions.RequestException as e:
            print("Error!")

    def mkdir(self,*,path):
        path = path.replace("[","").replace("]","").replace(")","").replace("(","").replace(" ","")
        path = path[:20]
        self.folder_name = path
        file_path = os.path.join(os.path.dirname(__file__) + "/", path)

        try:
            os.mkdir(file_path)
        except FileExistsError as e:
            print("文件已经存在,创建失败!")

        finally:
            return file_path


    def second_get(self,url):
        print("正在访问: {}".format(url))
        try:
                response =requests.get(url,headers=self.headers)
                if response.status_code == 200:
                    print("success!")
                    html = etree.HTML(response.text)
                    image_url=html.xpath('//img[@id="gimg"]/@src')[0].replace("1.jpg","")
                    print(image_url)
                    total_num = int(html.xpath('//span[@class="total_pages"]/text()')[0])
                    print("正在生成图片的地址 ...")

                    for i in range(1,total_num+1):
                        self.image_dict[str(i)] = image_url+str(i)+".jpg"
                    print("正在启动协程下载文件...")
                    self.mkdir(path=self.title) #todo 创建文件夹!

                    self.urlmidd.storage_items(self.image_dict) # todo 将所有的下载链接放入进去~
                    Task=[] #任务队列
                    for num,url in self.image_dict.items():
                        task=self.download_img(url,num)
                        Task.append(task)
                    self.loop.run_until_complete(asyncio.wait(Task))
                    print("成功{}: 失败:{} 总数:{}".format(self.success,self.fail,(self.success+self.fail)))

                    self.query.query(self.folder_name) #todo 将本地的下载文件地址传入进去~
                    fail_files = self.query.query_result() #todo 接收失败的文件夹~
                    self.urlmidd.download_middleware(fail_file=fail_files,
                                                     folder_path=self.folder_name) #todo 中间件进行二次下载,保证文件的完整性~
        except requests.exceptions.RequestException as e:
            print("未知错误!")


    async def download_img(self,url,num):
        headers = {
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }

        try:

            async with self.sem:
                async with aiohttp.ClientSession(headers=headers) as session:
                    print('正在下载第{}个 {}'.format(num, url))
                    async with session.get(url, proxy="http://127.0.0.1:1080") as resp:
                        content = await resp.read()
                        print('正在下载第 {} 个文件'.format(num))
                        with open(self.folder_name + "/" + num + ".jpg" ,"wb") as f:
                            f.write(content)
                        print('下载成功')
                        self.success += 1
        # except ClientConnectionError as e:
        #     print("客户端连接错误", e,url)
        #     self.fail += 1
        except Exception as e:
            print(url,e, '下载超时!')
            self.fail += 1



if __name__ == '__main__':
    c = ImHentai_Spider()
    c.get("url")
