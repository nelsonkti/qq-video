# -*- coding: utf-8 -*-
import scrapy
from QQVideo.items import QqvideoItem
from scrapy import Request
import json

class QqvideoSpider(scrapy.Spider):
    name = 'qqvideo'
    allowed_domains = ['v.qq.com']
    search_name = '完美关系'
    publish_time = '2020'
    detail_url_json_type = '&callback=_jsonp_0_c39d&_t=1582277769052'
    detail_url = 'http://s.video.qq.com/get_playsource?id=vooy2m9hi5p1jqm&plat=2&type=4&range=1-44&data_type=2&video_type=2&plname=qq&otype=json&uid=db5b6fae-3489-4e80-bdb1-464bfb6c95e9' + detail_url_json_type
    start_urls = ["https://v.qq.com/x/search/?q="+search_name+""]

    headers = {
        'authority': 's.video.qq.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'referer': 'https://v.qq.com/detail/m/m441e3rjq9kwpsc.html',
        'Content-Type': 'application/json',
        'cookie': 'tvfe_boss_uuid=8563d4f10756692a; pgv_pvid=5714545948; video_guid=dd4a1d4224bc645c; video_platform=2; pgv_pvi=6741800960; RK=gQIENdu8OW; ptcz=85ce55d3467778adf4a9a2f7b8f50bc88df3b01bc5098b7751f40cd5d48c3b22; pgv_info=ssid=s9571742832',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }

    def parse(self, response):
        item = QqvideoItem()
        print('【开始解析】')
        category_name = \
        response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/h2/a/span[2]/text()').extract()[0]
        print(category_name)

        title = response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/h2/a/em/text()').extract()[0]
        print(title)

        # 解析发布时间
        publish_time = self.publish_time + "-01-01 00:00:00"
        print(publish_time)

        img_url = 'http:' + response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/a/img/@src').extract()[0]
        print(img_url)
        # desc = response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[5]/span[2]/text()').extract()[0]
        # desc = response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[3]/span[2]/text()').extract()[0]
        desc = response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/span[2]/text()').extract()[0]
        print(desc)

        author_name_arr = []
        # 解析作者
        # authorList = response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[3]/span[2]/a')
        authorList = response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[3]/span[2]/a')
        # authorList = response.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/span[2]/a')
        print(authorList)

        i = 0
        author_name_string = ''
        for author in authorList:
            i = i + 1
            author_name = author.xpath("/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[3]/span[2]/a[" + str(i) + "]/text()").extract()[0]
            # author_name = author.xpath("/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/span[2]/a[" + str(i) + "]/text()").extract()[0]
            author_name_string = author_name_string + author_name + ' '

        print(author_name_string)

        print("整理数据")
        if title and img_url and author_name_string and desc and publish_time:
            print('数据 【完整】')

            item['category_name'] = category_name
            item['title'] = title
            item['img_url'] = img_url
            item['author_name'] = author_name_string
            item['desc'] = desc
            item['publish_time'] = publish_time
        else:
            print('数据 【不完整】')
            print('category_name')
            print(category_name)
            print('title')
            print(title)
            print('img_url')
            print(img_url)
            print('author_name')
            print(author_name)
            print('desc')
            print(desc)
            print('publish_time')
            print(publish_time)
            print('series')

            if category_name is None:
                print('category_name is None')

            if title is None:
                print('title is None')

            if img_url is None:
                print('img_url is None')

            if author_name_string is None:
                print('author_name_string is None')

            if desc is None:
                print('desc is None')

            if publish_time is None:
                print('publish_time is None')


        print(item)
        print('【剧集】获取')

        # yield scrapy.Request(self.detail_url, meta={"item": item}, callback=self.parsed)

        yield Request(self.detail_url, callback=self.parsed, meta={"item": item}, headers=self.headers, dont_filter=True)


    def parsed(self, response):
        item = response.meta["item"]

        body = response.body
        s2 = body.decode().strip("_jsonp_0_c39d(")
        s2 = s2.strip(")")
        s3 = json.loads(s2)
        # print('===============================')
        videoPlayList = s3['PlaylistItem']['videoPlayList']
        seriesArr = []
        for video in videoPlayList:
            # print('===============================')
            # print(video)
            series_num = video['title']
            # print(series_num)
            series_url = video['playUrl']
            seriesArr.append([series_num, series_url])


        print('===============================')
        # print(seriesArr)

        item['series'] = seriesArr

        print(item)
        yield item
