import json
import scrapy
import csv
from ..utils import clean


class VelocityGlobalSpider(scrapy.Spider):
    name = 'velocityglobal'

    def start_requests(self):
        yield scrapy.Request(
            url='https://velocityglobal.com/about-us/careers/#open',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jobs = response.xpath('//div[@class="jobs-item-holder"]')
        for job in jobs:
            link = job.xpath(".//@href").get()
            yield scrapy.Request(
                url=f'{link}',
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs={
                    'role': job.xpath('.//div[1]/h3[@class="jobs-item-title"]/text()').get(),
                    'location': job.xpath('.//div[1]/div[@class="jobs-item-location"]/text()').get(),
                    'desc': "\n".join(job.xpath('.//div[2]/div[@class="jobs-item-description"]').extract()),
                    'team': job.xpath('.//div[2]/div[@class="jobs-item-description"]/p/strong[contains(text(),"Department")]/text()').get(),
                }
            )

    def parse_detail(self, response, **kwargs):
        yield {
            'Name of the role': kwargs['role'],
            'Department': kwargs['team'].replace('Department: ', ''),
            'Location': kwargs['location'],
            'Job type': '',
            'Job description': clean(kwargs['desc']),
            'URL': 'https://velocityglobal.com/about-us/careers/#open'
        }
