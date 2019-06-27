# -*- coding: utf-8 -*-

import scrapy
from ..items import ImageItem, IgImage
import json
from bs4 import BeautifulSoup

class InstagramSpider(scrapy.Spider):
    name = 'igcrawler'
    start_urls = ['https://www.instagram.com/oppsweiiiii']
    def parse(self, response):
        items = ImageItem()
        urldata = response.body
        soup = BeautifulSoup(urldata, 'html.parser')
        json_part = soup.find_all("script", type="text/javascript")[3].string
        json_part = json_part[json_part.find('=')+2:-1]
        link = []
        data = json.loads(json_part)
        a = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        aftercode = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        # 總文章數
        count = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
        userid = data['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        # 取出個別文章中的照片連結
        for i in range(len(a)):
            item = IgImage()
            items['href'] = 'https://www.instagram.com/p/' + \
                a[i]['node']['shortcode'] + '/'
            link.append(items)
            href_url = items['href']
            yield scrapy.Request(href_url, callback=self.parse_images, meta={'item': item})

        nexturl = 'https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=%7B%22id%22%3A%22' + userid + '%22%2C%22first%22%3A12%2C%22after%22%3A%22' + aftercode.replace('=', '') + '%3D%3D"%7D'
        url = response.urljoin(nexturl)
        yield scrapy.Request(url, self.parse2)

    def parse2(self, response):
        items = ImageItem()
        urldata = response.body
        soup = BeautifulSoup(urldata, 'html.parser')
        rdata = json.loads(soup.text)
        count = rdata['data']['user']['edge_owner_to_timeline_media']['count']
        userid = rdata['data']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['owner']['id']
        for b in range(int((count-12)/12)):
            items = ImageItem()
            urldata = response.body
            soup = BeautifulSoup(urldata, 'html.parser')
            rdata = json.loads(soup.text)
            ra = rdata['data']['user']['edge_owner_to_timeline_media']['edges']
            link = []
            for i in range(len(ra)):
                item = IgImage()
                items['href'] = 'https://www.instagram.com/p/' + \
                    ra[i]['node']['shortcode'] + '/'
                link.append(items)
                href_url = items['href']
                yield scrapy.Request(href_url, callback=self.parse_images, meta={'item': item})
        aftercode = rdata['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        nexturl = 'https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=%7B%22id%22%3A%22' + userid + '%22%2C%22first%22%3A12%2C%22after%22%3A%22' + aftercode.replace('=', '') + '%3D%3D"%7D'
        url = response.urljoin(nexturl)
        yield scrapy.Request(url, self.parse2)

    def parse_images(self, response):
        urldata = response.body
        item = response.meta['item']
        imgurls = []
        soup = BeautifulSoup(urldata, 'html.parser')
        json_part = soup.find_all("script", type="text/javascript")[3].string
        json_part = json_part[json_part.find('=')+2:-1]
        data = json.loads(json_part)
        a = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
 # 取得每篇文章內的圖片
 # 如果有多張照片
        try:
            for i in range(len(a['edge_sidecar_to_children']['edges'])):
                url = a['edge_sidecar_to_children']['edges'][i]['node']['display_url']
                imgurls.append(url)
                item['image_urls'] = imgurls
            return item
# 如果只有一張
        except:
            url = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
            imgurls.append(url)
            item['image_urls'] = imgurls
            return item
