import json
import scrapy
import csv
from ..utils import clean


class AppinioSpider(scrapy.Spider):
    name = 'appinio'

    def start_requests(self):
        yield scrapy.Request(
            url='https://boards-api.greenhouse.io/v1/boards/appinio/jobs?content=true',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        jobs = jsonresponse['jobs']
        for job in jobs:
            yield scrapy.Request(
                url=f'https://api.greenhouse.io/v1/boards/appinio/jobs/{job["id"]}',
                callback=self.parse_detail,
                dont_filter=True,
            )

    def parse_detail(self, response, **kwargs):
        data = json.loads(response.text)
        departments = data['departments']
        dep = []
        for d in departments:
            dep.append(d['name'])
        yield {
            'Name of the role': data['title'],
            'Department': ', '.join(dep),
            'Location': data['location']['name'],
            'Job type': '',
            'Job description': clean(clean(data['content'])),
            'URL': data["absolute_url"],
        }
