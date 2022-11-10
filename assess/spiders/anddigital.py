import json
import scrapy
import csv
from ..utils import clean


class AndDigitalSpider(scrapy.Spider):
    name = 'anddigital'

    def start_requests(self):
        yield scrapy.Request(
            url='https://apply.workable.com/api/v1/widget/accounts/258996?origin=embed&callback=whrcallback',
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response, **kwargs):
        print(response.text)
        jsonresponse = json.loads(response.text[:-1].replace("/**/whrcallback(", ""))
        jobs = jsonresponse['jobs']
        for job in jobs:
            yield scrapy.Request(
                url=f'https://apply.workable.com/api/v2/accounts/and-digital/jobs/{job["shortcode"]}',
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
            'Job type': data['type'] if 'type' in data else '',
            'Job description': clean(data['description'] + data['requirements'] + data['benefits']),
            'URL': f'https://apply.workable.com/and-digital/j/{data["shortcode"]}/',
        }
