import scrapy
from chocolatescraper.items import ChocolateProduct

class ChocolatespiderSpider(scrapy.Spider):
    # su dung de chay donglenh quet scrapy crawl chocolatespider
    name = "chocolatespider"
    # lamot tuy chon de chi quet nhung trang co ten mien la chocolate.co.uk
    allowed_domains = ["chocolate.co.uk"]
    # url dau tien can quet
    start_urls = ["https://chocolate.co.uk/collections/all"]

    # ham duoc goi khi nhan phan hoi tu trang web muc tieu
    def parse(self, response):
        products = response.css('product-item')
        product_item = ChocolateProduct()
        for product in products:
            #here we put the data returned into the format we want to output for our csv or json file
            product_item['name'] = product.css('a.product-item-meta__title::text').get()
            product_item['price'] = product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>','')
            product_item['url'] = product.css('div.product-item-meta a').attrib['href']
            yield product_item
        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
           next_page_url = 'https://www.chocolate.co.uk' + next_page
           yield response.follow(next_page_url, callback=self.parse)
