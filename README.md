# First time I wrote a program using ChatGPT and I completed a Python Scrapy crawler

The global AI trend started by ChatGPT has been going on for almost half a year now.

<a href="https://ibb.co/Thj1L2B"><img src="https://i.ibb.co/x59YHLS/Google-Trends-Chat-GPT-12-Months.png" alt="Google-Trends-Chat-GPT-12-Months" border="0"></a>

<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3349_RC01/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("TIMESERIES", {"comparisonItem":[{"keyword":"chatgpt","geo":"","time":"today 12-m"}],"category":0,"property":""}, {"exploreQuery":"q=chatgpt&date=today 12-m","guestPath":"https://trends.google.com:443/trends/embed/"}); </script>

I haven't used ChatGPT and other Generative AI tools much before. But I have some friends who are very enthusiastic about using Generative AI tools for image/video, such as midjourney and Stable Diffusion.

Last week, a friend of mine asked me if I could help him crawl this site for Pokemen images and related intro text. 👉🔗<https://www.iyingdi.com/tz/tool/general/pcards>  
It doesn't look difficult to crawl the target content - Pokemon images and intro text. But I really don't know how to use any crawler framework, the only crawler framework I've tried before is Scrapy, a framework developed in Python, but only to the extent of writing a "Hello World". So I decided to try ChatGPT and see what kind of Scrapy crawler I could write.

The result was a shocking realization that instruction-tuned LLMs like ChatGPT are very powerful, and as an IT technician, mastering these relevant tools can really improve productivity to a great extent.
I wanted to document and share this experience.

## What were some of the things that stood out to me about ChatGPT during this experience?

- Generated the basic code for my Python Scrapy program, and I just need to make some detailed changes to my knowledge to make it a finished product.
- Generated code for me for algorithmic functions. For example, if I need to process raw text scraped from a web page, I tell ChatGPT a sample of the resulting text, and it generates the code for me on how to process it.
- Based on my prompt, it iteratively outputs the response. Since I had little understanding of what Scrapy could do, even if I knew what I wanted to do, I didn't know how to use Scrapy to do it. But I told ChatGPT the "use Scrapy to do it" condition, and then I iteratively modified my requirements, and it was able to keep modifying the code that came back to me. The code leverages some uses of the Scrapy framework that I hadn't learned.

One thing that all of the above experiences have in common is that ChatGPT **black boxes** the process of writing my code.

## How I completed this Scrapy crawler from start to finish, and what specific prompts I used.

First, I found the official Scrapy documentation - 🔗 <https://docs.scrapy.org/en/latest/intro/tutorial.html> and learned how to create a Scrapy project.
Yes, my knowledge of Scrapy is "nothing".

<a href="https://ibb.co/L54V1Gx"><img src="https://i.ibb.co/VmXfTKg/Scrapy-Tutorial-Minimum-Knowledge.png" alt="Scrapy-Tutorial-Minimum-Knowledge" border="0"></a>

☝ As you can see, the official Scrapy tutorial is very informative, and I'm sure if I read everything, I could write a decent crawler, but what would be the point of that?
What I need is a simple crawler done quickly.
I only read until the "A shortcut to the start_requests method" section in the diagram above, where I knew how to create a Scrapy project, and the section a little further down that contains the basic usage of the Scrapy Shell, so I knew how to quickly debug the Scrapy crawler, and then I started to present my prompts to ChatGPT.

### Requirement analysis

I debugged the specifics of each page I wanted to crawl in the Scrapy Shell before I dropped a systematic prompt to ChatGPT.
The notes from the debugging are in this Markdown file - 👉<https://github.com/aruruka/Note-FirstProgram-PythonScrapy-WithHelpOfChatGPT/blob/main/note.md>.

The general analysis of the data of the website I want to crawl is as follows.

1. The starting page is - <https://www.iyingdi.com/tz/tool/general/pcards>.
2. I want to crawl the image of the card, and the description text, in the specific page for each Pokemon card.

For example, this is the page for a specific Pokemon card - <https://www.iyingdi.com/tz/tool/general/pcards/8153>, as shown in the figure below.👇

<a href="https://ibb.co/dKQNjXz"><img src="https://i.ibb.co/Yjt5PJq/Pokemon-Card-Page-Sample.png" alt="Pokemon-Card-Page-Sample" border="0"></a>

___

So,

- For images, all I have to specifically do is, get the HTML alt-tag text of the image, use it as the file name when saving the image, and then download the image to the local disk.
- For the description text, what I have to do is, manipulate the original text content and save it to the local disk.

I also finished the debugging process by asking ChatGPT questions while debugging the crawled web content in Scrapy Shell.
Specifically, I figured out the following points.

- Scrapy encapsulates the crawled contents as Selector objects, so I can further use CSS selectors or XPath selectors and third-party packages to get the exact target contents.

For example, by debugging, I found that for each Pokemon card page, I can get the target description text with the following XPath selector.

```python
target_description_divs = response.xpath('//*[@id="__layout"]/div/div[3]/div/div/div[2]/div/div')
```

