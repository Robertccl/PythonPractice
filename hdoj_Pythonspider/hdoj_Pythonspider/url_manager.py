#coding:utf-8

class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        i=1000
        while(i<=5000):
            url1='http://acm.hdu.edu.cn/showproblem.php?pid='
            url2=str(i)
            url=url1+url2
            self.new_urls.add(url)
            i+=1
    
    
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    
    def has_new_url(self):
        return len(self.new_urls) != 0
    
    '''
    def set_new_urls(self):
        for i in range(1001,1002):
            url1='http://acm.hdu.edu.cn/showproblem.php?pid='
            url2=str(i)
            url=url2+url1
            self.new_urls.add(url)
    '''
    
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    '''
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
    '''        
    
    
    
    
    
    
    
    



