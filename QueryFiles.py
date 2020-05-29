



import os
# 查找本地下载的缺失文件~
class QueryFiles:
    def __init__(self):
        self.index = 1
        self.items = {}
        self.missing_value = []
        self.RangeNums = 1

    def query(self,path,*,query_format:str=".jpg",filter_format:str="txt"):
        """
        todo path:输入的文件地址
        todo query_format:查询的文件格式  比如是.jpg 还是.ts
        todo file_models:过滤的文件格式 比如里面有.txt 或者.mp4文件啊,就可以过滤
        """
        print("正在编排,请稍后...")

        for root , dir , files in os.walk(path):
            for file in files:
                if filter_format in file:
                    print("{} 不是我们所要排序的文件".format(filter_format))
                    continue
                num = int(file.replace(query_format, ""))
                self.items[num] = file



            for num in range(1,max(self.items)):
                try:
                    print(self.index,self.items[num])
                except KeyError as e:
                    print("出现错误~",e)
                    self.missing_value.append(self.index)
                self.index+=1

    def query_result(self):
        print("查询成功,目前该文件夹内共缺失了",len(self.missing_value),"个文件,分别是",self.missing_value,"已经结果返回~")
        return self.missing_value

if __name__ == '__main__':
    q = QueryFiles()
    #根据所提示的信息  来完成缺失文件的下载,所以我们需要queue!将已经下载的url存放进去!然后备注好信息,以便在
    #有缺失文件的时候在进行二次下载!
    q.query("C:/Users/Chrisiven/Desktop/UP/t/what the fuck/All_Porn/Porn/TennoKatsurayaNewhal")