# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.http import Request
from urllib import parse
import datetime
from scrapy.loader import ItemLoader

from ArticleSpider.items import  JobBoleArticleItem
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    """
    1. 获取文章列表中的文章并交给scrapy进行下载后进行解析
    2. 获取下一页的url并交给scrapy进行下载后进行解析
    """

    def parse(self, response):

        #解析列表页中的所有文章并交给scrapy进行下载
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url=post_node.css("img::attr(src)").extract_first("")
            post_url=post_node.css("::attr(href)").extract_first("")
            #parse.urljoin(response.url, post_url)
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail, dont_filter=True)

        """
        注意之前callback无法进入，百度了好久发现allowed_domains与post_url域名不一致造成的，allowed_domains之前写错了
            参考网址：https://blog.csdn.net/baidu_32542573/article/details/79722475
        """

        #提取下一页并交给scrapy下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    #爬虫解析的具体实现
    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        #文章标题  也可以写成*[@id="post-110287"]/div[1]/h1/text()   尽量使用div class否则每篇文章的id不一样，不能提取字段了就
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        #创建日期
        create_date = response.xpath('//div[@class="entry-meta"]/p/text()[1]').extract_first().strip().replace('·', '')
        #点赞 评论 收藏
        zan_num = int(response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract_first())

        comment_num = response.xpath('//a[@href="#article-comment"]/span/text()').extract_first()
        #取到这种格式“[' 26 收藏']”，用正则匹配取出数字即可
        match_re = re.match(".*(\d+).*", comment_num)
        if(match_re):
            comment_num = int(match_re.group(1))
        else:
            comment_num=0
        #同上
        fav_num = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract_first()
        match_re = re.match(".*(\d+).*", fav_num)
        if (match_re):
            fav_num = int(match_re.group(1))
        else:
            fav_num=0

        #这是另一种提取xpath的方法，使用div-class，之前都是在谷歌浏览器调试模式下直接拷贝出来的
        #使用div-class固定提取位置，提取文章正文
        content = response.xpath('//div[@class = "entry"]').extract_first()

        tag_list = response.xpath('//p[@class = "entry-meta-hide-on-mobile"]/a/text()').extract()

        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        tags = ",".join(tag_list)

        #文章封面图
        front_image_url = response.meta.get("front_image_url", "")

        #将把取到的信息放到item类中，备用
        article_item['title'] = title
        #转换日期格式，如果有错使用当前日期格式
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item['create_date'] = create_date
        article_item['url'] = response.url
        article_item['zan_num'] = zan_num
        article_item['comment_num'] = comment_num
        article_item['fav_num'] = fav_num
        article_item['tags'] = tags
        article_item['front_image_url'] = [front_image_url]
        article_item['content'] = content
        article_item['url_object_id'] = get_md5(response.url)




        #通过itemloader加载item
        item_loader = ItemLoader(item=JobBoleArticleItem(), response=response)
        #item_loader.add_xpath()
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("zan_num", ".vote-post-up h10::text")
        item_loader.add_css("comment_num", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_num", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()




        #yield可以当return理解？？，还不是太明白
        yield article_item

        print(title)
        print(tags)
        print(create_date)





        '''
        #通过css选择器提取字段
        title = response.css(".entry-header h1::text").extract_first()
        create_date = response.css(".entry-meta-hide-on-mobile::text").extract_first()
        zan_num = response.css(".vote-post-up::text").extract_first()

        fav_num = response.css(".bookmark-btn::text").extract_first()
        match_re = re.match(".*(\d+).*", fav_num)
        if (match_re):
            fav_num = match_re.group(1)

        comment_num = response.css("a[href='#article-comment'] span::text").extract_first()
        match_re = re.match(".*(\d+).*", comment_num)
        if (match_re):
            comment_num = match_re.group(1)

        content = response.css("div.entry").extract()[0]
        tags = response.css().extract("p.entry-meta-hide-on-mobile a::text")
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        tags = ",".join(tag_list)
        '''

