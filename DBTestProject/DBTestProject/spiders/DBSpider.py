import scrapy
import re
from scrapy.selector import Selector
from ..items import GetWordsItem


class DBSpider(scrapy.Spider):
    name = "DBSpider"

    def start_requests(self):
        with open('host.txt', 'r', encoding='utf-8') as f:
            urls = [url.strip() for url in f.readlines()]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'host': url})

    def clean_text(self, text):
        text = re.sub(r'\s+', ' ', text).strip()
        return re.findall(r'\w+', text.lower())

    def extract_with_scrapy(self, response):
        cleaned_html = re.sub(r'<(script|style).*?>.*?</\1>', '', response.text, flags=re.DOTALL)
        selector = Selector(text=cleaned_html)
        texts = selector.css('body *::text').getall()
        cleaned_texts = [word for text in texts for word in self.clean_text(text)]
        word_count = len(cleaned_texts)
        return word_count, ' '.join(cleaned_texts)

    def parse(self, response):
        items = GetWordsItem()
        host = response.meta['host']
        items['host'] = host
        word_count, cleaned_texts = self.extract_with_scrapy(response)
        items['word_count'] = word_count
        items['words'] = cleaned_texts
        yield items
