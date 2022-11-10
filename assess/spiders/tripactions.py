import json
import scrapy
import csv
from ..utils import clean


class TripActionsSpider(scrapy.Spider):
    name = 'tripactions'

    def start_requests(self):
        yield scrapy.Request(
            url=f'https://boards-api.greenhouse.io/v1/boards/tripactions/jobs?content=true',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        jobs = jsonresponse["jobs"]
        for job in jobs:
            yield scrapy.Request(
                url=job["absolute_url"],
                callback=self.parse_detail,
                dont_filter=True,
                cb_kwargs=({"job": job})
            )

    def parse_detail(self, response, **kwargs):
        title = response.xpath('//title/text()').get()
        h1 = response.xpath('//h1/text()').get()

        location = response.xpath('//span[contains(text(),"Location:")]/parent::p/text()').get()
        department = response.xpath('//span[contains(text(),"Department:")]/parent::p/text()').get()
        desc = response.xpath('//*[@id="gh-apply"]/div[1]/div[1]').get()
        
        job = kwargs['job']
        job['url'] = response.request.url
        job['location'] = location
        job['department'] = department
        job['desc'] = desc
        yield {
            'Name of the role': h1,
            'Department': department,
            'Location': location,
            'Job type': '',
            'Job description': clean(desc),
            'URL': response.request.url,
        }