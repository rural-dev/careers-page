import json
import scrapy
import csv
from ..utils import clean


class EasyShipSpider(scrapy.Spider):
    name = 'easyship'

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.easyship.com/careers',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jobs = response.xpath('//*[@id="open-roles"]/div[2]/ul/a')
        for job in jobs:
            link = job.xpath(".//@href").get()
            yield scrapy.Request(
                url=f'{link}',
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs={
                    'role': job.xpath(".//li/h3/text()").get(),
                    'location': job.xpath(".//li/div/p[1]/text()").get(),
                    'team': job.xpath(".//li/div/p[2]/text()").get(),
                }
            )

    def parse_detail(self, response, **kwargs):
        desc = "".join(response.xpath("//div[@class='description']").extract())
        yield {
            'Name of the role': kwargs['role'],
            'Department': kwargs['team'],
            'Location': kwargs['location'],
            'Job type': '',
            'Job description': clean(desc),
            'URL': response.request.url,
        }
