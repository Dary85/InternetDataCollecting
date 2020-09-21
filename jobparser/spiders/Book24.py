import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class Book24Spider(scrapy.Spider):
    name = 'Book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=python']

    def parse(self, response: HtmlResponse):
        books = response.xpath("//a[@class='book__image-link js-item-element ddl_product_link']/@href").extract()
        for book in books:
            yield response.follow(book, callback=self.book_parse)

        next_page = response.xpath("//a[@class='catalog-pagination__item _text js-pagination-catalog-item']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        name = response.css("h1::text").extract_first()
        author = response.xpath("//div[@class='item-tab__chars-item']//span[contains(text(),'Автор')]//..//span//a//text()").extract()
        main_price = response.css("div.item-actions__price-old::text").extract_first()
        discount_price = response.xpath("//div[@class='item-actions__price']//b//text()").extract_first()
        rating = 0 #response.xpath("//div[@id='rate']//text()").extract_first()
        yield JobparserItem(name=name, href=response.url,author = author,main_price=main_price,discount_price=discount_price,rating=rating)

