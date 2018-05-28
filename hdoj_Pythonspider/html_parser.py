
#coding:utf-8

from bs4 import BeautifulSoup
import re
import urllib
from urllib.parse import urljoin



class HtmlParser(object):
    '''
    def _get_new_urls(self, page_url, soup):
        new_urls = set();
        #/view/123.htm
        links = soup.find_all('a', href=re.compile(r"/view/\d+\.htm"))
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        
        return new_urls
    

    def _get_new_data(self, page_url, soup):
        res_data = {}
        
        #url
        res_data['url'] = page_url
        
        #<dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        res_data['title'] = title_node.get_text()
        
        #<div class = "lemma-summary">
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()
        
        return res_data
    
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
    '''
    
    def _get_new_data(self, page_url, soup):
        res_data = {}
        
        #url
        res_data['url'] = page_url
        
        #res_data['number'] = i
        
       
        node = soup.find('table')
        res_data['title'] = node.find("h1").get_text()
             
        res_data['h1']="Problem Description"
        res_data['h2']="Input"
        res_data['h3']="Output"
        res_data['h4']="Sample Input"
        res_data['h5']="Sample Output"
        res_data['h6']="Author"
        count=0
        if(node.find('div', text="Problem Description").find_next('div',attrs={'class':'panel_content'}) != None):
            res_data['h1_content'] = node.find('div', text="Problem Description").find_next('div',attrs={'class':'panel_content'}).get_text()
        else:
            count+=1
            res_data['h1_content'] = "######"
            
        if(node.find('div', text="Input") != None):
            res_data['h2_content'] = node.find('div', text="Input").find_next('div',attrs={'class':'panel_content'}).get_text()
        else:
            count+=1
            res_data['h2_content'] = "######"  
        
        if(node.find('div', text="Output") != None):     
            res_data['h3_content'] = node.find('div', text="Output").find_next('div',attrs={'class':'panel_content'}).get_text()
        else:
            count+=1
            res_data['h3_content'] = "######"
        
        if(node.find('div', text="Sample Input") != None):    
            res_data['h4_content'] = node.find('div', text="Sample Input").find_next('div',attrs={'class':'panel_content'}).get_text()
        else:
            count+=1
            res_data['h4_content'] = "######" 
        
        if(node.find('div', text="Sample Output") != None):  
            res_data['h5_content'] = node.find('div', text="Sample Output").find_next('div',attrs={'class':'panel_content'}).get_text()
        else:
            count+=1
            res_data['h5_content'] = "######"   
        #res_data['h6_content'] = node.find('div', text="Author").find_next('div',attrs={'class':'panel_content'}).get_text()
        
        if(count<5):
            res_data['title'] = node.find("h1").get_text()
        else:
            res_data['title'] = "No Such Problem"
       
        return res_data
    
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='gb18030')
        
        new_data = self._get_new_data(page_url, soup)
        return new_data
    
    
    
    
