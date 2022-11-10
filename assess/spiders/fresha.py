import json
import scrapy
import csv
from ..utils import clean


class FreshaSpider(scrapy.Spider):
    name = 'fresha'

    def start_requests(self):
        yield scrapy.Request(
            url='https://api.fresha.com/job-openings',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)
        jobs = jsonresponse['data']
        for job in jobs:
            yield scrapy.Request(
                url=f'https://apply.workable.com/api/v2/accounts/fresha/jobs/{job["id"]}',
                callback=self.parse_detail,
                dont_filter=True,
            )

    def parse_detail(self, response, **kwargs):
        data = json.loads(response.text)
        location = data['location']
        yield {
            'Name of the role': data['title'],
            'Department': ', '.join(data['department']),
            'Location': location['city'] + ', ' + location['region'] + ', ' + location['country'],
            'Job type': 'Full time' if data['type'] == 'full' else 'Contract',
            'Job description': clean(data['description'] + data['requirements'] + data['benefits']),
            'URL': f'https://apply.workable.com/fresha/j/{data["shortcode"]}/',
        }
