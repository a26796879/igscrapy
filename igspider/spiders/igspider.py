# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:44:19 2019

@author: user
"""
#userid = input('Please input user id:')
import scrapy
#from ..items import PtttestItem, PttImage
#domain = 'https://instagram.com'

import json
import requests
from bs4 import BeautifulSoup
'''
url = 'https://www.instagram.com/niceguy331'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
json_part = soup.find_all("script", type="text/javascript")[3].string
json_part = json_part[json_part.find('=')+2:-1]

data = json.loads(json_part)
a = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
'''
class InstagramSpider(scrapy.Spider):
    name = 'igcrawler'
    start_urls = ['https://instagram.com/niceguy331',]
    
    def parse(self, response):
        url = 'https://www.instagram.com/niceguy331'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        json_part = soup.find_all("script", type="text/javascript")[3].string
        json_part = json_part[json_part.find('=')+2:-1]
        
        data = json.loads(json_part)
        a = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        print(a[0]['node']['shortcode'])


'''
        for i in a:#range(len(a)):
            #href = 'https://www.instagram.com/p/' + a[i]['node']['shortcode']
            #print (href)
            href_url = 'https://www.instagram.com/p/' + a[i]['node']['shortcode']
            #yield scrapy.Request(href_url)#, callback = self.parse_images)      \
            print(href_url)
'''