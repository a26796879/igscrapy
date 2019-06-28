import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.instagram.com/p/BzAzOW3nOWo'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
json_part = soup.find_all("script", type="text/javascript")[3].string
json_part = json_part[json_part.find('=')+2:-1]
data = json.loads(json_part)
a = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']

#for i in range(len(a['edge_sidecar_to_children']['edges'])):
    #print(a['edge_sidecar_to_children']['edges'][i]['node']['display_url'])

#print (a['video_url'])
# 單篇文章的照片
'''
for i in range(12):
    if data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['is_video'] is True:
        print (data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['video_url'])
'''
# 多照片的文章
# data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][i]['node']['display_url']