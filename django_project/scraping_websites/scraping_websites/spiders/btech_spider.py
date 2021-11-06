import scrapy

class AmazonSpider(scrapy.Spider):
    name = 'btech'
    start_urls = ['https://btech.com/en/moblies/mobile-phones-smartphones/smartphones/apple-honor-huawei-nokia-samsung-infinix-oppo-xiaomi-realme.html']

    def parse(self, response):
        for products in response.css('div.product-item-view'):
                yield {
                    'name' : products.css('h2.plpTitle::text').get(),
                    'price' : products.css('span.price-wrapper ::text').get(),
                    'link': products.css('a.listingWrapperSection').attrib['href']
                }
            

