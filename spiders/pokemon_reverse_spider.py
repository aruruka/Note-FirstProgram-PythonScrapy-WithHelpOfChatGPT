from pathlib import Path

import scrapy
import os
import requests
from urllib.parse import urljoin
import re

class PokemonSpider(scrapy.Spider):
    name = "pokemon_reverse"
    allowed_domains = ["iyingdi.com"]
    start_url = "https://www.iyingdi.com/tz/tool/general/pcards/8152"
    page_number = 0

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        target_img_selector = response.css(
            "#__layout > div > div.default-main-container.w-full.pl-90.big\:pl-250.pt-56 > div > div > div.marvel-card-detail-page > div > img"
        )

        # Extract the relative URL of the image from the Selector
        relative_url = target_img_selector.css("::attr(src)").get()
        print(relative_url)

        # Construct the absolute URL of the image
        absolute_url = urljoin(response.url, relative_url)
        print(absolute_url)

        target_img_alt = target_img_selector.css("::attr(alt)").get()
        print(target_img_alt)

        # Send a GET request to download the image
        image_response = requests.get(absolute_url)

        # Check if the request was successful
        if image_response.status_code == 200:
            # Save the image to a file
            with open(f"./crawled_images/{target_img_alt}.png", "wb") as file:
                file.write(image_response.content)
                print(
                    f"Image downloaded successfully. URL: {absolute_url}. ImageFileName: {target_img_alt}.png."
                )
        else:
            print(
                f"Failed to download the image.  URL: {absolute_url}. ImageFileName: {target_img_alt}.png."
            )

        # Save the target description as a text file
        description_filename = f"{target_img_alt}.txt"
        description_path = f"./crawled_description/{description_filename}"

        target_description_divs = response.xpath(
            '//*[@id="__layout"]/div/div[3]/div/div/div[2]/div/div'
        )
        target_description_list = target_description_divs.css("div::text").getall()

        clean_target_description_list = [
            s for s in target_description_list if s.strip()
        ]
        print(clean_target_description_list)

        clean_target_description_list = [
            re.sub(r"[ \t]+", "", s).replace("：", ":")
            for s in clean_target_description_list
        ]
        print(clean_target_description_list)

        # use a list comprehension to replace the ":\n" with ": " and merge the strings
        concat_target_description_list = [
            s[:-1] + " " + clean_target_description_list[i + 1]
            if s.endswith(":\n")
            else s
            for i, s in enumerate(clean_target_description_list)
        ]
        # print the new list
        print(concat_target_description_list)

        # use a list comprehension to remove the elements that are subsets of other elements
        clean_concat_target_description_list = [
            s
            for s in concat_target_description_list
            if not any(s in t for t in concat_target_description_list if s != t)
        ]
        # print the new list
        print(clean_concat_target_description_list)

        # Finally, we can combine the elements of the list to a single string
        combine_target_description_str = "".join(clean_concat_target_description_list)
        print(combine_target_description_str)

        with open(description_path, "w") as file:
            file.write(combine_target_description_str)
            print(f"Description saved successfully. File: {description_filename}.")

        paragraph = combine_target_description_str

        yield {
            "webpage_url": response.url,
            "image_url": absolute_url,
            "paragraph": paragraph,
        }

        if "不好意思，页面被法师撕掉了！" not in response.text:
            self.page_number -= 1
            next_url = f"https://www.iyingdi.com/tz/tool/general/pcards/{8152 + self.page_number}"
            yield scrapy.Request(url=next_url, callback=self.parse)
