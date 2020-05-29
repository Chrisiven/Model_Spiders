from queue import Queue
import time
class LoopQueue:
    #todo 数据的队列
    def __init__(self,maxsize:int=1000,task_time:int=1):
        self._queue = Queue(maxsize)
        self._time = task_time
    def make(self,data):
        #生产url
        if isinstance(data,dict):
            for item in data.items():
                print("put :",item)
                self._queue.put(item)
                if self._queue.empty():
                    print("生产完毕,当前队列有:{}".format(self._queue.qsize()))
                    break
        elif isinstance(data,(list,tuple)):
            for item in data:
                print("put:",item)
                self._queue.put(item)
                if self._queue.empty():
                    print("生产完毕,当前队列有:{}".format(self._queue.qsize()))
                    break

    def consu(self):
        #消费
        while self._queue.qsize() > 0:
            item = self._queue.get()
            print("get :",item)
            yield item






if __name__ == '__main__':
    c = LoopQueue(50,1)
    data = [1,2,3,4,5,6]
