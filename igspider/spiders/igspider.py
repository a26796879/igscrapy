# -*- coding: utf-8 -*-
#userid = input('Please input user id:')
import scrapy
#from ..items import PtttestItem, PttImage
#domain = 'https://instagram.com'
from ..items import ImageItem, IgImage
import json
from bs4 import BeautifulSoup


class InstagramSpider(scrapy.Spider):
    name = 'igcrawler'
    start_urls = ['https://www.instagram.com/niceguy331']

    def parse(self, response):
        items = ImageItem()
        urldata = response.body
        soup = BeautifulSoup(urldata, 'html.parser')
        json_part = soup.find_all("script", type="text/javascript")[3].string
        json_part = json_part[json_part.find('=')+2:-1]
        link = []
        data = json.loads(json_part)
        a = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for i in range(len(a)):
            item = IgImage()
            items['href'] = 'https://www.instagram.com/p/' + a[i]['node']['shortcode'] +'/'
            link.append(items)
            href_url = items['href']
            yield scrapy.Request(href_url, callback = self.parse_images, meta={'item': item}) 
        #return link

    def parse_images(self, response):
        urldata = response.body
        item = response.meta['item']
        imgurls = []
        soup = BeautifulSoup(urldata, 'html.parser')
        json_part = soup.find_all("script", type="text/javascript")[3].string
        json_part = json_part[json_part.find('=')+2:-1]
        data = json.loads(json_part)
        a = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
    # 取得每篇文章內的 圖片
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
