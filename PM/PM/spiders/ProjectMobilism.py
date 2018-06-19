import scrapy
from bs4 import BeautifulSoup
import re

class mobilism(scrapy.Spider):
    name = "mobilism_spider"
    start_urls = [
        'https://forum.mobilism.org/viewforum.php?f=1295&sid=560134163f032fc9325f034e00723352',
    ]

    def __get_page_no(self, response):
        page_no = response.url.rsplit('=', 1)[1]
        try:
            return int(page_no) + 1
        except ValueError:
            return 1

    def parse(self, response):
        for i, topic in enumerate(response.css('.topictitle')):
            if i > 2:
                soup = BeautifulSoup(topic.extract(), 'html.parser')
                topic_author = soup.find('a').text.rsplit('by', 1)
                book_detail = {'topic': topic_author[0].strip()}
                if len(topic_author) > 1:
                    book_detail['author'] = topic_author[1].split('(', 1)[0].strip()
                else:
                    book_detail['author'] = ''
                link = soup.find('a')['href'][2:]
                book_detail['link'] = 'https://forum.mobilism.org/' + link
                book_detail['_id'] = int(link.split("t=")[1].split('&')[0])
                yield book_detail
        next_page = response.css('div.pagination ul li:last-child a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

