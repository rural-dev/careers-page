import json
import scrapy
import csv
from ..utils import clean


class IntecrowdSpider(scrapy.Spider):
    name = 'intecrowd'

    def start_requests(self):
        yield scrapy.Request(
            url='https://boards.greenhouse.io/embed/job_board?for=intecrowd&b=https://intecrowd.com/careers/',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        sections = response.xpath('//section[@class="level-0"]')
        for section in sections:
            dep = section.xpath(".//h3/text()").get()
            jobs = section.xpath(".//div")
            for job in jobs:
                link = job.xpath(".//a/@href").get()
                location = job.xpath(".//span[@class='location']/text()").get()
                yield scrapy.Request(
                    url=f'https://boards.greenhouse.io/embed/job_app?for=intecrowd&token={link.replace("https://intecrowd.com/careers/?gh_jid=","")}&b=https%3A%2F%2Fintecrowd.com%2Fcareers%2F',
                    callback=self.parse_detail,
                    dont_filter=True,
                    cb_kwargs={
                        'role': job.xpath(".//a/text()").get(),
                        'location': location,
                        'team': dep,
                    }
                )

    def parse_detail(self, response, **kwargs):
        desc = "".join(response.xpath('//*[@id="content"]').extract())
        yield {
            'Name of the role': kwargs['role'],
            'Department': kwargs['team'],
            'Location': kwargs['location'],
            'Job type': '',
            'Job description': clean(desc),
            'URL': response.request.url,
        }
