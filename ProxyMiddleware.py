

class ProxyMiddleware:


    def __init__(self):

        self.proxy = {
            "http":"you proxy",
            "https": "you proxy"
        }


    def gethttp(self):
        return self.proxy["http"]

    def gethttps(self):
        return self.proxy["https"]


if __name__ == '__main__':
    c = ProxyMiddleware()
    print(c.gethttp()
          )
