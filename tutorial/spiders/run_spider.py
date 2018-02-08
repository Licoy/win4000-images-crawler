import scrapy

from tutorial.items import CardItem, ImagesItem


class RunSpider(scrapy.Spider):

    name = "run"

    headers = {
        "Referer": "http://www.win4000.com/zt/xinggan.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/63.0.3239.84 Safari/537.36 "
    }

    def start_requests(self):
        url = "http://www.win4000.com/zt/xinggan.html"

        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        li_list = response.css("div.list_cont.Left_list_cont.Left_list_cont1 > div.tab_tj > div > div > ul > li")
        url_list = []
        for li in li_list:
            item = CardItem()
            href = li.css("a::attr(href)").extract_first()
            item['href'] = href
            item['title'] = li.css("a::attr(title)").extract_first()
            url_list.append(href)
            yield item
        for i in url_list:
            print("->>>正在获取详情： %s" % i)
            yield scrapy.Request(url=i, callback=self.detail_parse, headers=self.headers)

        # 检测是否有下一页
        next_page = response.css("div.pages a.next")
        if len(next_page) > 0:
            next_url = next_page.css("::attr(href)").extract_first()
            print(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def detail_parse(self, response):
        li_list = response.css("#scroll > li")
        for i in range(1, len(li_list)):
            href = li_list[i].css("a::attr(href)").extract_first()
            yield scrapy.Request(url=href,headers=self.headers, callback=self.detail_img_download)
        self.detail_img_download(response)

    def detail_img_download(self, response):
        img = response.css("body > div.main > div > div.pic_main > div > div.col-main > div > div.pic-meinv > a > "
                           "img.pic-large")
        if len(img) > 0:
            item = ImagesItem()
            image_urls = img.css("::attr(src)").extract()
            item['image_urls'] = image_urls
            yield item
