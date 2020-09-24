import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader

class LeruaruSpider(scrapy.Spider):
    name = 'leroymerlin.ru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self,search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response:HtmlResponse):
        ads_links = response.xpath("//a[@slot='picture']/@href")
        for link in ads_links:
            yield response.follow(link, callback= self.parse_lerua)
        next_page = response.xpath("//div[@class = 'next-paginator-button-wrapper']/a").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_lerua(self, response:HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(),response=response)
        print()

        loader.add_xpath('name',"//h1[@slot='title']/text()")
        loader.add_xpath('price',"//uc-pdp-price-view [@slot = 'primary-price']//span [@slot='price']/text()")
        loader.add_xpath('image_urls',"//uc-pdp-media-carousel[@slot = 'media-content']//img[@slot = 'thumbs']/@src")
        loader.add_value('href',response.url)
        loader.add_xpath('def_list_keys',"//div[@class='def-list__group']//dt[@class='def-list__term']/text()")
        loader.add_xpath('def_list_values',"//div[@class='def-list__group']//dd[@class='def-list__definition']/text()")
        yield loader.load_item()


        # name = response.xpath("//h1/span/text()").extract_first()
        # price = response.xpath('(//span[@class="js-item-price"])[1]/text()').extract_first()
        # photo = response.xpath("//div[contains(@class,'gallery-img-wrapper')]/div[contains(@class,'gallery-img-frame')]/@data-url").extract()
        # yield AvitoparserItem(name=name,photo=photo,price=price)



