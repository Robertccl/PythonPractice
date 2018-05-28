#coding:utf-8

import codecs
#import sys

class HtmlOutputer(object):
    


    #reload(sys)
    #sys.setdefaultencoding('utf-8') 
    
    def __init__(self):
        self.datas = []
    
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)
                      
    def output_html(self):
        fout = codecs.open('outputhan.html', 'w', 'utf-8')
        fout.write("<html>")
        fout.write("<body>")
        
        fout.write("<table>") 
        
        for data in self.datas:
            
            fout.write("<tr>") 
            fout.write("<td>")
            fout.write("<h1>%s</h1>" % data['title'] )
            
            fout.write("%s" % data['url'] )
            fout.write("<div>%s</div>" % data['h1'] )  
            fout.write("<div>%s</div>" % data['h1_content'] ) 
             
            fout.write("<div>%s</div>" % data['h2'] )  
            fout.write("<div>%s</div>" % data['h2_content'] ) 
            
            fout.write("<div>%s</div>" % data['h3'] ) 
            fout.write("<div>%s</div>" % data['h3_content'] ) 
              
            fout.write("<div>%s</div>" % data['h4'] ) 
            fout.write("<div>%s</div>" % data['h4_content'] ) 
            
            fout.write("<div>%s</div>" % data['h5'] ) 
            fout.write("<div>%s</div>" % data['h5_content'] ) 
              
            #fout.write("<div>%s</div>" % data['h6'].encode('utf-8')) 
            #fout.write("<div>%s</div>" % data['h6_content'].encode('utf-8')) 
            fout.write("</td>")
            fout.write("</tr>")
            
        fout.write("</html>") 
        fout.write("</body>")
        fout.write("</table>")
        fout.close()  