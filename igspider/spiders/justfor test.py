import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.instagram.com/p/BiEy_sTA9Vv/'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
json_part = soup.find_all("script", type="text/javascript")[3].string
json_part = json_part[json_part.find('=')+2:-1]
data = json.loads(json_part)
a = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']

#for i in range(len(a['edge_sidecar_to_children']['edges'])):
    #print(a['edge_sidecar_to_children']['edges'][i]['node']['display_url'])


# 單篇文章的照片
print(data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url'])

# 多照片的文章
# data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][i]['node']['display_url']