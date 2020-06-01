from QueueMiddleware import LoopQueue
from Spider_Model import Model_Spider
import requests,time


class Spider(Model_Spider,LoopQueue):
    def __init__(self,proxy):
        super(Spider, self).__init__(proxy=proxy)
        self.title = ''
        self.data_dict = {}
    def parse(self,response):
        for key,value in response.json().items():
            self.data_dict[key] = value["sizes"].get('full')
        print(self.data_dict)
        self.download_middleware(title=self.title,items=self.data_dict,file_model='.jpg')
    #自己定制需要的东西





if __name__ == '__main__':

    S = Spider({"http":"http://127.0.0.1:1080"})
    S.put_urls(urls=["https://www.simply-hentai.com/original-work/nyotaika-cheat-ga-souzou-ijou-ni-bannou-sugita-sono-1-aa034"])
    

