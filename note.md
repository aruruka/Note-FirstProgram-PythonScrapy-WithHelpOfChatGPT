Go to the path of the project and activate the Python virtual environment.

```shell
# python -m venv /home/raymondyan/hobby/PythonWebCrawler/LaobanPokemon
cd /home/raymondyan/hobby/PythonWebCrawler/LaobanPokemon/
source ./bin/activate
```

First page: 8153
Totle pages: 3419

```shell
scrapy shell 'https://www.iyingdi.com/tz/tool/general/pcards/8153'
scrapy shell 'https://www.iyingdi.com/tz/tool/general/pcards/8161'

scrapy shell 'https://www.iyingdi.com/tz/tool/general/pcards/8800'
```

```shell
cd tutorial
scrapy crawl pokemon -o output.json
scrapy crawl pokemon_reverse -o output_reverse.json
```

___

检查访问的页面是否包含指定文本:

```python
print(response.text)
print("不好意思，页面被法师撕掉了！" not in response.text)
```

Extract the target description text:

```python
target_description_divs = response.xpath('//*[@id="__layout"]/div/div[3]/div/div/div[2]/div/div')
target_description_list = target_description_divs.css('div::text').getall()
"""
我有以下的一个列表:
['能量转移', ' ', '\n          系列：对战派对组合 草\n        ']

如你所见，这个list中的元素是字符串，其中某些字符串只包含空格字符，我想去除这些只包含空格的字符串元素。
"""
clean_target_description_list = [s for s in target_description_list if s.strip()]
print(clean_target_description_list)
# 👇 Output:
['能量转移', '\n          系列：对战派对组合 草\n        ', '\n              类型：\n              ', '训练家', '\n              属性：\n              ', '一般', '\n              稀有度：\n              ', '-', '\n              效果：\n              ', '将附着于自己场上宝可梦身上的1个基本能量，转附于自己其他宝可梦身上。', '\n              画家：\n              ', 'Ryo Ueda', '\n              类别：\n              ', '物品']


import re
clean_target_description_list = [re.sub(r"[ \t]+", "", s).replace("：", ":") for s in clean_target_description_list]
print(clean_target_description_list)
# 👇 Output:
['能量转移', '\n系列:对战派对组合草\n', '\n类型:\n', '训练家', '\n属性:\n', '一般', '\n稀有度:\n', '-', '\n效果:\n', '将附着于自己场上宝可梦身上的1个基本能量，转附于自己其他宝可梦身上。', '\n画家:\n', 'RyoUeda', '\n类别:\n', '物品']

# use a list comprehension to replace the ":\n" with ": " and merge the strings
concat_target_description_list = [s[:-1] + " " + clean_target_description_list[i+1] if s.endswith(":\n") else s for i, s in enumerate(clean_target_description_list)]
# print the new list
print(concat_target_description_list)
# 👇 Output:
['能量转移', '\n系列:对战派对组合草\n', '\n类型: 训练家', '训练家', '\n属性: 一般', '一般', '\n稀有度: -', '-', '\n效果: 将附着于自己场上宝可梦身上的1个基本能量，转附于自己其他宝可梦身上。', '将附着于自己场上宝可梦身上的1个基本能量，转附于自己其他宝可梦身上。', '\n画家: RyoUeda', 'RyoUeda', '\n类别: 物品', '物品']
# ☝ Note that some elements in the list above are subsets of the previous element. For example: '训练家' is a subset of '\n类型: 训练家'.

# use a list comprehension to remove the elements that are subsets of other elements
clean_concat_target_description_list = [s for s in concat_target_description_list if not any(s in t for t in concat_target_description_list if s != t)]
# print the new list
print(clean_concat_target_description_list)

# Finally, we can combine the elements of the list to a single string
combine_target_description_str = "".join(clean_concat_target_description_list)
print(combine_target_description_str)
```

Extract the target image:

```python
target_img_selector = response.css("#__layout > div > div.default-main-container.w-full.pl-90.big\:pl-250.pt-56 > div > div > div.marvel-card-detail-page > div > img")

# Extract the relative URL of the image from the Selector
relative_url = target_img_selector.css("::attr(src)").get()
print(relative_url)

# Construct the absolute URL of the image
from urllib.parse import urljoin
absolute_url = urljoin(response.url, relative_url)
print(absolute_url)

target_img_alt = target_img_selector.css('::attr(alt)').get()
print(target_img_alt)

# Send a GET request to download the image
import requests
response = requests.get(absolute_url)

# Check if the request was successful
if response.status_code == 200:
    # Save the image to a file
    with open(f'./crawled_images/{target_img_alt}.png', 'wb') as file:
        file.write(response.content)
        print(f"Image downloaded successfully. URL: {absolute_url}. ImageFileName: {target_img_alt}.png.")
else:
    print(f"Failed to download the image.  URL: {absolute_url}. ImageFileName: {target_img_alt}.png.")
```
