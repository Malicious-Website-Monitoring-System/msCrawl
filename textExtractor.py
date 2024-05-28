import re
import json
import logging
from scrapy import Spider
from scrapy.http import Response
from scrapy.selector import Selector


class TextExtractorSpider(Spider):
    name = "textExtractor"

    start_urls = [
        'https://m.stock.naver.com/'  # 예시 사이트
    ]

    def clean_text(self, text):
        # 텍스트에서 특수기호를 제거
        text = re.sub(r'[.,!?\"\'%\s]+', ' ', text)

        # 텍스트를 공백 기준으로 나누고, 각 단어에서 불필요한 공백을 제거
        return [word.strip() for word in text.split() if word.strip()]

    def extract_with_scrapy(self, response: Response):
        # 스크립트 및 스타일 태그 제거
        cleaned_html = re.sub(r'<(script|style).*?>.*?</\1>', '', response.text, flags=re.DOTALL)

        # 클린된 HTML로부터 텍스트 추출
        selector = Selector(text=cleaned_html)
        texts = selector.css('body *::text').getall()

        # 텍스트 리스트에서 공백 제거 및 정리
        cleaned_texts = [word for text in texts for word in self.clean_text(text)]

        # 디버깅: 추출된 텍스트 확인
        for text in cleaned_texts:
            self.log(f"Extracted text: {text}", level=logging.DEBUG)

        # 단어 개수 계산
        word_count = len(cleaned_texts)

        self.log(f"Extracted {word_count} words", level=logging.INFO)

        # JSON 파일로 저장
        try:
            with open('extractResult.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'wCount': word_count,
                    'text_list': cleaned_texts
                }, f, ensure_ascii=False, indent=4)
            self.log("Successfully Done", level=logging.INFO)
        except Exception as e:
            self.log(f"Failed : {e}", level=logging.ERROR)


    def parse(self, response):
        self.extract_with_scrapy(response)