The sample text obtained is as follows.

```
['能量转移', ' ', '\n          系列：对战派对组合 草\n        ']
```

☝ As you can see, the elements in this list are strings, and some of them contain only space characters, and I want to remove those string elements that contain only spaces.

It's amazing what I can do when I send a request like this to ChatGPT for processing raw text and getting actual working Python code!
Of course, the prerequisite is that you have some knowledge of Python coding so that your prompts are detailed and precise.

___

### The whole prompts for ChatGPT to write the Python Scrapy crawler

Then, finally comes the whole prompts I sent to ChatGPT, which is documented in this Markdown file - 👉<https://github.com/aruruka/Note-FirstProgram-PythonScrapy-WithHelpOfChatGPT/blob/main/prompt.md>.

And below is the screenshots.

<a href="https://ibb.co/GcVRNMr"><img src="https://i.ibb.co/t8bDF21/Chat-GPT-Scrapy-Image-Text-1.png" alt="Chat-GPT-Scrapy-Image-Text-1" border="0"></a>
<a href="https://ibb.co/Gcj7T3Z"><img src="https://i.ibb.co/r4JksfB/Chat-GPT-Scrapy-Image-Text-2.png" alt="Chat-GPT-Scrapy-Image-Text-2" border="0"></a>
<a href="https://ibb.co/HpX3pfY"><img src="https://i.ibb.co/93GS3k2/Chat-GPT-Scrapy-Image-Text-3.png" alt="Chat-GPT-Scrapy-Image-Text-3" border="0"></a>
<a href="https://ibb.co/gWjSZ9F"><img src="https://i.ibb.co/C91bK8s/Chat-GPT-Scrapy-Image-Text-4.png" alt="Chat-GPT-Scrapy-Image-Text-4" border="0"></a>
<a href="https://ibb.co/WtjhrQT"><img src="https://i.ibb.co/Hd3Sc0J/Chat-GPT-Scrapy-Image-Text-5.png" alt="Chat-GPT-Scrapy-Image-Text-5" border="0"></a>
<a href="https://ibb.co/QpY7gG3"><img src="https://i.ibb.co/q7mLSw3/Chat-GPT-Scrapy-Image-Text-6.png" alt="Chat-GPT-Scrapy-Image-Text-6" border="0"></a>
<a href="https://ibb.co/bRmrF8D"><img src="https://i.ibb.co/XkLzDvM/Chat-GPT-Scrapy-Image-Text-7.png" alt="Chat-GPT-Scrapy-Image-Text-7" border="0"></a>
<a href="https://ibb.co/5BkBnx5"><img src="https://i.ibb.co/Gc9ct3V/Chat-GPT-Scrapy-Image-Text-8.png" alt="Chat-GPT-Scrapy-Image-Text-8" border="0"></a>
<a href="https://ibb.co/0cHz4P5"><img src="https://i.ibb.co/XbcG0mH/Chat-GPT-Scrapy-Image-Text-9.png" alt="Chat-GPT-Scrapy-Image-Text-9" border="0"></a>
<a href="https://ibb.co/sbL6sSs"><img src="https://i.ibb.co/ydLYgTg/Chat-GPT-Scrapy-Image-Text-10.png" alt="Chat-GPT-Scrapy-Image-Text-10" border="0"></a>
<a href="https://ibb.co/kJQmRMs"><img src="https://i.ibb.co/Jq53fCw/Chat-GPT-Scrapy-Image-Text-11.png" alt="Chat-GPT-Scrapy-Image-Text-11" border="0"></a>
<a href="https://ibb.co/bmbpTGD"><img src="https://i.ibb.co/c3Yz0sV/Chat-GPT-Scrapy-Image-Text-12.png" alt="Chat-GPT-Scrapy-Image-Text-12" border="0"></a>
<a href="https://ibb.co/G7x2DCM"><img src="https://i.ibb.co/R2v0KQ6/Chat-GPT-Scrapy-Image-Text-13.png" alt="Chat-GPT-Scrapy-Image-Text-13" border="0"></a>
<a href="https://ibb.co/9WY54JC"><img src="https://i.ibb.co/bXd9vx8/Chat-GPT-Scrapy-Image-Text-14.png" alt="Chat-GPT-Scrapy-Image-Text-14" border="0"></a>

___

## Conclusion

At the time I used ChatGPT to complete the above Python Scrapy crawler, I had not yet learned the basic skills of prompt engineering.
After this experience, I am determined to learn the usage and principles of the tools currently available on the market in a systematic way.

ChatGPT and similar instruction-tuned LLMs can help IT techs be very productive.
But it won't help you achieve your goals if you haven't learned systematically about what you want to accomplish.
You still need to have a systematic, specialized knowledge of what you're doing.
ChatGPT is perhaps most useful because it can save you time that you would otherwise spend reading, or practicing (to deepen your proficiency).

If you don't have the expertise and systematic knowledge, then you can't tell if ChatGPT is giving you the right answers.
