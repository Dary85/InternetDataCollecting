import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class LabirintSpider(scrapy.Spider):
    name = 'Labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/история/?stype=0']

    def parse(self, response: HtmlResponse):
        books = response.css("div.b-search-page-content a.product-title-link::attr(href)").extract()
        for book in books:
            yield response.follow(book, callback=self.book_parse)

        next_page = response.css("a.pagination-next__text::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        name = response.css("h1::text").extract_first()
        author = response.css("div.authors a::text").extract_first()
        main_price = response.css("div.buying-priceold-val span.buying-priceold-val-number::text").extract_first()
        discount_price = response.css("div.buying-pricenew span.buying-pricenew-val-number::text").extract_first()
        rating = response.xpath("//div[@id='rate']//text()").extract_first()
        yield JobparserItem(name=name, href=response.url,author = author,main_price=main_price,discount_price=discount_price,rating=rating)

