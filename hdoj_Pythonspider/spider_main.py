#coding:utf-8

from muke_pythonbaike import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        
    def craw(self):
        count=1
        num=0
        #self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url =self.urls.get_new_url()
                print ('craw %d : %s' % (count, new_url))
                html_cont = self.downloader.download(new_url)
                #new_urls, new_data = self.parser.parse(new_url, html_cont)
                #self.urls.add_new_urls(new_urls)
                new_data = self.parser.parse(new_url, html_cont)
                self.outputer.collect_data(new_data)
            
                count+=1    
                
            except:
                print('craw failed')
                num+=1
        self.outputer.output_html() 
        
        print(count)
        print(num)
                
    


if __name__=="__main__":
    root_url = "http://acm.hdu.edu.cn/showproblem.php?pid=1001"
    obj_spider = SpiderMain()
    obj_spider.craw()