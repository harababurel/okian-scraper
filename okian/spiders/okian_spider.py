# -*- coding: utf-8 -*-
import scrapy
import urllib.parse

BASE_URL = "https://www.okian.ro"


class OkianSpiderSpider(scrapy.Spider):
    name = 'okian_spider'
    allowed_domains = ['okian.ro']
    start_urls = [
        "https://www.okian.ro:443/carti/arta-arhitectura-si-fotografie/",
        "https://www.okian.ro:443/carti/biografii/",
        "https://www.okian.ro:443/carti/business-finante-si-drept/",
        "https://www.okian.ro:443/carti/calatorii-hobby-si-sport/",
        "https://www.okian.ro:443/carti/calculatoare-si-it/",
        "https://www.okian.ro:443/carti/carti-pentru-copii-si-educative/",
        "https://www.okian.ro:443/carti/casa-si-gradina/",
        "https://www.okian.ro:443/carti/dezvoltare-personala-relatii-si-sanatate/",
        "https://www.okian.ro:443/carti/educatie-si-predare/",
        "https://www.okian.ro:443/carti/enciclopedii-referinta-si-studii-interdisciplinare/",
        "https://www.okian.ro:443/carti/geografie-si-mediul-inconjurator/",
        "https://www.okian.ro:443/carti/istorie-si-geografie/",
        "https://www.okian.ro:443/carti/literatura-si-fictiune/",
        "https://www.okian.ro:443/carti/mancare-si-bautura/",
        "https://www.okian.ro:443/carti/manga-si-comics/",
        "https://www.okian.ro:443/carti/media-si-comunicare/",
        "https://www.okian.ro:443/carti/medicina/",
        "https://www.okian.ro:443/carti/muzica-teatru-si-film/",
        "https://www.okian.ro:443/carti/poezie-drama-si-critica-literara/",
        "https://www.okian.ro:443/carti/psihologie-si-psihiatrie/",
        "https://www.okian.ro:443/carti/religie-si-credinta/",
        "https://www.okian.ro:443/carti/self-help/",
        "https://www.okian.ro:443/carti/societate-politica-si-filosofie/",
        "https://www.okian.ro:443/carti/stiinta-tehnica-si-industrie/",
        "https://www.okian.ro:443/carti/stiinte-sociale/"
    ]

    def parse(self, response):
        for article in response.xpath(
                "//article[@class='product-list-item clearfix']"):

            pub_data = dict(
                zip(
                    article.css(
                        'div ul.product-list-item-details li strong::text')
                    .extract(), [
                        x[3:] if x.startswith(" : ") else x
                        for x in article.css(
                            'div ul.product-list-item-details li::text')
                        .extract()
                    ]))

            discount = article.css('span.price-percent::text').extract_first()
            if discount:
                discount = discount[2:-1]

            item = {
                "Title":
                article.css('a img.product-list-item-image::attr(alt)')
                .extract_first(),
                "Author":
                article.css('div span.product-list-item-author a::text')
                .extract_first(),
                "Publisher":
                article.css('div span.product-list-item-brand a::text')
                .extract_first(),
                "Format":
                pub_data.get("Format"),
                "Publication date":
                pub_data.get("Data Publicarii"),
                "ISBN":
                pub_data.get("ISBN"),
                "Price":
                article.css('span.price-good::text').extract_first(),
                "Old price":
                article.css('span.price-old::text').extract_first(),
                "Discount":
                discount,
                "Link":
                article.css('a::attr(href)').extract_first(),
                "Cover":
                response.urljoin(
                    article.css('a img.product-list-item-image::attr(src)')
                    .extract_first()),
            }

            yield item

        next_page = response.css("li.next a::attr(href)").extract_first()
        if next_page:
            yield response.follow(
                response.urljoin(next_page), callback=self.parse)

    def parse_book(self, response):
        yield {"url": urllib.parse.urljoin(BASE_URL, response.extract())}
