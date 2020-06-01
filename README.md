# Spider_Model.py


    Spider_Model.py主要是解决一些大量二进制文件的下载,例如 mp4,mp3,jpg等等文件.
主要使用方法是:

	1.自己创建一个爬虫文件,继承Spider_Model.py里面的Model_Spider的类
	2.重写parse()方法,将数据清洗后,直接调用downLoad_middleware()方法
	3.在调用downLoad_middleware()的时候注意,items的类型必须是dict.
	4.put_urls()方法是将你传递的url发送给queue队列.
	具体使用案例请看其余的 test文件
	

parse()规则就自己写了,因为不同的网站规则不同.
本模块我会后期维护的.

使用方法:
    class mySpider(Model_Spider):
        def __init__(self):
            super(mySpider, self).__init__()
        def parse(self):
            pass 写你的parse函数
            self.downLoad_middleware() #直接调用,注意传参!

    model = Model_Spider()
    model.put_urls(["url","url2"])
    # 直接使用put_urls()即可,它会直接启动的~

===================================================================================================

QueueMiddleware.py

    处理url的队列
    loopQ = LoopQueue()
    data = [url,url,url,url]
    loopQ.make(data) 生产
    loopQ.consu() 消费
    Spider_Model.py 内部会调用,当然也可以自行使用~


QueryFiles.py

    处理使用model_spider下载缺失的文件
    q = QueryFiles()
    q.query(path="本地文件地址",query_format="查询的文件格式,例如:.jpg",filter_format="过滤的文件格式 例如:.txt")
    q.query_result() # 查询在本地的缺失文件结果,返回一个list!


UrlMiddleware.py

    处理缺失文件的二次下载
    url = UrlMiddleware()
    url.storage_items(items) # 传递一个dict! 必须是已经编好号码的了~ 例如: d = {"2":"2.jpg","1":"1.jpg","56":"56.jpg"}
    url.downLoad_middleware(fail_file = "失败的文件列表",对应的是query_files.query_result()的查询结果,folder_path="本地文件")
    url.download() 会自动调用,请放心~


ProxyMiddleware.py

    自己设置的代理
    proxy = ProxyMiddleware()
    proxy.gethttp() #获取 http代理
    proxy.gethttps() #获取  https代理
    #是给你自己写的程序调用的,前提是你访问的网站是需要 proxy 的~


技巧:
    QueryFiles.py 和 UrlMiddleware.py 建议一起配合使用~


使用案例(using example):
    请看 Test_queryfile_urlmiddleware.py 和 Test_Spider_Model__QueueMiddleware.py 文件~






