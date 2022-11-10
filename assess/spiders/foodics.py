import json
import scrapy
import csv
from ..utils import clean


class FoodicsSpider(scrapy.Spider):
    name = 'foodics'

    def start_requests(self):
        data = {"query": "", "location": [], "department": [], "worktype": [], "remote": []}
        yield scrapy.Request(
            url='https://apply.workable.com/api/v3/accounts/foodics/jobs',
            callback=self.parse,
            dont_filter=True,
            method='POST',
            body=json.dumps(data),
        )

    def parse(self, response, **kwargs):
        print(response.text)
        jsonresponse = json.loads(response.text)
        jobs = jsonresponse['results']
        for job in jobs:
            yield scrapy.Request(
                url=f'https://apply.workable.com/api/v2/accounts/foodics/jobs/{job["shortcode"]}',
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
            'URL': f'https://apply.workable.com/foodics/j/{data["shortcode"]}/',
        }
