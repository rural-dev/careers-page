import json
import scrapy
import csv

from scrapy import Selector

from ..utils import clean


class SimpplrSpider(scrapy.Spider):
    name = 'simpplr'

    def start_requests(self):

        for i in range(1,6):
            url = f'https://www.simpplr.com/wp-json/bornfight/v1/fetch-jobs-route/?posts_per_page=8&paged={i}&filters=' + '[{%22value%22:%22%22,%22type%22:%22departments%22},{%22value%22:%22%22,%22type%22:%22location%22}]'
            yield scrapy.Request(
                url= url,
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        partial = jsonresponse['partial']
        sel = Selector(text=partial)
        jobs = sel.xpath('//div[@class="c-card-open-position"]')
        for job in jobs:
            link = job.xpath(".//a/@href").get()
            role = job.xpath(".//a/div/div/div[1]/h4/text()").get()
            dep = job.xpath(".//a/div/div/div[2]/span/text()").get()
            location = job.xpath(".//a/div/div/div[3]/span/text()").get()

            yield scrapy.Request(
                url=link,
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs={
                    'role': role,
                    'location': location,
                    'team': dep,
                }
            )

    def parse_detail(self, response, **kwargs):
        desc = "/n".join(response.xpath('//div[@id="content"]').extract())
        yield {
            'Name of the role': kwargs['role'],
            'Department': kwargs['team'],
            'Location': kwargs['location'],
            'Job type': '',
            'Job description': clean(desc),
            'URL': response.request.url,
        }
