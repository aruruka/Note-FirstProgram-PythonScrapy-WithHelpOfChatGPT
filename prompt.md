我正在写一个Python程序。我使用Scrapy爬取一个网站的内容。

我打算用这个网页"<https://www.iyingdi.com/tz/tool/general/pcards/8153>"作为起始网页。
我打算依次爬取5个网页，第二网页是"<https://www.iyingdi.com/tz/tool/general/pcards/8154>"，第三个网页是"<https://www.iyingdi.com/tz/tool/general/pcards/8155>"，你应该已经注意到了，目标网页的URL的最后一个部分是一个递增的数字。

对于 start_urls，我希望我的程序可以一直尝试爬取下一个网页，直到爬取到错误的网页。
错误的网页会包含以下的文本:  
"不好意思，页面被法师撕掉了！"

每个目标网页中有1张图片，和一段文字。

___

对于目标图片，我已经知道可以使用以下这段Python代码来下载。

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

___

对于目标文本，我已经知道可以使用以下这段Python代码来获取。

```python
target_description_divs = response.xpath('//*[@id="__layout"]/div/div[3]/div/div/div[2]/div/div')
target_description_list = target_description_divs.css('div::text').getall()

clean_target_description_list = [s for s in target_description_list if s.strip()]
print(clean_target_description_list)

import re
clean_target_description_list = [re.sub(r"[ \t]+", "", s).replace("：", ":") for s in clean_target_description_list]
print(clean_target_description_list)

# use a list comprehension to replace the ":\n" with ": " and merge the strings
concat_target_description_list = [s[:-1] + " " + clean_target_description_list[i+1] if s.endswith(":\n") else s for i, s in enumerate(clean_target_description_list)]
# print the new list
print(concat_target_description_list)

# use a list comprehension to remove the elements that are subsets of other elements
clean_concat_target_description_list = [s for s in concat_target_description_list if not any(s in t for t in concat_target_description_list if s != t)]
# print the new list
print(clean_concat_target_description_list)

# Finally, we can combine the elements of the list to a single string
combine_target_description_str = "".join(clean_concat_target_description_list)
print(combine_target_description_str)
```

上面这段代码中，{combine_target_description_str} 这个变量就是我想保存的文本。  
我希望把这段目标文本保存在"crawled_description"这个目录中，文件名为 {target_img_alt}.txt。  
其中，{target_img_alt} 是刚才下载图片时获取的变量。

___

通过上面的代码，我顺利地爬取了300多个网页，把目标图片和文本都保存下来了。

现在我想反向地爬取，也就是从"<https://www.iyingdi.com/tz/tool/general/pcards/8153>"这个网页开始，依次爬取"<https://www.iyingdi.com/tz/tool/general/pcards/8152>"、"<https://www.iyingdi.com/tz/tool/general/pcards/8151>"，等等。

你应该已经发现了，我想爬取的网页的最后一个部分是一个递减的数字。

同样地，对于 start_urls，我希望我的程序可以一直尝试爬取下一个网页，直到爬取到错误的网页。
错误的网页会包含以下的文本:  
"不好意思，页面被法师撕掉了！"