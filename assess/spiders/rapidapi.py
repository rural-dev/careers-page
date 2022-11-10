import json
import scrapy
import csv
from ..utils import clean


class RapidApiSpider(scrapy.Spider):
    name = 'rapidapi'

    def start_requests(self):
        yield scrapy.Request(
            url='https://rapidapi.com/company/careers/',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jobs = response.xpath("//div[@class='page-careers_positions--listings']/a")
        for job in jobs:
            link = job.xpath(".//@href").get()
            yield scrapy.Request(
                url=f'{link}',
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs={
                    'role': job.xpath(".//div[1]/text()").get(),
                    'location': job.xpath(".//div[2]/text()").get(),
                    'team': job.xpath(".//div[3]/text()").get(),
                }
            )

    def parse_detail(self, response, **kwargs):
        type = response.xpath("//div[@class='posting-categories']/div[3]/text()").get()
        desc = "".join(response.xpath("//div[@class='content']/div[2]").extract())
        yield {
            'Name of the role': kwargs['role'],
            'Department': kwargs['team'],
            'Location': kwargs['location'],
            'Job type': type,
            'Job description': clean(desc),
            'URL': response.request.url,
        }
