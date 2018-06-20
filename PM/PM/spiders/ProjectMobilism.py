import scrapy
from bs4 import BeautifulSoup
import pymongo
import time
from scrapy.conf import settings

class mobilism(scrapy.Spider):
    name = "mobilism_spider"
    start_urls = [
        'https://forum.mobilism.org/viewforum.php?f=1295&sid=560134163f032fc9325f034e00723352',
    ]

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        collection = db[settings['MONGODB_COLLECTION']]
        if settings['MONGODB_COLLECTION'] in db.collection_names():
            self.first_id = collection.find_one()['_id']
        else:
            self.first_id = 0

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
                link = soup.find('a')['href'][2:]
                id = int(link.split("t=")[1].split('&')[0])
                if id <= self.first_id:
                    raise StopIteration
                topic_author = soup.find('a').text.rsplit('by', 1)
                book_detail = {'_id': id,
                               'topic': topic_author[0].strip(),
                               'link': 'https://forum.mobilism.org/' + link}
                if len(topic_author) > 1:
                    book_detail['author'] = topic_author[1].split('(', 1)[0].strip()
                else:
                    book_detail['author'] = ''
                yield book_detail
        next_page = response.css('div.pagination ul li:last-child a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

